# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 00:23:29 2022

@author: anggapark
"""

# set up packages
import requests
from bs4 import BeautifulSoup
import lxml
import pandas as pd

site = "https://editorial.rottentomatoes.com/guide/140-essential-action-movies-to-watch-now/"
response = requests.get(site)

html = response.content
soup = BeautifulSoup(html, 'lxml')


# =============================================================================
# Find and Extract Data from Website
# =============================================================================

divs = soup.find_all('div', {'class': 'col-sm-18 col-full-xs countdown-item-content'})

""" Headings """
headings = [div.find('h2') for div in divs]
# get title
titles = [heading.find('a').string for heading in headings]

# get year
years = [heading.find('span', {'class': 'subtle start-year'}).string for heading in headings]
years = [int(year.strip('()')) for year in years]

# get scores
scores = [heading.find('span', {'class': 'tMeterScore'}).string for heading in headings]
# remove percentage(%)
scores = [scr.strip('%') for scr in scores]


""" Contents """
contents = soup.find_all('div', {'class': 'row countdown-item-details'})

# get critics consensus
consensus = [content.find('div', {'class': 'info critics-consensus'}) for content in contents]
# drop 'Critics Consensus: ' from string
common_text = "Critics Consensus: "
common_len = len(common_text)
consensus_text = [con.text[common_len:] for con in consensus]

# get director
directors = [content.find('div', {'class': 'info director'}) for content in contents]
directors = [director.find('a').string for director in directors]

# get cast
casts = [content.find('div', {'class': 'info cast'}) for content in contents]
cast = []
for c in casts:
    cast_name = [info.string for info in c.find_all('a')]
    cast.append(', '.join(cast_name))

# get synopsis
synopsis = [content.find('div', {'class': 'info synopsis'}) for content in contents]
synopsis_text = [s.contents[1] for s in synopsis]



# =============================================================================
# Set Dataframe
# =============================================================================

data = {'Movie Title': titles,
        'Year': years,
        'Score': scores,
        'Director': directors,
        'Cast': cast,
        'Synopsis': synopsis_text,
        'Critics Consensus': consensus_text,}

movies = pd.DataFrame(data=data)
movies.head()

# write data do CSV file
# movies.to_csv('rottentomatoes_movies.csv', index=False, header=True)