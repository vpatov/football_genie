import httplib2
from bs4 import BeautifulSoup
import re
import csv



### this file will have a function, extract_data(url),
### that when given the url of a match (on scoreboard.com),
### will get the meaningful data from it, and add it to a list
### to be ready for writing to a .csv file

matches = []

def extract_data(url):
    pass