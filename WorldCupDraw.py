from scipy.stats import binom, bernoulli
import numpy as np
import pandas as pd
import random

pot_data = pd.read_csv(r"C:\Users\samwc\PycharmProjects\WorldCup\PotTest.csv")
pot_data = pot_data.sort_values(by=['World_Rank'])

pot1 = pot_data.iloc[:8, :]
pot2 = pot_data.iloc[8:16, :]
pot3 = pot_data.iloc[16:24, :]
pot4 = pot_data.iloc[24:32, :]

pot1 = pot1.sample(frac=1)
pot2 = pot2.sample(frac=1)
pot3 = pot3.sample(frac=1)
pot4 = pot4.sample(frac=1)

potbig = pd.concat([pot1, pot2, pot3, pot4])

groupA = potbig.iloc[[0, 8, 16, 24], :]
groupA = groupA.set_index([pd.Index([0, 1, 2, 3]), ])
groupB = potbig.iloc[[1, 9, 17, 25], :]
groupB = groupB.set_index([pd.Index([0, 1, 2, 3]), ])
groupC = potbig.iloc[[2, 10, 18, 26], :]
groupC = groupC.set_index([pd.Index([0, 1, 2, 3]), ])
groupD = potbig.iloc[[3, 11, 19, 27], :]
groupD = groupD.set_index([pd.Index([0, 1, 2, 3]), ])
groupE = potbig.iloc[[4, 12, 20, 28], :]
groupE = groupE.set_index([pd.Index([0, 1, 2, 3]), ])
groupF = potbig.iloc[[5, 13, 21, 29], :]
groupF = groupF.set_index([pd.Index([0, 1, 2, 3]), ])
groupG = potbig.iloc[[6, 14, 22, 30], :]
groupG = groupG.set_index([pd.Index([0, 1, 2, 3]), ])
groupH = potbig.iloc[[7, 15, 23, 31], :]
groupH = groupH.set_index([pd.Index([0, 1, 2, 3]), ])

for group in [groupA, groupB, groupC, groupD, groupE, groupF, groupG, groupH]:
    for i, j in zip((0, 0, 0, 1, 1, 2), (1, 2, 3, 2, 3, 3)):
        if i < j:
            team1 = group.loc[i, 'Country']
            team2 = group.loc[j, 'Country']
            a1, d1 = group.loc[i, 'Attack'], group.loc[i, 'Defence']
            a2, d2 = group.loc[j, 'Attack'], group.loc[j, 'Defence']
            p1 = 0.014 * (a1 / d2)
            q1 = 1 - p1
            p2 = 0.014 * (a2 / d1)
            q2 = 1 - p2
            quantile = np.arange(0.01, 1, 0.1)
            Ber1 = bernoulli.rvs(p1, q1, size=90)
            Ber2 = bernoulli.rvs(p2, q2, size=90)
            goals1 = sum(Ber1)
            goals2 = sum(Ber2)
            print(team1, goals1, " - ", goals2, team2)
            # print(team1, "xG/m", format(p1, ".4f"), " xG/norm", format((p1 / 0.014), ".4f"), "xG_total",
            # format((p1 * 90), ".4f"))
            # print(team2, "xG/m", format(p2, ".4f"), " xG/norm", format((p2 / 0.014), ".4f"), "xG_total",
            # format((p2 * 90), ".4f"))
    print("################")
