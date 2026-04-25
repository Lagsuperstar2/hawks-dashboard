# Cleans and standardizes raw Hawks game log data
 
import pandas as pd
 
 
NUMERIC_COLS = [
    "MIN", "FGM", "FGA", "FG_PCT",
    "FG3M", "FG3A", "FG3_PCT",
    "FTM", "FTA", "FT_PCT",
    "OREB", "DREB", "REB",
    "AST", "STL", "BLK", "TOV",
    "PF", "PTS", "PLUS_MINUS"
]
 
 
def clean_gamelogs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize the raw game log DataFrame.
 
    Steps:
        - Parse GAME_DATE as datetime
        - Coerce numeric columns to float
        - Drop duplicate rows
        - Sort by player and game date (ascending)
        - Reset index
    """
    df = df.copy()
 
    # Parse date
    df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"], format="%b %d, %Y", errors="coerce")
 
    # Coerce numerics
    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
 
    # Drop full duplicates
    df = df.drop_duplicates()
 
    # Sort per player by game date ascending so rolling windows work correctly
    df = df.sort_values(["PLAYER_ID", "GAME_DATE"]).reset_index(drop=True)
 
    return df