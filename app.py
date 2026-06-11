import streamlit as st

st.set_page_config(page_title="IPL Analytics Dashboard", layout="wide")
st.title("🏏 IPL Analytics Dashboard")
st.write("Welcome to the IPL Analytics Dashboard.")

import streamlit as st

st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Colour scheme from Figma, simple clean CSS ───────────────
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

    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #1E1E2B;
        border-radius: 12px;
        padding: 16px;
        border: 1px solid rgba(255,255,255,0.06);
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background-color: #1E1E2B;
        border: 1px solid rgba(255,255,255,0.1);
        color: white;
    }

    /* Divider */
    hr {
        border-color: rgba(255,255,255,0.08) !important;
    }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<div style='background:#E9001C; border-radius:8px; padding:8px 16px;"
        "font-size:22px; font-weight:900; color:white; text-align:center;"
        "margin-bottom:16px;'>🏏 IPL</div>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    page = st.selectbox(
        "Navigate",
        [
            "🏠  Home",
            "🏆  Team Performance",
            "🏏  Batting Stats",
            "🎳  Bowling Stats",
            "🏟️  Venue Analysis",
            "📅  Season Overview"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.caption("📅 Seasons: 2008 – 2020")
    st.caption("📦 Source: Kaggle")

# ── MAIN CONTENT ──────────────────────────────────────────────
if page == "🏠  Home":
    st.markdown("## Analytics:")
    st.markdown("Historical data from **2008 to 2020** · 816 matches · 15 teams")
    st.divider()

    # Stat cards
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Matches", "816")
    c2.metric("Total Seasons", "13")
    c3.metric("Teams", "15")
    c4.metric("Venues", "34")

    st.divider()

    # Two column layout
    left, right = st.columns([2, 1])

    with left:
        st.markdown("### 🎬 Highlights")
        st.info("**SRH v/s PBK** · Punjab Kings won by 6 wickets")
        st.info("**CSK v/s KKR** · Chennai Super Kings won by 2 wickets")
        st.info("**RCB v/s MI** · Harshal Patel hat-trick, RCB won by 54 runs")

    with right:
        st.markdown("### 📊 Points Table (2020)")
        data = {
            "Team": ["Delhi Capitals", "Chennai Super Kings", "Royal Challengers Bangalore", "Mumbai Indians", "Rajasthan Royals"],
            "PTS": [12, 10, 10, 8, 6]
        }
        st.dataframe(data, hide_index=True, use_container_width=True)

        st.markdown("---")
        st.markdown("### 🟠Orange Cap")
        st.success("**Shikhar Dhawan** · 380 runs")

else:
    st.markdown(f"## {page}")
    st.divider()
    st.warning("🚧 Under construction — coming soon!")

pg = st.navigation([
    st.Page("pages/home.py", title="Home"),
    st.Page("pages/team_performance.py", title="Team Performance"),
    st.Page("pages/batting_stats.py", title="Batting Stats"),
    st.Page("pages/bowling_stats.py", title="Bowling Stats"),
    st.Page("pages/venue_analysis.py", title="Venue Analysis"),  # ← ADD THIS
])