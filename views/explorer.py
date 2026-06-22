"""S₁ × S₂ explorer — the two-dimensional signature plot."""
import plotly.express as px
import streamlit as st

from lib.i18n import current_lang, make_t, city_label, type_label
from lib.data import load_stations, cities_ordered, year_bounds
from lib.charts import style_fig
from lib.theme import TYPE_COLORS, TYPE_ORDER, MUTED

lang = current_lang()
t = make_t(lang)

st.markdown(f"## 🎯 {t('page_2d')}")
st.caption(t("explorer_subtitle"))

stations = load_stations()
ymin, ymax = year_bounds()

c1, c2 = st.columns([2, 2])
with c1:
    year = st.slider(t("ctrl_year"), ymin, ymax, ymax, step=1, key="ex_year")
with c2:
    cities = cities_ordered()
    focus = st.selectbox(
        t("ctrl_city"), ["__all__"] + cities, key="ex_city",
        format_func=lambda c: t("ctrl_all") if c == "__all__" else city_label(c, lang))

yr_all = stations[stations["year"] == year]
thr_s1 = yr_all["s1"].median()           # national annual medians = type thresholds
thr_s2 = yr_all["s2"].median()
dfp = yr_all if focus == "__all__" else yr_all[yr_all["city"] == focus]
dfp = dfp.copy()
dfp["name"] = dfp["name_cn"] if lang == "zh" else dfp["name_en"].fillna(dfp["name_cn"])
dfp["type_disp"] = dfp["type_2d"].map(lambda c: f"{c} · {type_label(c, lang)}")

if dfp.empty:
    st.info(f"{city_label(focus, lang)} · {year}: no stations." if lang == "en"
            else f"{city_label(focus, lang)} 在 {year} 年尚无地铁站。")
    st.stop()

left, right = st.columns([3, 1], gap="large")

with left:
    fig = px.scatter(
        dfp, x="s1", y="s2", color="type_2d",
        color_discrete_map=TYPE_COLORS, category_orders={"type_2d": TYPE_ORDER},
        log_x=True, log_y=True, hover_name="name",
        custom_data=["type_disp", "s1", "s2"],
        labels={"s1": t("s1_name"), "s2": t("s2_name")},
    )
    fig.update_traces(
        marker=dict(size=7, opacity=0.55, line=dict(width=0)),
        hovertemplate="<b>%{hover_name}</b><br>"
                      "S₁ %{customdata[1]:,.0f} · S₂ %{customdata[2]:,.0f}<br>"
                      "%{customdata[0]}<extra></extra>")
    for tr in fig.data:
        tr.name = f"{tr.name} · {type_label(tr.name, lang)}"
    fig.add_vline(x=thr_s1, line=dict(color=MUTED, width=1, dash="dash"))
    fig.add_hline(y=thr_s2, line=dict(color=MUTED, width=1, dash="dash"))
    corners = {"HH": (0.99, 0.99, "right", "top"), "HL": (0.99, 0.01, "right", "bottom"),
               "LH": (0.01, 0.99, "left", "top"), "LL": (0.01, 0.01, "left", "bottom")}
    for code, (x, y, xa, ya) in corners.items():
        fig.add_annotation(x=x, y=y, xref="paper", yref="paper", xanchor=xa, yanchor=ya,
                           text=f"<b>{code}</b>", showarrow=False,
                           font=dict(size=15, color=TYPE_COLORS[code]), opacity=0.9)
    style_fig(fig, height=560, legend_top=True)
    st.plotly_chart(fig, config={"displayModeBar": False})

with right:
    st.markdown(f"**{year}**")
    st.caption(("虚线 = 全国年度中位数；四象限即四种站点类型。"
                if lang == "zh" else
                "Dashed lines = national annual medians; the four quadrants are "
                "the four station types."))
    counts = dfp["type_2d"].value_counts()
    total = len(dfp)
    for code in TYPE_ORDER:
        n = int(counts.get(code, 0))
        pct = n / total if total else 0
        st.markdown(
            f"<div style='border-left:4px solid {TYPE_COLORS[code]};"
            f"padding:2px 10px;margin:6px 0'>"
            f"<b style='color:{TYPE_COLORS[code]}'>{code}</b> "
            f"<span style='color:{MUTED};font-size:.8rem'>{type_label(code, lang)}</span><br>"
            f"<span style='font-size:1.1rem'>{n:,}</span> "
            f"<span style='color:{MUTED}'>({pct:.0%})</span></div>",
            unsafe_allow_html=True)

st.caption(t("data_note"))
