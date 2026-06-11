import streamlit as st
import pandas as pd
import plotly.express as px

# ── Load data ──────────────────────────────────────
@st.cache_data
def load_data():
    matches = pd.read_csv("data/matches.csv")
    return matches

matches = load_data()

# ── Page title ─────────────────────────────────────
st.title("🏟️ Venue Analysis")
st.markdown("How different venues affect match outcomes and toss decisions.")

st.divider()

# ══════════════════════════════════════════════════
# SECTION 1 — Matches per Venue
# ══════════════════════════════════════════════════
st.header("📊 Matches Played per Venue")

venue_counts = (
    matches["venue"]
    .value_counts()
    .reset_index()
)
venue_counts.columns = ["Venue", "Matches"]

# Show only top 15 venues (less clutter)
top_venues = venue_counts.head(15)

fig1 = px.bar(
    top_venues,
    x="Matches",
    y="Venue",
    orientation="h",
    color="Matches",
    color_continuous_scale="Blues",
    title="Top 15 Venues by Number of Matches"
)
fig1.update_layout(
    plot_bgcolor="#13131A",
    paper_bgcolor="#13131A",
    font_color="#FFFFFF",
    yaxis=dict(autorange="reversed"),
    coloraxis_showscale=False
)
st.plotly_chart(fig1, use_container_width=True)

st.divider()

# ══════════════════════════════════════════════════
# SECTION 2 — Toss Decision per Venue
# ══════════════════════════════════════════════════
st.header("🎯 Toss Decision Breakdown by Venue")

# Count how many times each venue had bat vs field decision
toss_venue = (
    matches.groupby(["venue", "toss_decision"])
    .size()
    .reset_index(name="count")
)

# Filter to top 10 venues only (readable chart)
top10 = venue_counts.head(10)["Venue"].tolist()
toss_venue_top10 = toss_venue[toss_venue["venue"].isin(top10)]

fig2 = px.bar(
    toss_venue_top10,
    x="venue",
    y="count",
    color="toss_decision",
    barmode="group",
    color_discrete_map={"bat": "#E9001C", "field": "#00D4FF"},
    title="Bat vs Field Toss Decision — Top 10 Venues"
)
fig2.update_layout(
    plot_bgcolor="#13131A",
    paper_bgcolor="#13131A",
    font_color="#FFFFFF",
    xaxis_tickangle=-45,
    legend_title="Toss Decision"
)
st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ══════════════════════════════════════════════════
# SECTION 3 — Win % After Winning Toss per Venue
# ══════════════════════════════════════════════════
st.header("🏆 Toss Win → Match Win % per Venue")

# Step 1: Mark whether toss winner = match winner
matches["toss_won_match"] = matches["toss_winner"] == matches["winner"]

# Step 2: Group by venue → calculate win %
toss_win_pct = (
    matches.groupby("venue")["toss_won_match"]
    .agg(["sum", "count"])
    .reset_index()
)
toss_win_pct.columns = ["Venue", "Toss_Then_Won", "Total_Matches"]
toss_win_pct["Win_Pct"] = round(
    (toss_win_pct["Toss_Then_Won"] / toss_win_pct["Total_Matches"]) * 100, 2
)

# Filter: only venues with 10+ matches (small sample = unreliable %)
toss_win_pct = toss_win_pct[toss_win_pct["Total_Matches"] >= 10]
toss_win_pct = toss_win_pct.sort_values("Win_Pct", ascending=False)

fig3 = px.bar(
    toss_win_pct,
    x="Win_Pct",
    y="Venue",
    orientation="h",
    color="Win_Pct",
    color_continuous_scale=["#1E1E2B", "#E9001C"],
    title="Win % After Winning Toss (min 10 matches)"
)
fig3.update_layout(
    plot_bgcolor="#13131A",
    paper_bgcolor="#13131A",
    font_color="#FFFFFF",
    yaxis=dict(autorange="reversed"),
    coloraxis_showscale=False
)
fig3.add_vline(
    x=50,
    line_dash="dash",
    line_color="#888888",
    annotation_text="50% baseline",
    annotation_font_color="#888888"
)
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ══════════════════════════════════════════════════
# SECTION 4 — EDEN GARDENS DEEP DIVE
#              THIS IS YOUR EVAL NOTES INSIGHT
# ══════════════════════════════════════════════════
st.header("🔍 Eden Gardens Deep Dive")

# Filter only Eden Gardens matches
eden = matches[matches["venue"] == "Eden Gardens"].copy()

total_eden = len(eden)

if total_eden == 0:
    st.warning("No Eden Gardens matches found. Check venue name in your dataset.")
else:
    # Toss winner = match winner %
    eden["toss_won_match"] = eden["toss_winner"] == eden["winner"]
    eden_toss_win_pct = round(eden["toss_won_match"].mean() * 100, 2)

    # Toss decision breakdown
    toss_dec_eden = eden["toss_decision"].value_counts()

    # Most common decision
    most_common_decision = toss_dec_eden.idxmax()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        label="Total Matches at Eden Gardens",
        value=total_eden
    )
    col2.metric(
        label="Toss Winner → Match Winner %",
        value=f"{eden_toss_win_pct}%"
    )
    col3.metric(
        label="Most Common Toss Decision",
        value=most_common_decision.upper()
    )

    st.markdown("---")

    # Toss decision pie
    fig4 = px.pie(
        values=toss_dec_eden.values,
        names=toss_dec_eden.index,
        color_discrete_map={"bat": "#E9001C", "field": "#00D4FF"},
        title="Toss Decision at Eden Gardens"
    )
    fig4.update_layout(
        plot_bgcolor="#13131A",
        paper_bgcolor="#13131A",
        font_color="#FFFFFF"
    )
    st.plotly_chart(fig4, use_container_width=True)

    # ── THE EVAL NOTE NUMBER ────────────────────────
    st.subheader("📝 Key Insight for Eval Notes")
    st.info(
        f"At **Eden Gardens**, the toss winner went on to win the match "
        f"**{eden_toss_win_pct}%** of the time across {total_eden} matches. "
        f"Teams most commonly chose to **{most_common_decision}** after winning the toss. "
        f"This suggests toss advantage at Eden Gardens is "
        f"{'significant' if eden_toss_win_pct > 55 else 'below average' if eden_toss_win_pct < 45 else 'roughly average'}."
    )

    # Show raw Eden Gardens data
    with st.expander("See raw Eden Gardens match data"):
        st.dataframe(
            eden[["season", "date", "team1", "team2",
                  "toss_winner", "toss_decision", "winner"]],
            use_container_width=True
        )