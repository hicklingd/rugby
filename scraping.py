import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

start = datetime.now()

URL = 'https://www.ultimaterugby.com/match/list?date=recent&page=1'

page = requests.get(URL)

soup = BeautifulSoup(page.text, 'html.parser')
years_list = []
years = soup.select("div.main-content div.match-detail")
for year in years:
    year_1=year.find_all("a")
    for year_i in year_1:
        year_f = year_i.string.split(' ')[-1]
        years_list.append(year_f)

print(years_list)

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
        # will need to work out years at some point, in class match-detail
        date = score.select("div.kickoff span.date")
        for i in date:
            date_m = str(i.string)
            date_f=datetime.strptime(date_m, "%a, %b %d")
            print(date_f.strftime("%d/%m"))

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

print(list_of_scores)
print(list_of_names)
print(len(list_of_scores))
print(len(list_of_names))

print(datetime.now()-start)