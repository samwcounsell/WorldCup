from Host import host_selector
from AFC import afc
from CAF import caf
from CONCACAF import concacaf
from CONMEBOL import conmebol
from OFC import ofc
from UEFA import uefa

import pandas as pd
import plotly.express as px

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

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
player_data = player_data.sort_values(by=['Goals'], ascending=False)
player_data['Goals_Per_Game'] = player_data['Goals'] / player_data['P']
player_data['Assists_Per_Game'] = player_data['Assists'] / player_data['P']
player_data = player_data.sort_values(by=['Goals_Per_Game'], ascending=False)
#print(player_data.to_string(columns=['P', 'Goals', 'Goals_Per_Game']))

nation_data = nation_data.sort_values(by=['total_GF'], ascending=False)
#print(nation_data)



# Plotly Test Graph

uefa_player_data = player_data[player_data['Confederation'] == 'UEFA']
print(uefa_player_data.to_string(columns=['P', 'Goals', 'Assists', 'Goals_Per_Game', 'Assists_Per_Game']))

fig = px.scatter(uefa_player_data, x=uefa_player_data.Assists_Per_Game, y=uefa_player_data.Goals_Per_Game, size=uefa_player_data.P,
                 hover_data=[uefa_player_data.index], color='Country')
fig.show()
