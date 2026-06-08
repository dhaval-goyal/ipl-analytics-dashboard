import streamlit as st
import pandas as pd
import plotly.express as px

#Now setting dark theme same as the team performance one.
st.set_page_config(page_title="Batting Stats", layout="wide")

st.markdown("""
    <style>
        .block-container { background-color: #13131A; }
    </style>
""", unsafe_allow_html=True)

#Loading both the csv files
@st.cache_data
def load_data():
    deliveries = pd.read_csv("data/deliveries.csv")
    matches = pd.read_csv("data/matches.csv")
    return deliveries, matches

deliveries, matches = load_data()

#Merging the two dataframes on match_id to get season information in deliveries
# Get only match_id and season from matches
match_season = matches[["id", "season"]].rename(columns={"id": "match_id"})

# Join season column into deliveries
deliveries = deliveries.merge(match_season, on="match_id", how="left")

#Applying the same season filter as team performance page
st.sidebar.header("Filters")

# Season filter
all_seasons = ["All Seasons"] + sorted(deliveries["season"].unique().tolist())
selected_season = st.sidebar.selectbox("Select Season", all_seasons)

# Team filter
all_teams = ["All Teams"] + sorted(deliveries["batting_team"].unique().tolist())
selected_team = st.sidebar.selectbox("Select Batting Team", all_teams)

filtered = deliveries.copy()

if selected_season != "All Seasons":
    filtered = filtered[filtered["season"] == selected_season]

if selected_team != "All Teams":
    filtered = filtered[filtered["batting_team"] == selected_team]


#Aggregate — Runs + Balls + Strike Rate
batting_stats = (
    filtered.groupby("batter")
    .agg(
        Runs=("batsman_runs", "sum"),       # total runs scored
        Balls=("batsman_runs", "count"),    # balls faced = rows count
    )
    .reset_index()
)
# Add strike rate column
batting_stats["Strike Rate"] = (
    (batting_stats["Runs"] / batting_stats["Balls"]) * 100
).round(2)

# Top 10 by runs
top10 = batting_stats.sort_values("Runs", ascending=False).head(10)

#creating the chart priotising horizontal bars to fit long names and match the team performance style
st.title("🏏 Batting Stats")
st.subheader(f"Top 10 Batsmen — {selected_season} | {selected_team}")

fig = px.bar(
    top10,
    x="Runs",              # runs on X axis (horizontal bar needs x=value, y=category)
    y="batter",            # batter names on Y axis
    orientation="h",       # h = horizontal
    color="Strike Rate",   # color by strike rate
    color_continuous_scale="Reds",
    text="Runs",           # show run value on bar
    title="Top 10 Batsmen by Runs",
    template="plotly_dark",
)

fig.update_layout(
    plot_bgcolor="#13131A",
    paper_bgcolor="#13131A",
    font_color="white",
    yaxis={"categoryorder": "total ascending"},  # highest at top
)

fig.update_traces(textposition="outside")  # run numbers outside bar

st.plotly_chart(fig, use_container_width=True)

st.markdown("### 📊 Full Stats Table")
display_df = batting_stats.sort_values("Runs", ascending=False).reset_index(drop=True)
display_df.index = display_df.index + 1
st.dataframe(display_df, use_container_width=True)

