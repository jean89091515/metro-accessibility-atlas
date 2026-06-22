"""
Build the app's data files from the (de-identified) capsule data.

Inputs  (capsule, build-time only — never shipped with the app):
  - intermediate.csv   year, city, station_id, stop_id, S1, S2, opening_yr
  - metro_stops_with_opening_years.shp   lon/lat + public station names

Outputs (shipped with the app, in ./data):
  - stations.parquet   one row per station-year, with coords + type + tier
  - city_year.parquet  one row per city-year: medians, Gini, type mix, new stations

Station typing (HH/HL/LH/LL) and city tiers reuse the paper's own
shared_config so the platform matches the publication exactly.
"""
import os
import sys
import pandas as pd
import numpy as np
import geopandas as gpd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "data")
os.makedirs(OUT, exist_ok=True)

# Path to the de-identified Code Ocean capsule (build-time input only).
# Override with:  METRO_CAPSULE=/path/to/codeocean_capsule python build_data.py
CAPSULE = os.environ.get("METRO_CAPSULE", os.path.join(HERE, "_capsule"))
sys.path.insert(0, os.path.join(CAPSULE, "code"))
from shared_config import add_station_types, get_city_tier, calculate_gini  # noqa: E402

# ── 1. Load the de-identified panel ───────────────────────────────────
df = pd.read_csv(os.path.join(CAPSULE, "data", "intermediate.csv"))
df["stop_id"] = df["stop_id"].astype(str)
print(f"panel: {len(df):,} rows  {df['city'].nunique()} cities  "
      f"{df['year'].min()}–{df['year'].max()}")

# ── 2. Coordinates + public station names from the shapefile ──────────
shp = gpd.read_file(os.path.join(CAPSULE, "data", "shp",
                                 "metro_stops_with_opening_years.shp"))
if shp.crs is None or shp.crs.to_epsg() != 4326:
    shp = shp.to_crs(4326)
shp["lon"] = shp.geometry.x
shp["lat"] = shp.geometry.y
geo = (shp[["stop_id", "lon", "lat", "name_cn", "name_en"]]
       .dropna(subset=["stop_id"]).copy())
geo["stop_id"] = geo["stop_id"].astype(str)
geo = geo.drop_duplicates("stop_id")
df = df.merge(geo, on="stop_id", how="left")
cov = df["lon"].notna().mean()
print(f"coord join coverage: {cov:6.2%}  "
      f"({df['lon'].isna().sum():,} rows without coords)")

# ── 3. City tier ──────────────────────────────────────────────────────
df["tier"] = df["city"].apply(get_city_tier)
print("tier distribution (stations-years):")
print(df["tier"].value_counts().to_string())

# ── 4. Station type via the paper's annual-median method ──────────────
# Thresholds are computed on the studied (tiered) set, exactly as the
# paper does, then applied to every station so the map can show all of them.
tiered = df[df["tier"] != "Other"].copy()
typed = add_station_types(tiered)
thr = (typed.groupby("year")[["S1_threshold", "S2_threshold"]]
       .first().reset_index())
df = df.merge(thr, on="year", how="left")
df["type_2d"] = (np.where(df["served_population"] > df["S1_threshold"], "H", "L")
                 + np.where(df["cumulative_opportunities"] > df["S2_threshold"], "H", "L"))

# ── 5. Tidy station-year table ────────────────────────────────────────
stations = df.rename(columns={
    "served_population": "s1",
    "cumulative_opportunities": "s2",
}).copy()
stations = stations[[
    "year", "city", "tier", "station_id", "stop_id",
    "name_cn", "name_en", "lon", "lat", "s1", "s2", "type_2d", "opening_yr",
]]
stations.to_parquet(os.path.join(OUT, "stations.parquet"), index=False)
print(f"\nwrote stations.parquet  {len(stations):,} rows")

# ── 6. City-year aggregates ───────────────────────────────────────────
rows = []
for (city, year), g in df.groupby(["city", "year"]):
    tmix = g["type_2d"].value_counts(normalize=True)
    rows.append({
        "city": city,
        "tier": g["tier"].iloc[0],
        "year": year,
        "n_stations": len(g),
        "n_new": int((g["opening_yr"] == year).sum()),
        "s1_median": g["served_population"].median(),
        "s2_median": g["cumulative_opportunities"].median(),
        "s1_mean": g["served_population"].mean(),
        "s2_mean": g["cumulative_opportunities"].mean(),
        "gini_s1": calculate_gini(g["served_population"].values),
        "gini_s2": calculate_gini(g["cumulative_opportunities"].values),
        "pct_HH": tmix.get("HH", 0.0),
        "pct_HL": tmix.get("HL", 0.0),
        "pct_LH": tmix.get("LH", 0.0),
        "pct_LL": tmix.get("LL", 0.0),
    })
city_year = pd.DataFrame(rows).sort_values(["city", "year"]).reset_index(drop=True)
city_year.to_parquet(os.path.join(OUT, "city_year.parquet"), index=False)
print(f"wrote city_year.parquet  {len(city_year):,} rows "
      f"({city_year['city'].nunique()} cities)")

# ── 7. Quick sanity print ─────────────────────────────────────────────
print("\nnational type mix by year (check vs ED Table 2):")
for y in [2000, 2010, 2020, 2025]:
    sub = df[(df["year"] == y) & (df["tier"] != "Other")]
    mix = sub["type_2d"].value_counts(normalize=True)
    print(f"  {y}: N={len(sub):5d}  "
          f"HH={mix.get('HH',0):.1%} HL={mix.get('HL',0):.1%} "
          f"LH={mix.get('LH',0):.1%} LL={mix.get('LL',0):.1%}")
