from Host import host_selector
from AFC import afc
from CAF import caf
from CONCACAF import concacaf
from CONMEBOL import conmebol
from OFC import ofc
from UEFA import uefa
from MatchSim import TLKO_simulation, TLKO_simulation_wc_16, TLKO_simulation_wc_late, WorldCupGroupStage
from GroupDraw import GD4

import pandas as pd
#import plotly.express as px

# Lists for use in code
alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
group_names = ["Group A", "Group B", "Group C", "Group D", "Group E", "Group F", "Group G", "Group H"]

# Welcome to the world cup

# Ensuring pandas displays the whole data frame
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# For developers
test = input("For Developers: Is this a test Y/N: ")

# Customise your time delay (each time unit is one minute within a game)
if test != "Y":
    td = input("Choose your time delay for the Qualifiers (0 - 0.1 recommended): ")
    time_delay = float(td)
else:
    time_delay = 0

# Reading in the player and nation data, this is where data is also recorded
player_data = pd.read_csv("player_data.csv")
player_data = player_data.set_index('Name')

nation_data = pd.read_csv("nation_data.csv")
nation_data = nation_data.set_index('Country')

# Randomising the host of the World Cup
host, host_df = host_selector()

# Running all the World Cup Qualifiers
player_data, nation_data, afc, ict1 = afc(time_delay, player_data, nation_data, test)
player_data, nation_data, caf = caf(time_delay, player_data, nation_data)
player_data, nation_data, concacaf, ict2 = concacaf(time_delay, player_data, nation_data)
player_data, nation_data, conmebol, ict3 = conmebol(time_delay, player_data, nation_data)
player_data, nation_data, ict4 = ofc(time_delay, player_data, nation_data)
player_data, nation_data, uefa = uefa(time_delay, player_data, nation_data)

teams = pd.concat([host_df, afc, caf, concacaf, conmebol, uefa])

ict = pd.concat([ict1, ict2, ict3, ict4])
ict = ict.reset_index()
ict = ict.drop(['index'], axis=1)

td = input("Choose your time delay for the Inter-Continental Playoff (0 - 0.1 recommended): ")
time_delay = float(td)

print("\nThe Intercontinental Playoff\n")

player_data, nation_data, ict = TLKO_simulation(2, time_delay, player_data, nation_data, ict, ict)
ict = ict.iloc[4:6]

teams = pd.concat([teams, ict])
teams = teams.sort_values(by='World_Rank')
teams = teams.reset_index()
teams = teams.drop(['index'], axis=1)
print(teams.to_string(columns=['Country', 'World_Rank'], index=False))

world_cup_teams = teams
world_cup_teams[['P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']] = 0

td = input("Choose your time delay for the Group Stage (0 - 0.1 recommended): ")
time_delay = float(td)

# The world cup

pot1 = world_cup_teams.iloc[:8, :]
pot2 = world_cup_teams.iloc[8:16, :]
pot3 = world_cup_teams.iloc[16:24, :]
pot4 = world_cup_teams.iloc[24:32, :]
pot1 = pot1.sample(frac=1)
pot2 = pot2.sample(frac=1)
pot3 = pot3.sample(frac=1)
pot4 = pot4.sample(frac=1)

world_cup_teams = pd.concat([pot1, pot2, pot3, pot4])

for i in range(8):
    group_names[i] = GD4(i, 8, world_cup_teams)
    print("\nGroup", alphabet[i])
    print("\n", group_names[i].to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False),
          "\n")

player_data, nation_data, group_names = WorldCupGroupStage(time_delay, player_data, nation_data, group_names)

# Round of 16

td = input("Choose your time delay for the Round of 16 (0.1 recommended): ")
time_delay = float(td)

for i in range(8):
    qualified = group_names[i].iloc[0:2, :]
    world_cup_teams = pd.concat([world_cup_teams, qualified])

round_of_16 = world_cup_teams.iloc[32:48, :]

print(round_of_16)

round_of_16 = round_of_16.reset_index()
round_of_16 = round_of_16.drop(['index'], axis=1)

player_data, nation_data, round_of_16 = TLKO_simulation_wc_16(8, time_delay, player_data, nation_data, round_of_16, round_of_16)
print("\n", "The Quarter-Finals", "\n")

print(round_of_16)
quarter_finalists = round_of_16.iloc[16:24]
print(quarter_finalists)

td = input("Choose your time delay for the Quarter Finals (0.1 recommended): ")
time_delay = float(td)

quarter_finalists = quarter_finalists.reset_index()
quarter_finalists = quarter_finalists.drop(['index'], axis=1)

player_data, nation_data, quarter_finalists = TLKO_simulation_wc_late(4, time_delay, player_data, nation_data, quarter_finalists, quarter_finalists)
#Bugs, need to display extra time goals and match goals together, only an issue in world cup knockout stage

td = input("Choose your time delay for the Semi Finals (0.1 recommended): ")
time_delay = float(td)

print("\n", "The Semi-Finals", "\n")

semi_finalists = quarter_finalists.iloc[8:12]
print(semi_finalists)

semi_finalists = semi_finalists.reset_index()
semi_finalists = semi_finalists.drop(['index'], axis=1)

player_data, nation_data, semi_finalists = TLKO_simulation_wc_late(2, time_delay, player_data, nation_data, semi_finalists, semi_finalists)

td = input("Choose your time delay for the Final (0.2 recommended): ")
time_delay = float(td)

print("\n", "The Final", "\n")

finalists = semi_finalists.iloc[4:6]
print(finalists)

finalists = finalists.reset_index()
finalists = finalists.drop(['index'], axis=1)

player_data, nation_data, finalists = TLKO_simulation_wc_late(1, time_delay, player_data, nation_data, finalists, finalists)

champion = finalists.iloc[2:3]

print("\n", "The World Cup Winner is", champion.to_string(columns=['Country'], index=False))
