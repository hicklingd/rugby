from datetime import datetime
import pandas as pd
p='Sat, Feb 20'
d=datetime.strptime(p, "%a, %b %d")
print(d.strftime("%d/%m"))

list_of_names_h=[]
list_of_names_a=[]
list_of_scores=[]
date_list=[]
dataframe = pd.DataFrame({
    'Home Team': list_of_names_h,
    'Away Team': list_of_names_a,
    'Home score': list_of_scores[0::2],
    'Away Score': list_of_scores[1::2],
    'Date': date_list
})

print(dataframe.head())

#datetime_object = datetime.datetime.strptime(p)