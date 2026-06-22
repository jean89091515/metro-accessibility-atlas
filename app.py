"""China Metro Accessibility Atlas — Streamlit entry point / router."""
import streamlit as st

from lib.i18n import language_selector, make_t

st.set_page_config(
    page_title="China Metro Accessibility Atlas · 中国地铁可达性图谱",
    page_icon="🚇",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Language toggle lives in the sidebar and drives every label, including nav.
lang = language_selector()
t = make_t(lang)

st.sidebar.markdown(f"### 🚇 {t('app_title')}")
st.sidebar.caption(t("app_tagline"))

pages = [
    st.Page("views/home.py", title=t("nav_home"), icon=":material/home:", default=True),
    st.Page("views/national_map.py", title=t("page_map"), icon=":material/map:"),
    st.Page("views/explorer.py", title=t("page_2d"), icon=":material/scatter_plot:"),
    st.Page("views/city_profile.py", title=t("page_city"), icon=":material/location_city:"),
    st.Page("views/rankings.py", title=t("page_rank"), icon=":material/leaderboard:"),
]

st.navigation(pages).run()

st.sidebar.divider()
st.sidebar.caption(t("data_note"))
