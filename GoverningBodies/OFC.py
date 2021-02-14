from scipy.stats import binom, bernoulli
import numpy as np
import pandas as pd
import time
import random
import sys
from MatchSim import TLKO, GRP5, GRP6

#pot_data = pd.read_csv(r"C:\Users\samwc\PycharmProjects\WorldCup\OFC.csv")
pot_data = pd.read_csv(r"/Users/keanerussell/Documents/Documents/Home/Python/OFC.csv")

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

group1 = GRP5(group1)
group1 = group1.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])
group1 = group1.reset_index()
group1 = group1.drop(['index'], axis=1)
print(group1)

group2 = GRP6(group2)
group2 = group2.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])
group2 = group2.reset_index()
group2 = group2.drop(['index'], axis=1)
print(group2)
#uc = input("Press enter to continue: ")  # uc = user continue

print("\nROUND 2\n")

winner1 = group1.iloc[0:2, :]
winner2 = group2.iloc[0:2, :]
winner = pd.concat([winner1, winner2])
winner = winner.sample(frac=1)
winner = winner.set_index([pd.Index([0, 1, 2, 3]), ])
winner = TLKO(2, winner, winner, 0.5)
#uc = input("Press enter to continue: ")  # uc = user continue

print("ROUND 3\n")

ict = winner.iloc[4:, :]
ict = ict.set_index([pd.Index([0, 1]), ])
ict = TLKO(1, ict, ict, 0.5)
ict = ict.iloc[2:, :]
ict = ict[['Country', 'World_Rank']]
print("QUALIFIED FOR INTERCONTINENTAL PLAYOFF\n")
print(ict)
