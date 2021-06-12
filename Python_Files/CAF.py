from scipy.stats import binom, bernoulli
import numpy as np
import pandas as pd
import time
import random
import sys
from Round_Simulation import TLKO_simulation, GRP4HA
from Group_Draws import GD4


def caf(time_delay, player_data, nation_data, awards_data, test):
    from Host import host_selector

    CAFhosts = ["South Africa", "Egypt", "Morocco"]
    host, hostdf = host_selector()

    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]

    pot_data = pd.read_csv("CAF.csv")

    pot_data = pot_data.sort_values(by=['World_Rank'])
    round1 = pot_data.iloc[26:54]
    round1 = round1.sample(frac=1)
    round1 = round1.reset_index()
    round1 = round1.drop(['index'], axis=1)

    pot_data = pot_data.iloc[:26, :]

    print("\nWELCOME TO CAF WORLD CUP QUALIFYING\n")
    print("ROUND 1\n")

    a = 14
    player_data, nation_data, pot_data = TLKO_simulation(a, time_delay, player_data, nation_data, round1, pot_data)

    if test != "Y":
        input("Press enter to continue: ")

    pot_data = pot_data.sort_values(by=['World_Rank'])
    pot_data = pot_data.reset_index()
    pot_data = pot_data.drop(['index'], axis=1)

    pot1 = pot_data.iloc[:10, :]
    pot2 = pot_data.iloc[10:20, :]
    pot3 = pot_data.iloc[20:30, :]
    pot4 = pot_data.iloc[30:40, :]

    pot1 = pot1.sample(frac=1)
    pot2 = pot2.sample(frac=1)
    pot3 = pot3.sample(frac=1)
    pot4 = pot4.sample(frac=1)
    potbig = pd.concat([pot1, pot2, pot3, pot4])

    print("ROUND 2\n")

    for i in range(10):
        group = GD4(i, 10, potbig)
        print("\nGroup", alphabet[i])
        print("\n", group.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False),
              "\n")

        player_data, nation_data, group = GRP4HA(time_delay, player_data, nation_data, group)
        group = group.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])
        group = group.reset_index()
        group = group.drop(['index'], axis=1)
        print("\n", group.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False),
              "\n")
        if host in CAFhosts:
            group = group[group.Country != host]
        round3 = group.iloc[0:1, :]
        pot_data = pd.concat([pot_data, round3])

        if test != "Y":
            input("Press enter to continue: ")

    pot_data = pot_data.iloc[40:, :]
    print(pot_data.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False))

    print("ROUND 3\n")

    pot_data = pot_data.sample(frac=1)
    pot_data = pot_data.reset_index()
    pot_data = pot_data.drop(['index'], axis=1)

    if test != "Y":
        input("Press enter to continue: ")

    a = 5
    player_data, nation_data, pot_data = TLKO_simulation(a, time_delay, player_data, nation_data, pot_data, pot_data)  # number of games, dataframe x2, time delay
    pot_data = pot_data.iloc[10:, :]

    print("QUALIFIED FOR THE WORLD CUP FROM AFRICA\n")
    print(pot_data.to_string(columns=['Country'], index=False, header=False))
    if host in CAFhosts:
        print("\nQUALIFIED AS HOST\n")
        print(host)

    # The Awards
    caf_player_data = player_data.loc[player_data['Confederation'] == 'CAF']

    # Ordering data frame for the Golden Boot winner
    caf_player_data = caf_player_data.sort_values(by=['Goals', 'Assists'], ascending=False)
    caf_player_data = caf_player_data.reset_index()
    # Isolating the Golden Boot winner
    caf_Golden_Boot = caf_player_data.loc[0, 'Name']
    caf_player_data = caf_player_data.set_index('Name')
    caf_GBN = caf_player_data.loc[caf_Golden_Boot, 'Goals']

    # Ordering data frame for the Golden Playmaker winner
    caf_player_data = caf_player_data.sort_values(by=['Assists', 'Goals'], ascending=False)
    caf_player_data = caf_player_data.reset_index()
    # Isolating the Golden Playmaker winner
    caf_Golden_Playmaker = caf_player_data.loc[0, 'Name']
    caf_player_data = caf_player_data.set_index('Name')
    caf_GPN = caf_player_data.loc[caf_Golden_Playmaker, 'Assists']
    
    # Updating the Award Winners database
    caf_award_1 = caf_Golden_Boot + " with " + str(caf_GBN) + " Goals"
    caf_award_2 = caf_Golden_Playmaker + " with " + str(caf_GPN) + " Assists"
    awards_data.at['CAF Golden Boot'] = caf_award_1
    awards_data.at['CAF Golden Playmaker'] = caf_award_2

    # Displaying the Award Winners
    print("\nAWARDS")
    print("\nThe CAF Golden Boot Winner is", caf_Golden_Boot, "with", caf_GBN, "Goals")
    print("\nThe CAF Golden Playmaker Winner is", caf_Golden_Playmaker, "with", caf_GPN, "Assists")

    input("\nEnd of CAF qualifiers, press enter to continue to the next Confederation: ")

    return player_data, nation_data, pot_data, awards_data
