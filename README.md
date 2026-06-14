# 🏏 IPL Analytics Dashboard

An interactive cricket analytics web app built with Python and Streamlit — exploring **13 seasons** of IPL data (2008–2020) across **816 matches**, **15 teams**, and **34 venues**.

---

## 📌 About

This dashboard transforms raw IPL ball-by-ball data into actionable insights across 5 analytical pages:

| Page | What it shows |
|------|--------------|
| 🏠 Home | Season overview, key metrics, highlights, points table |
| 🏆 Team Performance | Wins per team, season filter, color-scaled bar chart |
| 🏏 Batting Stats | Top 10 batsmen by runs + strike rate, team/season filter |
| 🎯 Bowling Stats | Top 10 wicket-takers by economy, min 20 overs threshold |
| 🏟️ Venue Analysis | Toss→win % per venue, 50% baseline reference, deep dive |

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

---

## ⚙️ Setup Instructions

```bash
# 1. Clone repo
git clone https://github.com/YOUR_USERNAME/ipl-analytics-dashboard.git
cd ipl-analytics-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run app
streamlit run app.py
```

> App opens at `http://localhost:8501`

---

## 📸 Screenshots

### 🏠 Home — Season Overview
![Home Page](assets/home.png)

### 🏆 Team Performance
![Team Performance](assets/team_performance.png)

### 🏏 Batting Stats
![Batting Stats](assets/batting_stats.png)

### 🎯 Bowling Stats
![Bowling Stats](assets/bowling_stats.png)

### 🏟️ Venue Analysis
![Venue Analysis](assets/venue_analysis.png)

---

## 🚀 Live Demo

🔗 **[ipl-analytics-dashboard.streamlit.app](https://ipl-analytics-dashboard-g5jttpzbyymuqwtz9xubp7.streamlit.app/)**

---

## 📦 Dataset Source

📊 **[IPL Ball-by-Ball 2008–2020 — Kaggle](https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020)**

- `matches.csv` — match-level metadata
- `deliveries.csv` — ball-by-ball records

---

## 📝 Evaluation Notes

### What works well
- Dark-themed UI (`#13131A` bg, `#E9001C` accent) consistent across all pages
- Dual-metric Plotly charts (bar length = primary stat, color = secondary stat)
- Season + team filters on Batting/Bowling pages
- Venue toss-win analysis with 50% baseline reference line

### Known limitations
- Dataset capped at IPL 2020 (no 2021–2024 data)
- `batter` column rename required for newer Pandas compatibility (`batsman` → `batter`)
- No player headshots / team logos (future scope)

### Potential improvements
- Add Head-to-Head matchup page
- Integrate live 2024 IPL data via CricAPI
- Deploy with Docker for reproducibility

---

## 📁 Project Structure

```
ipl-analytics-dashboard/
├── app.py                  # Main Streamlit entry point
├── pages/
│   ├── Team_Performance.py
│   ├── Batting_Stats.py
│   ├── Bowling_Stats.py
│   └── venue_analysis.py
├── data/
│   ├── matches.csv
│   └── deliveries.csv
├── assets/                 # Screenshots
├── requirements.txt
└── README.md
```

---

*Built as Month 1 portfolio project | Data Science & AI Engineering roadmap*
