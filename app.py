import streamlit as st

st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stApp {
        background-color: #13131A;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(160deg, #282833 0%, #121217 100%);
        border-right: 1px solid rgba(255,255,255,0.07);
    }

    [data-testid="stMetric"] {
        background-color: #1E1E2B;
        border-radius: 12px;
        padding: 16px;
        border: 1px solid rgba(255,255,255,0.06);
    }

    .stSelectbox > div > div {
        background-color: #1E1E2B;
        border: 1px solid rgba(255,255,255,0.1);
        color: white;
    }

    hr {
        border-color: rgba(255,255,255,0.08) !important;
    }

    /* Sidebar nav links */
    [data-testid="stSidebarNav"] a {
        font-size: 15px;
        padding: 8px 12px;
        border-radius: 8px;
        color: #CCCCCC !important;
    }

    [data-testid="stSidebarNav"] a:hover {
        background-color: rgba(233,0,28,0.15);
        color: #FFFFFF !important;
    }

    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background-color: rgba(233,0,28,0.25);
        color: #FFFFFF !important;
        font-weight: 700;
        border-left: 3px solid #E9001C;
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar branding ──────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<div style='background:#E9001C; border-radius:8px; padding:8px 16px;"
        "font-size:22px; font-weight:900; color:white; text-align:center;"
        "margin-bottom:8px;'>🏏 IPL Analytics</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align:center; color:#888; font-size:12px;"
        "margin-bottom:16px;'>2008 – 2020 · 816 Matches</p>",
        unsafe_allow_html=True
    )
    st.markdown("---")
    st.caption("📦 Source: Kaggle IPL Dataset")
    st.caption("🛠️ Built with Python + Streamlit")

# ── Navigation ────────────────────────────────────────────────
pg = st.navigation([
    st.Page("pages/home.py",              title="🏠  Home"),
    st.Page("pages/team_performance.py",  title="🏆  Team Performance"),
    st.Page("pages/batting_stats.py",     title="🏏  Batting Stats"),
    st.Page("pages/bowling_stats.py",     title="🎳  Bowling Stats"),
    st.Page("pages/venue_analysis.py",    title="🏟️  Venue Analysis"),
    st.Page("pages/season_overview.py",   title="📅  Season Overview"),
])

pg.run()
