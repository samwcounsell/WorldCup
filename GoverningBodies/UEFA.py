from scipy.stats import binom, bernoulli
import numpy as np
import pandas as pd
import time
import random
import sys
from MatchSim import TLKO, GRP4, GRP5, GRP6
from GroupDraw import GD4, GD5, GD6

#REMOVE HOST BEFORE ROUND1, CHANGE IT TO 4x6 and 6x5
alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]

pot = pd.read_csv(r"C:\Users\samwc\PycharmProjects\WorldCup\UEFA.csv")

pot1 = pot.iloc[:10, :]
pot2 = pot.iloc[10:20, :]
pot3 = pot.iloc[20:30, :]
pot4 = pot.iloc[30:40, :]
pot5 = pot.iloc[40:50, :]
pot6 = pot.iloc[50:, :]

pot1 = pot1.sample(frac=1)
pot2 = pot2.sample(frac=1)
pot3 = pot3.sample(frac=1)
pot4 = pot4.sample(frac=1)
pot = pd.concat([pot1, pot2, pot3, pot4, pot5, pot6])

for i in range(5):
    group6 = GD6(i, 10, pot)
    print("\nGroup", alphabet[i])
    print("\n", group6, "\n")

    group6 = GRP6(group6)
    group6 = group6.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])
    group6 = group6.reset_index()
    group6 = group6.drop(['index'], axis=1)
    round2 = group6.iloc[0:2, :]
    pot = pd.concat([pot, round2])

    print("\n", group6, "\n")

    uc = input("Press enter to continue: ")  # uc = user continue

for i in range(5):
    group5 = GD5(i + 5, 10, pot)
    print("\nGroup", alphabet[i + 5])
    print("\n", group5, "\n")

    group5 = GRP5(group5)
    group5 = group5.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])
    group5 = group5.reset_index()
    group5 = group5.drop(['index'], axis=1)
    round2 = group5.iloc[0:2, :]
    pot = pd.concat([pot, round2])

    print("\n", group5, "\n")

    uc = input("Press enter to continue: ")  # uc = user continue

pot = pot.iloc[55:, :]
print(pot)
pot[['P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']] = 0

potbig = pot.loc[0, :]
runnerup = pot.loc[1, :]

#Round2

for i in range(2):
    group = GD5(i, 2, runnerup)
    print("\nGroup", alphabet[i])
    print("\n", group, "\n")

    group = GRP5(group)
    group = group.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])
    group = group.reset_index()
    group = group.drop(['index'], axis=1)
    round3 = group.iloc[0:2, :]
    potbig = pd.concat([potbig, round3])

    print("\n", group, "\n")

    uc = input("Press enter to continue: ")  # uc = user continue

print(potbig)
qualified = potbig.loc[0, :]
playoff = potbig.loc[1, :]

playoff = playoff.reset_index()
playoff = playoff.drop(['index'], axis=1)

qualified = TLKO(1, playoff, qualified, 0.5)

print(qualified)
