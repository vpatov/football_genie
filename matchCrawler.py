import httplib2
from bs4 import BeautifulSoup
import re
import csv

score_pattern = re.compile('\d+-\d+')


http = httplib2.Http()
user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'



example_url = 'www.11v11.com/teams/arsenal/tab/matches/season/2017/'

base_url = 'http://www.11v11.com/teams/'
matches_url = '/tab/matches/season/'

seasons = ['2017','2016','2015','2014','2013']


def make_url(team,season):
    team_name = team.replace(' ','-')
    team_name = team_name.lower()
    return base_url + team_name + matches_url + str(season)

#status, response = http.request(base_url,headers={ 'User-Agent' : user_agent })


def init_teams():
    teams = []
    teamstring = """
     AFC Bournemouth
     Arsenal
     Burnley
     Chelsea
     Crystal Palace
     Everton
     Hull City
     Leicester City
     Liverpool
     Manchester City
     Manchester United
     Middlesbrough
     Southampton
     Stoke City
     Sunderland
     Swansea City
     Tottenham Hotspur
     Watford
     West Bromwich Albion
     West Ham United"""

    for team in teamstring.split('\n'):
        if len(team.strip()) > 1:
            teams.append(team.strip())

    return teams
teams = init_teams()

season_histories = {season:None for season in seasons}

def crawl_team(team,season):
    url = make_url(team,season)
    status, response = http.request(url,headers={ 'User-Agent' : user_agent })
    soup = BeautifulSoup(response,'lxml')
    soup.prettify()
    table = soup.find('table')
    matches = table.find('tbody').find_all('tr')
    match_list = []
    for match in matches:
        tds = match.find_all('td')
        date = tds[0].text
        two_teams = tds[1].text.split(' v ')
        home = two_teams[0]
        away = two_teams[1]
        score = score_pattern.findall(tds[3].text)[0].split('-')
        home_goals, away_goals = int(score[0]),int(score[1])
        result = None

        league = tds[4].text.strip()
        if (home_goals > away_goals):
            result = 'W'
        elif (home_goals == away_goals):
            result = 'D'
        else:
            result = 'L'

        match_info = (date,home,away,home_goals,away_goals,result,league)
        match_list.append(match_info)

    return match_list


def crawl_season(season):
    global season_histories
    season = str(season)
    season_history = []
    for team in teams:
        match_list = crawl_team(team,season)
        season_history += match_list
        print "crawled",team,season
    season_histories[season] = season_history

def write_season_history(season):
    season = str(season)
    csvfile = open('premier-league-' + season + '.csv', 'wb')
    fieldnames = ['date', 'home', 'away', 'home_goals','away_goals','result','league']
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)

    for match in season_histories[season]:
        writer.writerow(match)

    csvfile.close()

for season in seasons:
    crawl_season(season)
    write_season_history(season)





