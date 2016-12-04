from bs4 import BeautifulSoup
import re
import csv
import dryscrape


### this file will have a function, extract_data(url),
### that when given the url of a match (on scoreboard.com),
### will get the meaningful data from it, and add it to a list
### to be ready for writing to a .csv file

matches = []

def extract_data(url):
	session = dryscrape.Session()
	session.visit(url)
	response = session.body()
	soup = BeautifulSoup(response,'lxml')
	f = open('test_output.txt','w')
	f.write(soup.prettify().encode('utf-8'))
	f.close()
	print('written to file\n');

test_url = 'http://www.scoreboard.com/en/match/west-ham-arsenal-2016-2017/zRp4p5Xc/#match-summary|match-statistics;0|lineups;1'

extract_data(test_url)
