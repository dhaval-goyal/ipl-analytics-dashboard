import streamlit as st
import pandas as pd

st.title("🏏 IPL Analytics Dashboard")
st.markdown(
    "<p style='color:#888; font-size:15px;'>"
    "Historical data from <b style='color:white;'>2008 to 2020</b> · "
    "816 matches · 15 teams · 34 venues</p>",
    unsafe_allow_html=True
)

st.divider()

from PIL import Image
img = Image.open("assets/ipl_logo.png")
st.image(img, width=200)

# ── Stat cards ────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("🎯 Total Matches", "816")
c2.metric("📅 Total Seasons", "13")
c3.metric("🏟️ Teams", "15")
c4.metric("📍 Venues", "34")

st.divider()

# ── Two column layout ─────────────────────────────────────────
left, right = st.columns([2, 1])

with left:
    st.markdown("### 🏆 2018 Season — Champion & Runner Up")

    st.success("🥇 **Champion — Chennai Super Kings (CSK)**")
    st.error("🥈 **Runner Up — Sunrisers Hyderabad (SRH)**")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### 🏅 2018 Individual Awards")
    col1, col2 = st.columns(2)
    col1.info("🟠 **Orange Cap**\nKane Williamson · 735 runs")
    col2.info("🟣 **Purple Cap**\nAndrew Tye · 24 wickets")

with right:
    st.markdown("### 📊 Points Table (2018)")
    data = {
        "Team": [
            "Sunrisers Hyderabad",
            "Chennai Super Kings",
            "Kolkata Knight Riders",
            "Rajasthan Royals",
            "Mumbai Indians",
            "Royal Challengers Bangalore",
            "Kings XI Punjab",
            "Delhi Daredevils"
        ],
        "W": [9, 9, 8, 7, 6, 6, 6, 2],
        "L": [5, 5, 6, 7, 8, 8, 8, 12],
        "PTS": [18, 18, 16, 14, 12, 12, 12, 4]
    }
    st.dataframe(
        pd.DataFrame(data),
        hide_index=True,
        use_container_width=True
    )