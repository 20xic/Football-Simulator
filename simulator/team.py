from simulator.player import Player
from simulator.manager import Manager
from simulator.data_provider import DataProvider

class Team:
    def __init__(self, team_name):
        self.name = team_name
        self.manager = Manager()
        self.players = {}
        self.squad = {}
        self.attack = 0
        self.midfield = 0
        self.defence = 0
        self.overall = 0
        
        # Используем DataProvider для получения данных
        self.data_provider = DataProvider()
        self.set_players()
        self.set_stats()
        self.set_squad()

    def set_players(self):
        df_team_players_data = self.data_provider.get_players_by_team(self.name)
        for index, df_player in df_team_players_data.iterrows():
            self.players[df_player["long_name"]] = Player(df_player)

    def set_stats(self):
        self.attackers = [
            player for player in self.players.values() if player.is_attacker()
        ]
        self.defenders = [
            player for player in self.players.values() if player.is_defender()
        ]
        self.midfielders = [
            player for player in self.players.values() if player.is_midfielder()
        ]
        self.goalkeepers = [
            player for player in self.players.values() if player.is_goalkeeper()
        ]
        
        # Более точный расчет рейтингов команды
        if self.attackers:
            self.attack = sum(player.overall for player in self.attackers) // len(self.attackers)
        else:
            self.attack = 50  # Значение по умолчанию
            
        if self.defenders and self.goalkeepers:
            defence_total = (sum(player.overall for player in self.defenders) + 
                           sum(player.overall for player in self.goalkeepers))
            self.defence = defence_total // (len(self.defenders) + len(self.goalkeepers))
        else:
            self.defence = 50  # Значение по умолчанию
            
        if self.midfielders:
            self.midfield = sum(player.overall for player in self.midfielders) // len(self.midfielders)
        else:
            self.midfield = 50  # Значение по умолчанию
            
        # Общий рейтинг команды
        self.overall = (self.attack + self.defence + self.midfield) // 3

    def set_squad(self):
        [num_attackers, num_midfielders, num_defenders] = self.manager.formation
        
        # Выбор стартового состава на основе рейтинга игроков
        self.attackers.sort(key=lambda x: x.overall, reverse=True)
        self.midfielders.sort(key=lambda x: x.overall, reverse=True)
        self.defenders.sort(key=lambda x: x.overall, reverse=True)
        self.goalkeepers.sort(key=lambda x: x.overall, reverse=True)
        
        squad_attackers = self.attackers[:num_attackers]
        squad_midfielders = self.midfielders[:num_midfielders]
        squad_defenders = self.defenders[:num_defenders]
        squad_gk = self.goalkeepers[:1]  # только один вратарь
        
        # Помечаем игроков как стартовых
        for player in squad_attackers + squad_midfielders + squad_defenders + squad_gk:
            player.set_as_starter()
            
        self.squad = {
            "attackers": squad_attackers,
            "midfielders": squad_midfielders,
            "defenders": squad_defenders,
            "goalkeeper": squad_gk,
        }