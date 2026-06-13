import pandas as pd

# Load deliveries data (adjust path to yours)
deliveries = pd.read_csv("data/deliveries.csv")

# Wickets — only count actual dismissals, not run outs credited to fielder
# 'is_wicket' column = 1 if wicket fell on that ball
wickets = (
    deliveries[deliveries["is_wicket"] == 1]
    .groupby("bowler")["is_wicket"]
    .sum()
    .reset_index()
    .rename(columns={"is_wicket": "wickets"})
)

# Runs given per bowler
runs_given = (
    deliveries.groupby("bowler")["total_runs"]
    .sum()
    .reset_index()
    .rename(columns={"total_runs": "runs_given"})
)

# Balls bowled per bowler (each row = 1 ball)
balls_bowled = (
    deliveries.groupby("bowler")
    .size()
    .reset_index(name="balls")
)

# Convert balls → overs (6 balls = 1 over)
balls_bowled["overs"] = balls_bowled["balls"] / 6

# Merge all 3 dataframes on 'bowler'
bowling_stats = wickets.merge(runs_given, on="bowler").merge(balls_bowled, on="bowler")

# Economy rate = runs given per over
bowling_stats["economy"] = (bowling_stats["runs_given"] / bowling_stats["overs"]).round(2)

# Remove bowlers who bowled < 20 overs (too little data = misleading stats)
bowling_stats = bowling_stats[bowling_stats["overs"] >= 20]

top10_wickets = bowling_stats.nlargest(10, "wickets").reset_index(drop=True)

import streamlit as st
import plotly.express as px

st.title("🎯 Bowling Stats")

# --- Top 10 Bowlers by Wickets Chart ---
st.subheader("Top 10 Wicket Takers")

fig = px.bar(
    top10_wickets,
    x="wickets",
    y="bowler",
    orientation="h",           # horizontal bar → easier to read long names
    color="economy",           # color = economy rate (bonus insight)
    color_continuous_scale=["green", "yellow", "red"],  # low economy = good = green
    labels={"wickets": "Wickets", "bowler": "Bowler", "economy": "Economy"},
    title="Top 10 Bowlers by Wickets (min 20 overs)"
)

fig.update_layout(
    paper_bgcolor="#13131A",
    plot_bgcolor="#13131A",
    font_color="white",
    yaxis={"categoryorder": "total ascending"},  # highest wickets at top
)

st.plotly_chart(fig, use_container_width=True)

# --- Stats Table ---
st.subheader("Bowling Stats Table")
st.dataframe(
    bowling_stats.sort_values("wickets", ascending=False).head(20),
    use_container_width=True
)
