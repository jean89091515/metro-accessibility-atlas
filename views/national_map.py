"""National map — every station, year by year."""
import math
import numpy as np
import plotly.express as px
import streamlit as st

from lib.i18n import current_lang, make_t, city_label, tier_label, type_label
from lib.data import load_stations, cities_ordered, year_bounds
from lib.theme import TYPE_COLORS, TYPE_ORDER, TIER_ORDER, SEQ_BLUE, MUTED

lang = current_lang()
t = make_t(lang)

st.markdown(f"## 🗺️ {t('page_map')}")
st.caption(t("map_subtitle"))

stations = load_stations()
ymin, ymax = year_bounds()

# ── Controls ──────────────────────────────────────────────────────────
c1, c2, c3 = st.columns([2, 1.3, 1.3])
with c1:
    year = st.slider(t("ctrl_year"), ymin, ymax, ymax, step=1)
with c2:
    color_opts = {
        "type": t("color_by_type"),
        "s1": t("color_by_s1"),
        "s2": t("color_by_s2"),
    }
    color_by = st.selectbox(t("ctrl_color_by"), list(color_opts),
                            format_func=lambda k: color_opts[k])
with c3:
    cities = cities_ordered()
    focus = st.selectbox(
        t("ctrl_city"), ["__all__"] + cities,
        format_func=lambda c: t("ctrl_all") if c == "__all__" else city_label(c, lang))

dfm = stations[stations["year"] == year].copy()
if focus != "__all__":
    dfm = dfm[dfm["city"] == focus]
dfm["name"] = dfm["name_cn"] if lang == "zh" else dfm["name_en"].fillna(dfm["name_cn"])
dfm["city_disp"] = dfm["city"].map(lambda c: city_label(c, lang))

if dfm.empty:
    msg = (f"{city_label(focus, lang)} 在 {year} 年尚无地铁站。" if lang == "zh"
           else f"No metro stations in {city_label(focus, lang)} in {year}.")
    st.info(msg)
    st.stop()


def view(d):
    lat0, lat1, lon0, lon1 = d.lat.min(), d.lat.max(), d.lon.min(), d.lon.max()
    center = dict(lat=(lat0 + lat1) / 2, lon=(lon0 + lon1) / 2)
    span = max(lat1 - lat0, (lon1 - lon0) * 0.7, 0.04)
    zoom = max(2.6, min(11.0, math.log2(360.0 / span) - 0.6))
    return center, zoom


center, zoom = view(dfm)
common = dict(lat="lat", lon="lon", hover_name="name", zoom=zoom, center=center,
              custom_data=["city_disp", "s1", "s2", "type_2d"])

if color_by == "type":
    fig = px.scatter_map(
        dfm, color="type_2d", color_discrete_map=TYPE_COLORS,
        category_orders={"type_2d": TYPE_ORDER}, **common)
    for tr in fig.data:
        tr.name = f"{tr.name} · {type_label(tr.name, lang)}"
else:
    dfm["_c"] = np.log10(dfm[color_by].clip(lower=1))
    fig = px.scatter_map(
        dfm, color="_c", color_continuous_scale=SEQ_BLUE, **common)
    fig.update_coloraxes(colorbar_title=color_opts[color_by],
                         colorbar_title_side="right")

fig.update_traces(marker=dict(size=6, opacity=0.8),
                  hovertemplate="<b>%{customdata[0]}</b> · %{hover_name}<br>"
                                "S₁ %{customdata[1]:,.0f} · S₂ %{customdata[2]:,.0f}"
                                " · %{customdata[3]}<extra></extra>")
fig.update_layout(
    map_style="carto-positron",
    margin=dict(l=0, r=0, t=0, b=0),
    height=620,
    legend=dict(orientation="h", yanchor="bottom", y=0.0, xanchor="left", x=0,
                bgcolor="rgba(255,255,255,0.7)", title_text=""),
)
st.plotly_chart(fig, config={"displayModeBar": False})

n = len(dfm)
st.caption(("显示 " if lang == "zh" else "Showing ")
           + f"**{n:,}** "
           + ("个站点 · " if lang == "zh" else "stations · ")
           + f"{year}" + (f" · {city_label(focus, lang)}" if focus != "__all__" else ""))
st.caption(t("data_note"))
