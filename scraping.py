import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = 'https://www.ultimaterugby.com/match/list?date=recent&page=1'

page = requests.get(URL)

soup = BeautifulSoup(page.text, 'html.parser')

job_elems = soup.select("div.status span.score")
for i in job_elems:
    print(i)



#print(results.prettify())
#print(html)
