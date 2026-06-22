"""Bilingual (English / 中文) text for the whole app.

Usage in a page:
    from lib.i18n import language_selector, make_t, city_label
    lang = language_selector()       # renders the sidebar toggle, returns 'en'|'zh'
    t = make_t(lang)
    st.title(t("app_title"))
"""
import streamlit as st

# ── City names (44 studied cities) ────────────────────────────────────
CITY_CN = {
    "Beijing": "北京", "Shanghai": "上海", "Guangzhou": "广州", "Shenzhen": "深圳",
    "Chengdu": "成都", "Chongqing": "重庆", "Hangzhou": "杭州", "Wuhan": "武汉",
    "Xian": "西安", "Zhengzhou": "郑州", "Nanjing": "南京", "Tianjin": "天津",
    "Suzhou": "苏州", "Changsha": "长沙", "Dongguan": "东莞", "Shenyang": "沈阳",
    "Qingdao": "青岛", "Ningbo": "宁波", "Foshan": "佛山", "Kunming": "昆明",
    "Hefei": "合肥", "Dalian": "大连", "Fuzhou": "福州", "Xiamen": "厦门",
    "Harbin": "哈尔滨", "Changchun": "长春", "Nanchang": "南昌", "Wuxi": "无锡",
    "Guiyang": "贵阳", "Shijiazhuang": "石家庄", "Nanning": "南宁", "Taiyuan": "太原",
    "Lanzhou": "兰州", "Urumqi": "乌鲁木齐", "Hohhot": "呼和浩特", "Jinan": "济南",
    "Changzhou": "常州", "Nantong": "南通", "Wenzhou": "温州", "Xuzhou": "徐州",
    "Shaoxing": "绍兴", "Luoyang": "洛阳", "Wuhu": "芜湖", "Chuzhou": "滁州",
}

TIER_LABEL = {
    "Tier-1": {"en": "Tier-1", "zh": "一线"},
    "New Tier-1": {"en": "New Tier-1", "zh": "新一线"},
    "Tier-2": {"en": "Tier-2", "zh": "二线"},
    "Tier-3": {"en": "Tier-3", "zh": "三线"},
}

# Two-dimensional types: short code + descriptive label
TYPE_LABEL = {
    "HH": {"en": "High service · High access", "zh": "高服务 · 高可达"},
    "HL": {"en": "High service · Low access", "zh": "高服务 · 低可达"},
    "LH": {"en": "Low service · High access", "zh": "低服务 · 高可达"},
    "LL": {"en": "Low service · Low access", "zh": "低服务 · 低可达"},
}

# ── Core UI strings ───────────────────────────────────────────────────
STR = {
    "app_title": {"en": "China Metro Accessibility Atlas",
                  "zh": "中国地铁可达性图谱"},
    "app_tagline": {
        "en": "How 44 Chinese cities scaled their metros — and what it did to service, 2000–2025",
        "zh": "44 座中国城市的地铁如何扩张，又如何稀释了服务 · 2000–2025"},
    "nav_home": {"en": "Home", "zh": "首页"},
    "lang_label": {"en": "Language", "zh": "语言"},

    # framework
    "s1_name": {"en": "Service intensity (S₁)", "zh": "服务强度 (S₁)"},
    "s2_name": {"en": "Network accessibility (S₂)", "zh": "网络可达性 (S₂)"},
    "s1_desc": {"en": "Residents served within a station's catchment",
                "zh": "站点覆盖范围内的服务人口"},
    "s2_desc": {"en": "Opportunities reachable through the network",
                "zh": "经由网络可达的机会数量"},
    "framework_title": {"en": "The two-dimensional framework",
                        "zh": "二维分析框架"},
    "framework_body": {
        "en": "Every station is placed on two axes — how many people it serves "
              "(**service intensity, S₁**) and how much of the city it can reach "
              "(**network accessibility, S₂**). Splitting each axis at its annual "
              "median sorts stations into four types. As networks expand outward, "
              "new stations increasingly land in low-service zones — service is "
              "**diluted** even as reach grows.",
        "zh": "每个站点都被放在两条轴上——它服务多少人(**服务强度 S₁**)、又能触达城市多大范围"
              "(**网络可达性 S₂**)。把两条轴各自按年度中位数一分为二，站点便归入四种类型。"
              "随着网络向外扩张，新站越来越多地落在低服务区——可达性提升的同时，服务被**稀释**了。"},

    # KPIs / metrics
    "kpi_cities": {"en": "Cities", "zh": "城市"},
    "kpi_stations": {"en": "Stations (2025)", "zh": "站点数 (2025)"},
    "kpi_years": {"en": "Years covered", "zh": "覆盖年份"},
    "kpi_s1_drop": {"en": "Median S₁ change, 2000→2025",
                    "zh": "S₁ 中位数变化 2000→2025"},
    "metric_median_s1": {"en": "Median service intensity", "zh": "服务强度中位数"},
    "metric_median_s2": {"en": "Median network accessibility", "zh": "网络可达性中位数"},
    "metric_gini_s1": {"en": "Service inequality (Gini, S₁)", "zh": "服务不均(基尼 S₁)"},
    "metric_gini_s2": {"en": "Access inequality (Gini, S₂)", "zh": "可达不均(基尼 S₂)"},
    "metric_n": {"en": "Number of stations", "zh": "站点数量"},
    "metric_new": {"en": "New stations this year", "zh": "当年新增站点"},

    # controls
    "ctrl_city": {"en": "City", "zh": "城市"},
    "ctrl_cities": {"en": "Cities", "zh": "城市"},
    "ctrl_year": {"en": "Year", "zh": "年份"},
    "ctrl_tier": {"en": "Tier", "zh": "城市层级"},
    "ctrl_color_by": {"en": "Colour by", "zh": "着色依据"},
    "ctrl_metric": {"en": "Metric", "zh": "指标"},
    "ctrl_all": {"en": "All", "zh": "全部"},
    "color_by_type": {"en": "Station type", "zh": "站点类型"},
    "color_by_s1": {"en": "Service intensity (S₁)", "zh": "服务强度 (S₁)"},
    "color_by_s2": {"en": "Network accessibility (S₂)", "zh": "网络可达性 (S₂)"},

    # pages
    "page_map": {"en": "National map", "zh": "全国地图"},
    "page_2d": {"en": "S₁ × S₂ explorer", "zh": "S₁ × S₂ 探索器"},
    "page_city": {"en": "City profile", "zh": "城市档案"},
    "page_rank": {"en": "Rankings & compare", "zh": "排名与对比"},
    "map_subtitle": {"en": "Every metro station, year by year",
                     "zh": "逐年展开的每一个地铁站"},
    "explorer_subtitle": {"en": "Where each station sits on the two axes",
                          "zh": "每个站点在双维度上的位置"},
    "city_subtitle": {"en": "One city's trajectory in depth",
                      "zh": "单座城市的演化轨迹"},
    "rank_subtitle": {"en": "Compare and rank all 44 cities",
                      "zh": "对全部 44 城排名与对比"},

    # misc
    "download_csv": {"en": "Download data (CSV)", "zh": "下载数据 (CSV)"},
    "data_note": {
        "en": "Data: de-identified station-year panel from the study; station "
              "coordinates and names from the public metro dataset. Service values "
              "are model outputs, not personal data.",
        "zh": "数据：研究所用的去标识站点-年面板；站点坐标与名称来自公开地铁数据集。"
              "服务数值为模型输出，非个人数据。"},
    "play": {"en": "▶ Play years", "zh": "▶ 播放年份"},
    "type_legend": {"en": "Station types", "zh": "站点类型"},
}


def language_selector() -> str:
    """Render the sidebar language toggle and return 'en' or 'zh'."""
    if "lang" not in st.session_state:
        st.session_state["lang"] = "zh"
    choice = st.sidebar.radio(
        "🌐 Language / 语言",
        options=["中文", "English"],
        index=0 if st.session_state["lang"] == "zh" else 1,
        horizontal=True,
        key="_lang_radio",
    )
    st.session_state["lang"] = "zh" if choice == "中文" else "en"
    return st.session_state["lang"]


def current_lang() -> str:
    """Read the active language without rendering the toggle (for views)."""
    return st.session_state.get("lang", "zh")


def make_t(lang: str):
    def t(key: str) -> str:
        entry = STR.get(key)
        if entry is None:
            return key
        return entry.get(lang, entry.get("en", key))
    return t


def city_label(city_en: str, lang: str) -> str:
    if lang == "zh":
        return CITY_CN.get(city_en, city_en)
    return city_en


def tier_label(tier: str, lang: str) -> str:
    return TIER_LABEL.get(tier, {}).get(lang, tier)


def type_label(code: str, lang: str) -> str:
    return TYPE_LABEL.get(code, {}).get(lang, code)
