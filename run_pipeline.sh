#!/bin/bash

# Daily pipeline runner for Hawks dashboard
cd /Users/linds/Desktop/hawks-dashboard/src

source /Users/linds/Desktop/hawks-dashboard/.venv/bin/activate

echo "=== Starting Hawks pipeline: $(date) ==="

python pull_gamelogs_raw.py
python process_gamelogs.py

echo "=== Pipeline complete: $(date) ==="