##Unfortunately, I must call this code from a VM because I cannot install dryscrape on my windows machine,
##and I need dryscrape to scrape from webpages that use javascript to generate content.

### WHAT THIS NEEDS: this needs a timeout error function, after which it will place the unsuccessful url
### into a queue that will be tried again either immediately, or later, or put into a list of unsuccessful urls
### for manual inspection.

from bs4 import BeautifulSoup
import time
import re
import csv
import dryscrape
import os
import signal
import sys


def handler(signum, frame):
	print "scraping has timed out."
	raise Exception("scrape timeout")

signal.signal(signal.SIGALRM, handler)


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
	f = open(filename, 'w+')
	f.write(soup.prettify().encode('utf-8'))
	f.close()
	print "written soup to", filename



test_match_stats_url = 'http://www.scoreboard.com/en/match/west-ham-arsenal-2016-2017/zRp4p5Xc/#match-summary|match-statistics;0|lineups;1'
test_player_stats_url = 'http://www.scoreboard.com/en/match/west-ham-arsenal-2016-2017/zRp4p5Xc/#player-statistics;0'

# test_soup = get_generated_dom(test_match_stats_url)
# write_soup_to_file(test_soup,'example_scoreboard_soup.txt')


##### new code added by Rui

seasons = ['2016_2017', '2015_2016', '2014_2015', '2013_2014', '2012_2013', '2011_2012', '2010_2011']

def get_match_data_to_files(start_index=0):
    for season in ['2014_2015']:
		filename = season + '_match_urls.txt'
		urls = [line.rstrip('\n') for line in open(filename)]
		failed_urls = []
        # create target filepath
		target_directory = './match_stats_soup_files/' + season + '/'
		for i in range(start_index,len(urls)):
			url = urls[i]
			if url != "":
				gameId = url.split('/')[-2]
				target_filename = target_directory + gameId

				if i % 5 == 0:
					print '\n\nsleeping for 10 seconds during iteration',i,'\n\n'
					time.sleep(10)
				try:
					signal.alarm(25)
					print 'scraping', i, ':', gameId
					soup = get_generated_dom(url)
					write_soup_to_file(soup, target_filename)
					print 'scraped', i,'\n'
				except Exception as e:
					failed_urls.append(url)
					print "failed to scrape from url:",gameId,i
					print e

		f = open('failed_urls_' + season + '.txt','wb')
		for failed_url in failed_urls:
			f.write(failed_url)
		f.close()

def get_player_data_to_files():
	for season in ['2014_2015']:
		filename = season + '_player_stats_urls.txt'
		urls = [line.rstrip('\n') for line in open('.player_stats_urls/' + filename)]
						

		# create target filepath
        current_season = '_'.join(filename.split('_')[0:2])
        target_directory = './player_stats_soup_files/' + current_season + '/'
        for url in urls:
        	if url != "":
				print url
				gameId = url.split('/')[-2]
				target_filename = target_directory + gameId
				soup = get_generated_dom(url)
				write_soup_to_file(soup, target_filename)



if len(sys.argv) > 1:
	get_match_data_to_files(int(sys.argv[1]))
else:
	get_match_data_to_files()
#get_match_data_to_files()
#get_player_data_to_files()

