import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

continents = ["North America", "Europe", "South America", "Asia", "Africa", "Oceania"]

#load the main table for today
URL = 'https://www.worldometers.info/coronavirus/'
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html.parser')
table_html = soup.find(id='main_table_countries_today')




#load column titles
headerTitles = []
for colTitle in table_html.select('thead th')[:7]:
    headerTitles.append(re.sub(r"(\w)([A-Z])", r"\1 \2", colTitle.text))

data = []

#load data
rows = table_html.select('tbody tr')
for row in rows:
    d = dict()
    rowEntries = row.select('td')[:7]
    for idx,rowEntry in enumerate(rowEntries):
        if rowEntry == '':
            print("NONE")
        try:
            d[headerTitles[idx]] = float(rowEntry.text.strip().strip('+').replace(',', ''))
        except:
            d[headerTitles[idx]] = rowEntry.text.strip()
    data.append(d)
    if len(data) == 40:
        break


data = data[:40]

filter_by_country = [x for x in data if x['Country,Other'] not in continents + ["", "World"]][:10]
filter_by_continent = [x for x in data if x['Country,Other'] in continents]


df = pd.DataFrame(filter_by_country)
df['Total Cases'] = df['Total Cases']/1000.0


plt.rcdefaults()
fig, ax = plt.subplots()


ax.barh(df['Country,Other'], df['Total Cases'], align='center')
ax.invert_yaxis()
ax.set_xlabel('Total Cases (in thousands)')
ax.set_title('Top 10 Countries with Most Covid Cases')


for i, v in enumerate(df["Total Cases"]):
    plt.text(v+0.2, i, str(round(v, 2)), color='steelblue', va="center")

plt.show()
