import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = 'https://www.ultimaterugby.com/match/list?date=recent&page=1'

page = requests.get(URL)

#html_bytes = page.read()

#html = html_bytes.decode("utf-8")

soup = BeautifulSoup(page.content, 'html.parser')
#
results = soup.find(id='teams')


job_elems = soup.find_all('div', **{"class":"team-home"} )
job_elems = soup.select('div.team-home span.score win')
for i in job_elems:
    print(i)
'''
for job in job_elems:
    print(job, end='n'*2)

job_elems = soup.find_all('div', **{"class":"teams"})
for job in job_elems:
    pp=job.find_all('span', **{"class":"score win"})
    print(pp)
    #print(job, end='n'*2)
'''

#print(results.prettify())
#print(html)
