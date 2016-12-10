import httplib2
import urllib2
from bs4 import BeautifulSoup

http = httplib2.Http()
user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'

base_url = 'http://www.scoreboard.com/soccer/england/premier-league-'

seasons = ['2016_2017', '2015_2016', '2014_2015', '2013_2014', '2012_2013', '2011_2012', '2010_2011']

def get_main_page():
    result = {}
    for season in seasons:
        result[season] = []

        source_url = base_url + season + '/results'
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        page = opener.open(source_url).read()
        soup = BeautifulSoup(page, "lxml")
        soup.prettify()
        # print soup

        container_div = soup.find('div', class_='container')
        main_div = container_div.find('div', class_='main')
        main_ledt_div = main_div.find('div', class_='main-left')
        tournament_page = main_ledt_div.find('div', class_='center col-center tournament_page')
        body_div = tournament_page.find('div', id='fsbody')
        data_div = body_div.find('div', style='display: none').find('div', id='tournament-page-data-results')
        print data_div.get_text()

        fs_results_div = body_div.find('div', id='fs-results')
        table_section = body_div.find('table', class_='soccer')
        # print '-----------------2'
        # print body_div

        table_sections = soup.find_all('table', class_='soccer')

def get_data_from_local(season):
    local_file_name = "Premier League " + season + " Scores _ Results _ Scoreboard.com.html"
    soup = BeautifulSoup(open(local_file_name), "lxml")


    container_div = soup.find('div', class_='container')
    main_div = container_div.find('div', class_='main')
    main_left_div = main_div.find('div', class_='main-left')
    tournament_page = main_left_div.find('div', class_='center col-center tournament_page')
    body_div = tournament_page.find('div', id='fsbody')
    results_div = body_div.find('div', id='fs-results')
    table_body_div = results_div.find('table', class_='soccer').find('tbody')
    table_rows = table_body_div.find_all('tr')

    target_urls = []
    # print '--------------------------'
    # print season
    target_basic_url = 'http://www.scoreboard.com/game/manchester-united-tottenham-'
    season_url = '-'.join(season.split('_'))

    save_to_file = season + '_match_urls.txt'
    f = open(save_to_file, 'w')

    # get id, form url, and save in file
    for row in table_rows:
        if row.has_attr('id'):
            id = row['id'].split('_')[-1]
            url = target_basic_url + season_url + '/' + id + '/#game-summary|game-statistics;0|lineups;1'
            print url
            target_urls.append(url)
            f.write(url + '\n')

    f.close()


# only from year 2013 do the website provide player stats
player_stats_seasons = ['2013_2014', '2014_2015', '2015_2016', '2016_2017']
def get_players_stats_urls():
    for season in player_stats_seasons:
        local_filename = season + '_match_urls.txt'
        lines = [line.rstrip('\n') for line in open(local_filename)]
        target_filename = './player_stats_urls/' + season + '_player_stats_urls.txt'
        with open(target_filename, 'w+') as f:
            for line in lines:
                if line != '':
                    target_url = line.split('#')[0] + '#player-statistics;0' + '\n'
                    f.write(target_url)
        f.close()


# get_players_stats_urls()

# for season in seasons:
#     get_data_from_local(season)