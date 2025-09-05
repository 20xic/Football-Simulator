import pandas as pd
from tabulate import tabulate

from simulator.match import Match
from simulator.team import Team
from simulator.data_provider import DataProvider

class League:
    LEAGUE_TABLE_ATTRIBUTES = [
        "Club",
        "Matches Played",
        "Wins",
        "Draws",
        "Losses",
        "Points",
        "GF",
        "GA",
        "GD",
    ]

    def __init__(self):
        self.week = 0
        self.data_provider = DataProvider()
        self.name = self.data_provider.get_league_name()
        self.players = {}
        self.teams = {}
        self.team_names = self.data_provider.get_all_teams()
        self.set_teams()
        self.set_players()
        self.schedule = self.create_balanced_round_robin(self.team_names)
        self.standings = self.init_league_table()

    def set_teams(self):
        for name in self.team_names:
            team = Team(name)
            self.teams[name] = team

    def set_players(self):
        for team in self.teams.values():
            self.players.update(team.players)

    def create_balanced_round_robin(self, teams):
        """Create a schedule for the teams in the list and return it"""
        schedule = []
        if len(teams) % 2 == 1:
            teams = teams + [None]

        team_count = len(teams)
        mid = team_count // 2

        for _ in range(team_count - 1):
            first_half = teams[:mid]
            second_half = teams[mid:]
            second_half.reverse()

            round_schedule = [(t1, t2) for t1, t2 in zip(first_half, second_half)]
            round_schedule += [(t2, t1) for t1, t2 in zip(second_half, first_half)]

            schedule.append(round_schedule)

            teams.insert(1, teams.pop())

        return schedule

    def init_league_table(self):
        table = pd.DataFrame(columns=League.LEAGUE_TABLE_ATTRIBUTES)
        for team in self.team_names:
            row = pd.DataFrame(
                [[team, 0, 0, 0, 0, 0, 0, 0, 0]],
                columns=League.LEAGUE_TABLE_ATTRIBUTES,
            )
            table = pd.concat([table, row])
        table = table.reset_index(drop=True)
        table.index = table.index + 1
        return table

    def show_league_table(self):
        print(f"\n{self.name} - Current Standings:")
        print(tabulate(self.standings, headers=self.standings.columns, tablefmt="github"))

    def update_league_table(self, match):
        (result, winner, loser) = match.evaluate_match_result()
        table = self.standings
        num_winner_goals = match.stats[winner]["Goal"]
        num_loser_goals = match.stats[loser]["Goal"]
        goal_difference = num_winner_goals - num_loser_goals
        
        if result == "Draw":
            for team in [winner, loser]:
                table.loc[(table["Club"] == team.name)] += [
                    "",
                    1,
                    0,
                    1,
                    0,
                    1,
                    num_winner_goals,
                    num_loser_goals,
                    0,
                ]
        else:
            table.loc[(table["Club"] == winner.name)] += [
                "",
                1,
                1,
                0,
                0,
                3,
                num_winner_goals,
                num_loser_goals,
                goal_difference,
            ]
            table.loc[(table["Club"] == loser.name)] += [
                "",
                1,
                0,
                0,
                1,
                0,
                num_loser_goals,
                num_winner_goals,
                -goal_difference,
            ]
        
        table.sort_values(by=["Points", "GD", "GF"], 
                         inplace=True, 
                         ascending=[False, False, False])
        table.reset_index(drop=True, inplace=True)

    def simulate_match(self, home_team_name, away_team_name):
        home_team = self.teams[home_team_name]
        away_team = self.teams[away_team_name]
        match = Match(home_team, away_team)
        match.simulate()
        self.update_league_table(match)

    def simulate_week(self):
        print(f"\nSimulating Week {self.week + 1}:")
        for home_team, away_team in self.schedule[self.week]:
            if home_team and away_team:  # Пропускаем None (если есть)
                print(f"  {home_team} vs {away_team}")
                self.simulate_match(home_team, away_team)
        self.week += 1

    def simulate_league(self):
        print(f"Starting {self.name} simulation with {len(self.team_names)} teams...")
        while self.week < len(self.schedule):
            self.simulate_week()
            self.show_league_table()
        
        print(f"\n{self.name} simulation completed!")