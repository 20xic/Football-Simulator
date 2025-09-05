import copy
import random

from simulator.configs.odds import odds
from simulator.event import Event

class Match:
    reverse = {"Home": "Away", "Away": "Home"}
    eventkeys = list(odds[0]["Home"]["Events"].keys())
    foulkeys = ["Free kick won", "Yellow card", "Second yellow card", "Red card"]

    def __init__(self, home_side, away_side):
        self.odds = copy.deepcopy(odds)
        tlist = copy.deepcopy(Match.eventkeys)
        tlist.extend(
            ["On target", "Saved", "Off target", "Blocked", "Hit the bar", "Goal"]
        )
        self.home_stats = dict(zip(tlist, [0] * len(tlist)))
        self.away_stats = dict(zip(tlist, [0] * len(tlist)))
        self.home_side = home_side
        self.away_side = away_side
        self.sides = {home_side: "Home", away_side: "Away"}
        self.reverse = {home_side: away_side, away_side: home_side}
        self.matchevents = []
        self.stats = dict(
            zip(
                [self.home_side, self.away_side],
                [copy.copy(self.home_stats), copy.copy(self.away_stats)],
            )
        )
        self.home_players = home_side.players
        self.home_squad = home_side.squad
        self.away_players = away_side.players
        self.away_squad = away_side.squad
        self.home_goals = 0
        self.away_goals = 0
        self.set_odds()

    def set_odds(self):

        home_advantage = 1.1 
        
        home_attack = self.home_side.attack * home_advantage
        away_defense = self.away_side.defence
        
        away_attack = self.away_side.attack
        home_defense = self.home_side.defence * home_advantage
        
        hdf = (home_attack ** 2 * self.home_side.midfield) / (
            away_defense ** 2 * self.away_side.midfield
        )
        
        adf = (away_attack ** 2 * self.away_side.midfield) / (
            home_defense ** 2 * self.home_side.midfield
        )
        
        for minute in range(100):
            self.odds[minute]["Home"]["Events"]["Attempt"] = self.odds[minute]["Home"][
                "Events"
            ]["Attempt"] * min(2.0, max(0.5, hdf))
            
            self.odds[minute]["Away"]["Events"]["Attempt"] = self.odds[minute]["Away"][
                "Events"
            ]["Attempt"] * min(2.0, max(0.5, adf))

    def add_event(self, event):
        for e in event.evaluate_event():
            if e.event == "Substitution":
                if self.stats[e.side][e.event] < 3:
                    self.track_event(e)
            else:
                self.track_event(e)
            e.show_event()
            self.matchevents.append(e)

    def set_events(self):
        for minute in range(100):
            for _ in range(135):
                if random.uniform(0, 1) < self.odds[minute]["Event"]:
                    plist = []
                    plist.append(self.odds[minute]["Home"]["Probability"])
                    plist.append(self.odds[minute]["Away"]["Probability"])
                    side = random.choices([self.home_side, self.away_side], plist, k=1)[0]
                    event = random.choices(
                        Match.eventkeys,
                        list(self.odds[minute][self.sides[side]]["Events"].values()),
                        k=1
                    )[0]
                    if event not in Match.foulkeys:
                        e = Event(event, side, minute)
                        e.set_home_and_away_sides(self.home_side, self.away_side)
                        self.add_event(e)

    def track_event(self, event):
        if event.side == self.home_side:
            self.home_stats[event.event] = self.home_stats[event.event] + 1
            if event.event == "Goal":
                self.home_goals += 1
        else:
            self.away_stats[event.event] = self.away_stats[event.event] + 1
            if event.event == "Goal":
                self.away_goals += 1
                
        self.stats = dict(
            zip(
                [self.home_side, self.away_side],
                [copy.copy(self.home_stats), copy.copy(self.away_stats)],
            )
        )

    def evaluate_match_result(self):
        hg = self.stats[self.home_side]["Goal"]
        ag = self.stats[self.away_side]["Goal"]
        if hg == ag:
            return ("Draw", self.home_side, self.away_side)
        elif hg > ag:
            return ("Win", self.home_side, self.away_side)
        else:
            return ("Win", self.away_side, self.home_side)

    def show_match_result(self):
        if self.home_goals > self.away_goals:
            print(f"  {self.home_side.name} {self.home_goals}-{self.away_goals} {self.away_side.name}")
        elif self.away_goals > self.home_goals:
            print(f"  {self.home_side.name} {self.home_goals}-{self.away_goals} {self.away_side.name}")
        else:
            print(f"  {self.home_side.name} {self.home_goals}-{self.away_goals} {self.away_side.name}")

    def simulate(self):
        self.set_events()
        self.show_match_result()