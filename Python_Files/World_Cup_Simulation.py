from Host import host_selector
from AFC import afc
from CAF import caf
from CONCACAF import concacaf
from CONMEBOL import conmebol
from OFC import ofc
from UEFA import uefa
from Round_Simulation import TLKO_simulation, TLKO_simulation_wc_16, TLKO_simulation_wc_late, WorldCupGroupStage
from Group_Draws import GD4

import pandas as pd
import time

# Pre-World Cup data-sets, settings and the Inter-Continental Playoff

# Lists for use in code
alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
group_names = ["Group A", "Group B", "Group C", "Group D", "Group E", "Group F", "Group G", "Group H"]

# Ensuring pandas displays the whole data frame
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

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

# For developers
test = input("For Developers: Is this a test Y/N: ")

# Customise your time delay (each time unit is one minute within a game)
if test != "Y":
    td = input("\nChoose your time delay for the Qualifiers (0 - 0.1 recommended): ")
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

input("\nPress enter to continue to the World Cup Qualifiers: ")

# Running all the World Cup Qualifiers from their respective functions
player_data, nation_data, afc, ict1, awards_data = afc(time_delay, player_data, nation_data, awards_data, test)
player_data, nation_data, caf, awards_data = caf(time_delay, player_data, nation_data,awards_data, test)
player_data, nation_data, concacaf, ict2, awards_data = concacaf(time_delay, player_data, nation_data, awards_data, test)
player_data, nation_data, conmebol, ict3, awards_data = conmebol(time_delay, player_data, nation_data, awards_data)
player_data, nation_data, ict4, awards_data = ofc(time_delay, player_data, nation_data, awards_data, test)
player_data, nation_data, uefa, awards_data = uefa(time_delay, player_data, nation_data, awards_data, test)

# Joining all the qualified teams
teams = pd.concat([host_df, afc, caf, concacaf, conmebol, uefa])

# Joining all the teams for the intercontinental playoffs
ict = pd.concat([ict1, ict2, ict3, ict4])
ict = ict.reset_index()
ict = ict.drop(['index'], axis=1)

# Customise your time delay (each time unit is one minute within a game)
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
    print("\nIntercontinental Playoff Match ", a + 1, ":", team1, "v", team2)

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

# Customise your time delay (each time unit is one minute within a game)
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

# Drawing the groups, and displaying them
for i in range(8):
    group_names[i] = GD4(i, 8, world_cup_teams)
    print("\nGroup", alphabet[i])
    print("\n", group_names[i].to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False),
          "\n")

# Running the group stage
player_data, nation_data, group_names = WorldCupGroupStage(time_delay, player_data, nation_data, group_names)

# Displaying the final group standings
for i in range(8):
    print("\n", group_names[i].to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False),
          "\n")

# Collating the 16 teams qualified for the next round, then displaying them
for i in range(8):
    qualified = group_names[i].iloc[0:2, :]
    world_cup_teams = pd.concat([world_cup_teams, qualified])

round_of_16 = world_cup_teams.iloc[32:48, :]

print("\nQUALIFIED FOR THE ROUND OF 16")
print("\n", round_of_16.to_string(columns=['Country', 'World_Rank'], index=False))

input("\nEnd of the World Cup Group Stage, press enter to continue to the Round of 16: ")

# Customise your time delay (each time unit is one minute within a game)
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

input("\nPress enter to continue to Match Day: \n")

# Running the Round of 16
player_data, nation_data, round_of_16 = TLKO_simulation_wc_16(8, time_delay, player_data, nation_data, round_of_16,
                                                              round_of_16)

print("QUALIFIED FOR THE QUARTER-FINALS")

# Collating the 8 teams qualified for the next round, then displaying them
quarter_finalists = round_of_16.iloc[16:24]
print("\n", quarter_finalists.to_string(columns=['Country', 'World_Rank'], index=False))

# Customise your time delay (each time unit is one minute within a game)
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

print()
input("Press enter to continue to Match Day: \n")

# Running the Quarter-Finals
player_data, nation_data, quarter_finalists = TLKO_simulation_wc_late(4, time_delay, player_data, nation_data,
                                                                      quarter_finalists, quarter_finalists)

print("QUALIFIED FOR THE SEMI-FINALS")

# Collating the 4 teams qualified for the next round, then displaying them
semi_finalists = quarter_finalists.iloc[8:12]
print("\n", semi_finalists.to_string(columns=['Country', 'World_Rank'], index=False))

# Customise your time delay (each time unit is one minute within a game)
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

print()
input("Press enter to continue to Match Day: ")

# Running the Semi-Finals
player_data, nation_data, semi_finalists = TLKO_simulation_wc_late(2, time_delay, player_data, nation_data,
                                                                   semi_finalists, semi_finalists)

print("\nQUALIFIED FOR THE FINAL")

# Collating the 2 teams qualified for the next round, then displaying them
finalists = semi_finalists.iloc[4:6]
print("\n", finalists.to_string(columns=['Country', 'World_Rank'], index=False))

# Customise your time delay (each time unit is one minute within a game)
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

input("Press enter to continue to Match Day: ")

finalist1, finalist2 = finalists.loc[0, 'Country'], finalists.loc[1, 'Country']
finalist_nations = [finalist1, finalist2]
line_up1 = player_data[(player_data.Country == finalist1)]
line_up2 = player_data[(player_data.Country == finalist2)]
print("\n", line_up1.to_string(columns=['Position', 'ShirtNumber']), "\n\n", line_up2.to_string(columns=['Position', 'ShirtNumber']), "\n")
time.sleep(time_delay * 5)

# Running the Final
player_data, nation_data, finalists = TLKO_simulation_wc_late(1, time_delay, player_data, nation_data, finalists,
                                                              finalists)

# Displaying the winner of the World Cup
champion = finalists.iloc[2:3]
champion = champion.reset_index()
champion = champion.loc[0, 'Country']
print("The World Cup Winner is", champion)

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

print("\nIn Development: A DashApp to display all the data from your World Cup simulation")
print("If you select the Dash_App file in the DashApp folder it will generate a link to the application")

# Exporting data sets for the Dash App
player_data.to_csv('../DashApp/Player_Data_Set.csv')
nation_data.to_csv('../DashApp/Nation_Data_Set.csv')
awards_data.to_csv('../DashApp/Award_Data_Set.csv')
