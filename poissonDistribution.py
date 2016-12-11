import pandas as pd
season = '2016'
df = pd.read_csv('premier-league-' + season +'.csv')

pl_games = df[(df['league'] == 'Premier League')]
pl_games = pl_games.reset_index(drop=True)

home_json_data = {}
away_json_data = {}

# 1. read raw data from csv file, organize the data
for index, row in pl_games.iterrows():
    homeTeam = str(row['home'])
    awayTeam = str(row['away'])
    home_goals = int(row['home_goals'])
    away_goals = int(row['away_goals'])
    if homeTeam in home_json_data:
        home_json_data[homeTeam]['games_played'] += 1
        home_json_data[homeTeam]['goals_for'] += home_goals
        home_json_data[homeTeam]['goals_against'] += away_goals
    else:
        home_json_data[homeTeam] = {}
        home_json_data[homeTeam]['games_played'] = 1
        home_json_data[homeTeam]['goals_for'] = home_goals
        home_json_data[homeTeam]['goals_against'] = away_goals

    if awayTeam in away_json_data:
        away_json_data[awayTeam]['games_played'] += 1
        away_json_data[awayTeam]['goals_for'] += away_goals
        away_json_data[awayTeam]['goals_against'] += home_goals
    else:
        away_json_data[awayTeam] = {}
        away_json_data[awayTeam]['games_played'] = 1
        away_json_data[awayTeam]['goals_for'] = away_goals
        away_json_data[awayTeam]['goals_against'] = home_goals

home_total_game_count = 0
home_total_goals_for = 0
home_total_goals_against = 0
home_average_goals_for = 0
home_average_goals_against = 0

away_total_game_count = 0
away_total_goals_for = 0
away_total_goals_against = 0
away_average_goals_for = 0
away_average_goals_against = 0

# 2. get basic stats of home and away data
for team in home_json_data.keys():
    average_goals_for = float(home_json_data[team]['goals_for']) / float(home_json_data[team]['games_played'])
    average_goals_against = float(home_json_data[team]['goals_against']) / float(home_json_data[team]['games_played'])

    home_json_data[team]['average_goals_for'] = average_goals_for
    home_json_data[team]['average_goals_against'] = average_goals_against

    home_total_game_count += home_json_data[team]['games_played']
    home_total_goals_for += home_json_data[team]['goals_for']
    home_total_goals_against += home_json_data[team]['goals_against']
    home_average_goals_against += home_json_data[team]['average_goals_for']
    home_average_goals_for += home_json_data[team]['average_goals_against']

all_teams = list(home_json_data.keys())
home_team_counts = len(all_teams)
home_json_data['total'] = {'games_played': home_total_game_count,
                           'goals_for': home_total_goals_for,
                           'average_goals_for': home_average_goals_for,
                           'goals_against': home_average_goals_against,
                           'average_goals_against': home_average_goals_against}

home_json_data['average'] = {'games_played': home_total_game_count / home_team_counts,
                           'goals_for': home_total_goals_for / float(home_team_counts),
                           'average_goals_for': home_average_goals_for / float(home_team_counts),
                           'goals_against': home_average_goals_against / float(home_team_counts),
                           'average_goals_against': home_average_goals_against / float(home_team_counts)}


for team in away_json_data.keys():
    average_goals_for = float(away_json_data[team]['goals_for']) / float(away_json_data[team]['games_played'])
    average_goals_against = float(away_json_data[team]['goals_against']) / float(away_json_data[team]['games_played'])

    away_json_data[team]['average_goals_for'] = average_goals_for
    away_json_data[team]['average_goals_against'] = average_goals_against

    away_total_game_count += away_json_data[team]['games_played']
    away_total_goals_for += away_json_data[team]['goals_for']
    away_total_goals_against += away_json_data[team]['goals_against']
    away_average_goals_against += away_json_data[team]['average_goals_for']
    away_average_goals_for += away_json_data[team]['average_goals_against']

away_team_counts = len(all_teams)
away_json_data['total'] = {'games_played': away_total_game_count,
                           'goals_for': away_total_goals_for,
                           'average_goals_for': away_average_goals_for,
                           'goals_against': away_average_goals_against,
                           'average_goals_against': away_average_goals_against}

away_json_data['average'] = {'games_played': away_total_game_count / away_team_counts,
                           'goals_for': away_total_goals_for / float(away_team_counts),
                           'average_goals_for': away_average_goals_for / float(away_team_counts),
                           'goals_against': away_average_goals_against / float(away_team_counts),
                           'average_goals_against': away_average_goals_against / float(away_team_counts)}

home_df = pd.DataFrame(home_json_data).T
away_df = pd.DataFrame(away_json_data).T
# print home_df
# print away_df

# 3. calculate attack and defense strength

strength_json = {}
home_average_attacking_strength = 0.0
home_average_defensive_strength = 0.0
away_average_attacking_strength = 0.0
away_average_defensive_strength = 0.0

for team in all_teams:
    strength_json[team] = {}
    home_attacking_strength = home_json_data[team]['average_goals_for'] / home_json_data['average']['average_goals_for']
    home_defensive_strength = home_json_data[team]['average_goals_against'] / home_json_data['average']['average_goals_against']
    away_attacking_strength = away_json_data[team]['average_goals_for'] / away_json_data['average']['average_goals_for']
    away_defensive_strength = away_json_data[team]['average_goals_against'] / away_json_data['average']['average_goals_against']
    strength_json[team]['home_attacking_strength'] = home_attacking_strength
    strength_json[team]['home_defensive_strength'] = home_defensive_strength
    strength_json[team]['away_attacking_strength'] = away_attacking_strength
    strength_json[team]['away_defensive_strength'] = away_defensive_strength

    home_average_attacking_strength += home_attacking_strength
    home_average_defensive_strength += home_defensive_strength
    away_average_attacking_strength += away_attacking_strength
    away_average_defensive_strength += away_defensive_strength


home_average_attacking_strength /= float(len(all_teams))
home_average_defensive_strength /= float(len(all_teams))
away_average_attacking_strength /= float(len(all_teams))
away_average_defensive_strength /= float(len(all_teams))

strength_json['average'] = {'home_attacking_strength': home_attacking_strength,
                            'home_defensive_strength': home_defensive_strength,
                            'away_attacking_strength': away_average_attacking_strength,
                            'away_defensive_strength': away_average_defensive_strength}

strength_df = pd.DataFrame(strength_json).T
print strength_df

# 4. goal expectancy
# calculate how many goals we expect a team to score in a particular match - we call this the Goal Expectancy
# Home Team Goal Expectancy: home attacking strength x away defensive strength x average goals home
# Away Team Goal Expectancy: away attacking strength x home defensive strength x average goals away
def get_goal_expectancy(homeTeam, awayTeam):
    global home_json_data, away_json_data, strength_json
    home_team_goal_expectancy = strength_json[homeTeam]['home_attacking_strength'] \
                                * strength_json[awayTeam]['away_defensive_strength'] \
                                * home_json_data['average']['average_goals_for']

    away_team_goal_expectancy = strength_json[awayTeam]['away_attacking_strength'] \
                                * strength_json[homeTeam]['home_defensive_strength'] \
                                * away_json_data['average']['average_goals_for']

    return (home_team_goal_expectancy, away_team_goal_expectancy)

# print get_goal_expectancy('Arsenal', 'Chelsea')


# 5. calculate poisson distribution

from scipy.stats import poisson
# poisson.pmf(x, mu)
def get_poisson_distribution(homeTeam, awayTeam):
    goal_home_size = 11
    goal_away_size = 11
    # from 0-0 to 10-10
    poisson_distribution_json = {}
    for home_goal_count in range(goal_home_size):
        current_row = {}
        for away_goal_count in range(goal_away_size):
            home_expectancy, away_expectancy = get_goal_expectancy(awayTeam, homeTeam)
            home_poisson_value = poisson.pmf(home_goal_count, home_expectancy)
            away_poisson_value = poisson.pmf(away_goal_count, away_expectancy)
            current_row[away_goal_count] = home_poisson_value * away_poisson_value * 100

        poisson_distribution_json[home_goal_count] = current_row

    return poisson_distribution_json

poisson_json = get_poisson_distribution('Arsenal', 'Chelsea')
poisson_df = pd.DataFrame(poisson_json).T

# 6. get_winning_rate_from_poisson_distribution
def get_winning_rate_from_poisson_distribution(homeTeam, awayTeam):
    poisson_json = get_poisson_distribution(homeTeam, awayTeam)
    home_win_probability = 0.0
    draw_probability = 0.0
    away_win_probability = 0.0

    for home_goal_count in poisson_json.keys():
        current_row = poisson_json[home_goal_count]
        for away_goal_count in current_row.keys():
            if home_goal_count < away_goal_count:
                away_win_probability += current_row[away_goal_count]
            elif home_goal_count == away_goal_count:
                draw_probability += current_row[away_goal_count]
            else:
                home_win_probability += current_row[away_goal_count]


    return {'home_win': {'probability': '{0}%'.format(home_win_probability)},
            'draw': {'probability': '{0}%'.format(draw_probability)},
            'away_win': {'probability': '{0}%'.format(away_win_probability)}}


print get_winning_rate_from_poisson_distribution('Arsenal', 'Chelsea')