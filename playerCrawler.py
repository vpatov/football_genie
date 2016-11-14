import urllib2
from bs4 import BeautifulSoup

base_url = 'http://sofifa.com/players?offset='
player_info_base_url = 'http://sofifa.com/player/'


players_data = {}

def get_players(offset):
    source_url = base_url + str(offset)
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    page = opener.open(source_url).read()
    soup = BeautifulSoup(page, "lxml")
    soup.prettify()

    table = soup.find('table', {"class": "table table-striped table-hover"})
    players = table.find('tbody').find_all('tr')


    if (len(players) > 0):
        # print len(players)
        for player in players:
            add_player(player)
            offset += 100
            # get_players(offset)
    else:
        print "Finished reading all players data"
            # break

def add_player(playerWebInfo):
    player_id = playerWebInfo.find('img')['id']
    player_info_url = player_info_base_url + str(player_id)

    tds = playerWebInfo.find_all('td')
    attributes = playerWebInfo.find_all('a')
    player_name = attributes[0].get_text()
    player_nationality = attributes[1].find('span')["title"].strip(' \t\n\r')
    player_age = tds[2].get_text().strip(' \t\n\r')
    player_positions_meta = tds[3].find_all('a')
    player_positions = []
    for position in player_positions_meta:
        current_position = position.find('span').get_text()
        player_positions.append(str(current_position))
    player_OVA = tds[4].find('span').get_text().strip(' \t\n\r')
    player_POT = tds[5].find('span').get_text().strip(' \t\n\r')

    if tds[6].find('a').has_attr('title'):
        player_team = tds[6].find('a')['title'].strip(' \t\n\r')
    else:
        player_team = "Free"
    player_contract_time = tds[7].get_text().strip(' \t\n\r')
    player_value = value_converter(tds[8].get_text())
    print player_info_url
    print player_name
    print player_nationality
    print player_age
    print player_positions
    print player_OVA
    print player_POT
    print player_team
    print player_contract_time
    print player_value
    get_detail_from_url(player_info_url)
    print "--------------------------------\n"

def value_converter(valueString):
    import string
    printable = set(string.printable)
    valueString = filter(lambda x: x in printable, valueString)
    valueString = str(valueString).strip(' \t\n\r')
    print valueString
    if len(valueString) < 2:
        return 0.0

    value_subString = valueString

    number_string = value_subString[:-1]
    unit = value_subString[-1]
    print "valueString: " + valueString + " lenth is: " + str(len(valueString))
    print "number+unit: " + value_subString
    print "number: " + number_string
    print unit
    if (unit == "M"):
        return float(number_string) * 1000000.0
    else:
        return float(number_string) * 1000.0

def get_players_main():
    offset = 0
    while offset <= 17500:
        get_players(offset)
        offset += 100

def get_detail_from_url(player_url):
    detail_json = {}
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    page = opener.open(player_url).read()
    soup = BeautifulSoup(page, "lxml")
    soup.prettify()
    # aside = soup.find('aside', {"class": "column"})
    # side_target_section = aside.find_all('div', {"class": "card mb-20"})[1]
    # side_target_section = side_target_section.find_all('div', {"id": "similar"})[0]
    # side_table = side_target_section.find('table')

    right_side_Section = soup.find("article", {"class": "column"})


    right_divs = right_side_Section.find_all('div', {"class": "columns mb-20"})
    divs_section1 = right_divs[0].find_all('div', {"class": "column col-3"})
    divs_section2 = right_divs[1].find_all('div', {"class": "column col-3"})

    attacking_div = divs_section1[0].find('div').find_all('div')[1]
    skill_div = divs_section1[1].find('div').find_all('div')[1]
    movement_div = divs_section1[2].find('div').find_all('div')[1]
    power_div = divs_section1[3].find('div').find_all('div')[1]

    mentality_div = divs_section2[0].find('div').find_all('div')[1]
    defending_div = divs_section2[1].find('div').find_all('div')[1]
    goalkeeping_div = divs_section2[2].find('div').find_all('div')[1]

    useful_divs = [attacking_div, skill_div, movement_div, power_div, mentality_div, defending_div, goalkeeping_div]

    # attacking = {}
    # skill = {}
    # movement = {}
    # power = {}
    # mentality = {}
    # defending = {}
    # goalkeeping = {}

    for div in useful_divs:
        for li in attacking_div.find_all('li'):
            skill_set = li.get_text().strip('\t\n\r').split(' ')
            skill_value = skill_set[0]
            skill_name = ' '.join(skill_set[1:])

            print skill_name
            print skill_value

    # for li in attacking_div.find_all('li'):
    #     skill_set = li.get_text().strip('\t\n\r').split(' ')
    #     skill_value = skill_set[0]
    #     skill_name = ' '.join(skill_set[1:])
    #
    #     print skill_name
    #     print skill_value



# player_url = 'http://sofifa.com/player/200108'
# get_detail_from_url(player_url)
# get_players(400)
get_players_main()

