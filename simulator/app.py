from simulator.league import League

welcome_message = """
Welcome to the English Premier League Simulator!
You can simulate the complete season of the English Premier League.
"""

def run():
    print(welcome_message)
    league = League()
    league.simulate_league()