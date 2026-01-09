#Pulls Hawks roster and game logs for the season

import os
from datetime import datetime

from config import TEAM_ID, TEAM_NAME, SEASON, RAW_DIR
from fetch.hawks_roster import fetch_hawks_roster
from fetch.player_gamelogs import fetch_roster_gamelogs

def main():
    os.makedirs(RAW_DIR, exist_ok=True)

    #pulls player
    roster_df = fetch_hawks_roster(TEAM_ID, SEASON)
    print(f"{TEAM_NAME} roster players: {len(roster_df)}")

    #gamelogs
    logs_df = fetch_roster_gamelogs(roster_df, SEASON)
    print(f"Total gamelogs pulled: {len(logs_df)}")

    #save
    out_path = os.path.join(RAW_DIR, f"hawks_gamelogs_raw_{SEASON}.csv")
    logs_df.to_csv(out_path, index=False)
    print(f"Saved raw game logs to: {out_path}")
    print(f"Run time: {datetime.now().isoformat(timespec='seconds')}")

if __name__ == "__main__":
    main()