import pandas as pd
from simulator.configs.league import get_player_data, TEAMS

class DataProvider:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._players_data = get_player_data()
        return cls._instance
    
    def get_players_by_team(self, team_name):
        """Получить всех игроков указанной команды"""
        return self._players_data[self._players_data["club"] == team_name]
    
    def get_all_teams(self):
        """Получить список всех команд лиги"""
        return TEAMS
    
    def get_league_name(self):
        """Получить название лиги"""
        from simulator.configs.league import LEAGUE_NAME
        return LEAGUE_NAME