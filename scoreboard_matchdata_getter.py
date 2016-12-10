from bs4 import BeautifulSoup
import re
import csv
import dryscrape


matches = []

## visit the url using dryscrape to be able to access the javacsript-generated content,
## and return the soup object
def get_generated_dom(url):
	session = dryscrape.Session()
	session.visit(url)
	response = session.body()
	soup = BeautifulSoup(response,'lxml')
	return soup

def write_soup_to_file(soup,filename):
	f = open(filename,'w')
	f.write(soup.prettify().encode('utf-8'))
	f.close()
	print "written soup to", filename



#test_match_stats_url = 'http://www.scoreboard.com/en/match/west-ham-arsenal-2016-2017/zRp4p5Xc/#match-summary|match-statistics;0|lineups;1'
#test_player_stats_url = 'http://www.scoreboard.com/en/match/west-ham-arsenal-2016-2017/zRp4p5Xc/#player-statistics;0'

#test_soup = get_generated_dom(test_match_stats_url)
#write_soup_to_file(test_soup,'example_scoreboard_soup.txt')

test_batch_urls = []
f = open('2010_2011_match_urls.txt','r')
for line in f:
	test_batch_urls.append(line.strip())

i = 0
for i in range(0,len(test_batch_urls)):
	url = test_batch_urls[i]
	#soup = get_generated_dom(url)
	#write_soup_to_file(soup,'test' + str(i) + '.txt')
	print "written", i
	i += 1




