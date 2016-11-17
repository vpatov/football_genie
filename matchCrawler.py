import httplib2
from bs4 import BeautifulSoup

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
     print response


crawl_team(teams[0],seasons[0])


