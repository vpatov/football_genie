import pandas as pd
import datetime as time
import numpy as np
from sklearn.model_selection import train_test_split
from lastSixMatches import *
season = ['1011', '1112', '1213', '1314', '1415', '1516']
dataframe = pd.DataFrame()
list_ = []
for s in season:
    df = pd.read_csv('epl' + s + '.csv')
    col = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'Referee', 'HST', 'AST', 'HC', 'AC', 'HR', 'AR']
    df_temp = df[col]
    list_.append(df_temp)
dataframe = pd.concat(list_)
#
# col = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'Referee', 'HST', 'AST', 'HC', 'AC', 'HR', 'AR', \
#        '6HW','6AW','6HL','6AL','6HD','6AD','6FTHGS', '6FTHGC', '6FTAGS', '6FTAGC', '6HST', '6AST', '6HC', '6AC', '6HR', '6AR','H2H6FTHGS', 'H2H6FTHGC', \
#        'H2H6FTAGS', 'H2H6FTAGC', 'H2H6HST', 'H2H6AST', 'H2H6HC', 'H2H6AC', 'H2H6HR', 'H2H6AR']
#
# df_final = pd.DataFrame(columns=col)

season1 = ['1112', '1213', '1314', '1415', '1516']
newlist_ = []
result = []
for s in season1:
    df = pd.read_csv('epl' + s + '.csv')
    col = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'Referee', 'HST', 'AST', 'HC', 'AC', 'HR', 'AR']
    result = result + df['FTR'].tolist()
    df_temp = df[col]
    newlist_.append(df_temp)
newdataframe = pd.concat(newlist_)
#print(len(result))
newdataframe.loc[newdataframe['FTR'] == 'A','FTR'] = 0
newdataframe.loc[newdataframe['FTR'] == 'D','FTR'] = 1
newdataframe.loc[newdataframe['FTR'] == 'H','FTR'] = 2
# print newdataframe.corr(method='pearson')
#print newdataframe.iloc[0]
# col = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'Referee', 'HST', 'AST', 'HC', 'AC', 'HR', 'AR', \
#        '6HW','6AW','6HL','6AL','6HD','6AD','6FTHGS', '6FTHGC', '6FTAGS', '6FTAGC', '6HST', '6AST', '6HC', '6AC', '6HR', '6AR','H2H6FTHGS', 'H2H6FTHGC', \
#        'H2H6FTAGS', 'H2H6FTAGC', 'H2H6HST', 'H2H6AST', 'H2H6HC', 'H2H6AC', 'H2H6HR', 'H2H6AR']
#
_6HW = []
_6HL = []
_6HD = []
_6AW = []
_6AL = []
_6AD = []
_6FTHGS = []
_6FTHGC = []
_6FTAGS = []
_6FTAGC = []
_6HST = []
_6AST = []
_6HC = []
_6AC = []
_6HR = []
_6AR = []
_H2H6FTHGS = []
_H2H6FTAGS = []
_H2H6FTHGC = []
_H2H6FTAGC = []
_H2H6HST = []
_H2H6AST = []
_H2H6HC = []
_H2H6AC = []
_H2H6HR = []
_H2H6AR = []

# building the final data frame
for _,row in newdataframe.iterrows():
    _6HW.append(get_number_of_wins(dataframe, str(row['Date']), str(row['HomeTeam'])))
    _6AW.append(get_number_of_wins(dataframe, str(row['Date']), str(row['AwayTeam'])))
    # print(get_number_of_draws(dataframe, str(row['Date']), str(row['HomeTeam'])))
    _6HD.append(get_number_of_draws(dataframe, str(row['Date']), str(row['HomeTeam'])))
    _6AD.append(get_number_of_draws(dataframe, str(row['Date']), str(row['AwayTeam'])))
    _6HL.append(get_number_of_losses(dataframe, str(row['Date']), str(row['HomeTeam'])))
    _6AL.append(get_number_of_losses(dataframe, str(row['Date']), str(row['AwayTeam'])))
    _6FTHGS.append(get_number_of_goals_scored(dataframe, str(row['Date']), str(row['HomeTeam'])))
    _6FTHGC.append(get_number_of_goals_conceded(dataframe, str(row['Date']), str(row['HomeTeam'])))
    _6FTAGS.append(get_number_of_goals_scored(dataframe, str(row['Date']), str(row['AwayTeam'])))
    _6FTAGC.append(get_number_of_goals_conceded(dataframe, str(row['Date']), str(row['AwayTeam'])))
    _6HST.append(get_number_of_shots_on_target(dataframe, str(row['Date']), str(row['HomeTeam'])))
    _6AST.append(get_number_of_shots_on_target(dataframe, str(row['Date']), str(row['AwayTeam'])))
    _6HC.append(get_number_of_corners(dataframe, str(row['Date']), str(row['HomeTeam'])))
    _6AC.append(get_number_of_corners(dataframe, str(row['Date']), str(row['AwayTeam'])))
    _6HR.append(get_number_of_red_cards(dataframe, str(row['Date']), str(row['HomeTeam'])))
    _6AR.append(get_number_of_red_cards(dataframe, str(row['Date']), str(row['AwayTeam'])))
    _H2H6FTHGS.append(get_number_of_h2h_home_goals_scored(dataframe, str(row['Date']), str(row['HomeTeam']), str(row['AwayTeam']), str(row['HomeTeam'])))
    _H2H6FTAGS.append(get_number_of_h2h_away_goals_scored(dataframe, str(row['Date']), str(row['HomeTeam']), str(row['AwayTeam']), str(row['AwayTeam'])))
    _H2H6FTHGC.append(get_number_of_h2h_home_goals_conceded(dataframe, str(row['Date']), str(row['HomeTeam']), str(row['AwayTeam']), str(row['HomeTeam'])))
    _H2H6FTAGC.append(get_number_of_h2h_away_goals_conceded(dataframe, str(row['Date']), str(row['HomeTeam']), str(row['AwayTeam']), str(row['AwayTeam'])))
    _H2H6HST.append(get_number_of_h2h_home_shot_on_target(dataframe, str(row['Date']), str(row['HomeTeam']), str(row['AwayTeam']), str(row['HomeTeam'])))
    _H2H6AST.append(get_number_of_h2h_away_shot_on_target(dataframe, str(row['Date']), str(row['HomeTeam']), str(row['AwayTeam']), str(row['AwayTeam'])))
    _H2H6HC.append(get_number_of_h2h_home_corners(dataframe, str(row['Date']), str(row['HomeTeam']), str(row['AwayTeam']), str(row['HomeTeam'])))
    _H2H6AC.append(get_number_of_h2h_away_corners(dataframe, str(row['Date']), str(row['HomeTeam']), str(row['AwayTeam']), str(row['AwayTeam'])))
    _H2H6HR.append(get_number_of_h2h_home_red_cards(dataframe, str(row['Date']), str(row['HomeTeam']), str(row['AwayTeam']), str(row['HomeTeam'])))
    _H2H6AR.append(get_number_of_h2h_away_red_cards(dataframe, str(row['Date']), str(row['HomeTeam']), str(row['AwayTeam']), str(row['AwayTeam'])))
newdataframe['6HW'] = _6HW
newdataframe['6AW'] = _6AW
newdataframe['6HD'] = _6HD
newdataframe['6AD'] = _6AD
newdataframe['6HL'] = _6HL
newdataframe['6AL'] = _6AL
newdataframe['6FTHGS'] = _6FTHGS
newdataframe['6FTHGC'] = _6FTHGC
newdataframe['6FTAGS'] = _6FTAGS
newdataframe['6FTAGC'] = _6FTAGC
newdataframe['6HST']=_6HST
newdataframe['6AST']=_6AST
newdataframe['6HC']=_6HC
newdataframe['6AC']=_6AC
newdataframe['6HR'] = _6HR
newdataframe['6AR']=_6AR
newdataframe['H2H6FTHGS']=_H2H6FTHGS
newdataframe['H2H6FTAGS']=_H2H6FTAGS
newdataframe['H2H6FTHGC']=_H2H6FTHGC
newdataframe['H2H6FTAGC']=_H2H6FTAGC
newdataframe['H2H6HST']=_H2H6HST
newdataframe['H2H6AST']=_H2H6AST
newdataframe['H2H6HC']=_H2H6HC
newdataframe['H2H6AC']=_H2H6AC
newdataframe['H2H6HR']=_H2H6HR
newdataframe['H2H6AR']=_H2H6AR
#print(newdataframe.isnull())
newdataframe = newdataframe.dropna()
#print(newdataframe.isnull().any())
#newdataframe = newdataframe[pd.notnull()]
# #print(newdataframe)
# #print result
#
# #print(newdataframe.corr())
# #print(newdataframe.isnan().any())
columns = newdataframe.columns.tolist()
columns = [c for c in columns if c not in ['Date', 'HomeTeam', 'AwayTeam', 'Referee']]
target = 'FTR'
#
from sklearn.linear_model import LinearRegression
model = LinearRegression()
X_train, X_test, y_train, y_test = \
    train_test_split(newdataframe[columns], newdataframe[target], test_size=0.2, random_state=0)
model.fit(X_train, y_train)
#
#
from sklearn.metrics import mean_squared_error
predictions = model.predict(X_test)
print mean_squared_error(predictions, y_test)
print model.score(X_test, y_test)

