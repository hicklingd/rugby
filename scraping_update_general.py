import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from time import sleep 
from random import randint
import numpy as np
import sqlite3 as sql

start = datetime.now()

#setting up sqlite
conn = sql.connect('rugby_data.db')
c = conn.cursor()
# Find last row of database in form 
# ((13838, 'Benetton Rugby', 'Cardiff', 14.0, 29.0, '14/03/2021', 'Pro14'),)
last_row = tuple(c.execute("SELECT * FROM rugby_data where id= (SELECT MAX(id) FROM rugby_data)"))


page_n = 1

Master_Home_Team = []
Master_Away_Team=[]
Master_Home_Score=[]
Master_Away_Score=[]
Master_Date=[]
Master_Tournament=[]

breaker = True

while breaker == True:
    sleep(randint(2,10))
    #setting up soup object for page
    URL = 'https://www.ultimaterugby.com/match/list?date=recent&page='+str(page_n)
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

    
    Home_Score = list_of_scores[0::2]
    Away_Score = list_of_scores[1::2]

    #checking date home team and home score are the same
    for index, date in enumerate(date_list):
        if Home_Score[index] != 'n/a':
            if date == last_row[0][5]:
                print('true1') 
                if last_row[0][1] == list_of_names_h[index]:
                    print('true2') 

                    if last_row[0][3] == float(Home_Score[index]):
                        print('true3')
                        
                        breaker = False
                        break
        # will store data from most recent to furthest away, will have to reverse these when putting in the database
        Master_Home_Team.append(list_of_names_h[index])
        Master_Away_Team.append(list_of_names_a[index])
        Master_Home_Score.append(Home_Score[index])
        Master_Away_Score.append(Away_Score[index])
        Master_Date.append(date_list[index])
        Master_Tournament.append(tournament_list[index])
    print('next_page')
    page_n +=1




max_id= list(c.execute("SELECT MAX(id) FROM rugby_data").fetchall()[0])[0]
id_list = [num_2 for num_2 in reversed(range(max_id+1,max_id+1+len(Master_Home_Team)))]
for index in reversed(range(len(Master_Home_Team))): 
    id_v = id_list[index]
    Home_Team_v=Master_Home_Team[index].replace(' ', '')
    Away_Team_v=Master_Away_Team[index].replace(' ', '')
    if Master_Home_Score[index] != 'n/a':
        Home_Score_v=float(Master_Home_Score[index])
        Away_Score_v=float(Master_Away_Score[index])
    else:
        Home_Score_v=Master_Home_Score[index]
        Away_Score_v=Master_Away_Score[index]
    Date_v=Master_Date[index]
    Tournament_v=Master_Tournament[index].replace(' ', '')
    c.execute("INSERT INTO rugby_data (id, Home_Team, Away_Team, Home_score, Away_Score, Date, Tournament) VALUES (?,?,?,?,?,?,?);", (id_v,Home_Team_v,Away_Team_v,Home_Score_v,Away_Score_v,Date_v,Tournament_v))

# c.execute("INSERT INTO employees VALUES ('Mary', 'Schafer', 70000)")
conn.commit()

conn.close()



print(datetime.now()-start)