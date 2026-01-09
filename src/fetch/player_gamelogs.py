#Pulls  season game logs for each player

import time
import pandas as pd
from nba_api.stats.endpoints import playergamelog

def fetch_player_gamelog(player_id: int, season: str) -> pd.DataFrame:
    """Fetch one player's season game log."""
    gl = playergamelog.PlayerGameLog(player_id = player_id, season = season)
    df = gl.get_data_frames()[0]
    df["PLAYER_ID"] = player_id
    return df

def fetch_roster_gamelogs(roster_df: pd.DataFrame, season: str, sleep_s: float = 0.7) -> pd.DataFrame:
    """Fetch season game logs for each player"""
    all_logs = []

    for pid in roster_df["PLAYER_ID"].tolist():
        try:
            df = fetch_player_gamelog(pid, season)
            all_logs.append(df)
        except Exception as e:
            print(f"Skipped PLAYER_ID={pid} due to error: {e}")
        time.sleep(sleep_s)

    return pd.concat(all_logs, ignore_index = True) if all_logs else pd.DataFrame()

