# 🦅 Atlanta Hawks Player Performance Dashboard

An end-to-end analytics pipeline built to track Atlanta Hawks player 
performance across the 2025–26 NBA season. The project mirrors front 
office-style workflows by pulling live data, engineering features, and 
surfacing trends through an interactive dashboard.

---

## Overview

Built around the idea that basketball operations teams don't just look 
at box scores — they monitor trends, usage patterns, and short-term vs. 
long-term performance shifts. This pipeline automates that process from 
raw data all the way to a live visual dashboard.

---

## What's Built

### Data Pipeline
- Pulls the current Hawks roster via the NBA Stats API
- Collects game-by-game logs for every rostered player
- Saves raw, unmodified datasets as the source of truth

### Data Cleaning & Feature Engineering
- Standardizes column types, naming, and sort order
- Computes rolling averages across last 3, 5, and 10 games
- Calculates cumulative season averages (no data leakage)
- Derives efficiency metrics:
  - **True Shooting %**
  - **Game Score** (Hollinger)
  - **Stocks** (STL + BLK)
  - **Assist-to-Turnover Ratio**

### Interactive Dashboard (Streamlit)
- Player selector and stat selector via sidebar
- Toggleable rolling average window (3 / 5 / 10 games)
- Per-game bar chart with rolling average trend line
- Season average reference line
- Metric cards showing season avg, last 3, and last 10 with deltas
- Last 10 games table

### Automation
- Shell script + cron job runs the full pipeline daily at 3am
- Keeps the dataset current as the season progresses
- Logs each run to `logs/pipeline.log`

---

## Project Structure

## Running the Project

**Pull fresh data:**
```bash
cd src
python pull_gamelogs_raw.py
```

**Process and engineer features:**
```bash
python process_gamelogs.py
```

**Launch the dashboard:**
```bash
python -m streamlit run dashboard.py
```

---

## Tools Used

- Python
- pandas
- nba_api
- Plotly
- Streamlit
- Git / GitHub
- cron (macOS automation)

---

## Next Steps

- Team-wide comparison view (all players side by side)
- Date range filtering