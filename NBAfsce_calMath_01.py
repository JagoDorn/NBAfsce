import json
from datetime import date, timedelta, datetime
import numpy as np
import pandas as pd
import pickle
import matplotlib as plt
import time

#time_s = time.perf_counter()

data_01 = pd.read_pickle("NBAfsce_Cal_01.pkl")
#print(data.iloc[:,2])

#print("Time after Loading Teams", round(time.perf_counter()-time_s, ndigits=3))

def getUniqueness(data_df):
    game_dif = pd.DataFrame(0,index=range(435),columns=['Name 1', 'Name 2', 'Difference'])#[435,2])np.zeros([435,2])
    game_dif = game_dif.astype({'Name 1':str,'Name 2':str, 'Difference':int})

    idx1=0
    #print(game_dif['Name'][idx1])
    for i in range(1,31):
        for j in range (i+1,31):
            #print(data_df.columns[i],data_df.columns[j])
            game_dif.loc[idx1, 'Difference'] = sum(abs(data_df.iloc[:,i]-data_df.iloc[:,j]))
            game_dif.loc[idx1, 'Name 1'] = str(data_df.columns[i])
            game_dif.loc[idx1, 'Name 2'] = str(data_df.columns[j])
            idx1=idx1+1

    #print(game_dif)
    game_dif3 = np.zeros(30)
    team_n = np.zeros(30,dtype=list)
    for i in range(1,31):
        game_dif2 = game_dif.loc[(game_dif["Name 1"].isin([data_df.columns[i]]) | game_dif["Name 2"].isin([data_df.columns[i]])),"Difference"].tolist()
        game_dif3[i-1] = round(sum(game_dif2)/29, ndigits=1)
        team_n[i-1] = data_df.columns[i]
    #print(team_n)
    game_dif4 = pd.DataFrame(zip(team_n, game_dif3), columns = ["Names", "Uniqueness"])
    #print(game_dif4.sort_values("Uniqueness", ascending=False))

    return game_dif4.sort_values("Uniqueness", ascending=False)

#print(getUniqueness(data_01))


#print(80-sum(data_01.iloc[:,1]&data_01.iloc[:,2]))#&data_01.iloc[:,3])

def getBetterUniqueness(data_df):

    game_empty = np.zeros([30,30],dtype=int)
    for i in range(1, 31):
        for j in range(i+1, 31):
            game_empty[i-1][j-1] = 80-sum(data_01.iloc[:,i]&data_01.iloc[:,j])

    game_percent = np.round(100*game_empty/80,1)
    
    return game_percent

#print(getBetterUniqueness(data_01))

print(data_01[["Miami Heat", "LA Clippers", "Golden State Warriors", "Philadelphia 76ers", "New York Knicks", "Los Angeles Lakers", "Milwaukee Bucks", "Portland Trail Blazers", "Boston Celtics", "Oklahoma City Thunder"]].to_string())