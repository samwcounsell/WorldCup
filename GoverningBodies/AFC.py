from scipy.stats import binom, bernoulli
import numpy as np
import pandas as pd
import time
import random
import sys

#afcpot_data = pd.read_csv(r"C:\Users\samwc\PycharmProjects\WorldCup\AFC.csv")
#afcpot_data = pd.read_csv(r"/Users/keanerussell/Documents/Documents/Home/Python/AFC.csv")  # Keane file location
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
    for leg in (1, 2):
        if leg == 1:
            p1 = 0.014 * (a1 / d2)
            p2 = 0.014 * (a2 / d1) * 0.8
            Ber1 = bernoulli.rvs(p1, size=90)
            Ber2 = bernoulli.rvs(p2, size=90)
            hgoals1 = sum(Ber1)
            agoals2 = sum(Ber2)
            print(team1, hgoals1, " - ", agoals2, team2)
            time.sleep(1)

        if leg == 2:
            p1 = 0.014 * (a1 / d2) * 0.8
            p2 = 0.014 * (a2 / d1)
            Ber1 = bernoulli.rvs(p1, size=90)
            Ber2 = bernoulli.rvs(p2, size=90)
            agoals1 = sum(Ber1)
            hgoals2 = sum(Ber2)
            goals1 = hgoals1 + agoals1
            goals2 = hgoals2 + agoals2
            print(team1, agoals1, "[", goals1, "]", " - ", "[", goals2, "]", hgoals2, team2)

    if goals1 > goals2:
        winner = team1
        df = afcround1.iloc[(2 * a):(2 * a + 1), :]
        afcpot_data = pd.concat([afcpot_data, df])

    if goals1 < goals2:
        winner = team2
        df = afcround1.iloc[(2 * a + 1):(2 * a + 2), :]
        afcpot_data = pd.concat([afcpot_data, df])

    if goals1 == goals2:
        if agoals1 > agoals2:
            winner = team1
            df = afcround1.iloc[(2 * a):(2 * a + 1), :]
            afcpot_data = pd.concat([afcpot_data, df])

        if agoals2 > agoals1:
            winner = team2
            df = afcround1.iloc[(2 * a + 1):(2 * a + 2), :]
            afcpot_data = pd.concat([afcpot_data, df])

        if agoals1 == agoals2:
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

uc = input("Press enter to continue: ")  # uc = user continue


afcpot_data = afcpot_data.sort_values(by=['World_Rank'])
afcpot_data = afcpot_data.reset_index()
afcpot_data = afcpot_data.drop(['index'], axis=1)
# print(afcpot_data)

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
        d = 0
        c = 1
        b = 2
        e = 3
        f = 4

        for m in range(5):

            time.sleep(0.8)
            print("MATCHDAY", m + ((k - 1) * 5) + 1)
            team1 = group.loc[b, 'Country']
            team2 = group.loc[c, 'Country']
            a1, d1 = group.loc[b, 'Attack'], group.loc[b, 'Defence']
            a2, d2 = group.loc[c, 'Attack'], group.loc[c, 'Defence']
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

            group.loc[b, 'P'], group.loc[c, 'P'] = group.loc[b, 'P'] + 1, group.loc[c, 'P'] + 1
            group.loc[b, 'GF'], group.loc[b, 'GA'] = group.loc[c, 'GF'] + goals1, group.loc[b, 'GA'] + goals2
            group.loc[c, 'GF'], group.loc[c, 'GA'] = group.loc[c, 'GF'] + goals2, group.loc[c, 'GA'] + goals1
            group.loc[b, 'GD'] = group.loc[b, 'GF'] - group.loc[b, 'GA']
            group.loc[c, 'GD'] = group.loc[c, 'GF'] - group.loc[c, 'GA']

            if goals1 > goals2:
                winner = team1
                group.loc[b, 'Pts'] = group.loc[b, 'Pts'] + 3
                group.loc[b, 'W'], group.loc[c, 'L'] = group.loc[b, 'W'] + 1, group.loc[c, 'L'] + 1

            if goals1 < goals2:
                winner = team2
                group.loc[c, 'Pts'] = group.loc[c, 'Pts'] + 3
                group.loc[c, 'W'], group.loc[b, 'L'] = group.loc[c, 'W'] + 1, group.loc[b, 'L'] + 1

            if goals1 == goals2:
                group.loc[b, 'Pts'] = group.loc[b, 'Pts'] + 1
                group.loc[c, 'Pts'] = group.loc[c, 'Pts'] + 1
                group.loc[b, 'D'], group.loc[c, 'D'] = group.loc[b, 'D'] + 1, group.loc[c, 'D'] + 1

            #############

            team1 = group.loc[e, 'Country']
            team2 = group.loc[f, 'Country']
            a1, d1 = group.loc[e, 'Attack'], group.loc[e, 'Defence']
            a2, d2 = group.loc[f, 'Attack'], group.loc[f, 'Defence']
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

            group.loc[e, 'P'], group.loc[f, 'P'] = group.loc[e, 'P'] + 1, group.loc[f, 'P'] + 1
            group.loc[e, 'GF'], group.loc[e, 'GA'] = group.loc[f, 'GF'] + goals1, group.loc[e, 'GA'] + goals2
            group.loc[f, 'GF'], group.loc[f, 'GA'] = group.loc[f, 'GF'] + goals2, group.loc[f, 'GA'] + goals1
            group.loc[e, 'GD'] = group.loc[e, 'GF'] - group.loc[e, 'GA']
            group.loc[f, 'GD'] = group.loc[f, 'GF'] - group.loc[f, 'GA']

            if goals1 > goals2:
                winner = team1
                group.loc[e, 'Pts'] = group.loc[e, 'Pts'] + 3
                group.loc[e, 'W'], group.loc[f, 'L'] = group.loc[e, 'W'] + 1, group.loc[f, 'L'] + 1

            if goals1 < goals2:
                winner = team2
                group.loc[f, 'Pts'] = group.loc[f, 'Pts'] + 3
                group.loc[f, 'W'], group.loc[e, 'L'] = group.loc[f, 'W'] + 1, group.loc[e, 'L'] + 1

            if goals1 == goals2:
                group.loc[e, 'Pts'] = group.loc[e, 'Pts'] + 1
                group.loc[f, 'Pts'] = group.loc[f, 'Pts'] + 1
                group.loc[e, 'D'], group.loc[f, 'D'] = group.loc[e, 'D'] + 1, group.loc[f, 'D'] + 1

            nd = c
            nc = e
            nb = d
            ne = f
            nf = b

            d = nd
            c = nc
            b = nb
            e = ne
            f = nf
            
    time.sleep(1)
    group = group.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])
    group = group.reset_index()
    group = group.drop(['index'], axis=1)
    print(group)
    
    afcround3 = group.iloc[0:2, :]
    afcpot_data = pd.concat([afcpot_data, afcround3])

    uc = input("Press enter to continue: ")  # uc = user continue

    print("################")
    
    
afcpot_data = afcpot_data.iloc[40:, :]

groupwinner = afcpot_data.loc[0, :]

runnerup = afcpot_data.loc[1, :]
runnerup = runnerup.sort_values(by=['Pts'], ascending = False)
runnerup = runnerup.iloc[:4, :]

round3big = pd.concat([groupwinner, runnerup])
round3big = round3big.sort_values(by=['World_Rank'])

afcpot1 = round3big.iloc[:2, :]
afcpot2 = round3big.iloc[2:4, :]
afcpot3 = round3big.iloc[4:6, :]
afcpot4 = round3big.iloc[6:8, :]
afcpot5 = round3big.iloc[8:10, :]
afcpot6 = round3big.iloc[10:12, :]

afcpot1 = afcpot1.sample(frac=1)
afcpot2 = afcpot2.sample(frac=1)
afcpot3 = afcpot3.sample(frac=1)
afcpot4 = afcpot4.sample(frac=1)
afcpot5 = afcpot5.sample(frac=1)
afcpot6 = afcpot6.sample(frac=1)

round3big = pd.concat([afcpot1, afcpot2, afcpot3, afcpot4, afcpot5, afcpot6])
round3big[['P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']] = 0

afcgroupA = round3big.iloc[[0, 2, 4, 6, 8, 10], :]
afcgroupA = afcgroupA.set_index([pd.Index([0, 1, 2, 3, 4, 5]), ])
afcgroupB = round3big.iloc[[1, 3, 5, 7, 9, 11], :]
afcgroupB = afcgroupB.set_index([pd.Index([0, 1, 2, 3, 4, 5]), ])


for group in [afcgroupA, afcgroupB]:
    print("############  AFC ROUND 3  ############")
    print(group)
    #time.sleep(2)
    print("############")
    for k in (1, 2):
        for i, j in zip((0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4), (1, 2, 3, 4, 5, 2, 3, 4, 5, 3, 4, 5, 4, 5, 5)):
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

                group.loc[i, 'P'], group.loc[j, 'P'] = group.loc[i, 'P'] + 1, group.loc[j, 'P'] + 1
                group.loc[i, 'GF'], group.loc[i, 'GA'] = group.loc[i, 'GF'] + goals1, group.loc[i, 'GA'] + goals2
                group.loc[j, 'GF'], group.loc[j, 'GA'] = group.loc[j, 'GF'] + goals2, group.loc[j, 'GA'] + goals1
                group.loc[i, 'GD'] = group.loc[i, 'GF'] - group.loc[i, 'GA']
                group.loc[j, 'GD'] = group.loc[j, 'GF'] - group.loc[j, 'GA']

                if goals1 > goals2:
                    winner = team1
                    group.loc[i, 'Pts'] = group.loc[i, 'Pts'] + 3
                    group.loc[i, 'W'], group.loc[j, 'L'] = group.loc[i, 'W'] + 1, group.loc[j, 'L'] + 1

                if goals1 < goals2:
                    winner = team2
                    group.loc[j, 'Pts'] = group.loc[j, 'Pts'] + 3
                    group.loc[j, 'W'], group.loc[i, 'L'] = group.loc[j, 'W'] + 1, group.loc[i, 'L'] + 1

                if goals1 == goals2:
                    group.loc[i, 'Pts'] = group.loc[i, 'Pts'] + 1
                    group.loc[j, 'Pts'] = group.loc[j, 'Pts'] + 1
                    group.loc[i, 'D'], group.loc[j, 'D'] = group.loc[i, 'D'] + 1, group.loc[j, 'D'] + 1

                # print(team1, "xG/m", format(p1, ".4f"), " xG/norm", format((p1 / 0.014), ".4f"), "xG_total",
                # format((p1 * 90), ".4f"), "sd", format(((p1 * (1 - p1) * 90) ** 0.5), ".4f"))
                # print(team2, "xG/m", format(p2, ".4f"), " xG/norm", format((p2 / 0.014), ".4f"), "xG_total",
                # format((p2 * 90), ".4f"), "sd", format(((p2 * (1 - p2) * 90) ** 0.5), ".4f"))
            #time.sleep(0.3)
    #time.sleep(1)
    group = group.sort_values(by=['Pts'], ascending = False)
    group = group.reset_index()
    group = group.drop(['index'], axis=1)
    print("############  AFC ROUND 3  ############")
    print(group)

    afcround4 = group.iloc[2:3, :]
    afcpot_data = pd.concat([afcpot_data, afcround4])


    uc = input("Do you wish to continue, 1 if yes, 0 if no: ")  # uc = user continue
    if uc == 0:
        sys.exit


afcround4 = afcpot_data.iloc[16:, :]
afcround4 = afcround4.sample(frac=1)
afcround4 = afcround4.set_index([pd.Index([0, 1]), ])
afcpot_data = afcpot_data.iloc[16:, :]


print("############  AFC ROUND 4  ############")
for a in range(2):
    team1 = afcround4.loc[(2 * a), 'Country']
    team2 = afcround4.loc[(2 * a + 1), 'Country']
    a1, d1 = afcround4.loc[(2 * a), 'Attack'], afcround4.loc[(2 * a), 'Defence']
    a2, d2 = afcround4.loc[(2 * a), 'Attack'], afcround4.loc[(2 * a), 'Defence']
    for leg in (1, 2):
        if leg == 1:
            p1 = 0.014 * (a1 / d2)
            p2 = 0.014 * (a2 / d1) * 0.8
            Ber1 = bernoulli.rvs(p1, size=90)
            Ber2 = bernoulli.rvs(p2, size=90)
            hgoals1 = sum(Ber1)
            agoals2 = sum(Ber2)
            print(team1, hgoals1, " - ", agoals2, team2)
            time.sleep(1)

        if leg == 2:
            p1 = 0.014 * (a1 / d2) * 0.8
            p2 = 0.014 * (a2 / d1)
            Ber1 = bernoulli.rvs(p1, size=90)
            Ber2 = bernoulli.rvs(p2, size=90)
            agoals1 = sum(Ber1)
            hgoals2 = sum(Ber2)
            goals1 = hgoals1 + agoals1
            goals2 = hgoals2 + agoals2
            print(team1, agoals1, "[", goals1, "]", " - ", "[", goals2, "]", hgoals2, team2)

    if goals1 > goals2:
        winner = team1
        df = afcround4.iloc[(2 * a):(2 * a + 1), :]
        afcpot_data = pd.concat([afcpot_data, df])

    if goals1 < goals2:
        winner = team2
        df = afcround4.iloc[(2 * a + 1):(2 * a + 2), :]
        afcpot_data = pd.concat([afcpot_data, df])

    if goals1 == goals2:
        if agoals1 > agoals2:
            winner = team1
            df = afcround4.iloc[(2 * a):(2 * a + 1), :]
            afcpot_data = pd.concat([afcpot_data, df])

        if agoals2 > agoals1:
            winner = team2
            df = afcround4.iloc[(2 * a + 1):(2 * a + 2), :]
            afcpot_data = pd.concat([afcpot_data, df])

        if agoals1 == agoals2:
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
                df = afcround4.iloc[(2 * a + 1):(2 * a + 2), :]
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
                    df = afcround4.iloc[(2 * a):(2 * a + 1), :]
                    afcpot_data = pd.concat([afcpot_data, df])
                    print(team1, goals1, "(", pen1, ") - (", pen2, ")", goals2, team2)
                if pen1 < pen2:
                    winner = team2
                    df = afcround4.iloc[(2 * a + 1):(2 * a + 2), :]
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
                                df = afcround4.iloc[(2 * a):(2 * a + 1), :]
                                afcpot_data = pd.concat([afcpot_data, df])
                                print(team1, goals1, "(", pen1, ") - (", pen2, ")", goals2, team2)
                                break
                            if pen1 < pen2:
                                winner = team2
                                df = afcround4.iloc[(2 * a + 1):(2 * a + 2), :]
                                afcpot_data = pd.concat([afcpot_data, df])
                                print(team1, goals1, "(", pen1, ") - (", pen2, ")", goals2, team2)
                                break

    time.sleep(1)
    print("############")

uc = input("Press enter to continue: ")  # uc = user continue
