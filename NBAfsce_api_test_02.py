import requests
import time
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

team_names = np.array(['Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers', 'LA Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies', 'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks', 'Oklahoma City Thunder', 'Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards'])

def get_stats(url):
    print("Requesting from site")

    stat_reply = requests.get(url, timeout=15)
    time.sleep(30)

    # Check for HTTP errors
    stat_reply.raise_for_status()

    # Convert JSON response to a Python dictionary
    stat_page = stat_reply.json()

    with open("NBAfsce_espn_01.json", "w", encoding="utf-8") as f:
        json.dump(stat_page, f, indent=2)

    print("Saved site response to file")

    #print(data.keys())

#stat_url = "https://site.web.api.espn.com/apis/common/v3/sports/basketball/nba/statistics/byteam"
#get_stats(stat_url)

with open("NBAfsce_espn_01.json", "r", encoding="utf-8") as f:
    page_data = json.load(f)

#print(page_data.keys())

stat_arr = np.zeros([30,43,2], dtype=float)
stat_arr_col_name = np.zeros(43, dtype=list)
stat_arr_row_name = np.zeros(30,dtype=list)

for cat_idx in range(43):
    for vs_idx in range(2):
        if vs_idx == 0:
            if cat_idx < 10:
                stat_arr_col_name[cat_idx] = page_data['categories'][0]['displayNames'][cat_idx]
#                stat_arr[team_idx,cat_idx,vs_idx] = page_data['teams'][team_idx]['categories'][0+vs_idx]['totals'][cat_idx]
            elif cat_idx < 16:
                stat_arr_col_name[cat_idx] = page_data['categories'][2]['displayNames'][cat_idx-10]
#                stat_arr[team_idx,cat_idx,vs_idx] = page_data['teams'][team_idx]['categories'][2+vs_idx]['totals'][cat_idx-10]
            elif cat_idx < 43:
                stat_arr_col_name[cat_idx] = page_data['categories'][4]['displayNames'][cat_idx-16]
#                stat_arr[team_idx,cat_idx,vs_idx] = page_data['teams'][team_idx]['categories'][4+vs_idx]['totals'][cat_idx-16]
            
            
#            print(page_data['teams'][team_idx]['categories'][cat_idx]['values'])

        for team_idx in range(30):

            if cat_idx == 0 & vs_idx == 0:
                stat_arr_row_name[team_idx] = page_data['teams'][team_idx]['team']['displayName']
#                print(page_data['teams'][team_idx]['team']['displayName'])#,'name','id'])
#        if 'displayNames' in page_data['categories'][cat_idx]:
#            print('\n', page_data['categories'][cat_idx]['name'])
#            print(page_data['categories'][cat_idx]['displayNames'])
            
#        print(page_data['teams'][team_idx]['categories'][cat_idx]['displayName'])
#        print(page_data['teams'][team_idx]['categories'][cat_idx]['values'])
            if cat_idx < 10:
                stat_arr[team_idx,cat_idx,vs_idx] = page_data['teams'][team_idx]['categories'][0+vs_idx]['values'][cat_idx]
            elif cat_idx < 16:
                stat_arr[team_idx,cat_idx,vs_idx] = page_data['teams'][team_idx]['categories'][2+vs_idx]['values'][cat_idx-10]
            elif cat_idx < 43:
                stat_arr[team_idx,cat_idx,vs_idx] = page_data['teams'][team_idx]['categories'][4+vs_idx]['values'][cat_idx-16]
#            stat_arr[team_idx,cat_idx] = len(page_data['teams'][team_idx]['categories'][cat_idx]['totals'])

#print(team_names)
#print(stat_arr_row_name)

stat_arr_row_idx = np.array(np.squeeze([np.where(team_names == x) for x in stat_arr_row_name]),dtype=int)
#print(stat_arr_row_idx)
#team_names[stat_arr_row_name]

#stat_df = [pd.DataFrame(data = stat_arr[:,:,idx1], columns = stat_arr_col_name, index = stat_arr_row_name) for idx1 in range(2)]
#print([stat_df[idx2].index.tolist() for idx2 in range(2)])
#print(stat_df[0].columns.tolist())
#print([stat_df[idx3]['Rebounds Per Game'] for idx3 in range(2)])
#col_rebound = [i for i, col in enumerate(stat_df[0].columns) if col == "Rebounds"]

stat_df_own_dup = pd.DataFrame(data = stat_arr[:,:,0], columns = stat_arr_col_name, index = stat_arr_row_name)
stat_df_own = stat_df_own_dup.loc[:, ~stat_df_own_dup.columns.duplicated()]
stat_df_own.columns = "Own " + stat_df_own.columns
stat_df_opp_dup = pd.DataFrame(data = stat_arr[:,:,1], columns = stat_arr_col_name, index = stat_arr_row_name)
stat_df_opp = stat_df_opp_dup.loc[:, ~stat_df_opp_dup.columns.duplicated()]
stat_df_opp.columns = "Opp " + stat_df_opp.columns
stat_df = pd.concat([stat_df_own, stat_df_opp], axis=1)
#print(stat_df.columns.tolist)

#plt.figure(0)
#plt.scatter(stat_df[0]['Defensive Rebounds'], stat_df[1]['Offensive Rebounds'])

plt.rcParams.update({
    "axes.titlesize": 9,
    "axes.labelsize": 8,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7
})

fig, axes = plt.subplots(5,8, figsize=(15, 8), layout="constrained")
ax_0 = 0
ax_1 = 0
#print(range(int(stat_df.size/30/2)))
for idx3 in range(int(stat_df.size/30/2)):
#   print(stat_df.columns[idx+39])    
    sns.regplot(x = stat_df.columns[idx3], y = stat_df.columns[idx3+39], data = stat_df, ax=axes[ax_0, ax_1])

    if np.mod(idx3, 8) == 7:
        ax_0 = ax_0 + 1
        ax_1 = 0
    else:
        ax_1 = ax_1 + 1


manager = plt.get_current_fig_manager()
manager.window.showMaximized()
plt.tight_layout()
plt.show()

#stat_df_uniq = stat_df.loc[:, ~stat_df.columns.duplicated()]

#print(stat_arr[0,:,0])
#print(stat_arr_col_name)
#print(page_data['categories'][0])#['displayName'][cat_idx])

#        if team_idx == 29:
#            print('\n', stat_arr[team_idx,cat_idx])

#print(len(page_data['categories']))

#for idx0 in range(7):