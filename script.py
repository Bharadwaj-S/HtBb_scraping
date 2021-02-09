#!/usr/bin/env python
# coding: utf-8
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Webscraping
htb = requests.get('https://hashtagbasketball.com/fantasy-basketball-projections').content
soup = BeautifulSoup(htb, 'html.parser')

player_data = []
rows = soup.find(id='ContentPlaceHolder1_GridView1').find_all('tr')
for row in rows:
    data = row.find_all('td')
    if len(data) > 0 and data[0].text != 'R#':
        player_data.append([d.text.strip('\n') for d in data])

# Data cleaning
player_df = pd.DataFrame(player_data)
player_df = player_df.drop(columns=[0, 4, 5, 15])
player_df.columns = ['Player', 'Position', 'Team', 'FG%', 'FT%', '3PM', 
                    'PTS', 'REB', 'AST', 'STL', 'BLK', 'TO']
player_notes = player_df['Player'].str.split('\n')
player_df['Player'] = player_notes.map(lambda x : x[0].lstrip().rstrip())
# raw_df['Notes'] = player_notes.map(lambda x : x[-1])
fgp = player_df['FG%'].str.split('\n').map(lambda x : x[-1][1:-1].split('/'))
ftp = player_df['FT%'].str.split('\n').map(lambda x : x[-1][1:-1].split('/'))
player_df['FGM'] = fgp.map(lambda x : x[0])
player_df['FGA'] = fgp.map(lambda x : x[1])
player_df['FTM'] = ftp.map(lambda x : x[0])
player_df['FTA'] = ftp.map(lambda x : x[1])
player_df = player_df.drop(columns=['FG%', 'FT%'])
player_df.head()

scoring = {'FGM':2, 'FGA':-1, 'FTM':1, 'FTA':-1, '3PM':1, 
           'REB':1, 'AST':2, 'STL':4, 'BLK':4, 'TO':-2, 'PTS':1}

player_df["Total"] = 0
for col in scoring:
    player_df["Total"] += player_df[col].astype('float') * scoring[col]

player_df = player_df.sort_values('Total', ascending=False)
player_df.to_csv('Player data.csv', index=None)
