import pandas as pd
import datetime as time

season = ['1011', '1112', '1213', '1314', '1415', '1516']
dataframe = pd.DataFrame()
list_ = []
for s in season:
    df = pd.read_csv('epl' + s + '.csv')
    col = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'Referee', 'HST', 'AST', 'HC', 'AC', 'HR', 'AR']
    df_temp = df[col]
    df_temp = df_temp
    list_.append(df_temp)
    ofile = open('pl' + s + '.csv', 'w')
    df_temp.to_csv(ofile, index=True)
    ofile.close()
dataframe = pd.concat(list_)
ofile = open('plmatchdata.csv', 'w')
dataframe.to_csv(ofile, index=False)
ofile.close()


#method to get last x matches
def get_lastmatches_data(dataframe, date1, team, x=6):
    prev_matches = dataframe[(dataframe['HomeTeam'] == team) | (dataframe['AwayTeam'] == team)]
    prev_matches = prev_matches.reset_index(drop=True)
    # print prev_matches
    i = 0
    # get the last x games
    index1 = 0
    for index, row in prev_matches.iterrows():
        date = str(row['Date'])
        if time.datetime.strptime(date, "%d/%m/%y") \
                < time.datetime.strptime(date1, "%d/%m/%y"):
            continue
        else:
            index1 = index
            break
    df_temp = prev_matches.iloc[index1 - 6:index1]
    #print(df_temp)
    return df_temp

#method to get last x matches
def get_lastmatchesH2H_data(dataframe, date1, hometeam, awayteam, x=6):
   prev_matches = dataframe[(dataframe['HomeTeam'] == hometeam) & (dataframe['AwayTeam'] == awayteam) \
      | (dataframe['AwayTeam'] == hometeam) & (dataframe['HomeTeam'] == awayteam)]
   prev_matches = prev_matches.reset_index(drop=True)
   # print prev_matches
   i = 0
   # get the last x games
   index1 = prev_matches.shape[0]
   for index, row in prev_matches.iterrows():
       date = str(row['Date'])
       if time.datetime.strptime(date, "%d/%m/%y") \
               < time.datetime.strptime(date1, "%d/%m/%y"):
           continue
       else:
           index1 = index
           break
   # print index1
   if index1 - 6 >= 0:
       df_temp = prev_matches.iloc[index1 - 6:index1]
   else:
       df_temp = prev_matches.iloc[0:prev_matches.shape[0]]
   return df_temp


# helper functions
def get_number_of_losses(matches, date, team, x=6):
    last_matches_df = get_lastmatches_data(matches, date, team, x)
    count = 0
    for _, row in last_matches_df.iterrows():
        # if team is home team
        if row['HomeTeam'] == team:
            if row['FTR'] == 'A':
                count += 1
        else:
            # team is away team
            if row['FTR'] == 'H':
                count += 1
    return count


def get_number_of_draws(matches, date, team, x=6):
    last_matches_df = get_lastmatches_data(matches, date, team, x)
    count = 0
    for _, row in last_matches_df.iterrows():
        if row['FTR'] == 'D':
            count += 1
    return count


def get_number_of_wins(matches, date, team, x=6):
    last_matches_df = get_lastmatches_data(matches, date, team, x)
    count = 0
    for _, row in last_matches_df.iterrows():
        # if team is home team
        if row['HomeTeam'] == team:
            if row['FTR'] == 'H':
                count += 1
        else:
            # team is away team
            if row['FTR'] == 'A':
                count += 1
    return count


def get_number_of_h2h_losses(matches, date, home_team, away_team, target_team, x=6):
    last_matches_df = get_lastmatchesH2H_data(matches, date, home_team, away_team, x)
    count = 0
    for _, row in last_matches_df.iterrows():
        # if team is home team
        if row['HomeTeam'] == target_team:
            if row['FTR'] == 'A':
                count += 1
        else:
            # team is away team
            if row['FTR'] == 'H':
                count += 1
    return count


def get_number_of_h2h_draws(matches, date, home_team, away_team, target_team=None, x=6):
    last_matches_df = get_lastmatchesH2H_data(matches, date, home_team, away_team, x)
    count = 0
    for _, row in last_matches_df.iterrows():
        if row['FTR'] == 'D':
            count += 1
    return count


def get_number_of_h2h_wins(matches, date, home_team, away_team, target_team, x=6):
    last_matches_df = get_lastmatchesH2H_data(matches, date, home_team, away_team, x)
    count = 0
    for _, row in last_matches_df.iterrows():
        # if team is home team
        if row['HomeTeam'] == target_team:
            if row['FTR'] == 'H':
                count += 1
        else:
            # team is away team
            if row['FTR'] == 'A':
                count += 1
    return count


def get_number_of_goals_scored(matches, date, team, x=6):
    last_matches_df = get_lastmatches_data(matches, date, team, x)
    count = 0
    for _, row in last_matches_df.iterrows():
        # if team is home team
        if row['HomeTeam'] == team:
            count += row['FTHG']
        else:
            # team is away team
            count += row['FTAG']
    return count


def get_number_of_goals_conceded(matches, date, team, x=6):
    last_matches_df = get_lastmatches_data(matches, date, team, x)
    count = 0
    for _, row in last_matches_df.iterrows():
        # if team is home team
        if row['HomeTeam'] == team:
            count += row['FTAG']
        else:
            # team is away team
            count += row['FTHG']
    return count


def get_number_of_shots_on_target(matches, date, team, x=6):
    last_matches_df = get_lastmatches_data(matches, date, team, x)
    count = 0
    for _, row in last_matches_df.iterrows():
        # if team is home team
        if row['HomeTeam'] == team:
            count += row['HST']
        else:
            # team is away team
            count += row['AST']
    return count


def get_number_of_corners(matches, date, team, x=6):
    last_matches_df = get_lastmatches_data(matches, date, team, x)
    count = 0
    for _, row in last_matches_df.iterrows():
        # if team is home team
        if row['HomeTeam'] == team:
            count += row['HC']
        else:
            # team is away team
            count += row['AC']
    return count


def get_number_of_red_cards(matches, date, team, x=6):
    last_matches_df = get_lastmatches_data(matches, date, team, x)
    count = 0
    for _, row in last_matches_df.iterrows():
        # if team is home team
        if row['HomeTeam'] == team:
            count += row['HR']
        else:
            # team is away team
            count += row['AR']
    return count


def get_number_of_h2h_home_goals_scored(matches, date, home_team, away_team, target_team, x=6):
    last_matches_df = get_lastmatchesH2H_data(matches, date, home_team, away_team, x)
    count = 0
    # print last_matches_df
    for _, row in last_matches_df.iterrows():
        # if team is home team
        if row['HomeTeam'] == target_team:
            count += row['FTHG']
    return count


def get_number_of_h2h_home_goals_conceded(matches, date, home_team, away_team, target_team, x=6):
    last_matches_df = get_lastmatchesH2H_data(matches, date, home_team, away_team, x)
    count = 0
    for _, row in last_matches_df.iterrows():
        # if team is home team
        if row['HomeTeam'] == target_team:
            count += row['FTAG']
    return count


def get_number_of_h2h_away_goals_scored(matches, date, home_team, away_team, target_team, x=6):
    last_matches_df = get_lastmatchesH2H_data(matches, date, home_team, away_team, x)
    count = 0
    for _, row in last_matches_df.iterrows():
        # if team is away team
        if row['AwayTeam'] == target_team:
            count += row['FTAG']
    return count


def get_number_of_h2h_away_goals_conceded(matches, date, home_team, away_team, target_team, x=6):
    last_matches_df = get_lastmatchesH2H_data(matches, date, home_team, away_team, x)
    count = 0
    for _, row in last_matches_df.iterrows():
        # if team is away team
        if row['AwayTeam'] == target_team:
            count += row['FTHG']
    return count


def get_number_of_h2h_home_shot_on_target(matches, date, home_team, away_team, target_team, x=6):
    last_matches_df = get_lastmatchesH2H_data(matches, date, home_team, away_team, x)
    count = 0
    for _, row in last_matches_df.iterrows():
        # if team is home team
        if row['HomeTeam'] == target_team:
            count += row['HST']
    return count


def get_number_of_h2h_away_shot_on_target(matches, date, home_team, away_team, target_team, x=6):
    last_matches_df = get_lastmatchesH2H_data(matches, date, home_team, away_team, x)
    count = 0
    for _, row in last_matches_df.iterrows():
        # if team is away team
        if row['AwayTeam'] == target_team:
            count += row['AST']
    return count


def get_number_of_h2h_home_corners(matches, date, home_team, away_team, target_team, x=6):
    last_matches_df = get_lastmatchesH2H_data(matches, date, home_team, away_team, x)
    count = 0
    for _, row in last_matches_df.iterrows():
        # if team is home team
        if row['HomeTeam'] == target_team:
            count += row['HC']
    return count


def get_number_of_h2h_away_corners(matches, date, home_team, away_team, target_team, x=6):
    last_matches_df = get_lastmatchesH2H_data(matches, date, home_team, away_team, x)
    count = 0
    for _, row in last_matches_df.iterrows():
        # if team is away team
        if row['AwayTeam'] == target_team:
            count += row['AC']
    return count


def get_number_of_h2h_home_red_cards(matches, date, home_team, away_team, target_team, x=6):
    last_matches_df = get_lastmatchesH2H_data(matches, date, home_team, away_team, x)
    count = 0
    for _, row in last_matches_df.iterrows():
        # if team is home team
        if row['HomeTeam'] == target_team:
            count += row['HR']
    return count


def get_number_of_h2h_away_red_cards(matches, date, home_team, away_team, target_team, x=6):
    last_matches_df = get_lastmatchesH2H_data(matches, date, home_team, away_team, x)
    count = 0
    for _, row in last_matches_df.iterrows():
        # if team is away team
        if row['AwayTeam'] == target_team:
            count += row['AR']
    return count

# print(get_lastmatches_data(dataframe, 'Arsenal', '24/04/16'))
# print(get_lastmatchesH2H_data(dataframe, 'Arsenal', 'Liverpool', '24/04/16'))

# print get_number_of_losses(dataframe, '24/04/16', 'Arsenal')
# print get_number_of_draws(dataframe, '24/04/16', 'Arsenal')
# print get_number_of_wins(dataframe, '24/04/16', 'Arsenal')
#
# print get_number_of_h2h_losses(dataframe, '24/04/16', 'Arsenal', 'Liverpool', 'Arsenal')
# print get_number_of_h2h_draws(dataframe, '24/04/16', 'Arsenal', 'Liverpool', 'Arsenal')
# print get_number_of_h2h_wins(dataframe, '24/04/16', 'Arsenal', 'Liverpool', 'Arsenal')
#
# print get_number_of_goals_scored(dataframe, '24/04/16', 'Arsenal')
# print get_number_of_goals_conceded(dataframe, '24/04/16', 'Arsenal')
#
# print get_number_of_shots_on_target(dataframe, '24/04/16', 'Arsenal')
# print get_number_of_corners(dataframe, '24/04/16', 'Arsenal')
# print get_number_of_red_cards(dataframe, '24/04/16', 'Arsenal')

# print get_number_of_h2h_home_goals_scored(dataframe, '24/04/16', 'Arsenal', 'Liverpool', 'Arsenal')
# print get_number_of_h2h_home_goals_conceded(dataframe, '24/04/16', 'Arsenal', 'Liverpool', 'Arsenal')
#
# print get_number_of_h2h_away_goals_scored(dataframe, '24/04/16', 'Arsenal', 'Liverpool', 'Arsenal')
# print get_number_of_h2h_away_goals_conceded(dataframe, '24/04/16', 'Arsenal', 'Liverpool', 'Arsenal')
# print get_number_of_h2h_home_shot_on_target(dataframe, '24/04/16', 'Arsenal', 'Liverpool', 'Arsenal')
# print get_number_of_h2h_away_shot_on_target(dataframe, '24/04/16', 'Arsenal', 'Liverpool', 'Arsenal')
# print get_number_of_h2h_home_corners(dataframe, '24/04/16', 'Arsenal', 'Liverpool', 'Arsenal')
# print get_number_of_h2h_away_corners(dataframe, '24/04/16', 'Arsenal', 'Liverpool', 'Arsenal')
#
# print get_number_of_h2h_home_red_cards(dataframe, '24/04/16', 'Arsenal', 'Liverpool', 'Arsenal')
# print get_number_of_h2h_away_red_cards(dataframe, '24/04/16', 'Arsenal', 'Liverpool', 'Arsenal')
