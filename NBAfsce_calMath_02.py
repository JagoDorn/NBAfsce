import numpy as np
import pandas as pd
from itertools import combinations
import matplotlib.pyplot as plt
import time

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Global variables
team_names = np.array(['Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers', 'LA Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies', 'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks', 'Oklahoma City Thunder', 'Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards'])
date_list = [['Week_01', '10/20/2026', '10/25/2026'], ['Week_02', '10/26/2026', '11/01/2026'], ['Week_03', '11/02/2026', '11/08/2026'], 
             ['Week_04', '11/09/2026', '11/15/2026'], ['Week_05', '11/16/2026', '11/22/2026'], ['Week_06', '11/23/2026', '11/29/2026'],
             ['Week_07', '11/30/2026', '12/05/2026'], ['Week_08', '12/07/2026', '12/13/2026'], ['Week_09', '12/14/2026', '12/20/2026'],
             ['Week_10', '12/21/2026', '12/27/2026'], ['Week_11', '12/28/2026', '01/03/2027'], ['Week_12', '01/04/2027', '01/10/2027'],
             ['Week_13', '01/11/2027', '01/17/2027'], ['Week_14', '01/18/2027', '01/24/2027'], ['Week_15', '01/25/2027', '01/31/2027'],
             ['Week_16', '02/01/2027', '02/07/2027'], ['Week_17', '02/08/2027', '02/14/2027'], ['Week_18', '02/15/2027', '02/18/2027'],
             ['Week_19', '02/25/2027', '02/28/2027'], ['Week_20', '03/01/2027', '03/07/2027'], ['Week_21', '03/08/2027', '03/14/2027'],
             ['Week_22', '03/15/2027', '03/21/2027'], ['Week_23', '03/22/2027', '03/28/2027'], ['Week_24', '03/29/2027', '04/04/2027'],
             ['Week_25', '04/05/2027', '04/11/2027']]
team_input_text = " Atlanta Hawks: 1\n	Boston Celtics: 2\n	Brooklyn Nets: 3\n	Charlotte Hornets: 4\n	Chicago Bulls: 5\n	Cleveland Cavaliers: 6\n	Dallas Mavericks: 7\n	Denver Nuggets: 8\n	Detroit Pistons: 9\n	Golden State Warriors: 10\n	Houston Rockets: 11\n	Indiana Pacers: 12\n	LA Clippers: 13\n	Los Angeles Lakers: 14\n	Memphis Grizzlies: 15\n	Miami Heat: 16\n	Milwaukee Bucks: 17\n	Minnesota Timberwolves: 18\n	New Orleans Pelicans: 19\n	New York Knicks: 20\n	Oklahoma City Thunder: 21\n	Orlando Magic: 22\n	Philadelphia 76ers: 23\n	Phoenix Suns: 24\n	Portland Trail Blazers: 25\n	Sacramento Kings: 26\n	San Antonio Spurs: 27\n	Toronto Raptors: 28\n	Utah Jazz: 29\n	Washington Wizards: 30\nInput 10 team numbers seperated by spaces:\n"
fppg_input_text = "Input FPPG in the same order as the teams seperated by spaces:\n"
calendar_full_pkl = "NBAfsce_Cal_01.pkl"
team_combo_full_npy = "NBAfsce_Cmb_Week_All.npy"

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Function: Creates array of number of non-overlapping games for every combination of 10 unique teams
def teamComboCreate():
    data_02 = pd.read_pickle(calendar_full_pkl)
    #print(data_02)
    data_df = data_02.to_numpy()

    ## Start timer for debugging
    time_s = time.perf_counter()

    ## Initialize 30!/((30-10!)*(10!)) unique combinations array
    data_03 = np.empty([30045015,11])
    out_idx=0
    ## Loop through each combination
    for cols in combinations(range(1,31),10):

        ## Sum team# column games to maximum of 5 for each date, store along with team#s
        data_02 = np.sum(data_df[:,cols], axis=1)
        data_03[out_idx][10] = sum(np.minimum(data_02,5))
        data_03[out_idx][0:10] = cols
        out_idx = out_idx+1

    print("Time after Loading Combos", round(time.perf_counter()-time_s, ndigits=1))
    print(data_03)
    data_Cmb = data_03.astype(np.uint16)
    np.save("NBAfsce_Cmb_Week_All.npy", data_Cmb)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Function: Prints stats and rankings of number of overlapped games for 10 input teams
def teamComboCheck():
    ## Load in full team combo games available, full schedule
    data_back = np.load(team_combo_full_npy)
    schedule_load = pd.read_pickle(calendar_full_pkl)

    ## Request terminal input 10 unique team numbers
    team_input_list = list(input(team_input_text).split())
    team_input_array = [int(x) for x in team_input_list]
    team_ordered = sorted(team_input_array)
    ## Return playable games value for input
    team_return = data_back[np.all(np.all(data_back[:,[range(10)]] == team_ordered, axis = 1), axis = 1),10]
    print("Playable games value:", np.squeeze(team_return))

    ## Reduce full schedule to input teams
    team_schedule_array = np.array(schedule_load.iloc[:,team_ordered])

    game_lap = np.zeros(10)
    for idx5 in range(10):
        ## For iteration team, sum amount of games input teams play on days iteration team plays above 5 games per day
        game_lap[idx5] = sum(np.maximum(np.squeeze(team_schedule_array[:,[idx5-1]])*np.sum(team_schedule_array,axis=1),5)-5)

    ## Sort teams by number of overlapped games
    team_ordered_np = np.array(team_ordered)
    game_lap_idx = np.argsort(game_lap)[::-1]
    game_lap_arr = np.array(game_lap_idx)

    ## Print teams by number of overlapped games
    print("Teams ranked by games overlapped:")
    for idx6 in range(10):    
        print("#", idx6+1, " ", team_names[team_ordered_np[game_lap_arr[idx6]]-1], ": ", np.squeeze(game_lap[game_lap_arr[idx6]]))

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Function: Print summary statistics for loaded schedule
def teamComboSumm():
    data_back = teamComboRecallTimeRange()

    ## Print summary statistics of loaded games available array
    print("Range:")
    print(np.max(data_back[:, 10])-np.min(data_back[:, 10]))
    print("Mean:")
    print(round(np.mean(data_back[:, 10]),1))
    print("SD:")
    print(round(np.std(data_back[:,10]),1))

    ## Create histogram of loaded games available array
    counts, bins = np.histogram(data_back[:,10],np.max(data_back[:, 10])-np.min(data_back[:, 10]))

    ## Print statistics and values for indicated z score
    print("Bins with Z Score >3:")
    print(bins[bins[:]>(np.mean(data_back[:, 10])+(3*np.std(data_back[:,10])))])
    print("Total Combinations with Z Score >3:")
    print(sum(counts[bins[:-1]>(np.mean(data_back[:, 10])+(3*np.std(data_back[:,10])))]))

    plt.hist(bins[:-1], bins, weights = counts)
    plt.title("Games Available Histogram")
    plt.show()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Function: Creates array of number of non-overlapping games for every combination of 10 unique teams for each week of season
def teamComboCreateTimeRange():
    data_in = pd.read_pickle(calendar_full_pkl)

    ## Check values of weeks for possible errors
    for idx1 in range(len(date_list)):
        date_01, date_02 = date_list[idx1][1], date_list[idx1][2]

        if not any(data_in.index == date_01) & any(data_in.index == date_02):
            raise ValueError("Invalid date")
        elif pd.to_datetime(date_01) > pd.to_datetime(date_02):
            date_01, date_02 = date_02, date_01
#           #raise ValueError("Invalid date order")
        
#        print(data_02.loc[date_01:date_02])

        ## Define time range to check games over
        data_timerange = data_in.loc[date_01:date_02]
        data_df = data_timerange.to_numpy()

        ## Start timer for debugging
        time_s = time.perf_counter()

        ## Initialize 30!/((30-10!)*(10!)) unique combinations array
        data_03 = np.empty([30045015,11])
        out_idx=0
        for cols in combinations(range(1,31),10):
            ## Sum team# column games to maximum of 5 for each date, store along with team#s
            data_02 = np.sum(data_df[:,cols], axis=1)
            data_03[out_idx][10] = sum(np.minimum(data_02,5))
            data_03[out_idx][0:10] = cols
            out_idx = out_idx+1

        print("Time after Loading Combo", round(time.perf_counter()-time_s, ndigits=1))

        ## Save data to file with unique week name
        data_03_toSave = data_03.astype(np.uint16)
        file_save_name = 'NBAfsce_Cmb_' + date_list[idx1][0] + '.npy'
        np.save(file_save_name, data_03_toSave)
        print("Saved ", file_save_name)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Function: Returns array for full team combinations of given week range
def teamComboRecallTimeRange():
    week = list()

    ## Request input weeks as integers
    week.append(input("Start Week: "))
    week.append(input("End Week: "))

    ## Error handling on input weeks
    for idx1 in range(2):
        if not week[idx1].isdigit():
            raise ValueError('Input not a number')
        elif not 0<int(week[idx1])<26:
            raise ValueError('Input not acceptable week')

    ## Initialize variables, create range of weeks
    week_range = list(range(int(week[0]),int(week[1])+1))
    team_combo_week_range = []

    ## Iterate through weeks, collecting team combinations on first iteration and number of games available on all iterations
    for idx2 in range(len(week_range)):
        if len(str(week_range[idx2])) == 1:
            week_range[idx2] = '0' + str(week_range[idx2])

#    week_range[0] = 'NBAfsce_Cmb_Week_' + str(week_range[idx3]) + '.npy'
#    team_combo_week_range.append(np.load(week_range[0]))
#    print('Loaded ', week_range[0])
        week_range[idx2] = 'NBAfsce_Cmb_Week_' + str(week_range[idx2]) + '.npy'
#        if team_combo_week_range == []:
        team_combo_week = np.load(week_range[idx2])
        if idx2 == 0:
            team_combo_week_teams = (team_combo_week[:,:-1])
        
        team_combo_week_range.append(team_combo_week[:,-1])
#        else team_combo_week_range
        #print(week_range[idx2])
        print('Loaded ', week_range[idx2])

    ## Return concatenated array with team combinations and sum of games available over time range
    team_combo_week_int = np.column_stack((team_combo_week_teams, np.sum(team_combo_week_range,axis=0)))
    return team_combo_week_int

#team_combo_test = teamComboRecallTimeRange()
#print(team_combo_test[0:10,:])

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Function: Return time range of valid dates based on user input
def ScheduleTimeRangeCreate():
    schedule_load = pd.read_pickle(calendar_full_pkl)

    ## User input dates
    date_01 = input("Start Date (MM/DD/YYYY): ")
    date_02 = input("End Date (MM/DD/YYYY): ")

    ## Error handling
    if not any(schedule_load.index == date_01) & any(schedule_load.index == date_02):
        raise ValueError("Invalid date")
    elif pd.to_datetime(date_01) > pd.to_datetime(date_02):
        date_01, date_02 = date_02, date_01 
        #raise ValueError("Invalid date order")

    ## Create and return date range
    schedule_load_timerange = schedule_load.loc[date_01:date_02]
    return(schedule_load_timerange)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Function: Prints rankings of team inputs over input range by number of games overlapped
def teamComboCheckTimeRange():
    ## Call function to generate team combos based on weeks input
    data_back = np.load(team_combo_full_npy)#teamComboRecallTimeRange()
    ## Request time range input, call date range creator function
    schedule_load_timerange = ScheduleTimeRangeCreate(calendar_full_pkl)

    ## Request 10 unique team input
    team_input_list = list(input(team_input_text).split())
    team_input_array = [int(x) for x in team_input_list]
    team_ordered = sorted(team_input_array)

    ## Find and print teams names from team input
    team_return = data_back[np.all(np.all(data_back[:,[range(10)]] == team_ordered, axis = 1), axis = 1),10]
    print("Playable games value:", np.squeeze(team_return))

    ## Reduce schedule to input teams
    team_schedule_array = np.array(schedule_load_timerange.iloc[:,team_ordered])

    game_lap = np.zeros(10)
    for idx5 in range(10):
        ## For iteration team, sum amount of games input teams play on days iteration team plays above 5 games per day
        game_lap[idx5] = sum(np.maximum(np.squeeze(team_schedule_array[:,[idx5-1]])*np.sum(team_schedule_array,axis=1),5)-5)

    ## Sort and print team input by games overlapped
    team_ordered_np = np.array(team_ordered)
    game_lap_idx = np.argsort(game_lap)[::-1]
    game_lap_arr = np.array(game_lap_idx)
    print("Teams ranked by games overlapped:")
    for idx6 in range(10):    
        print("#", idx6+1, " ", team_names[team_ordered_np[game_lap_arr[idx6]]-1], ": ", np.squeeze(game_lap[game_lap_arr[idx6]]))

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Function: 
def teamComboRankTimeRange():
    ## Request z score user input
    z_score = int(input("Z score to test:\n"))

    ## Call function to generate team combos based on weeks input
    data_back = teamComboRecallTimeRange()

    ## Iterate through list to search for values more than z score*standard deviation above mean
    data_z = np.mean(data_back[:, 10])+(int(z_score)*np.std(data_back[:,10]))
    data_z_list = []
    for idx4 in range(len(data_back)):
        if data_back[idx4,10] >= data_z:
            data_z_list.append(data_back[idx4,:])

    ## If no values were found, raise error
    data_z_arr = np.squeeze(np.array([data_z_list]))
    if len(data_z_list) == 0:
        raise ValueError("No values meet z score given")

    ## If list is exceptionally long, request permission to proceed
    if len(data_z_list) > 10000:
        user_response = input(f"There are {len(data_z_list)} values that exceed the given z score, do you want to proceed? (y/n)").strip().lower()
        if str(user_response) == 'n':
            raise ValueError("Stopped computation")
        elif str(user_response) != 'y':
            raise ValueError("Response was not y or n")

    ## Sort found values
    data_z_arr_sort = data_z_arr[np.squeeze(np.argsort(data_z_arr[:,-1]))]

    ## Create dataframes from arrays
    data_z_pd_sort = pd.DataFrame(data_z_arr_sort,dtype=str)
    data_z_pd_sort_names = pd.DataFrame(np.zeros(list(data_z_pd_sort.shape),dtype = list))

    ## Translate team numbers to team names
    for j in range(data_z_pd_sort.shape[0]):
        for i in range(data_z_pd_sort.shape[1]-1):
            data_z_pd_sort_names.iloc[j, i] = team_names[int(data_z_pd_sort.iloc[j, i])-1]
            data_z_pd_sort_names.iloc[j, 10] = data_z_pd_sort.iloc[j, 10]            

    print(data_z_pd_sort_names.iloc[-30:,:])

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Function: Prints rankings of team inputs over input range by number of fantasy points unavailable
def teamComboCheckTimeFPPG():
    ## Call function to generate team combos based on weeks input
    data_back = np.load(team_combo_full_npy)#teamComboRecallTimeRange()
    ## Request time range input, call date range creator function
    schedule_load_timerange = ScheduleTimeRangeCreate()

    ## Request 10 unique team input
    team_input_list = list(input(team_input_text).split())
    team_input_array = [int(x) for x in team_input_list]

    ## Request fppg for each team input
    fppg_input_list = list(input(fppg_input_text).split())
    fppg_input_array = [float(x) for x in fppg_input_list]

    input_array_concat = np.array([team_input_array, fppg_input_array])
    #8 9 10 13 16 2 14 17 21 26
    #3.0 28.0 7.5 6.5 18.5 5.0 21.0 12.5 5.4 8.0
    print(input_array_concat)

    team_ordered = input_array_concat[:, np.argsort(input_array_concat[0,:])]#sorted(team_input_array)
    
    ## Find and print teams names from team input
    team_return = data_back[np.all(np.all(data_back[:,[range(10)]] == team_ordered[0,:], axis = 1), axis = 1),10]
    print("Playable games value:", np.squeeze(team_return))

    ## Reduce schedule to input teams
    team_schedule_array = np.array(schedule_load_timerange.iloc[:,team_ordered[0,:]])


    ## MUST CHANGE: 
    game_lap = np.zeros(10)
    for idx5 in range(10):
        ## For iteration team, sum amount of games input teams play on days iteration team plays above 5 games
        game_lap[idx5] = sum(np.maximum(np.squeeze(team_schedule_array[:,[idx5-1]])*np.sum(team_schedule_array,axis=1),5)-5)

    ## Sort and print team input by games overlapped
    team_ordered_np = np.array(team_ordered[0,:])
    game_lap_idx = np.argsort(game_lap)[::-1]
    game_lap_arr = np.array(game_lap_idx)
    print("Teams ranked by games overlapped:")
    for idx6 in range(10):    
        print("#", idx6+1, " ", team_names[team_ordered_np[game_lap_arr[idx6]]-1], ": ", np.squeeze(game_lap[game_lap_arr[idx6]]))

teamComboCheckTimeFPPG()