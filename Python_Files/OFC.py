from scipy.stats import binom, bernoulli
import numpy as np
import pandas as pd
import time
import random
import sys
from MatchSim import TLKO, GRP5, GRP6HA, TLKO_simulation

def ofc(time_delay, player_data, nation_data):
    pot_data = pd.read_csv(r"C:\Users\samwc\PycharmProjects\WorldCup\OFC.csv")
    # pot_data = pd.read_csv(r"/Users/keanerussell/Documents/Documents/Home/Python/OFC.csv")

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
    print("\n", group1)

    print("\nGROUP B")
    print(group2)
    player_data, nation_data, group2 = GRP6HA(time_delay, player_data, nation_data, group2)
    group2 = group2.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])
    group2 = group2.reset_index()
    group2 = group2.drop(['index'], axis=1)
    print("\n", group2)
    uc = input("Press enter to continue: ")  # uc = user continue

    print("\nROUND 2\n")
    winner1 = group1.iloc[0:1, :]
    runnerup1 = group1.iloc[1:2, :]
    winner2 = group2.iloc[0:1, :]
    runnerup2 = group2.iloc[1:2, :]
    winner = pd.concat([winner1, runnerup2, winner2, runnerup1])
    winner = winner.set_index([pd.Index([0, 1, 2, 3]), ])
    player_data, nation_data, winner = TLKO_simulation(2, time_delay, player_data, nation_data, winner, winner)
    uc = input("Press enter to continue: ")  # uc = user continue

    print("\nROUND 3\n")
    print(winner)
    ict = winner.iloc[4:, :]
    print(ict)
    # I think need to change above line from 4 to 5
    ict = ict.set_index([pd.Index([0, 1]), ])
    player_data, nation_data, ict = TLKO_simulation(1, time_delay, player_data, nation_data, ict, ict)
    ict = ict.iloc[2:, :]
    print("QUALIFIED FOR INTERCONTINENTAL PLAYOFF\n")
    print(ict)

    return player_data, nation_data, ict
