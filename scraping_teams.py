import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from time import sleep 
from random import randint
import numpy as np
start = datetime.now()

list_of_names_h=[]
list_of_names_a=[]
list_of_scores=[]
date_list=[]
tournament_list = []
dataframe = pd.DataFrame({
    'Home_Team': list_of_names_h,
    'Away_Team': list_of_names_a,
    'Home_score': list_of_scores[0::2],
    'Away_Score': list_of_scores[1::2],
    'Date': date_list,
    'Tournament': tournament_list
})
i=0
for page in range(1,2):#693):
    
    #base page with all fixtures
    URL = 'https://www.ultimaterugby.com/match/list?date=recent&page='+str(page)

    page = requests.get(URL)

    soup = BeautifulSoup(page.text, 'html.parser')
    tournament_list = []
    matches = soup.select("div.main-content div.match-detail")
    for match in matches:
        match_c = match.find_all('a', href=True) 
        for match_c1 in match_c:

            if i == 0:
                URL_base = 'https://www.ultimaterugby.com'+match_c1['href']
                page_base = requests.get(URL_base)
                soup_base = BeautifulSoup(page_base.text, 'html.parser')
                i+=1

                lineup_url_f = soup_base.select("div.main-content div.container ul.page-nav") 
                for lineup_url_f1 in lineup_url_f:
                    #picking the 2nd url in the board to get the url for the lineup
                    lineup_url = lineup_url_f1.find_all('a', href=True)[1]['href']
                    
                # now following this url to the lineup page 
                URL_lineup = 'https://www.ultimaterugby.com'+lineup_url
                print(URL_lineup)
                page_lineup = requests.get(URL_lineup)
                soup_lineup = BeautifulSoup(page_lineup.text, 'html.parser')
                # the + finds the first table element that is placed immediatly after the div elements
                #lineup_tms = soup_lineup.select("div.main-content div.container div.lineup-container + table td.team-home span.name")[0]
                home_squad = soup_lineup.select("td.team-home span.name")
                home_squad_list = []
                for player in home_squad:
                    #because of double barreled surnames and long first names we cant split at capital letters, so have to do it the convoluted way 
                    splitter = str(player).replace('<span class="name">\n\t\t\t\t\t\t','').replace('\t\t\t\t\t</span>','').replace('<br/>',' ')
                    home_squad_list.append(splitter)
                print(home_squad_list)   
                #print(home_squad)

                

                

                
    
    
    
    
    sleep(randint(2,10))



                



# dataframe.to_csv(r'all_pages_teams{date}.csv'.format(date=str(datetime.today().strftime("%d_%m_%Y"))), index = False, header= True)

# print(dataframe)
print(datetime.now()-start)