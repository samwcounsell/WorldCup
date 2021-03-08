from Host import host_selector
from AFC import afc
from CAF import caf
from CONCACAF import concacaf
from CONMEBOL import conmebol
from OFC import ofc
from UEFA import uefa

import pandas as pd

time_delay = 0
player_data = pd.read_csv("player_data.csv")
player_data = player_data.set_index('Name')

nation_data = pd.read_csv("nation_data.csv")
nation_data = nation_data.set_index('Country')

host, host_df = host_selector()

player_data, nation_data, afc, ict1 = afc(time_delay, player_data, nation_data)
player_data, nation_data, caf = caf(time_delay, player_data, nation_data)
player_data, nation_data, concacaf, ict2 = concacaf(time_delay, player_data, nation_data)
player_data, nation_data, conmebol, ict3 = conmebol(time_delay, player_data, nation_data)
player_data, nation_data, ict4 = ofc(time_delay, player_data, nation_data)
player_data, nation_data, uefa = uefa(time_delay, player_data, nation_data)

teams = host_df
teams = pd.concat([teams, afc])
teams = pd.concat([teams, caf])
teams = pd.concat([teams, concacaf])
teams = pd.concat([teams, conmebol])

teams = pd.concat([teams, uefa])
ict = pd.concat([ict1, ict2, ict3, ict4])

print(teams, "\n", ict)
print(player_data)
print(nation_data)