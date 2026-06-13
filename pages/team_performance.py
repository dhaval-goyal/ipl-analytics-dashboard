import streamlit as st
import pandas as pd
import plotly.express as px

# ─── Page Config ───────────────────────────────────────────────
st.set_page_config(page_title="Team Performance", layout="wide")

# ─── Custom Styling (your dark theme) ──────────────────────────
st.markdown("""
    <style>
        .block-container { background-color: #13131A; }
        body { color: white; }
    </style>
""", unsafe_allow_html=True)

# ─── Load Data ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/matches.csv")
    return df

df = load_data()

# ─── Sidebar Filter ────────────────────────────────────────────
st.sidebar.header("Filters")

seasons = ["All Seasons"] + sorted(df["season"].unique().tolist())
selected_season = st.sidebar.selectbox("Select Season", seasons)

# ─── Filter Logic ──────────────────────────────────────────────
if selected_season == "All Seasons":
    filtered_df = df
else:
    filtered_df = df[df["season"] == selected_season]

    # ─── Compute Wins Per Team ─────────────────────────────────────
wins = (
    filtered_df["winner"]
    .value_counts()
    .reset_index()
)
wins.columns = ["Team", "Wins"]
wins = wins.sort_values("Wins", ascending=False)

# ─── Chart ─────────────────────────────────────────────────────
st.title("🏆 Team Performance")
st.subheader(f"Wins per Team — {selected_season}")

fig = px.bar(
    wins,
    x="Team",
    y="Wins",
    color="Wins",                        # color bars by win count
    color_continuous_scale="Reds",       # red gradient (matches your #E9001C theme)
    title=f"Wins per Team ({selected_season})",
    template="plotly_dark",              # dark background chart
)

fig.update_layout(
    plot_bgcolor="#13131A",
    paper_bgcolor="#13131A",
    font_color="white",
    xaxis_tickangle=-45,                 # angled team names so they don't overlap
)

st.plotly_chart(fig, use_container_width=True)

# ─── Raw Data Preview (optional but useful) ────────────────────
with st.expander("📄 View Raw Data"):
    st.dataframe(wins, use_container_width=True)