# need to run a regression on all the data, 
#
#
# 
import pandas as pd
from datetime import datetime
start = datetime.now()

data = pd.read_csv('200_pages24_02_2021.csv')
list_of_games_h = []
list_of_games_a = []
for i,j in enumerate(data['Home_Team']):
    if j=='Bath':
        list_of_games_h.append(i)
    elif data['Away_Team'][i]=='Bath':
        list_of_games_a.append(i)


home_data = data.iloc[list_of_games_h,:]
away_data = data.iloc[list_of_games_a,:]
wins_h=0
wins_a=0

for index, row in home_data.iterrows():
    if row['Home_score']>row['Away_Score']:
        wins_h+=1

for index, row in away_data.iterrows():
    if row['Home_score']<row['Away_Score']:
        wins_a+=1
  

print('away win percentage '+str(wins_a/len(away_data)))
print('home win percentage '+str(wins_h/len(home_data)))


print(datetime.now()-start)