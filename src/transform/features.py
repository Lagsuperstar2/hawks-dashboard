# Feature engineering for Hawks game log data
 
import pandas as pd
 
 
# Stats to compute rolling averages for
ROLLING_STAT_COLS = [
    "PTS", "REB", "AST", "STL", "BLK",
    "TOV", "MIN", "FG_PCT", "FG3_PCT", "FT_PCT",
    "PLUS_MINUS"
]
 
 
def add_rolling_averages(df: pd.DataFrame, windows: list[int]) -> pd.DataFrame:
    """
    Add rolling averages per player for each stat in ROLLING_STAT_COLS.
 
    Columns added follow the pattern: {STAT}_LAST{N} (e.g. PTS_LAST5)
    Rolling is computed within each player group, ordered by GAME_DATE ascending.
    min_periods=1 ensures values are not null at the start of a player's season.
    """
    df = df.copy()
 
    for stat in ROLLING_STAT_COLS:
        if stat not in df.columns:
            continue
        for window in windows:
            col_name = f"{stat}_LAST{window}"
            df[col_name] = (
                df.groupby("PLAYER_ID")[stat]
                .transform(lambda s: s.rolling(window, min_periods=1).mean())
                .round(3)
            )
 
    return df
 
 
def add_season_averages(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add cumulative season averages per player up to (but not including) each game.
 
    Uses expanding().mean() so each row reflects the average of all prior games.
    This avoids data leakage — the current game is not included in its own average.
    Columns added follow the pattern: {STAT}_SEASON_AVG (e.g. PTS_SEASON_AVG)
    """
    df = df.copy()
 
    for stat in ROLLING_STAT_COLS:
        if stat not in df.columns:
            continue
        col_name = f"{stat}_SEASON_AVG"
        df[col_name] = (
            df.groupby("PLAYER_ID")[stat]
            .transform(lambda s: s.expanding().mean().shift(1))
            .round(3)
        )
 
    return df
 
 
def add_efficiency_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add derived efficiency and contribution metrics.
 
    Metrics added:
        - STOCKS:       STL + BLK (defensive impact)
        - AST_TOV:      AST / TOV ratio (playmaking efficiency, capped at 99 to avoid inf)
        - TRUE_SHOOTING: TS% = PTS / (2 * (FGA + 0.44 * FTA))
        - GAME_SCORE:   Hollinger's Game Score approximation
    """
    df = df.copy()
 
    # Defensive stocks
    if "STL" in df.columns and "BLK" in df.columns:
        df["STOCKS"] = df["STL"] + df["BLK"]
 
    # Assist-to-turnover ratio
    if "AST" in df.columns and "TOV" in df.columns:
        df["AST_TOV"] = (df["AST"] / df["TOV"].replace(0, float("nan"))).round(2)
        df["AST_TOV"] = df["AST_TOV"].clip(upper=99)
 
    # True Shooting %
    if all(c in df.columns for c in ["PTS", "FGA", "FTA"]):
        ts_denom = 2 * (df["FGA"] + 0.44 * df["FTA"])
        df["TRUE_SHOOTING"] = (df["PTS"] / ts_denom.replace(0, float("nan"))).round(3)
 
    # Hollinger Game Score
    if all(c in df.columns for c in ["PTS", "FGM", "FGA", "FTM", "FTA",
                                      "OREB", "DREB", "STL", "AST", "BLK",
                                      "PF", "TOV"]):
        df["GAME_SCORE"] = (
            df["PTS"]
            + 0.4 * df["FGM"]
            - 0.7 * df["FGA"]
            - 0.4 * (df["FTA"] - df["FTM"])
            + 0.7 * df["OREB"]
            + 0.3 * df["DREB"]
            + df["STL"]
            + 0.7 * df["AST"]
            + 0.7 * df["BLK"]
            - 0.4 * df["PF"]
            - df["TOV"]
        ).round(2)
 
    return df
 
 
def engineer_features(df: pd.DataFrame, windows: list[int]) -> pd.DataFrame:
    """
    Master feature engineering function. Applies all transformations in order.
    """
    df = add_rolling_averages(df, windows)
    df = add_season_averages(df)
    df = add_efficiency_metrics(df)
    return df