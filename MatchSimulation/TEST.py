from scipy.stats import binom, bernoulli
import numpy as np
import pandas as pd
import time
import random
import sys
from MatchGameSim import TLGRP90

alpha = pd.read_csv(r"/Users/keanerussell/Documents/Documents/Home/Python/TEST.csv")

for k in (1, 2):

    for m in range(3):

        print("\n", "MATCHDAY", m + ((k - 1) * 3) + 1)
        if k == 1:
            if m == 0:
                a, b, c, d, = 0, 1, 2, 3
            if m == 1:
                a, b, c, d, = 1, 2, 3, 0
            if m == 2:
                a, b, c, d, = 3, 1, 2, 0
        else:
            if m == 0:
                a, b, c, d, = 1, 3, 0, 2
            if m == 1:
                a, b, c, d, = 2, 1, 0, 3
            if m == 2:
                a, b, c, d, = 1, 0, 2, 3

        for g in range(2):
            if g == 0:
                t1 = a
                t2 = b
            if g == 1:
                t1 = c
                t2 = d

            team1 = alpha.loc[t1, 'Country']
            team2 = alpha.loc[t2, 'Country']
            a1, d1 = alpha.loc[t1, 'Attack'], alpha.loc[t1, 'Defence']
            a2, d2 = alpha.loc[t2, 'Attack'], alpha.loc[t2, 'Defence']

            goals1, goals2 = TLGRP90(k, a1, d1, a2, d2)

            print(team1, goals1, " - ", goals2, team2)

            alpha.loc[t1, 'P'], alpha.loc[t2, 'P'] = alpha.loc[t1, 'P'] + 1, alpha.loc[t2, 'P'] + 1
            alpha.loc[t1, 'GF'], alpha.loc[t1, 'GA'] = alpha.loc[t1, 'GF'] + goals1, alpha.loc[t1, 'GA'] + goals2
            alpha.loc[t2, 'GF'], alpha.loc[t2, 'GA'] = alpha.loc[t2, 'GF'] + goals2, alpha.loc[t2, 'GA'] + goals1
            alpha.loc[t1, 'GD'] = alpha.loc[t1, 'GF'] - alpha.loc[t1, 'GA']
            alpha.loc[t2, 'GD'] = alpha.loc[t2, 'GF'] - alpha.loc[t2, 'GA']

            if goals1 > goals2:
                alpha.loc[t1, 'Pts'] = alpha.loc[t1, 'Pts'] + 3
                alpha.loc[t1, 'W'], alpha.loc[t2, 'L'] = alpha.loc[t1, 'W'] + 1, alpha.loc[t2, 'L'] + 1

            if goals1 < goals2:
                alpha.loc[t2, 'Pts'] = alpha.loc[t2, 'Pts'] + 3
                alpha.loc[t2, 'W'], alpha.loc[t1, 'L'] = alpha.loc[t2, 'W'] + 1, alpha.loc[t1, 'L'] + 1

            if goals1 == goals2:
                alpha.loc[t1, 'Pts'] = alpha.loc[t1, 'Pts'] + 1
                alpha.loc[t2, 'Pts'] = alpha.loc[t2, 'Pts'] + 1
                alpha.loc[t1, 'D'], alpha.loc[t2, 'D'] = alpha.loc[t1, 'D'] + 1, alpha.loc[t2, 'D'] + 1
