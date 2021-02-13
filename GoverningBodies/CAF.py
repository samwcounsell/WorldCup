from scipy.stats import binom, bernoulli
import numpy as np
import pandas as pd
import time
import random
import sys
from MatchSim import TLKO, GRP4
from GroupDraw import GD4

alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]

pot_data = pd.read_csv(r"C:\Users\samwc\PycharmProjects\WorldCup\CAF.csv")
# pot_data = pd.read_csv(r"")

pot_data = pot_data.sort_values(by=['World_Rank'])
round1 = pot_data.iloc[26:54]
round1 = round1.sample(frac=1)
round1 = round1.reset_index()
round1 = round1.drop(['index'], axis=1)

pot_data = pot_data.iloc[:26, :]

print("\nWELCOME TO CAF WORLD CUP QUALIFYING\n")
print("ROUND 1\n")

a = 14
pot_data = TLKO(a, round1, pot_data, 0.5)

uc = input("Press enter to continue: ")  # uc = user continue

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
    print("\n", group, "\n")

    group = GRP4(group)
    group = group.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])
    group = group.reset_index()
    group = group.drop(['index'], axis=1)
    round3 = group.iloc[0:1, :]
    pot_data = pd.concat([pot_data, round3])

    print("\n", group, "\n")

    uc = input("Press enter to continue: ")  # uc = user continue

pot_data = pot_data.iloc[40:, :]
print(pot_data)

print("ROUND 3\n")

pot_data = pot_data.sample(frac=1)
pot_data = pot_data.reset_index()
pot_data = pot_data.drop(['index'], axis=1)

uc = input("Press enter to continue: ")  # uc = user continue

a = 5
pot_data = TLKO(a, pot_data, pot_data, 1)
pot_data = pot_data.iloc[10:, :]

print("QUALIFIED FOR THE WORLD CUP\n")
print(pot_data)

def CAF():
    caf = pot_data
    return caf

