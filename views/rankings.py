"""Rankings & compare — all 44 cities side by side (planner view)."""
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from lib.i18n import current_lang, make_t, city_label, tier_label, CITY_CN
from lib.data import load_city_year, cities_ordered, year_bounds
from lib.charts import style_fig
from lib.theme import TIER_COLORS, TIER_ORDER, PRIMARY, MUTED

lang = current_lang()
t = make_t(lang)

st.markdown(f"## 🏆 {t('page_rank')}")
st.caption(t("rank_subtitle"))

cy = load_city_year()
ymin, ymax = year_bounds()

METRICS = {
    "n_stations": (t("metric_n"), ",.0f", False),
    "s1_median": (t("metric_median_s1"), ",.0f", False),
    "s2_median": (t("metric_median_s2"), ",.0f", False),
    "gini_s1": (t("metric_gini_s1"), ".2f", False),
    "gini_s2": (t("metric_gini_s2"), ".2f", False),
    "pct_HH": ("HH " + ("占比" if lang == "zh" else "share"), ".0%", False),
}

c1, c2 = st.columns([1.4, 2])
with c1:
    year = st.slider(t("ctrl_year"), ymin, ymax, ymax, step=1, key="rk_year")
with c2:
    mkey = st.selectbox(t("ctrl_metric"), list(METRICS),
                        format_func=lambda k: METRICS[k][0])
label, fmt, asc = METRICS[mkey]

snap = cy[(cy["year"] == year) & (cy["n_stations"] > 0)].copy()
snap = snap.sort_values(mkey, ascending=asc)
snap["city_disp"] = snap["city"].map(lambda c: city_label(c, lang))

# ── Ranking bar chart ─────────────────────────────────────────────────
st.markdown(f"**{label} · {year}**")
fig = px.bar(snap, x=mkey, y="city_disp", orientation="h",
             color="tier", color_discrete_map=TIER_COLORS,
             category_orders={"tier": TIER_ORDER,
                              "city_disp": snap["city_disp"].tolist()[::-1]})
fig.update_layout(height=max(420, 16 * len(snap)),
                  yaxis_title="", xaxis_title=label)
fig.update_traces(hovertemplate="%{y}: %{x:" + fmt + "}<extra></extra>")
for tr in fig.data:
    tr.name = tier_label(tr.name, lang)
style_fig(fig, legend_top=True)
st.plotly_chart(fig, config={"displayModeBar": False})

# ── Full sortable table + download ────────────────────────────────────
st.markdown(f"**{'全部城市数据' if lang == 'zh' else 'All cities'} · {year}**")
tbl = snap[["city_disp", "tier", "n_stations", "s1_median", "s2_median",
            "gini_s1", "gini_s2", "pct_HH", "pct_HL", "pct_LH", "pct_LL"]].copy()
tbl.insert(0, "#", range(1, len(tbl) + 1))
st.dataframe(
    tbl, hide_index=True, width="stretch", height=420,
    column_config={
        "#": st.column_config.NumberColumn("#", width="small"),
        "city_disp": st.column_config.TextColumn(t("ctrl_city")),
        "tier": st.column_config.TextColumn(t("ctrl_tier")),
        "n_stations": st.column_config.NumberColumn(t("metric_n"), format="%d"),
        "s1_median": st.column_config.NumberColumn(t("metric_median_s1"), format="%.0f"),
        "s2_median": st.column_config.NumberColumn(t("metric_median_s2"), format="%.0f"),
        "gini_s1": st.column_config.NumberColumn(t("metric_gini_s1"), format="%.2f"),
        "gini_s2": st.column_config.NumberColumn(t("metric_gini_s2"), format="%.2f"),
        "pct_HH": st.column_config.NumberColumn("HH", format="%.0f%%"),
        "pct_HL": st.column_config.NumberColumn("HL", format="%.0f%%"),
        "pct_LH": st.column_config.NumberColumn("LH", format="%.0f%%"),
        "pct_LL": st.column_config.NumberColumn("LL", format="%.0f%%"),
    },
)
dl = snap.copy()
dl["city_cn"] = dl["city"].map(CITY_CN)
csv = dl[["city", "city_cn", "tier", "year", "n_stations", "s1_median",
          "s2_median", "gini_s1", "gini_s2",
          "pct_HH", "pct_HL", "pct_LH", "pct_LL"]].to_csv(index=False)
st.download_button(t("download_csv"), csv,
                   file_name=f"metro_cities_{year}.csv", mime="text/csv")

# ── Multi-city comparison over time ───────────────────────────────────
st.divider()
st.markdown(f"#### {'多城对比' if lang == 'zh' else 'Compare cities over time'}")
cities = cities_ordered()
cc1, cc2 = st.columns([2, 1.4])
with cc1:
    picks = st.multiselect(
        t("ctrl_cities"), cities, default=cities[:4],
        format_func=lambda c: city_label(c, lang))
with cc2:
    cmp_key = st.selectbox(
        t("ctrl_metric"),
        ["s2_median", "s1_median", "n_stations", "gini_s2"],
        format_func=lambda k: METRICS.get(k, (k,))[0], key="cmp_metric")

if picks:
    comp = cy[cy["city"].isin(picks) & (cy["n_stations"] > 0)]
    fig2 = go.Figure()
    for c in picks:
        d = comp[comp["city"] == c].sort_values("year")
        fig2.add_trace(go.Scatter(x=d["year"], y=d[cmp_key], mode="lines",
                                  name=city_label(c, lang), line=dict(width=2.5)))
    fig2.update_yaxes(title_text=METRICS.get(cmp_key, (cmp_key,))[0])
    style_fig(fig2, height=400)
    st.plotly_chart(fig2, config={"displayModeBar": False})
else:
    st.info("选择城市以对比。" if lang == "zh" else "Pick cities to compare.")
st.caption(t("data_note"))
