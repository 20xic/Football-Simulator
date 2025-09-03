from .league import League

welcome_message = """
Welcome to the League Simulator!
You can use this project to simulate Football Leagues across the world
Please enter the league you would like to simulate:
"""

leagues_message = """
1 - La Liga Santander
2 - Premier League
3 - Bundesliga
4 - Seria A
5 - Ligue 1
"""

def get_league_input():
    while True:
        try:
            num = int(input(leagues_message))
            if num in [1, 2, 3, 4, 5]:
                return num
            else:
                print('Please enter a number between 1-5!')
        except ValueError:
            print('Please enter a valid number!')


def run():
    print(welcome_message)
    league_no = get_league_input()
    league = League(league_no)
    league.simulate_league()
