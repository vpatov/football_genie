import csv
import scoreboard_matchdata_extractor

seasons = [2010,2011,2012,2013,2014,2015,2016]
filenames = []




test_match_db1 = open('test_match_db1.csv','wb')
test_player_db1 = open('test_player_db1.csv','wb')
test_match_writer = csv.writer(test_match_db1)
test_player_writer = csv.DictWriter(test_player_db1,fieldnames=scoreboard_matchdata_extractor.all_fields)
test_match_writer.writerow(scoreboard_matchdata_extractor.fieldnames)
test_player_writer.writeheader()

for i in range(0,67):
    f = open('test' + str(i) + '.txt')
    file_contents = f.read()

    #####TODO input the match_data_html, and the player_data_html.
    #####TODO you need to get the player_data_html's, meaning scrape them using dryscrape.
    scoreboard_matchdata_extractor.read_and_write()





