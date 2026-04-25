# central settings
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEAM_NAME = "Atlanta Hawks"
TEAM_ID = 1610612737
SEASON = "2025-26"
ROLLING_WINDOWS = [3, 5, 10]
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
LOG_DIR = os.path.join(BASE_DIR, "logs")