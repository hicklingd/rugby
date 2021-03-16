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

for page in range(1,201):
    sleep(randint(2,10))
    URL = 'https://www.ultimaterugby.com/match/list?date=recent&page='+str(page)

    page = requests.get(URL)

    soup = BeautifulSoup(page.text, 'html.parser')
    tournament_list = []
    tournaments = soup.select("div.main-content div.tournament")
    for tournament in tournaments:
        tournament_1=tournament.find_all("a")
        for tournament_i in tournament_1:
            tournament_s = str(tournament_i.string)

            tournament_list.append(tournament_s)

    date_list = []
    years = soup.select("div.main-content div.match-detail")
    for year in years:
        year_1=year.find_all("a")
        for year_i in year_1:
            #print(year_i.string)
            year_s = year_i.string.split(' ')
            if str(year_s[-1])!='TBC':
                year_f = ' '.join([year_s[-3].replace('th','').replace('st','').replace('nd','').replace('rd','').zfill(2)]+year_s[-2:])
                date_f=datetime.strptime(year_f, "%d %b %Y")
                date_list.append(date_f.strftime("%d/%m/%Y"))
            else:
                date_list.append('n/a')

    #finding scores, working down the page from right to left, can also work out the winners with this but will do so in data analysis
    # cant go straight to scores as we need to filter out matches that havent been played for one reason or another
    scores = soup.select("div.main-content div.status")
    list_of_scores = []
    list_of_dates = []
    count=0
    for score in scores:
        score_1 = score.select("span.score")   
        if score_1:
            for score_i in score_1:
                list_of_scores.append(str(score_i.string).strip())
        #games without scores are assumed to not have been played and therefore have a n/a score
        else:
            list_of_scores+=['n/a','n/a']
        
    #finding names of home teams
    names_h = soup.select("div.main-content div.team-home span.team-name")
    list_of_names_h = []
    for name in names_h:
        list_of_names_h.append(str(name.string).strip())

    #finding names of away teams
    names_a = soup.select("div.main-content div.team-away span.team-name")
    list_of_names_a = []
    for name in names_a:
        list_of_names_a.append(str(name.string).strip())

    # convert into one list with home then away teams, same order as the scores
    list_of_names = []
    for i,j in enumerate(list_of_names_h):
        list_of_names+=[j,list_of_names_a[i]]


    dataframe_temp = pd.DataFrame({
        'Home_Team': list_of_names_h,
        'Away_Team': list_of_names_a,
        'Home_score': list_of_scores[0::2],
        'Away_Score': list_of_scores[1::2],
        'Date': date_list,
        'Tournament': tournament_list
    })

    dataframe = dataframe.append(dataframe_temp, ignore_index=True)

    '''
    print(list_of_scores)
    print(list_of_names)
    print(len(list_of_scores))
    print(len(list_of_names))
    '''
dataframe.to_csv(r'all_pages{date}.csv'.format(date=str(datetime.today().strftime("%d_%m_%Y"))), index = False, header= True)

print(dataframe)
print(datetime.now()-start)