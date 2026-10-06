import json
from datetime import date, timedelta, datetime
import numpy as np
import pandas as pd
import pickle


team_n = ['Total Games', 'Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers', 'LA Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies', 'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks', 'Oklahoma City Thunder', 'Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards', 'TBD']

with open('converted_calendar3.json') as cal_f:
    cal_d = json.load(cal_f)

#print(cal_d['children'][0]['children'][#]['children'][0]['children'][0]['text'])
#                        ^week          ^date, skips 0                ^0: date, 1: num games on date

#print(cal_d['children'][0]['children'][1]['children'][1]['children'][#]['children'][0]['children'][1]['children'][#]['children'][0]['text'])#[1]['text'])
#                                                                     ^game of day                                 ^0: away team, 1: home team


date_s = date(2026, 10, 20)
#date_e = date(2027, 4, 11)

date_l = [(date_s + timedelta(days=i)).strftime("%m/%d/%Y") for i in range(174)]
date_l2 = np.zeros([32,174],dtype=int)

week_n = range(0,25)
#day_n = range(0,7)

for idx0 in week_n:
    week_g = range(1,len(cal_d['children'][idx0]['children']))

    for idx1 in week_g:
        date_g0 = cal_d['children'][idx0]['children'][idx1]['children'][0]['children'][0]['text']
        day_g_word1 = (cal_d['children'][idx0]['children'][idx1]['children'][0]['children'][1]['text'])
        day_g_word2 = day_g_word1.split(' ')
        day_g = int(day_g_word2[0])

        date_g1 = datetime.strptime(date_g0, "%A, %B %d").strftime("%m/%d")
        if int(date_g1[0])<1:
            date_g2 = date_g1+'/2027'
        else:
            date_g2 = date_g1+'/2026'
        date_index = int(date_l.index(date_g2))
        date_l2[0][date_index] = day_g
        day_g_r = range(0,day_g)

        for idx3 in day_g_r:
            team_1 = cal_d['children'][idx0]['children'][idx1]['children'][1]['children'][idx3]['children'][0]['children'][1]['children'][-2]['children'][0]['text']
            team_2 = cal_d['children'][idx0]['children'][idx1]['children'][1]['children'][idx3]['children'][0]['children'][1]['children'][-1]['children'][0]['text']
            team_index1 = int(team_n.index(team_1))
            if team_2 not in team_n:
                team_2 = cal_d['children'][idx0]['children'][idx1]['children'][1]['children'][idx3]['children'][0]['children'][1]['children'][-3]['children'][0]['text']
            team_index2 = int(team_n.index(team_2))
            date_l2[team_index1][date_index] = 1
            date_l2[team_index2][date_index] = 1


date_l3 = np.array(date_l2).T.tolist()
data_l4 = pd.DataFrame([date_l3])
data_l5 = pd.DataFrame(data_l4.iloc[0].tolist())
data_l5.columns = team_n
data_l5.index = date_l
print(data_l5)
data_l5.to_pickle("NBAfsce_Cal_01.pkl")