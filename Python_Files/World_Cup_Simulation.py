from Host import host_selector
from AFC import afc_f
from CAF import caf_f
from CONCACAF import concacaf_f
from CONMEBOL import conmebol_f
from OFC import ofc_f
from UEFA import uefa_f
from Round_Simulation import TLKO_simulation, TLKO_simulation_wc_16, TLKO_simulation_wc_late, WorldCupGroupStage
from Group_Draws import GD4, WorldCupDraw

import pandas as pd
import time

# Pre-World Cup data-sets, settings and the Inter-Continental Playoff

# Lists for use in code
alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
group_names = ["Group A", "Group B", "Group C", "Group D", "Group E", "Group F", "Group G", "Group H"]

# Ensuring pandas displays the whole data frame
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Importing data collecting datasets
complete_player_data = pd.read_csv("Empty_Player_Data.csv")
complete_nation_data = pd.read_csv("Empty_Nation_Data.csv")

# complete_nation_data = complete_nation_data.set_index("Country")

# Welcome to the world cup
print("\nWelcome to the Python World Cup, produced by Samwcounsell & Githubkeano\n")
print("This programme uses a binomial simulation to predict the outcome of the World Cup Qualifiers and Tournament")
print("Every nations ratings and squads are our choices, so expect some weird outcomes, we don't know as much as we "
      "wish we did...")
print("\nWe recommend setting the time delay to 0 for the Qualifiers, if you set it to 0.1, it will take roughly 3 "
      "hours!")
print("For your second run through feel free to answer Y to is this a test, you will no be stopped after each round "
      "of Qualification")
print("\nWe hope you enjoy a relatively realistic run through of the 2022 World Cup\n")

runs = input("Number of runs: \n")
runs = int(runs)

for i in range(runs):

    complete_nation_data = complete_nation_data.set_index("Country")

    if runs != 1:
        time_delay = 0
        test = "Y"

    if runs == 1:
        test = input("Would you like a quick run through (only stops at end of each confederation)? Y/N: ")

    # Customise your time delay (each time unit is one minute within a game)
    if runs == 1:
        if test != "Y":
            td = input("\nChoose your time delay for the Qualifiers (0 recommended): ")
            time_delay = float(td)
        else:
            time_delay = 0

    # Reading in the player and nation data, this is where data is also recorded
    player_data = pd.read_csv("player_data.csv")
    player_data = player_data.set_index('Name')

    nation_data = pd.read_csv("nation_data.csv")
    nation_data = nation_data.set_index('Country')

    awards_data = pd.read_csv("awards.csv")
    awards_data = awards_data.set_index('Award')

    # Randomising the host of the World Cup
    host, host_df = host_selector()

    print("\nThe 2022 World Cup will be hosted by", host)

    if runs == 1:
        input("\nPress enter to continue to the World Cup Qualifiers: ")

    # Running all the World Cup Qualifiers from their respective functions
    player_data, nation_data, afc, ict1, awards_data = afc_f(time_delay, player_data, nation_data, awards_data, test, runs, host)
    player_data, nation_data, caf, awards_data = caf_f(time_delay, player_data, nation_data, awards_data, test, runs, host)
    player_data, nation_data, concacaf, ict2, awards_data = concacaf_f(time_delay, player_data, nation_data, awards_data,
                                                                     test, runs, host)
    player_data, nation_data, conmebol, ict3, awards_data = conmebol_f(time_delay, player_data, nation_data, awards_data, runs, host)
    player_data, nation_data, ict4, awards_data = ofc_f(time_delay, player_data, nation_data, awards_data, test, runs)
    player_data, nation_data, uefa, awards_data = uefa_f(time_delay, player_data, nation_data, awards_data, test, runs, host)

    # Joining all the qualified teams
    teams = pd.concat([host_df, afc, caf, concacaf, conmebol, uefa])
    print(teams)

    # Joining all the teams for the intercontinental playoffs
    ict = pd.concat([ict1, ict2, ict3, ict4])
    ict = ict.reset_index()
    ict = ict.drop(['index'], axis=1)

    # Customise your time delay (each time unit is one minute within a game)
    if runs == 1:
        while True:
            td = input("\nChoose your time delay for the Inter-Continental Playoff (0 - 0.1 recommended): ")
            try:
                val = float(td)
                time_delay = float(td)
                break
            except ValueError:
                print("\nAren't you cheeky, please enter a number...")
                continue

    print("\nThe Inter-continental Playoff")

    # Displaying the Inter-continental Playoff fixtures
    for a in range(2):
        team1, team2 = ict.loc[2 * a, 'Country'], ict.loc[2 * a + 1, 'Country']
        print("\nIntercontinental Playoff Match", a + 1, ":", team1, "v", team2)

    if runs == 1:
        input("\nPress enter to continue to Match Day: \n")

    # Running the intercontinental playoff
    player_data, nation_data, ict = TLKO_simulation(2, time_delay, player_data, nation_data, ict, ict)
    ict = ict.iloc[4:6]

    # Joining and displaying the 32 World Cup teams
    teams = pd.concat([teams, ict])
    teams = teams.sort_values(by='World_Rank')
    teams = teams.reset_index()
    teams = teams.drop(['index'], axis=1)

    print("The 32 World Cup Nations\n")
    print(teams.to_string(columns=['Country', 'World_Rank'], index=False), "\n")

    # Resetting the data for the group stages
    world_cup_teams = teams
    world_cup_teams[['P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']] = 0

    # Adding data
    wct = world_cup_teams['Country'].to_numpy()
    l = len(wct)
    for i in range(l):
        complete_nation_data.loc[wct[i], "World_Cup_Apps"] = complete_nation_data.loc[wct[i], "World_Cup_Apps"] + 1

    # Customise your time delay (each time unit is one minute within a game)
    if runs == 1:
        while True:
            td = input("\nChoose your time delay for the Group Stages (0 - 0.1 recommended): ")
            try:
                val = float(td)
                time_delay = float(td)
                break
            except ValueError:
                print("\nAren't you cheeky, please enter a number...")
                continue

    # The World Cup

    # Randomising the 4 seeded pots
    pot1 = world_cup_teams.iloc[:8, :]
    pot2 = world_cup_teams.iloc[8:16, :]
    pot3 = world_cup_teams.iloc[16:24, :]
    pot4 = world_cup_teams.iloc[24:32, :]
    pot1 = pot1.sample(frac=1)
    pot2 = pot2.sample(frac=1)
    pot3 = pot3.sample(frac=1)
    pot4 = pot4.sample(frac=1)

    world_cup_teams = pd.concat([pot1, pot2, pot3, pot4])

    # New Group Draw
    print(world_cup_teams)
    group_names = WorldCupDraw(world_cup_teams)
    for i in range(8):
        print("\nGroup", alphabet[i])
        print("\n",
              group_names[i].to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False),
              "\n")

    # Running the group stage
    player_data, nation_data, group_names = WorldCupGroupStage(time_delay, player_data, nation_data, group_names, runs)

    # Displaying the final group standings
    for i in range(8):
        print("\n",
              group_names[i].to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False),
              "\n")

    # Collating the 16 teams qualified for the next round, then displaying them
    for i in range(8):
        qualified = group_names[i].iloc[0:2, :]
        world_cup_teams = pd.concat([world_cup_teams, qualified])

    round_of_16 = world_cup_teams.iloc[32:48, :]

    # Adding data
    ro16t = round_of_16['Country'].to_numpy()
    l = len(ro16t)
    for i in range(l):
        complete_nation_data.loc[ro16t[i], "RO16_Apps"] = complete_nation_data.loc[ro16t[i], "RO16_Apps"] + 1

    print("\nQUALIFIED FOR THE ROUND OF 16")
    print("\n", round_of_16.to_string(columns=['Country', 'World_Rank'], index=False))

    if runs == 1:
        input("\nEnd of the World Cup Group Stage, press enter to continue to the Round of 16: ")

    # Customise your time delay (each time unit is one minute within a game)
    if runs == 1:
        while True:
            td = input("\nChoose your time delay for the Round of 16 (0.1 recommended): ")
            try:
                val = float(td)
                time_delay = float(td)
                break
            except ValueError:
                print("\nAren't you cheeky, please enter a number...")
                continue

    print("\nTHE ROUND OF 16", "\n")

    # Re-indexing the teams, ensuring the correct teams match up
    round_of_16 = round_of_16.reset_index()
    round_of_16 = round_of_16.drop(['index'], axis=1)

    # Printing the round of 16 fixtures
    for a in range(8):
        if (a % 2) == 0:
            x, y = 2 * a, 2 * a + 3
            team1, team2 = round_of_16.loc[x, 'Country'], round_of_16.loc[y, 'Country']
        if (a % 2) != 0:
            x, y = 2 * a - 1, 2 * a
            team1, team2 = round_of_16.loc[x, 'Country'], round_of_16.loc[y, 'Country']

        print("\nRound of 16 Match ", a + 1, ":", team1, "v", team2)

    if runs == 1:
        input("\nPress enter to continue to Match Day: \n")

    # Running the Round of 16
    player_data, nation_data, round_of_16 = TLKO_simulation_wc_16(8, time_delay, player_data, nation_data, round_of_16,
                                                                  round_of_16, runs)

    print("QUALIFIED FOR THE QUARTER-FINALS")

    # Collating the 8 teams qualified for the next round, then displaying them
    quarter_finalists = round_of_16.iloc[16:24]
    print("\n", quarter_finalists.to_string(columns=['Country', 'World_Rank'], index=False))

    # Adding data
    qft = quarter_finalists['Country'].to_numpy()
    l = len(qft)
    for i in range(l):
        complete_nation_data.loc[qft[i], "QF_Apps"] = complete_nation_data.loc[qft[i], "QF_Apps"] + 1

    # Customise your time delay (each time unit is one minute within a game)
    if runs == 1:
        while True:
            td = input("\nChoose your time delay for the Quarter-Finals (0.1 recommended): ")
            try:
                val = float(td)
                time_delay = float(td)
                break
            except ValueError:
                print("\nAren't you cheeky, please enter a number...")
                continue

    print("\nTHE QUARTER-FINALS")

    # Re-indexing the teams, ensuring the correct teams match up
    quarter_finalists = quarter_finalists.reset_index()
    quarter_finalists = quarter_finalists.drop(['index'], axis=1)

    # Printing out the Quarter-Final fixtures
    for a in range(4):
        if a == 0:
            x, y = 0, 2
        if a == 1:
            x, y = 1, 3
        if a == 2:
            x, y = 4, 6
        if a == 3:
            x, y = 5, 7
        team1, team2 = quarter_finalists.loc[x, 'Country'], quarter_finalists.loc[y, 'Country']

        print("\nQuarter-Final ", a + 1, ":", team1, "v", team2)

    if runs == 1:
        input("\nPress enter to continue to Match Day: \n")

    # Running the Quarter-Finals
    player_data, nation_data, quarter_finalists = TLKO_simulation_wc_late(4, time_delay, player_data, nation_data,
                                                                          quarter_finalists, quarter_finalists, runs)

    print("QUALIFIED FOR THE SEMI-FINALS")

    # Collating the 4 teams qualified for the next round, then displaying them
    semi_finalists = quarter_finalists.iloc[8:12]
    print("\n", semi_finalists.to_string(columns=['Country', 'World_Rank'], index=False))

    sft = semi_finalists['Country'].to_numpy()
    l = len(sft)
    for i in range(l):
        complete_nation_data.loc[sft[i], "SF_Apps"] = complete_nation_data.loc[sft[i], "SF_Apps"] + 1

    # Customise your time delay (each time unit is one minute within a game)
    if runs == 1:
        while True:
            td = input("\nChoose your time delay for the Semi_Finals (0.1 recommended): ")
            try:
                val = float(td)
                time_delay = float(td)
                break
            except ValueError:
                print("\nAren't you cheeky, please enter a number...")
                continue

    print("\nTHE SEMI-FINALS")

    # Re-indexing the teams, ensuring the correct teams match up
    semi_finalists = semi_finalists.reset_index()
    semi_finalists = semi_finalists.drop(['index'], axis=1)

    # Displaying the Semi-Final fixtures
    for a in range(2):
        x, y = a, a + 2
        team1, team2 = semi_finalists.loc[x, 'Country'], semi_finalists.loc[y, 'Country']
        print("\nSemi-Final ", a + 1, ":", team1, "v", team2)

    if runs == 1:
        input("\nPress enter to continue to Match Day: ")

    # Running the Semi-Finals
    player_data, nation_data, semi_finalists = TLKO_simulation_wc_late(2, time_delay, player_data, nation_data,
                                                                       semi_finalists, semi_finalists, runs)

    print("\nQUALIFIED FOR THE FINAL")

    # Collating the 2 teams qualified for the next round, then displaying them
    finalists = semi_finalists.iloc[4:6]
    print("\n", finalists.to_string(columns=['Country', 'World_Rank'], index=False))

    ft = finalists['Country'].to_numpy()
    l = len(ft)
    for i in range(l):
        complete_nation_data.loc[ft[i], "Finals_Apps"] = complete_nation_data.loc[ft[i], "Finals_Apps"] + 1

    # Customise your time delay (each time unit is one minute within a game)
    if runs == 1:
        while True:
            td = input("\nChoose your time delay for the Final (0.2 recommended): ")
            try:
                val = float(td)
                time_delay = float(td)
                break
            except ValueError:
                print("\nAren't you cheeky, please enter a number...")
                continue

    print("\nTHE WORLD CUP FINAL", "\n")

    # Re-indexing the teams, ensuring the correct teams match up
    finalists = finalists.reset_index()
    finalists = finalists.drop(['index'], axis=1)

    # Add printing the final

    if runs == 1:
        input("Press enter to continue to Match Day, lets see the line ups for the World Cup Final: ")

    finalist1, finalist2 = finalists.loc[0, 'Country'], finalists.loc[1, 'Country']
    finalist_nations = [finalist1, finalist2]
    line_up1 = player_data[(player_data.Country == finalist1)]
    line_up2 = player_data[(player_data.Country == finalist2)]
    print("\n", line_up1.to_string(columns=['Position', 'ShirtNumber'], header=False), "\n\n",
          line_up2.to_string(columns=['Position', 'ShirtNumber'], header=False), "\n")
    time.sleep(time_delay * 5)

    # Running the Final
    player_data, nation_data, finalists = TLKO_simulation_wc_late(1, time_delay, player_data, nation_data, finalists,
                                                                  finalists, runs)

    # Displaying the winner of the World Cup
    champion = finalists.iloc[2:3]
    champion = champion.reset_index()
    champion = champion.loc[0, 'Country']
    print("The World Cup Winner is", champion)

    complete_nation_data.loc[champion, "World_Cup_Wins"] = complete_nation_data.loc[champion, "World_Cup_Wins"] + 11

    complete_nation_data['Total_P'] = complete_nation_data['Total_P'].add(nation_data['total_P'],
                                                                                                fill_value=0)
    complete_nation_data['Total_GF'] = complete_nation_data['Total_GF'].add(nation_data['total_GF'],
                                                                                                fill_value=0)
    complete_nation_data['Total_GA'] = complete_nation_data['Total_GA'].add(nation_data['total_GA'],
                                                                                                fill_value=0)
    complete_nation_data['Total_Clean_Sheets'] = complete_nation_data['Total_Clean_Sheets'].add(nation_data['total_CS'],
                                                                                                fill_value=0)

    complete_nation_data = complete_nation_data.reset_index()

    complete_nation_data['GF_PG'] = complete_nation_data['Total_GF'] / complete_nation_data['Total_P']
    complete_nation_data['GA_PG'] = complete_nation_data['Total_GA'] / complete_nation_data['Total_P']
    complete_nation_data['Clean_Sheet_%'] = complete_nation_data['Total_Clean_Sheets'] / complete_nation_data['Total_P']

    player_data = player_data.reset_index()
    nation_data = nation_data.reset_index()

    # Adding data to complete datasets
    complete_player_data['Total_P'] = complete_player_data['Total_P'].add(player_data['P'], fill_value=0)
    complete_player_data['Total_Goals'] = complete_player_data['Total_Goals'].add(player_data['Goals'], fill_value=0)
    complete_player_data['Total_Assists'] = complete_player_data['Total_Assists'].add(player_data['Assists'], fill_value=0)

    complete_player_data['Total_WC_P'] = complete_player_data['Total_WC_P'].add(player_data['WC_P'], fill_value=0)
    complete_player_data['Total_WC_Goals'] = complete_player_data['Total_WC_Goals'].add(player_data['WC_Goals'], fill_value=0)
    complete_player_data['Total_WC_Assists'] = complete_player_data['Total_WC_Assists'].add(player_data['WC_Assists'],
                                                                                      fill_value=0)

    complete_player_data['G_PG'] = complete_player_data['Total_Goals'] / complete_player_data['Total_P']
    complete_player_data['A_PG'] = complete_player_data['Total_Assists'] / complete_player_data['Total_P']
    complete_player_data['WC_G_PG'] = complete_player_data['Total_WC_Goals'] / complete_player_data['Total_WC_P']
    complete_player_data['WC_A_PG'] = complete_player_data['Total_WC_Assists'] / complete_player_data['Total_WC_P']

    # The Awards

    # Ordering data frame for the Golden Boot winner
    player_data = player_data.sort_values(by=['WC_Goals', 'WC_Assists'], ascending=False)
    player_data = player_data.reset_index()
    # Isolating the Golden Boot winner
    Golden_Boot = player_data.loc[0, 'Name']
    player_data = player_data.set_index('Name')
    GBN = player_data.loc[Golden_Boot, 'WC_Goals']

    # Ordering data frame for the Golden Playmaker winner
    player_data = player_data.sort_values(by=['WC_Assists', 'WC_Goals'], ascending=False)
    player_data = player_data.reset_index()
    # Isolating the Golden Playmaker winner
    Golden_Playmaker = player_data.loc[0, 'Name']
    player_data = player_data.set_index('Name')
    GPN = player_data.loc[Golden_Playmaker, 'WC_Assists']

    # Displaying the Award Winners
    if runs == 1:
        input("\n\n\nPress enter to continue the Awards: ")
    print("\nThe Golden Boot Winner is", Golden_Boot, "with", GBN, "Goals")
    print("\nThe Golden Playmaker Winner is", Golden_Playmaker, "with", GPN, "Assists")

    # Updating the Award Winners database
    WC_award_1 = Golden_Boot + " with " + str(GBN) + " Goals"
    WC_award_2 = Golden_Playmaker + " with " + str(GPN) + " Assists"
    awards_data.at['Golden Boot'] = WC_award_1
    awards_data.at['Golden Playmaker'] = WC_award_2

    # Post World Cup Text
    print("\n\n\nWe hope you enjoyed using the Python World Cup, feel free to run it again.")
    print("\nFeel free to send us any feature requests, or tell us about any issues you find on GitHub")



# Exporting data sets for the Dash App
player_data.to_csv('../DashApp/Player_Data_Set.csv')
nation_data.to_csv('../DashApp/Nation_Data_Set.csv')
awards_data.to_csv('../DashApp/Award_Data_Set.csv')

complete_nation_data.to_csv('../DashApp/CND_Data_Set.csv')
complete_player_data.to_csv('../DashApp/CPD_Data_Set.csv')
