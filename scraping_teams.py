import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from time import sleep 
from random import randint
import numpy as np
start = datetime.now()
print(start)
i=0
#my_dataframe = pd.read_csv('all_pages14_03_2021.csv')
#print(len(my_dataframe))
dataframe_squad = pd.read_csv('dataframe_squad.csv')
# read csv at the begining of each iteration, then save the csv at the end and export it, then read it and so on
print(dataframe_squad)
#print(dataframe_c)
count = 0
for page in range(1,3):#693):
    dataframe_squad = pd.read_csv('dataframe_squad.csv')
    count+=1
    print(count)
    #base page with all fixtures
    URL = 'https://www.ultimaterugby.com/match/list?date=recent&page='+str(page)

    page = requests.get(URL)

    soup = BeautifulSoup(page.text, 'html.parser')
    tournament_list = []
    matches = soup.select("div.main-content div.match-detail")
    list_of_home_teams=[]
    list_of_away_teams = []
    #goes to zero at the begining of a page
    counter_111 = 0
    for match in matches:
        
        match_c = match.find_all('a', href=True) 
        for match_c1 in match_c[0:1]:
            
            sleep(randint(2,6))
            
            URL_base = 'https://www.ultimaterugby.com'+match_c1['href']
            page_base = requests.get(URL_base)
            soup_base = BeautifulSoup(page_base.text, 'html.parser')
            

            lineup_url_f = soup_base.select("div.main-content div.container ul.page-nav") 
            for lineup_url_f1 in lineup_url_f:
                #picking the 2nd url in the board to get the url for the lineup
                lineup_url = lineup_url_f1.find_all('a', href=True)[1]['href']

            sleep(randint(2,6))    
            # now following this url to the lineup page 
            URL_lineup = 'https://www.ultimaterugby.com'+lineup_url

            page_lineup = requests.get(URL_lineup)
            soup_lineup = BeautifulSoup(page_lineup.text, 'html.parser')
            # the + finds the first table element that is placed immediatly after the div elements
            #lineup_tms = soup_lineup.select("div.main-content div.container div.lineup-container + table td.team-home span.name")[0]

            #home squad, first 15 are the starters
            home_squad = soup_lineup.select("td.team-home span.name")
            home_squad_list = []
            for player_h in home_squad:
                #because of double barreled surnames and long first names we cant split at capital letters, so have to do it the convoluted way
                # could try and use attributes 
                splitter = str(player_h).replace('<span class="name">\n\t\t\t\t\t\t','').replace('\t\t\t\t\t</span>','').replace('<br/>',' ')
                home_squad_list.append(splitter)
            #away squad, first 15 are the starters 
            away_squad = soup_lineup.select("td.team-away span.name")
            away_squad_list = []
            for player_a in away_squad:
                #because of double barreled surnames and long first names we cant split at capital letters, so have to do it the convoluted way 
                splitter = str(player_a).replace('<span class="name">\n\t\t\t\t\t\t','').replace('\t\t\t\t\t</span>','').replace('<br/>',' ')
                away_squad_list.append(splitter)
            # list of lists of squads of home and away teams
            list_of_home_teams.append(home_squad_list)
            list_of_away_teams.append(away_squad_list)
            # gives a dataframe of squads going down the results page, with lists 
            # need to create a dictionary with all the variables in it, dictionary comprehension, update the temp dataframe after each match, then add to main after every page
            #create dictionary on first match of page, then add to it on other matches, then add the page to the main dataframe
            if counter_111 ==0:
                data_dictionary_h = {('Home_position_{}'.format(i+1)): [v] for i,v in enumerate(home_squad_list)}
                data_dictionary_a = {('Away_position_{}'.format(i+1)): [v] for i,v in enumerate(away_squad_list)}
            if counter_111 !=0:
                # adding the teams of subsequent matches to the page dataframe 
                for index_c, key in enumerate(data_dictionary_h.keys()):
                    data_dictionary_h[key].append(home_squad_list[index_c])
                for index_c, key in enumerate(data_dictionary_a.keys()):
                    data_dictionary_a[key].append(away_squad_list[index_c])
            counter_111 +=1
                #dataframe_temp_squad = dataframe_temp_squad.append(pd.DataFrame.from_dict(data_dictionary_total
                #), ignore_index=True)

            
            
           
            
            
    # dictionary with keys as above and names of person in position as the value, at the end of the page
    data_dictionary_total = dict(data_dictionary_h, **data_dictionary_a) 
    #print(data_dictionary_total) 
    #dataframe_temp_squad = pd.DataFrame(data_dictionary_total)
    # I shall be creating a dataframe for the whole page, then adding this to the master at the end of the page
    current_page = pd.DataFrame(data_dictionary_total)
    dataframe_squad = dataframe_squad.append(current_page, ignore_index=True)
    dataframe_squad.to_csv(r'dataframe_squad.csv', index = False, header= True)

    sleep(randint(2,6))


print(dataframe_squad)    
#print(dataframe_squad)
#dataframe_squad.to_csv(r'all_pages_teams_squad{date}.csv'.format(date=str(datetime.today().strftime("%d_%m_%Y"))), index = False, header= True)

print(datetime.now()-start)