import streamlit as st
import pandas as pd
import plotly.express as px

# ════════════════════════════════════════════
# LOAD DATA
# ════════════════════════════════════════════
@st.cache_data
def load_data():
    matches = pd.read_csv("data/matches.csv")
    deliveries = pd.read_csv("data/deliveries.csv")
    return matches, deliveries

matches, deliveries = load_data()

# ════════════════════════════════════════════
# PAGE TITLE
# ════════════════════════════════════════════
st.title("📅 Season Overview")
st.markdown("IPL season-by-season breakdown — runs, winners, and record holders.")

st.divider()

# ════════════════════════════════════════════
# SECTION 1 — STAT CARDS (top of page)
# ════════════════════════════════════════════
st.header("🏅 All-Time Records")

# ── Card 1: Most Wins ──────────────────────
most_wins_team = (
    matches["winner"]
    .value_counts()
    .idxmax()
)
most_wins_count = (
    matches["winner"]
    .value_counts()
    .max()
)

# ── Card 2: Highest Run Scorer (Orange Cap all-time) ──
highest_scorer = (
    deliveries.groupby("batter")["batsman_runs"]
    .sum()
    .idxmax()
)
highest_scorer_runs = (
    deliveries.groupby("batter")["batsman_runs"]
    .sum()
    .max()
)

# ── Card 3: Purple Cap (Most Wickets all-time) ──
# Only count actual wickets — filter is_wicket == 1
# Exclude run outs (fielder takes credit, not bowler)
wickets_df = deliveries[
    (deliveries["is_wicket"] == 1) &
    (deliveries["dismissal_kind"] != "run out")
]
purple_cap_bowler = (
    wickets_df.groupby("bowler")["is_wicket"]
    .sum()
    .idxmax()
)
purple_cap_wickets = (
    wickets_df.groupby("bowler")["is_wicket"]
    .sum()
    .max()
)

# ── Display 3 cards side by side ──────────
col1, col2, col3 = st.columns(3)

col1.metric(
    label="🏆 Most Wins (All Time)",
    value=most_wins_team,
    delta=f"{most_wins_count} wins"
)

col2.metric(
    label="🧡 Orange Cap (All Time)",
    value=highest_scorer,
    delta=f"{highest_scorer_runs} runs"
)

col3.metric(
    label="💜 Purple Cap (All Time)",
    value=purple_cap_bowler,
    delta=f"{int(purple_cap_wickets)} wickets"
)

st.divider()

# ════════════════════════════════════════════
# SECTION 2 — LINE CHART: Runs per Season
# ════════════════════════════════════════════
st.header("📈 Total Runs Scored per Season")

# Step 1: merge deliveries with matches to get season column
# deliveries has match_id, matches has id → join on these
runs_per_season = (
    deliveries
    .merge(
        matches[["id", "season"]],   # only need id + season from matches
        left_on="match_id",
        right_on="id"
    )
    .groupby("season")["total_runs"]
    .sum()
    .reset_index()
)
runs_per_season.columns = ["Season", "Total Runs"]
runs_per_season = runs_per_season.sort_values("Season")

fig1 = px.line(
    runs_per_season,
    x="Season",
    y="Total Runs",
    markers=True,
    title="Total Runs Scored Across All Matches per Season",
    line_shape="spline"
)
fig1.update_traces(
    line_color="#E9001C",
    marker=dict(size=8, color="#FFFFFF", line=dict(color="#E9001C", width=2))
)
fig1.update_layout(
    plot_bgcolor="#13131A",
    paper_bgcolor="#13131A",
    font_color="#FFFFFF",
    xaxis=dict(showgrid=False, title="Season"),
    yaxis=dict(showgrid=True, gridcolor="#2A3445", title="Total Runs"),
    hovermode="x unified"
)
st.plotly_chart(fig1, use_container_width=True)

st.divider()

# ════════════════════════════════════════════
# SECTION 3 — BAR CHART: Wins per Team per Season
# ════════════════════════════════════════════
st.header("🏏 Team Wins per Season")

# Season selector dropdown
all_seasons = sorted(matches["season"].unique())
selected_season = st.selectbox(
    "Select Season",
    options=all_seasons,
    index=len(all_seasons) - 1   # default = latest season
)

# Filter matches for selected season
season_matches = matches[matches["season"] == selected_season]

# Count wins per team in that season
wins_in_season = (
    season_matches["winner"]
    .value_counts()
    .reset_index()
)
wins_in_season.columns = ["Team", "Wins"]

fig2 = px.bar(
    wins_in_season,
    x="Team",
    y="Wins",
    color="Wins",
    color_continuous_scale=["#1E2530", "#E9001C"],
    title=f"Team Wins in {selected_season} Season"
)
fig2.update_layout(
    plot_bgcolor="#13131A",
    paper_bgcolor="#13131A",
    font_color="#FFFFFF",
    xaxis_tickangle=-45,
    coloraxis_showscale=False,
    showlegend=False
)
st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ════════════════════════════════════════════
# SECTION 4 — SEASON STATS TABLE
# ════════════════════════════════════════════
st.header("📋 Season-by-Season Summary Table")

# Build summary per season
summary_rows = []

for season in sorted(matches["season"].unique()):
    s_matches = matches[matches["season"] == season]

    # Total matches that season
    total_matches = len(s_matches)

    # Champion = team with most wins that season
    if s_matches["winner"].notna().any():
        champion = s_matches["winner"].value_counts().idxmax()
    else:
        champion = "N/A"

    # Total runs that season
    season_ids = s_matches["id"].tolist()
    season_deliveries = deliveries[deliveries["match_id"].isin(season_ids)]
    total_runs_season = season_deliveries["total_runs"].sum()

    # Top scorer that season
    if len(season_deliveries) > 0:
        top_scorer = (
            season_deliveries.groupby("batter")["batsman_runs"]
            .sum()
            .idxmax()
        )
        top_scorer_runs = (
            season_deliveries.groupby("batter")["batsman_runs"]
            .sum()
            .max()
        )
    else:
        top_scorer = "N/A"
        top_scorer_runs = 0

    summary_rows.append({
        "Season": season,
        "Matches": total_matches,
        "Total Runs": total_runs_season,
        "Top Scorer": f"{top_scorer} ({top_scorer_runs})",
        "Most Wins": champion
    })

summary_df = pd.DataFrame(summary_rows)

st.dataframe(
    summary_df,
    use_container_width=True,
    hide_index=True
)
