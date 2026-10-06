import json
from datetime import date, timedelta, datetime
import numpy as np
import os
import pandas as pd
import pickle
import matplotlib as plt

data = pd.read_pickle("NBAfsce_Cal_01.pkl")
#print(data.iloc[:,2])

#print(str(data.columns[1]+' '+data.columns[2]))
#print(sum(data["Total Games"]))
#print(sum(data.values[1]))
game_dif = pd.DataFrame(0,index=range(435),columns=['Name 1', 'Name 2', 'Difference'])#[435,2])np.zeros([435,2])
game_dif = game_dif.astype({'Name 1':str,'Name 2':str, 'Difference':int})
#print(game_dif)

idx1=0
#print(game_dif['Name'][idx1])
for i in range(1,31):
    for j in range (i+1,31):
        #print(data.columns[i],data.columns[j])
        game_dif.loc[idx1, 'Difference'] = sum(abs(data.iloc[:,i]-data.iloc[:,j]))
        game_dif.loc[idx1, 'Name 1'] = str(data.columns[i])
        game_dif.loc[idx1, 'Name 2'] = str(data.columns[j])
        idx1=idx1+1

game_dif3 = np.zeros(30)
team_n = np.zeros(30,dtype=list)
for i in range(1,31):
    game_dif2 = game_dif.loc[(game_dif["Name 1"].isin([data.columns[i]]) | game_dif["Name 2"].isin([data.columns[i]])),"Difference"].tolist()
    game_dif3[i-1] = round(sum(game_dif2)/29, ndigits=1)
    team_n[i-1] = data.columns[i]


#print(team_n)
game_dif4 = pd.DataFrame(zip(team_n, game_dif3), columns = ["Names", "Uniqueness"])
print(game_dif4.sort_values("Uniqueness", ascending=False))

#plt(game_dif['Difference'].values)
#game_dif_sort = game_dif.sort_values("Difference", ascending=False)
#print(game_dif_sort.head(10))
#print(game_dif["Difference"].nlargest(10))