#import json
#from datetime import date, timedelta, datetime
import numpy as np
import pandas as pd
import pickle
from itertools import combinations
import matplotlib.pyplot as plt
import time

#-----------------------------------------------------------------------------------------

def teamComboCreate(pkl_name):

    data_02 = pd.read_pickle(pkl_name)
    #print(data_02)
    data_df = data_02.to_numpy()
    
    time_s = time.perf_counter()

    data_03 = np.empty([30045015,11])
    out_idx=0
    for cols in combinations(range(1,31),10):
        
        data_02 = np.sum(data_df[:,cols], axis=1)
        data_03[out_idx][10] = sum(np.minimum(data_02,5))
        data_03[out_idx][0:10] = cols
        out_idx = out_idx+1

    print("Time after Loading Combos", round(time.perf_counter()-time_s, ndigits=1))
    print(data_03)
    return data_03

#pkl_Cal_01 = "NBAfsce_Cal_01.pkl"
#data_combo = teamComboCreate(pkl_Cal_01)
#data_Cmb = data_combo.astype(np.uint16)
#np.save("NBAfsce_Cmb_01.npy", data_Cmb)

#print(data_combo)

#-----------------------------------------------------------------------------------------

def teamComboRank(Filename):
    data_back = np.load(Filename)

    #print(data_back)

    idx_sort = np.argsort(data_back[:, -1])[::-1]
    #print(data_back[idx_sort])
    data_sort_top = data_back[idx_sort[0:50]]
    #print(data_sort_top)

    data_sort_top_names = pd.DataFrame(data_sort_top,dtype=str)

    name_list = data_02.columns.tolist()
    #print(name_list[data_sort_top[1,1]])
    for j in range(len(data_sort_top)):
        for i in range(len(data_sort_top[0])-1):
            #print(name_list[data_sort_top[j, i]])
            data_sort_top_names.iloc[j, i] = name_list[data_sort_top[j, i]]
            #print(data_sort_top_names[j, i])
    #        #name_list[i]

    #print(data_sort_top_names)
    return data_sort_top_names

#npy_Cmb_01 = "NBAfsce_Cmb_01.npy"
#teamComboRank(npy_Cmb_01).to_pickle("NBAfsce_Cmb_02.pkl")
#data_combo_rank = pd.read_pickle("NBAfsce_Cmb_02.pkl")

#print(data_combo_rank.iloc[[0,1,2]])

#-----------------------------------------------------------------------------------------

def teamComboCheck(file_name, pickle_name):
    data_back = np.load(file_name)
    schedule_load = pd.read_pickle(pickle_name)

#    team_input_list = list(input("	Atlanta Hawks: 1\n	Boston Celtics: 2\n	Brooklyn Nets: 3\n	Charlotte Hornets: 4\n	Chicago Bulls: 5\n	Cleveland Cavaliers: 6\n	Dallas Mavericks: 7\n	Denver Nuggets: 8\n	Detroit Pistons: 9\n	Golden State Warriors: 10\n	Houston Rockets: 11\n	Indiana Pacers: 12\n	LA Clippers: 13\n	Los Angeles Lakers: 14\n	Memphis Grizzlies: 15\n	Miami Heat: 16\n	Milwaukee Bucks: 17\n	Minnesota Timberwolves: 18\n	New Orleans Pelicans: 19\n	New York Knicks: 20\n	Oklahoma City Thunder: 21\n	Orlando Magic: 22\n	Philadelphia 76ers: 23\n	Phoenix Suns: 24\n	Portland Trail Blazers: 25\n	Sacramento Kings: 26\n	San Antonio Spurs: 27\n	Toronto Raptors: 28\n	Utah Jazz: 29\n	Washington Wizards: 30\nInput 10 team numbers seperated by spaces:\n").split())
#    team_input_array = [int(x) for x in team_input_list]
#    team_ordered = sorted(team_input_array)
#    print(team_ordered)
#    team_return = data_back[np.all(np.all(data_back[:,[range(10)]] == team_ordered, axis = 1), axis = 1),10]
#    print("Playable games value:", team_return)
#    print(data_back[:,[range(10)]])
    print(schedule_load)

    
teamComboCheck("NBAfsce_Cmb_01.npy", "NBAfsce_Cal_01.pkl")

#-----------------------------------------------------------------------------------------

def teamComboSumm(Filename):
    data_back = np.load(Filename)
        
    print("Range:")
    print(np.max(data_back[:, 10])-np.min(data_back[:, 10]))
    print("Mean:")
    print(round(np.mean(data_back[:, 10]),1))
    print("SD:")
    print(round(np.std(data_back[:,10]),1))

    counts, bins = np.histogram(data_back[:,10],83)

    plt.hist(bins[:-1], bins, weights = counts)
    plt.show()

#    data_sort_stats = pd.DataFrame(data_back,dtype=str)

#    print(data_sort_stats)
#    return data_sort_stats

#teamComboSumm("NBAfsce_Cmb_01.npy")

