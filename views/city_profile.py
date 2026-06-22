"""City profile — one city's trajectory in depth."""
import math
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from lib.i18n import (current_lang, make_t, city_label, tier_label, type_label)
from lib.data import load_stations, load_city_year, cities_ordered
from lib.charts import style_fig, human
from lib.theme import TYPE_COLORS, TYPE_ORDER, PRIMARY, MUTED

lang = current_lang()
t = make_t(lang)

st.markdown(f"## 🏙️ {t('page_city')}")
st.caption(t("city_subtitle"))

stations = load_stations()
cy = load_city_year()
cities = cities_ordered()

city = st.selectbox(t("ctrl_city"), cities,
                    format_func=lambda c: city_label(c, lang))

cc = cy[cy["city"] == city].sort_values("year")
cc = cc[cc["n_stations"] > 0]
latest = cc.iloc[-1]
tier = latest["tier"]
first_year = int(cc["year"].iloc[0])

st.markdown(f"**{city_label(city, lang)}** · {tier_label(tier, lang)} · "
            f"{'首条线路' if lang == 'zh' else 'opened'} {first_year}")

k1, k2, k3, k4 = st.columns(4)
k1.metric(t("metric_n"), f"{int(latest['n_stations']):,}")
k2.metric(t("metric_median_s1"), human(latest["s1_median"]))
k3.metric(t("metric_median_s2"), human(latest["s2_median"]))
k4.metric(t("metric_gini_s2"), f"{latest['gini_s2']:.2f}")

left, right = st.columns(2, gap="large")

# ── Trajectory: city's own S1 / S2 indexed to first year ──────────────
with left:
    st.markdown(f"**{'服务 vs 可达 的演化' if lang == 'zh' else 'Service vs reach over time'}**")
    base1, base2 = cc["s1_median"].iloc[0], cc["s2_median"].iloc[0]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=cc["year"], y=cc["s2_median"] / base2 * 100,
                             name=t("s2_name"), line=dict(color=PRIMARY, width=3)))
    fig.add_trace(go.Scatter(x=cc["year"], y=cc["s1_median"] / base1 * 100,
                             name=t("s1_name"), line=dict(color="#EF4444", width=3)))
    fig.add_hline(y=100, line=dict(color=MUTED, width=1, dash="dot"))
    fig.update_yaxes(title_text=(f"指数 ({first_year}=100)" if lang == "zh"
                                 else f"Index ({first_year} = 100)"))
    style_fig(fig, height=330)
    st.plotly_chart(fig, config={"displayModeBar": False})

# ── Type composition over time (stacked area) ─────────────────────────
with right:
    st.markdown(f"**{'站点类型构成' if lang == 'zh' else 'Station-type mix'}**")
    fig2 = go.Figure()
    for code in TYPE_ORDER:
        fig2.add_trace(go.Scatter(
            x=cc["year"], y=cc[f"pct_{code}"] * 100, name=f"{code} · {type_label(code, lang)}",
            mode="lines", stackgroup="one", line=dict(width=0.5, color=TYPE_COLORS[code]),
            fillcolor=TYPE_COLORS[code]))
    fig2.update_yaxes(title_text="%", range=[0, 100])
    style_fig(fig2, height=330)
    st.plotly_chart(fig2, config={"displayModeBar": False})

# ── City map (latest year) ────────────────────────────────────────────
st.markdown(f"**{city_label(city, lang)} · {int(latest['year'])}**")
sm = stations[(stations["city"] == city) & (stations["year"] == int(latest["year"]))].copy()
sm["name"] = sm["name_cn"] if lang == "zh" else sm["name_en"].fillna(sm["name_cn"])
lat0, lat1, lon0, lon1 = sm.lat.min(), sm.lat.max(), sm.lon.min(), sm.lon.max()
span = max(lat1 - lat0, (lon1 - lon0) * 0.7, 0.04)
fig3 = px.scatter_map(
    sm, lat="lat", lon="lon", color="type_2d",
    color_discrete_map=TYPE_COLORS, category_orders={"type_2d": TYPE_ORDER},
    hover_name="name", custom_data=["s1", "s2", "type_2d"],
    zoom=max(8.0, min(12.0, math.log2(360.0 / span) - 0.6)),
    center=dict(lat=(lat0 + lat1) / 2, lon=(lon0 + lon1) / 2))
fig3.update_traces(marker=dict(size=8, opacity=0.85),
                   hovertemplate="<b>%{hover_name}</b><br>"
                                 "S₁ %{customdata[0]:,.0f} · S₂ %{customdata[1]:,.0f}"
                                 " · %{customdata[2]}<extra></extra>")
for tr in fig3.data:
    tr.name = f"{tr.name} · {type_label(tr.name, lang)}"
fig3.update_layout(map_style="carto-positron", height=480,
                   margin=dict(l=0, r=0, t=0, b=0),
                   legend=dict(orientation="h", y=0, x=0,
                               bgcolor="rgba(255,255,255,0.7)", title_text=""))
st.plotly_chart(fig3, config={"displayModeBar": False})
st.caption(t("data_note"))
