import urllib
from bs4 import BeautifulSoup

base_url = 'http://www.football-data.co.uk/'
source_pages = {'England': 'http://www.football-data.co.uk/englandm.php',
                'Scotland': 'http://www.football-data.co.uk/scotlandm.php',
                'Germany': 'http://www.football-data.co.uk/germanym.php',
                'Italy': 'http://www.football-data.co.uk/italym.php',
                'Spain': 'http://www.football-data.co.uk/spainm.php',
                'France': 'http://www.football-data.co.uk/francem.php',
                'Netherlands': 'http://www.football-data.co.uk/netherlandsm.php',
                'Belgium': 'http://www.football-data.co.uk/belgiumm.php',
                'Portugal': 'http://www.football-data.co.uk/portugalm.php',
                'Turkey': 'http://www.football-data.co.uk/turkeym.php',
                'Greece': 'http://www.football-data.co.uk/greecem.php'
                }

def get_urls(country, source_url):
    page = urllib.urlopen(source_url).read()
    soup = BeautifulSoup(page, "lxml")
    soup.prettify()

    tables = soup.find_all('table', {"cellspacing": "0"})
    target_table = tables[1]
    target_table_row = target_table.find_all('tr')[1]
    target_data_section = target_table_row.find_all('td', {"valign": "top"})[1]

    target_urls = target_data_section.find_all('a')
    print "---------------------------------------"
    print "Country:" + country
    file_download_tool = urllib.URLopener()
    for url_element in target_urls:
        link = str(url_element["href"])
        file_name = link.split("/")
        if len(file_name) > 0:
            file_extension = file_name[-1].split(".")[-1]
            if file_extension == "csv":
                cup_name = url_element.get_text()
                download_full_url = base_url + str(url_element["href"])
                year = link.split('/')[-2]
                download_filename = country + '_' + year + '_' + cup_name + '.csv'
                print "downloading from: " + download_full_url + " to " + download_filename
                file_download_tool.retrieve(download_full_url, download_filename)


for country in source_pages.keys():
    get_urls(country, source_pages[country])