"""Cached data access for the app."""
import os
import pandas as pd
import streamlit as st

from lib.theme import TIER_ORDER

_DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


@st.cache_data(show_spinner=False)
def load_stations() -> pd.DataFrame:
    df = pd.read_parquet(os.path.join(_DATA, "stations.parquet"))
    df["year"] = df["year"].astype(int)
    return df


@st.cache_data(show_spinner=False)
def load_city_year() -> pd.DataFrame:
    df = pd.read_parquet(os.path.join(_DATA, "city_year.parquet"))
    df["year"] = df["year"].astype(int)
    return df


@st.cache_data(show_spinner=False)
def year_bounds() -> tuple[int, int]:
    df = load_city_year()
    return int(df["year"].min()), int(df["year"].max())


@st.cache_data(show_spinner=False)
def cities_ordered() -> list[str]:
    """Cities ordered by tier, then by 2025 station count (largest first)."""
    cy = load_city_year()
    latest = cy[cy["year"] == cy["year"].max()]
    latest = latest.assign(
        _tier=latest["tier"].map({t: i for i, t in enumerate(TIER_ORDER)}).fillna(9)
    )
    latest = latest.sort_values(["_tier", "n_stations"], ascending=[True, False])
    return latest["city"].tolist()


@st.cache_data(show_spinner=False)
def city_tier_map() -> dict:
    cy = load_city_year()
    return dict(zip(cy["city"], cy["tier"]))
