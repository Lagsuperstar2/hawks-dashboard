# Reads raw game logs, cleans and engineers features, saves to processed/

import os
from datetime import datetime

from config import SEASON, RAW_DIR, PROCESSED_DIR, ROLLING_WINDOWS
from transform.clean import clean_gamelogs
from transform.features import engineer_features

import pandas as pd


def main():
    raw_path = os.path.join(RAW_DIR, f"hawks_gamelogs_raw_{SEASON}.csv")

    if not os.path.exists(raw_path):
        raise FileNotFoundError(
            f"Raw game log not found at: {raw_path}\n"
            "Run pull_gamelogs_raw.py first."
        )

    df = pd.read_csv(raw_path)
    print(f"Loaded {len(df)} rows from {raw_path}")

    roster_path = os.path.join(RAW_DIR, f"hawks_roster_{SEASON}.csv")
    roster_df = pd.read_csv(roster_path)[["PLAYER_ID", "PLAYER"]]
    df = df.drop(columns=["Player_ID"])
    df = df.merge(roster_df, on="PLAYER_ID", how="left")

    df = clean_gamelogs(df)
    print(f"After cleaning: {len(df)} rows, {df['PLAYER_ID'].nunique()} players")

    df = engineer_features(df, ROLLING_WINDOWS)
    print(f"Features engineered. Total columns: {len(df.columns)}")

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    out_path = os.path.join(PROCESSED_DIR, f"hawks_gamelogs_processed_{SEASON}.csv")
    df.to_csv(out_path, index=False)
    print(f"Saved processed game logs to: {out_path}")
    print(f"Run time: {datetime.now().isoformat(timespec='seconds')}")


if __name__ == "__main__":
    main()