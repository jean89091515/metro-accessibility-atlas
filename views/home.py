"""Home — the story in one screen."""
import plotly.graph_objects as go
import streamlit as st

from lib.i18n import current_lang, make_t
from lib.data import load_stations
from lib.charts import style_fig, human
from lib.theme import TYPE_COLORS, TYPE_ORDER, PRIMARY, MUTED
from lib.i18n import type_label

lang = current_lang()
t = make_t(lang)

stations = load_stations()
nat = (stations.groupby("year")
       .agg(s1=("s1", "median"), s2=("s2", "median"),
            n=("station_id", "nunique"))
       .reset_index())
y0, y1 = nat["year"].min(), nat["year"].max()
s1_0, s1_1 = nat["s1"].iloc[0], nat["s1"].iloc[-1]
s2_0, s2_1 = nat["s2"].iloc[0], nat["s2"].iloc[-1]
n_cities = stations["city"].nunique()
n_2025 = stations[stations["year"] == y1]["station_id"].nunique()

# ── Hero ──────────────────────────────────────────────────────────────
st.markdown(
    f"<h1 style='margin-bottom:0'>🚇 {t('app_title')}</h1>"
    f"<p style='font-size:1.15rem;color:{MUTED};margin-top:.2rem'>{t('app_tagline')}</p>",
    unsafe_allow_html=True,
)
st.write("")

# ── KPIs ──────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric(t("kpi_cities"), n_cities)
c2.metric(t("kpi_stations"), f"{n_2025:,}")
c3.metric(t("kpi_years"), f"{y0}–{y1}")
c4.metric(t("kpi_s1_drop"), f"{(s1_1 - s1_0) / s1_0:+.0%}",
          delta=f"{human(s1_1)} vs {human(s1_0)}", delta_color="off")

st.write("")
left, right = st.columns([3, 2], gap="large")

# ── Dilution chart (indexed to first year = 100) ──────────────────────
with left:
    headline = ("网络扩张，服务变薄" if lang == "zh"
                else "As the network grew, service thinned")
    st.subheader(headline)
    s1_idx = nat["s1"] / s1_0 * 100
    s2_idx = nat["s2"] / s2_0 * 100
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=nat["year"], y=s2_idx, name=t("s2_name"),
        mode="lines", line=dict(color=PRIMARY, width=3)))
    fig.add_trace(go.Scatter(
        x=nat["year"], y=s1_idx, name=t("s1_name"),
        mode="lines", line=dict(color="#EF4444", width=3)))
    fig.add_hline(y=100, line=dict(color=MUTED, width=1, dash="dot"))
    fig.update_yaxes(title_text=("指数 (2000=100)" if lang == "zh"
                                 else "Index (2000 = 100)"))
    style_fig(fig, height=340)
    st.plotly_chart(fig, config={"displayModeBar": False})
    st.caption(
        ("中位站点的网络可达性 S₂ 翻了一倍多，服务强度 S₁ 却持续下降——"
         "这就是“扩张却稀释”。" if lang == "zh"
         else "The median station's network reach (S₂) more than doubled while its "
              "service intensity (S₁) kept falling — the dilution effect."))

# ── Framework explainer + 2×2 legend ──────────────────────────────────
with right:
    st.subheader(t("framework_title"))
    st.markdown(t("framework_body"))
    st.write("")
    grid = "<div style='display:grid;grid-template-columns:1fr 1fr;gap:8px'>"
    for code in TYPE_ORDER:
        grid += (
            f"<div style='background:{TYPE_COLORS[code]}22;"
            f"border-left:4px solid {TYPE_COLORS[code]};border-radius:6px;"
            f"padding:8px 10px'>"
            f"<b style='color:{TYPE_COLORS[code]}'>{code}</b><br>"
            f"<span style='font-size:.8rem;color:{MUTED}'>{type_label(code, lang)}</span>"
            f"</div>")
    grid += "</div>"
    st.markdown(grid, unsafe_allow_html=True)

# ── Jump-off links ────────────────────────────────────────────────────
st.divider()
st.markdown(f"#### {'开始探索' if lang == 'zh' else 'Start exploring'}")
l1, l2, l3, l4 = st.columns(4)
with l1:
    st.page_link("views/national_map.py", label=t("page_map"), icon="🗺️")
with l2:
    st.page_link("views/explorer.py", label=t("page_2d"), icon="🎯")
with l3:
    st.page_link("views/city_profile.py", label=t("page_city"), icon="🏙️")
with l4:
    st.page_link("views/rankings.py", label=t("page_rank"), icon="🏆")
