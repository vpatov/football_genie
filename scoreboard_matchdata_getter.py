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



## visit the url using dryscrape to be able to access the javacsript-generated content,
## and return the soup object
def get_generated_dom(url,session):
	session.visit(url)
	response = session.body()
	soup = BeautifulSoup(response,'lxml')
	return soup

def write_soup_to_file(soup,filename):
	f = open(filename, 'w+')
	f.write(soup.prettify().encode('utf-8'))
	f.close()
	print "written soup to", filename




"""
def get_remaining_match_data_to_files(input_seasons,start_index=0):
	for season in input_seasons:
		filename = season + '_match_urls.txt'
        urls = [line.rstrip('\n') for line in open(filename)]
        # create target filepath
        target_directory = './match_stats_soup_files/' + season + '/'
        for i in range(start_index,len(urls)):
            url = urls[i]
            if url != "":
                gameId = url.split('/')[-2]
                target_filename = target_directory + gameId

                if os.path.isfile('./match_stats_soup_files/2014_2015/' + gameId):
                    print gameId, i
                continue


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
                    print "failed to scrape from url:",gameId,i
                    print e
"""
		


def get_match_data_to_files(input_seasons,start_index=0):
	all_scraped = True
	session = dryscrape.Session()
	for season in input_seasons:
		filename = season + '_match_urls.txt'
		urls = [line.rstrip('\n') for line in open(filename)]
		# create target filepath
		target_directory = './match_stats_soup_files/' + season + '/'
		for i in range(start_index,len(urls)):
			url = urls[i]
			if url != "":
				gameId = url.split('/')[-2]
				target_filename = target_directory + gameId

				if os.path.isfile('./match_stats_soup_files/' + season + '/' + gameId):
					print gameId, i, "is already scraped. not scraping."
					continue
				
				
				if i % 10 == 0:
					print '\n\nsleeping for 10 seconds during iteration',i,'\n\n'
					#cancel the active alarm, so that we dont timeout during sleep.
					signal.alarm(0)
					time.sleep(10)
				try:
					#attempt to scrape from a page should timeout if it takes more than 20 seconds.
					signal.alarm(20)
					print 'scraping', i, ':', gameId
					soup = get_generated_dom(url,session)
					write_soup_to_file(soup, target_filename)
					print 'scraped', i,'\n'

				except Exception as e:
					
					print "failed to scrape from url:",gameId,i
					print e
					if '104' in e.__str__():
						print "to avoid being blacklisted, crawler will now sleep for 60 seconds."
						signal.alarm(0)
						time.sleep(60)
					if '111' in e.__str__():
						print "Connection refused. wait 40 seconds, then try again."
						signal.alarm(0)
						time.sleep(40)

					all_scraped = False

	return all_scraped

def get_player_data_to_files(input_seasons,start_index=0):
	all_scraped = True
	session = dryscrape.Session()
	for season in input_seasons:
		filename = './player_stats_urls/' + season + '_player_stats_urls.txt'
		urls = [line.rstrip('\n') for line in open(filename)]
		# create target filepath
		target_directory = './player_stats_soup_files/' + season + '/'
		for i in range(start_index,len(urls)):
			url = urls[i]
			if url != "":
				gameId = url.split('/')[-2]
				target_filename = target_directory + gameId

				if os.path.isfile('./player_stats_soup_files/' + season + '/' + gameId):
					print gameId, i, "is already scraped. not scraping."
					continue
				
				
				if i % 5 == 0:
					print '\n\nsleeping for 10 seconds during iteration',i,'\n\n'
					#cancel the active alarm, so that we dont timeout during sleep.
					signal.alarm(0)
					time.sleep(10)
				try:
					#attempt to scrape from a page should timeout if it takes more than 20 seconds.
					signal.alarm(20)
					print 'scraping', i, ':', gameId
					soup = get_generated_dom(url,session)
					write_soup_to_file(soup, target_filename)
					print 'scraped', i,'\n'

				except Exception as e:
					
					print "failed to scrape from url:",gameId,i
					print e
					if '104' in e.__str__():
						print "to avoid being blacklisted, crawler will now sleep for 60 seconds."
						signal.alarm(0)
						time.sleep(60)
					if '111' in e.__str__():
						print "Connection refused. wait 40 seconds, then try again."
						signal.alarm(0)
						time.sleep(40)
		
					all_scraped = False

	return all_scraped	




if len(sys.argv) > 1:
	while (not get_match_data_to_files(start_index=int(sys.argv[1]),input_seasons=sys.argv[2:])):
		pass
	while (not get_player_data_to_files(start_index=int(sys.argv[1]),input_seasons=sys.argv[2:])):
		pass
	
else:
	print "need to input start index and seasons. input seasons in format 2012_2013 2013_2014...."
#get_match_data_to_files()
#get_player_data_to_files()

