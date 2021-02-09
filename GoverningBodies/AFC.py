from scipy.stats import binom, bernoulli
import numpy as np
import pandas as pd
import time
import random
import sys

afcpot_data = pd.read_csv(r"C:\Users\samwc\PycharmProjects\WorldCup\AFC.csv")
afcpot_data = afcpot_data.sort_values(by=['World_Rank'])

afcround1 = afcpot_data.iloc[34:46]
afcround1 = afcround1.sample(frac=1)
afcround1 = afcround1.set_index([pd.Index([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]), ])
afcpot_data = afcpot_data.iloc[:34, :]

for a in range(6):
    team1 = afcround1.loc[(2 * a), 'Country']
    team2 = afcround1.loc[(2 * a + 1), 'Country']
    a1, d1 = afcround1.loc[(2 * a), 'Attack'], afcround1.loc[(2 * a), 'Defence']
    a2, d2 = afcround1.loc[(2 * a), 'Attack'], afcround1.loc[(2 * a), 'Defence']
    p1 = 0.014 * (a1 / d2)
    p2 = 0.014 * (a2 / d1)
    Ber1 = bernoulli.rvs(p1, size=90)
    Ber2 = bernoulli.rvs(p2, size=90)
    goals1 = sum(Ber1)
    goals2 = sum(Ber2)
    print(team1, goals1, " - ", goals2, team2)

    if goals1 > goals2:
        winner = team1
        df = afcround1.iloc[(2 * a):(2 * a + 1), :]
        afcpot_data = pd.concat([afcpot_data, df])

    if goals1 < goals2:
        winner = team2
        df = afcround1.iloc[(2 * a + 1):(2 * a + 2), :]
        afcpot_data = pd.concat([afcpot_data, df])

    if goals1 == goals2:
        time.sleep(1)
        Ber1 = bernoulli.rvs(p1, size=30)
        Ber2 = bernoulli.rvs(p2, size=30)
        goals1 = sum(Ber1) + goals1
        goals2 = sum(Ber2) + goals2

        if goals1 > goals2:
            winner = team1
            df = afcround1.iloc[(2 * a):(2 * a + 1), :]
            afcpot_data = pd.concat([afcpot_data, df])
            print("ET:", team1, goals1, " - ", goals2, team2)

        if goals1 < goals2:
            winner = team2
            df = afcround1.iloc[(2 * a + 1):(2 * a + 2), :]
            afcpot_data = pd.concat([afcpot_data, df])
            print("ET:", team1, goals1, " - ", goals2, team2)

        if goals1 == goals2:
            print("ET:", team1, goals1, " - ", goals2, team2)
            time.sleep(1)
            Ber1 = bernoulli.rvs(0.7, size=5)
            Ber2 = bernoulli.rvs(0.7, size=5)
            pen1 = sum(Ber1)
            pen2 = sum(Ber2)

            if pen1 > pen2:
                winner = team1
                df = afcround1.iloc[(2 * a):(2 * a + 1), :]
                afcpot_data = pd.concat([afcpot_data, df])
                print(team1, goals1, "(", pen1, ") - (", pen2, ")", goals2, team2)
            if pen1 < pen2:
                winner = team2
                df = afcround1.iloc[(2 * a + 1):(2 * a + 2), :]
                afcpot_data = pd.concat([afcpot_data, df])
                print(team1, goals1, "(", pen1, ") - (", pen2, ")", goals2, team2)
            if pen1 == pen2:
                for b in range(100):
                    Ber1 = bernoulli.rvs(0.7, size=1)
                    Ber2 = bernoulli.rvs(0.7, size=1)
                    pen1 = sum(Ber1) + pen1
                    pen2 = sum(Ber2) + pen2
                    if pen1 != pen2:
                        if pen1 > pen2:
                            winner = team1
                            df = afcround1.iloc[(2 * a):(2 * a + 1), :]
                            afcpot_data = pd.concat([afcpot_data, df])
                            print(team1, goals1, "(", pen1, ") - (", pen2, ")", goals2, team2)
                            break
                        if pen1 < pen2:
                            winner = team2
                            df = afcround1.iloc[(2 * a + 1):(2 * a + 2), :]
                            afcpot_data = pd.concat([afcpot_data, df])
                            print(team1, goals1, "(", pen1, ") - (", pen2, ")", goals2, team2)
                            break
    time.sleep(1)
    print("############")

uc = input("Do you wish to continue, 1 if yes, 0 if no: ") #uc = user continue

if uc == 0:
    sys.exit

afcpot_data = afcpot_data.sort_values(by=['World_Rank'])
afcpot_data = afcpot_data.reset_index()
afcpot_data = afcpot_data.drop(['index'], axis=1)
#print(afcpot_data)

afcpot1 = afcpot_data.iloc[:8, :]
afcpot2 = afcpot_data.iloc[8:16, :]
afcpot3 = afcpot_data.iloc[16:24, :]
afcpot4 = afcpot_data.iloc[24:32, :]
afcpot5 = afcpot_data.iloc[32:40, :]

afcpot1 = afcpot1.sample(frac=1)
afcpot2 = afcpot2.sample(frac=1)
afcpot3 = afcpot3.sample(frac=1)
afcpot4 = afcpot4.sample(frac=1)
afcpot5 = afcpot5.sample(frac=1)

afcpotbig = pd.concat([afcpot1, afcpot2, afcpot3, afcpot4, afcpot5])

afcgroupA = afcpotbig.iloc[[0, 8, 16, 24, 32], :]
afcgroupA = afcgroupA.set_index([pd.Index([0, 1, 2, 3, 4]), ])
afcgroupB = afcpotbig.iloc[[1, 9, 17, 25, 33], :]
afcgroupB = afcgroupB.set_index([pd.Index([0, 1, 2, 3, 4]), ])
afcgroupC = afcpotbig.iloc[[2, 10, 18, 26, 34], :]
afcgroupC = afcgroupC.set_index([pd.Index([0, 1, 2, 3, 4]), ])
afcgroupD = afcpotbig.iloc[[3, 11, 19, 27, 35], :]
afcgroupD = afcgroupD.set_index([pd.Index([0, 1, 2, 3, 4]), ])
afcgroupE = afcpotbig.iloc[[4, 12, 20, 28, 36], :]
afcgroupE = afcgroupE.set_index([pd.Index([0, 1, 2, 3, 4]), ])
afcgroupF = afcpotbig.iloc[[5, 13, 21, 29, 37], :]
afcgroupF = afcgroupF.set_index([pd.Index([0, 1, 2, 3, 4]), ])
afcgroupG = afcpotbig.iloc[[6, 14, 22, 30, 38], :]
afcgroupG = afcgroupG.set_index([pd.Index([0, 1, 2, 3, 4]), ])
afcgroupH = afcpotbig.iloc[[7, 15, 23, 31, 39], :]
afcgroupH = afcgroupH.set_index([pd.Index([0, 1, 2, 3, 4]), ])

for group in [afcgroupA, afcgroupB, afcgroupC, afcgroupD, afcgroupE, afcgroupF, afcgroupG, afcgroupH]:
    print(group)
    time.sleep(2)
    print("############")
    for k in (1, 2):
        for i, j in zip((0, 0, 0, 0, 1, 1, 1, 2, 2, 3,), (1, 2, 3, 4, 2, 3, 4, 3, 4, 4)):
            if i != j:
                team1 = group.loc[i, 'Country']
                team2 = group.loc[j, 'Country']
                a1, d1 = group.loc[i, 'Attack'], group.loc[i, 'Defence']
                a2, d2 = group.loc[j, 'Attack'], group.loc[j, 'Defence']
                if k == 1:  # the * 1.2 gives the home team and advantage
                    p1 = 0.014 * (a1 / d2) * 1.2
                    p2 = 0.014 * (a2 / d1)
                if k == 2:  # the * 1.2 gives the home team and advantage
                    p1 = 0.014 * (a1 / d2)
                    p2 = 0.014 * (a2 / d1) * 1.2

                Ber1 = bernoulli.rvs(p1, size=90)
                Ber2 = bernoulli.rvs(p2, size=90)
                goals1 = sum(Ber1)
                goals2 = sum(Ber2)

                print(team1, goals1, " - ", goals2, team2)

                if goals1 > goals2:
                    winner = team1
                    group.loc[i, 'Pts'] = group.loc[i, 'Pts'] + 3

                if goals1 < goals2:
                    winner = team2
                    group.loc[j, 'Pts'] = group.loc[j, 'Pts'] + 3

                if goals1 == goals2:
                    group.loc[i, 'Pts'] = group.loc[i, 'Pts'] + 1
                    group.loc[j, 'Pts'] = group.loc[j, 'Pts'] + 1

                # print(team1, "xG/m", format(p1, ".4f"), " xG/norm", format((p1 / 0.014), ".4f"), "xG_total",
                # format((p1 * 90), ".4f"), "sd", format(((p1 * (1 - p1) * 90) ** 0.5), ".4f"))
                # print(team2, "xG/m", format(p2, ".4f"), " xG/norm", format((p2 / 0.014), ".4f"), "xG_total",
                # format((p2 * 90), ".4f"), "sd", format(((p2 * (1 - p2) * 90) ** 0.5), ".4f"))
            time.sleep(0.3)
    time.sleep(1)
    group = group.sort_values(by=['Pts'], ascending = False)
    group = group.reset_index()
    group = group.drop(['index'], axis=1)
    print(group)
    uc = input("Do you wish to continue, 1 if yes, 0 if no: ")  # uc = user continue
    if uc == 0:
        sys.exit

    print("################")
