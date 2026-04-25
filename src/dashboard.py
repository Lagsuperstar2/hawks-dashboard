# Atlanta Hawks Player Performance Dashboard — Polished UI

import os
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ── Config ─────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed", "hawks_gamelogs_processed_2025-26.csv")

STATS = {
    "Points": "PTS",
    "Rebounds": "REB",
    "Assists": "AST",
    "Steals": "STL",
    "Blocks": "BLK",
    "Turnovers": "TOV",
    "Minutes": "MIN",
    "Plus / Minus": "PLUS_MINUS",
    "True Shooting %": "TRUE_SHOOTING",
    "Game Score": "GAME_SCORE",
}

HAWKS_RED    = "#C8102E"
HAWKS_GOLD   = "#C4A951"
BG_DARK      = "#0D0D0D"
BG_CARD      = "#161616"
TEXT_PRIMARY = "#F0F0F0"
TEXT_DIM     = "#888888"

# ── Page setup ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Hawks Dashboard",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow+Condensed:wght@300;400;500;600;700&family=Barlow:wght@300;400;500&display=swap');

html, body, [class*="css"] {{
    background-color: {BG_DARK};
    color: {TEXT_PRIMARY};
    font-family: 'Barlow', sans-serif;
}}

.stApp {{ background-color: {BG_DARK}; }}

/* ── Header bar ── */
header[data-testid="stHeader"] {{
    background-color: {BG_DARK} !important;
    border-bottom: 1px solid #2A2A2A !important;
}}

/* ── Hide keyboard_double tooltip text ── */
[data-testid="stSidebarCollapsedControl"] span,
[data-testid="collapsedControl"] span,
button[kind="headerNoBorderless"] span {{
    display: none !important;
    visibility: hidden !important;
}}

/* ── Sidebar toggle arrow ── */
[data-testid="stSidebarCollapsedControl"] {{
    color: {TEXT_DIM} !important;
    opacity: 1 !important;
}}

[data-testid="stSidebarCollapsedControl"]:hover {{
    color: {TEXT_PRIMARY} !important;
}}

[data-testid="stSidebarCollapsedControl"] svg {{
    fill: {TEXT_DIM} !important;
}}

[data-testid="stSidebarCollapsedControl"]:hover svg {{
    fill: {TEXT_PRIMARY} !important;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background-color: {BG_CARD};
    border-right: 1px solid #2A2A2A;
}}

[data-testid="stSidebarHeader"] {{
    background-color: {BG_CARD} !important;
    border-bottom: 1px solid #2A2A2A !important;
}}

[data-testid="stSidebar"] * {{
    color: {TEXT_PRIMARY} !important;
    font-family: 'Barlow Condensed', sans-serif !important;
}}

[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio label {{
    font-size: 11px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: {TEXT_DIM} !important;
    font-weight: 600 !important;
}}

[data-testid="stSidebar"] .stSelectbox > div > div {{
    background-color: #222 !important;
    border: 1px solid #333 !important;
    border-radius: 2px !important;
}}

/* ── Main content ── */
.block-container {{
    padding-top: 60px !important;
    max-width: 1200px;
}}

/* ── Dashboard header ── */
.dash-header {{
    display: flex;
    align-items: flex-end;
    gap: 16px;
    padding: 32px 0 12px 0;
    border-bottom: 3px solid {HAWKS_RED};
    margin-bottom: 8px;
}}

.dash-title {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 54px;
    letter-spacing: 3px;
    color: {TEXT_PRIMARY};
    line-height: 1;
    margin: 0;
}}

.dash-subtitle {{
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 13px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: {HAWKS_GOLD};
    margin-bottom: 6px;
}}

/* ── Player header ── */
.player-header {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 40px;
    letter-spacing: 2px;
    color: {TEXT_PRIMARY};
    margin: 28px 0 0 0;
    line-height: 1;
}}

.player-stat-label {{
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 13px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: {HAWKS_RED};
    margin-bottom: 20px;
    margin-top: 4px;
}}

/* ── Metric cards ── */
.metric-row {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin: 4px 0 28px 0;
}}

.metric-card {{
    background: {BG_CARD};
    border: 1px solid #2A2A2A;
    border-top: 3px solid {HAWKS_RED};
    padding: 20px 24px 18px 24px;
}}

.metric-card.gold {{ border-top-color: {HAWKS_GOLD}; }}

.metric-label {{
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 11px;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: {TEXT_DIM};
    margin-bottom: 8px;
}}

.metric-value {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 46px;
    color: {TEXT_PRIMARY};
    line-height: 1;
    letter-spacing: 1px;
}}

.metric-delta {{
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 13px;
    font-weight: 600;
    margin-top: 6px;
}}

.delta-up     {{ color: #4CAF50; }}
.delta-down   {{ color: {HAWKS_RED}; }}
.delta-neutral {{ color: {TEXT_DIM}; }}

/* ── Section labels ── */
.section-label {{
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: {TEXT_DIM};
    border-bottom: 1px solid #2A2A2A;
    padding-bottom: 8px;
    margin: 4px 0 16px 0;
}}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)


# ── Load data ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv(PROCESSED_PATH, parse_dates=["GAME_DATE"])
    return df

df = load_data()

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style='font-family:Bebas Neue,sans-serif;font-size:24px;letter-spacing:3px;
        color:{TEXT_PRIMARY};border-bottom:2px solid {HAWKS_RED};
        padding-bottom:12px;margin-bottom:24px;'>
        🦅 HAWKS DASHBOARD
        </div>
    """, unsafe_allow_html=True)

    players = sorted(df["PLAYER"].unique().tolist())
    selected_player = st.selectbox("Select Player", players)

    stat_label = st.selectbox("Select Stat", list(STATS.keys()))
    stat_col = STATS[stat_label]

    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)
    rolling_window = st.radio("Rolling Average", [3, 5, 10], index=1, horizontal=True)
    rolling_col = f"{stat_col}_LAST{rolling_window}"

# ── Main header ────────────────────────────────────────────────────────────────
st.markdown(f"""
    <div class='dash-header'>
        <div>
            <div class='dash-title'>ATLANTA HAWKS</div>
            <div class='dash-subtitle'>Player Performance Dashboard &nbsp;·&nbsp; 2025–26 Season</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ── Filter to player ───────────────────────────────────────────────────────────
player_df = df[df["PLAYER"] == selected_player].sort_values("GAME_DATE").reset_index(drop=True)

# ── Player subheader ───────────────────────────────────────────────────────────
st.markdown(f"""
    <div class='player-header'>{selected_player}</div>
    <div class='player-stat-label'>{stat_label} &nbsp;/&nbsp; 2025–26 Regular Season</div>
""", unsafe_allow_html=True)

# ── Metric cards ───────────────────────────────────────────────────────────────
season_avg   = player_df[stat_col].mean()
last3_avg    = player_df[stat_col].tail(3).mean()
last10_avg   = player_df[stat_col].tail(10).mean()
games_played = len(player_df)

def delta_html(val, ref):
    diff = val - ref
    if diff > 0.05:
        return f"<div class='metric-delta delta-up'>▲ {diff:+.1f} vs season</div>"
    elif diff < -0.05:
        return f"<div class='metric-delta delta-down'>▼ {diff:.1f} vs season</div>"
    else:
        return f"<div class='metric-delta delta-neutral'>— vs season</div>"

st.markdown(f"""
<div class='metric-row'>
    <div class='metric-card'>
        <div class='metric-label'>Games Played</div>
        <div class='metric-value'>{games_played}</div>
    </div>
    <div class='metric-card'>
        <div class='metric-label'>Season Avg</div>
        <div class='metric-value'>{season_avg:.1f}</div>
    </div>
    <div class='metric-card gold'>
        <div class='metric-label'>Last 3 Avg</div>
        <div class='metric-value'>{last3_avg:.1f}</div>
        {delta_html(last3_avg, season_avg)}
    </div>
    <div class='metric-card gold'>
        <div class='metric-label'>Last 10 Avg</div>
        <div class='metric-value'>{last10_avg:.1f}</div>
        {delta_html(last10_avg, season_avg)}
    </div>
</div>
""", unsafe_allow_html=True)

# ── Trend chart ────────────────────────────────────────────────────────────────
st.markdown("<div class='section-label'>Performance Trend</div>", unsafe_allow_html=True)

fig = go.Figure()

fig.add_trace(go.Bar(
    x=player_df["GAME_DATE"],
    y=player_df[stat_col],
    name=f"{stat_label} per game",
    marker_color="rgba(200, 16, 46, 0.22)",
    marker_line_color="rgba(200, 16, 46, 0.55)",
    marker_line_width=1,
    hovertemplate="<b>%{x|%b %d, %Y}</b><br>" + stat_label + ": <b>%{y}</b><extra></extra>"
))

if rolling_col in player_df.columns:
    fig.add_trace(go.Scatter(
        x=player_df["GAME_DATE"],
        y=player_df[rolling_col],
        name=f"Last {rolling_window} avg",
        mode="lines",
        line=dict(color=HAWKS_RED, width=3),
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>Last " + str(rolling_window) + " avg: <b>%{y:.1f}</b><extra></extra>"
    ))

fig.add_hline(
    y=season_avg,
    line_dash="dot",
    line_color=HAWKS_GOLD,
    line_width=1.5,
    annotation_text=f"Season avg  {season_avg:.1f}",
    annotation_font_color=HAWKS_GOLD,
    annotation_font_size=12,
    annotation_position="top left"
)

fig.update_layout(
    plot_bgcolor="#111111",
    paper_bgcolor="#111111",
    font=dict(family="Barlow Condensed", color=TEXT_PRIMARY),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12, color=TEXT_DIM),
        tickformat="%b %d",
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="#2A2A2A",
        zeroline=False,
        tickfont=dict(size=12, color=TEXT_DIM),
        title=dict(text=stat_label, font=dict(size=12, color=TEXT_DIM)),
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(size=13),
        bgcolor="rgba(0,0,0,0)"
    ),
    hovermode="x unified",
    hoverlabel=dict(
        bgcolor="#1C1C1C",
        bordercolor="#333",
        font=dict(family="Barlow Condensed", size=14, color=TEXT_PRIMARY)
    ),
    height=430,
    margin=dict(t=32, b=16, l=8, r=8),
)

st.plotly_chart(fig, use_container_width=True)

# ── Recent games table ─────────────────────────────────────────────────────────
st.markdown("<div class='section-label'>Last 10 Games</div>", unsafe_allow_html=True)

display_cols = ["GAME_DATE", "MATCHUP", "WL", stat_col, rolling_col, f"{stat_col}_SEASON_AVG"]
display_cols = [c for c in display_cols if c in player_df.columns]

recent = (
    player_df[display_cols]
    .tail(10)
    .sort_values("GAME_DATE", ascending=False)
    .copy()
)
recent["GAME_DATE"] = recent["GAME_DATE"].dt.strftime("%b %d, %Y")

rename_map = {
    stat_col: stat_label,
    rolling_col: f"Last {rolling_window}",
    f"{stat_col}_SEASON_AVG": "Season Avg",
    "GAME_DATE": "Date",
    "MATCHUP": "Matchup",
    "WL": "W/L",
}
recent = recent.rename(columns=rename_map)

st.dataframe(recent, use_container_width=True, hide_index=True)