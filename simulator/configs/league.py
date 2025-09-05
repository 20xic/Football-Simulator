LEAGUE_NAME = "English Premier League"

TEAMS = [
    "Arsenal",
    "Aston Villa",
    "Bournemouth",
    "Brentford",
    "Brighton & Hove Albion",
    "Chelsea",
    "Crystal Palace",
    "Everton",
    "Fulham",
    "Leeds United",
    "Leicester City",
    "Liverpool",
    "Manchester City",
    "Manchester United",
    "Newcastle United",
    "Nottingham Forest",
    "Southampton",
    "Tottenham Hotspur",
    "West Ham United",
    "Wolverhampton Wanderers"
]

_player_data_cache = None

def get_player_data():
    global _player_data_cache
    if _player_data_cache is None:
        import pandas as pd
        _player_data_cache = pd.read_pickle("simulator/data/player_data")
    return _player_data_cache