from scipy.stats import binom, bernoulli
import numpy as np
import pandas as pd
import time
import random
import sys
from Round_Simulation import GRP5, GRP6HA, TLKO_simulation

def ofc_f(time_delay, player_data, nation_data, awards_data, test):
    pot_data = pd.read_csv("OFC.csv")

    print("\nWELCOME TO OFC WORLD CUP QUALIFYING\n")
    print("ROUND 1")

    pot_data = pot_data.sample(frac=1)
    pot_data = pot_data.reset_index()
    pot_data = pot_data.drop(['index'], axis=1)

    group1 = pot_data.iloc[0:5, :]
    group1 = group1.reset_index()
    group1 = group1.drop(['index'], axis=1)
    group2 = pot_data.iloc[5:11, :]
    group2 = group2.reset_index()
    group2 = group2.drop(['index'], axis=1)

    print("\nGROUP A")
    print(group1)
    player_data, nation_data, group1 = GRP5(time_delay, player_data, nation_data, group1)
    group1 = group1.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])
    group1 = group1.reset_index()
    group1 = group1.drop(['index'], axis=1)
    print("\n", group1.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False),
          "\n")

    print("\nGROUP B")
    print(group2)
    player_data, nation_data, group2 = GRP6HA(time_delay, player_data, nation_data, group2)
    group2 = group2.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])
    group2 = group2.reset_index()
    group2 = group2.drop(['index'], axis=1)
    print("\n", group2.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False),
              "\n")

    #print(nation_data[nation_data['Confederation'] == 'OFC'])

    if test != "Y":
        input("Press enter to continue: ")

    print("\nROUND 2\n")
    winner1 = group1.iloc[0:1, :]
    runnerup1 = group1.iloc[1:2, :]
    winner2 = group2.iloc[0:1, :]
    runnerup2 = group2.iloc[1:2, :]
    winner = pd.concat([winner1, runnerup2, winner2, runnerup1])
    winner = winner.set_index([pd.Index([0, 1, 2, 3]), ])
    print(winner.to_string(columns=['Country', 'World_Rank'], index=False), "\n")
    player_data, nation_data, winner = TLKO_simulation(2, time_delay, player_data, nation_data, winner, winner)

    #print(nation_data[nation_data['Confederation'] == 'OFC'])

    if test != "Y":
        input("Press enter to continue: ")

    print("\nROUND 3\n")
    ict = winner.iloc[4:, :]
    print(ict.to_string(columns=['Country', 'World_Rank'], index=False), "\n")
    # I think need to change above line from 4 to 5
    ict = ict.set_index([pd.Index([0, 1]), ])
    player_data, nation_data, ict = TLKO_simulation(1, time_delay, player_data, nation_data, ict, ict)
    ict = ict.iloc[2:, :]
    print("QUALIFIED FOR INTERCONTINENTAL PLAYOFF\n")
    print(ict.to_string(columns=['Country'], index=False, header=False))

    # The Awards
    ofc_player_data = player_data.loc[player_data['Confederation'] == 'OFC']

    # Ordering data frame for the Golden Boot winner
    ofc_player_data = ofc_player_data.sort_values(by=['Goals', 'Assists'], ascending=False)
    ofc_player_data = ofc_player_data.reset_index()
    # Isolating the Golden Boot winner
    ofc_Golden_Boot = ofc_player_data.loc[0, 'Name']
    ofc_player_data = ofc_player_data.set_index('Name')
    ofc_GBN = ofc_player_data.loc[ofc_Golden_Boot, 'Goals']

    # Ordering data frame for the Golden Playmaker winner
    ofc_player_data = ofc_player_data.sort_values(by=['Assists', 'Goals'], ascending=False)
    ofc_player_data = ofc_player_data.reset_index()
    # Isolating the Golden Playmaker winner
    ofc_Golden_Playmaker = ofc_player_data.loc[0, 'Name']
    ofc_player_data = ofc_player_data.set_index('Name')
    ofc_GPN = ofc_player_data.loc[ofc_Golden_Playmaker, 'Assists']
    
    # Updating the Award Winners database
    ofc_award_1 = ofc_Golden_Boot + " with " + str(ofc_GBN) + " Goals"
    ofc_award_2 = ofc_Golden_Playmaker + " with " + str(ofc_GPN) + " Assists"
    awards_data.at['OFC Golden Boot'] = ofc_award_1
    awards_data.at['OFC Golden Playmaker'] = ofc_award_2

    # Displaying the Award Winners
    print("\nAWARDS")
    print("\nThe OFC Golden Boot Winner is", ofc_Golden_Boot, "with", ofc_GBN, "Goals")
    print("\nThe OFC Golden Playmaker Winner is", ofc_Golden_Playmaker, "with", ofc_GPN, "Assists")

    input("\nEnd of OFC qualifiers, press enter to continue to the next Confederation: ")

    return player_data, nation_data, ict, awards_data
