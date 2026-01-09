# Atlanta Hawks Player Performance Dashboard

This project is an analytics pipeline that focuses on tracking the Atlanta Hawks' player performance over the course of the 2025-2026 NBA season.
It was built to focus on data engineering, analysis, and reporting workflows to reflect how basketball operations teams monitor player performance over the course of a season.

The goal of the project is to create a front office-style reporting that highlights player trends, usage, and performance over time.

So far, this project uses official NBA stats (via 'nba_api') that:
- Pulls the Hawks roster for the current 2025-2026 season
- Collects up-to-date game logs for every rostered player
- Saves clean, raw datasets for analysis and reporting

## Current Progress
- Project structure and environment setup
- Working Hawks roster pull for the 2025-2026 season
- Up-to-date player game logs saved as a raw dataset

## Next Steps
- Clean and standardize raw game log data
- Create rolling performance metrics (short-term vs. season-long trends)
- Build processed datasets
- Visualize results using Tableau
- Set up regular updates so that the dataset grows as the season continues

## Tools Used
- Python
- pandas
- nba_api
- Git / GitHub
