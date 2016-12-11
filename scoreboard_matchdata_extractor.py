from bs4 import BeautifulSoup


#globals

# this info is obtained from each player's <td> in the html
player_fields = ['name', 'team', 'goals', 'assists', 'goal_attempts', 'shots_on_goal', 'blocked_shots', 'offsides',
                     'fouls_committed', 'fouls_sufferred', 'yellow_cards', 'red_cards', 'pass_success', 'total_passes']

# these are ALL of the fields that we are writing to the csv, which include player_fields but also include the match_date, and the two team names
all_fields = ['home_team', 'away_team', 'game_date'] + player_fields

fieldnames = [
    # basic match info
    'home_team', 'away_team', 'game_date', 'result',

    # match statistics
    'home_goals', 'away_goals', 'referee', 'attendance', 'venue',
    'home_ball_possession', 'away_ball_possession', 'home_goal_attempts', 'away_goal_attempts',
    'home_shots_on_goal', 'away_shots_on_goal', 'home_shots_off_goal', 'away_shots_off_goal',
    'home_blocked_shots', 'away_blocked_shots', 'home_free_kicks', 'away_free_kicks',
    'home_corner_kicks', 'away_corner_kicks', 'home_offsides', 'away_offsides',
    'home_goalkeeper_saves', 'away_goalkeeper_saves', 'home_fouls', 'away_fouls',
    'home_yellow_cards', 'away_yellow_cards',
    # lineups
    'home_formation', 'away_formation', 'home_players', 'away_players', 'home_substitutes', 'away_substitutes',
    'substitutions_made',
    'home_coach', 'away_coach',

    # player_info - this will be done in a separate csv
    # 'all_players'
]



# match_data_html -     the javascript-generated html from scoreboard.com, with info on the match
# player_data_html -    the javascript-generated html from scoreboard.com, with info on players performance in match
# match_csv_writer -    a simple csv_writer object, that writes a list to a row
# player_csv_writer -   a dict csv_writer object, that writes a dict to a row
def read_and_write(match_data_html,player_data_html,match_csv_writer,player_csv_writer):

    soup = BeautifulSoup(match_data_html,'lxml')

    #####################################
    ### Cell 1 (Getting basic match info)
    home_team = soup.find('td', {'class': 'tname-home logo-enable'}).text.strip()
    away_team = soup.find('td', {'class': 'tname-away logo-enable'}).text.strip()

    score_div = soup.find('div', {'id': 'content-all'})
    scores = score_div.find_all('span', {'class': 'scoreboard'})
    home_goals = int(scores[0].text.strip())
    away_goals = int(scores[1].text.strip())

    if home_goals > away_goals:
        result = 'W'
    elif home_goals == away_goals:
        result = 'D'
    else:
        result = 'L'


    ### Cell 2 (getting game date)
    game_date = soup.find('td', {'id': 'utime'}).text.strip()[:10]

    ### Cell 3 (Getting ref, attendance, and venue info)
    match_info_trs = soup.find_all('tr', {'class': 'content'})

    referee = None
    attendance = None
    venue = None

    for match_info in match_info_trs:

        cur = match_info.text.strip()
        if ('Referee' in cur):
            ref_string = cur.split('Referee: ')
            referee = ref_string[1]
        if ('Attendance' in cur):
            attendance_string = cur.split('Attendance: ')
            attendance = attendance_string[1].strip()
            attendance = attendance[:attendance.index(',')]
            attendance = attendance.replace(' ', '')
        if ('Venue' in cur):
            venue_string = cur.split('Venue: ')
            venue = venue_string[1].strip()


    ### Cell 4 (getting game statistics)
    whole_game_stats = soup.find('div', {'id': 'tab-statistics-0-statistic'})
    whole_game_stats = whole_game_stats.findAll('div')

    # first_half_stats = soup.find('div',{'id':'tab-statistics-1-statistic'})
    # second_half_stats = soup.find('div',{'id':'tab-statistics-2-statistic'})

    stats = []
    for el in whole_game_stats:
        text = el.text
        if (len(text) > 0):
            stats.append(text)


    home_ball_possession = float(stats[0].strip('%')) / 100
    away_ball_possession = float(stats[1].strip('%')) / 100
    assert (home_ball_possession + away_ball_possession == 1.0)

    home_goal_attempts = int(stats[2])
    away_goal_attempts = int(stats[3])

    home_shots_on_goal = int(stats[4])
    away_shots_on_goal = int(stats[5])

    home_shots_off_goal = int(stats[6])
    away_shots_off_goal = int(stats[7])

    home_blocked_shots = int(stats[8])
    away_blocked_shots = int(stats[9])

    home_free_kicks = int(stats[10])
    away_free_kicks = int(stats[11])

    home_corner_kicks = int(stats[12])
    away_corner_kicks = int(stats[13])

    home_offsides = int(stats[14])
    away_offsides = int(stats[15])

    home_goalkeeper_saves = int(stats[16])
    away_goalkeeper_saves = int(stats[17])

    home_fouls = int(stats[18])
    away_fouls = int(stats[19])

    home_yellow_cards = int(stats[20])
    away_yellow_cards = int(stats[21])



    ### Cell 5 (Getting the lineups)
    game_lineups = soup.find('div', {'id': 'lineups-content'})
    game_lineups = game_lineups.findAll('td')

    # remove non_ascii and digits
    def remove_badchars(text):
        return ''.join([i if (ord(i) < 128 and
                              ((ord(i) < ord('0')) or (ord(i) > ord('9'))))
                        else '' for i in text])

    home_formation = game_lineups[0].text
    away_formation = game_lineups[2].text

    home_players = []
    away_players = []

    for i in range(4, 4 + 22):
        player_name = remove_badchars(game_lineups[i].text)
        if '(' in player_name:
            player_name = player_name[:player_name.index('(')]
        if (i % 2 == 0):
            home_players.append(player_name)
        else:
            away_players.append(player_name)

    i += 2
    home_substitutes = []
    away_substitutes = []

    # substitutions made will be a list of pairs (a:b) means a came off, and b came on.
    substitutions_made = []

    while (game_lineups[i].text != "Missing Players"):
        sub = remove_badchars(game_lineups[i].text)
        sub = sub.replace('(G)', '')
        sub = sub.replace('(C)', '')

        actual_player = sub
        if '(' in sub:
            actual_player = sub[:sub.index('(')]
            substitutions_made.append((actual_player, sub[sub.index('(') + 1:-1]))

        if (i % 2 != 0):
            home_substitutes.append(actual_player)
        else:
            away_substitutes.append(actual_player)
        i += 1

    # There is no need to collect info on missing players. Including our model the players that are present is enough.
    while (game_lineups[i].text != 'Coaches'):
        i += 1

    assert (game_lineups[i].text == 'Coaches')
    i += 1

    home_coach = remove_badchars(game_lineups[i].text)
    i += 1

    away_coach = remove_badchars(game_lineups[i].text)





    ### Cell 6 (opening the detailed player info html)
    soup = BeautifulSoup(player_data_html, 'lxml')



    ### Cell 7 (Getting detailed player info for the match)
    player_table = soup.find('div', {'id': 'tab-player-statistics-0-statistic'})

    all_players = []
    odd_players = player_table.find_all('tr', {'class': 'odd'})
    even_players = player_table.find_all('tr', {'class': 'even'})



    for player in odd_players + even_players:
        player_tds = player.find_all('td')
        player_info = dict()

        player_info['home_team'] = home_team
        player_info['away_team'] = away_team
        player_info['game_date'] = game_date

        assert (len(player_tds) == 14)
        for i in range(0, len(player_tds)):
            player_info[player_fields[i]] = '0' if player_tds[i].text == '-' else player_tds[i].text

        all_players.append(player_info)
    ### Cell 8 (organizing the fieldnames, and printing them for easy inclusion in this python code)


    for field in fieldnames:
        print field, ',',

    ### Cell 9 (Writing to csv)
    #match_csv_writer.writerow(fieldnames)
    match_csv_writer.writerow([home_team , away_team , game_date , result , home_goals , away_goals ,
                         referee , attendance , venue , home_ball_possession , away_ball_possession ,
                         home_goal_attempts , away_goal_attempts , home_shots_on_goal , away_shots_on_goal ,
                         home_shots_off_goal , away_shots_off_goal , home_blocked_shots , away_blocked_shots ,
                         home_free_kicks , away_free_kicks , home_corner_kicks , away_corner_kicks ,
                         home_offsides , away_offsides , home_goalkeeper_saves , away_goalkeeper_saves ,
                         home_fouls , away_fouls , home_yellow_cards , away_yellow_cards ,
                         home_formation , away_formation , home_players , away_players ,
                         home_substitutes , away_substitutes , substitutions_made ,
                         home_coach , away_coach])

    for player in all_players:
    	player_csv_writer.writerow(player)



def create_csvs(seasons):
	import csv
	for season in seasons:
		f_match = open('./data/scoreboard_matches_' + season + '.csv','wb')
		match_csv_writer = csv.writer(f_match)
		
		f_players = open('./data/scoreboard_players_' + season + '.csv','wb')

		##need to get the match_data_html and player_data_html from the dir.
		read_and_write(match_data_html,player_data_html,match_csv_writer,player_csv_writer)
	

