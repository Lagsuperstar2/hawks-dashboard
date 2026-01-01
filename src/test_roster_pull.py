# Tests updates

from config import TEAM_ID, SEASON, TEAM_NAME
from fetch.hawks_roster import fetch_hawks_roster

def main():
    # Fetch roster for the 2025-26 season
    roster_df = fetch_hawks_roster(TEAM_ID, SEASON)

    # Prints output
    print(f"{TEAM_NAME} roster rows: {len(roster_df)}")
    print(roster_df)

if __name__ == "__main__":
    main()