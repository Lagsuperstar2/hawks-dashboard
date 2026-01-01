# Atlanta Hawks roster

import pandas as pd
from nba_api.stats.endpoints import commonteamroster

def fetch_hawks_roster(team_id: int, season: str) -> pd.DataFrame:
    roster = commonteamroster.CommonTeamRoster(team_id=team_id, season=season)
    df = roster.get_data_frames()[0]

    keep = ["PLAYER_ID", "PLAYER", "POSITION", "AGE", "EXP"]
    keep = [c for c in keep if c in df.columns]
    return df[keep].copy()