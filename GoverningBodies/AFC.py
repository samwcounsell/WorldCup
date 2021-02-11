from scipy.stats import binom, bernoulli
import numpy as np
import pandas as pd
import time
import random
import sys

# pot_data = pd.read_csv(r"C:\Users\samwc\PycharmProjects\WorldCup\AFC.csv")
# pot_data = pd.read_csv(r"/Users/keanerussell/Documents/Documents/Home/Python/AFC.csv")
pot_data = pot_data.sort_values(by=['World_Rank'])

round1 = pot_data.iloc[34:46]
round1 = round1.sample(frac=1)
round1 = round1.set_index([pd.Index([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]), ])
pot_data = pot_data.iloc[:34, :]

print("\nWELCOME TO AFC WORLD CUP QUALIFYING\n")
print("ROUND 1\n")

for a in range(6):
    print("MATCH", a + 1)
    team1 = round1.loc[(2 * a), 'Country']
    team2 = round1.loc[(2 * a + 1), 'Country']
    a1, d1 = round1.loc[(2 * a), 'Attack'], round1.loc[(2 * a), 'Defence']
    a2, d2 = round1.loc[(2 * a), 'Attack'], round1.loc[(2 * a), 'Defence']
    for leg in (1, 2):
        if leg == 1:
            p1 = 0.014 * (a1 / d2)
            p2 = 0.014 * (a2 / d1) * 0.8
            Ber1 = bernoulli.rvs(p1, size=90)
            Ber2 = bernoulli.rvs(p2, size=90)
            hgoals1 = sum(Ber1)
            agoals2 = sum(Ber2)
            print(team1, hgoals1, " - ", agoals2, team2)
            time.sleep(0.7)

        if leg == 2:
            p1 = 0.014 * (a1 / d2) * 0.8
            p2 = 0.014 * (a2 / d1)
            Ber1 = bernoulli.rvs(p1, size=90)
            Ber2 = bernoulli.rvs(p2, size=90)
            agoals1 = sum(Ber1)
            hgoals2 = sum(Ber2)
            goals1 = hgoals1 + agoals1
            goals2 = hgoals2 + agoals2
            print(team2, hgoals2, "[", goals2, "]", " - ", "[", goals1, "]", agoals1, team1)

    if goals1 > goals2:
        winner = team1
        df = round1.iloc[(2 * a):(2 * a + 1), :]
        pot_data = pd.concat([pot_data, df])

    if goals1 < goals2:
        winner = team2
        df = round1.iloc[(2 * a + 1):(2 * a + 2), :]
        pot_data = pd.concat([pot_data, df])

    if goals1 == goals2:
        if agoals1 > agoals2:
            winner = team1
            df = round1.iloc[(2 * a):(2 * a + 1), :]
            pot_data = pd.concat([pot_data, df])

        if agoals2 > agoals1:
            winner = team2
            df = round1.iloc[(2 * a + 1):(2 * a + 2), :]
            pot_data = pd.concat([pot_data, df])

        if agoals1 == agoals2:
            time.sleep(0.7)
            Ber1 = bernoulli.rvs(p1, size=30)
            Ber2 = bernoulli.rvs(p2, size=30)
            goals1 = sum(Ber1) + goals1
            goals2 = sum(Ber2) + goals2

            if goals1 > goals2:
                winner = team1
                df = round1.iloc[(2 * a):(2 * a + 1), :]
                pot_data = pd.concat([pot_data, df])
                print("ET:", team1, goals1, " - ", goals2, team2)

            if goals1 < goals2:
                winner = team2
                df = round1.iloc[(2 * a + 1):(2 * a + 2), :]
                pot_data = pd.concat([pot_data, df])
                print("ET:", team1, goals1, " - ", goals2, team2)

            if goals1 == goals2:
                print("ET:", team1, goals1, " - ", goals2, team2)
                time.sleep(0.7)
                Ber1 = bernoulli.rvs(0.7, size=5)
                Ber2 = bernoulli.rvs(0.7, size=5)
                pen1 = sum(Ber1)
                pen2 = sum(Ber2)

                if pen1 > pen2:
                    winner = team1
                    df = round1.iloc[(2 * a):(2 * a + 1), :]
                    pot_data = pd.concat([pot_data, df])
                    print(team1, goals1, "(", pen1, ") - (", pen2, ")", goals2, team2)
                if pen1 < pen2:
                    winner = team2
                    df = round1.iloc[(2 * a + 1):(2 * a + 2), :]
                    pot_data = pd.concat([pot_data, df])
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
                                df = round1.iloc[(2 * a):(2 * a + 1), :]
                                pot_data = pd.concat([pot_data, df])
                                print(team1, goals1, "(", pen1, ") - (", pen2, ")", goals2, team2)
                                break
                            if pen1 < pen2:
                                winner = team2
                                df = round1.iloc[(2 * a + 1):(2 * a + 2), :]
                                pot_data = pd.concat([pot_data, df])
                                print(team1, goals1, "(", pen1, ") - (", pen2, ")", goals2, team2)
                                break

    time.sleep(0.7)
    print()

uc = input("Press enter to continue: ")  # uc = user continue

pot_data = pot_data.sort_values(by=['World_Rank'])
pot_data = pot_data.reset_index()
pot_data = pot_data.drop(['index'], axis=1)

pot1 = pot_data.iloc[:8, :]
pot2 = pot_data.iloc[8:16, :]
pot3 = pot_data.iloc[16:24, :]
pot4 = pot_data.iloc[24:32, :]
pot5 = pot_data.iloc[32:40, :]

pot1 = pot1.sample(frac=1)
pot2 = pot2.sample(frac=1)
pot3 = pot3.sample(frac=1)
pot4 = pot4.sample(frac=1)
pot5 = pot5.sample(frac=1)

potbig = pd.concat([pot1, pot2, pot3, pot4, pot5])

groupA = potbig.iloc[[0, 8, 16, 24, 32], :]
groupA = groupA.set_index([pd.Index([0, 1, 2, 3, 4]), ])
groupA.name = 'GROUP A'
groupB = potbig.iloc[[1, 9, 17, 25, 33], :]
groupB = groupB.set_index([pd.Index([0, 1, 2, 3, 4]), ])
groupB.name = 'GROUP B'
groupC = potbig.iloc[[2, 10, 18, 26, 34], :]
groupC = groupC.set_index([pd.Index([0, 1, 2, 3, 4]), ])
groupC.name = 'GROUP C'
groupD = potbig.iloc[[3, 11, 19, 27, 35], :]
groupD = groupD.set_index([pd.Index([0, 1, 2, 3, 4]), ])
groupD.name = 'GROUP D'
groupE = potbig.iloc[[4, 12, 20, 28, 36], :]
groupE = groupE.set_index([pd.Index([0, 1, 2, 3, 4]), ])
groupE.name = 'GROUP E'
groupF = potbig.iloc[[5, 13, 21, 29, 37], :]
groupF = groupF.set_index([pd.Index([0, 1, 2, 3, 4]), ])
groupF.name = 'GROUP F'
groupG = potbig.iloc[[6, 14, 22, 30, 38], :]
groupG = groupG.set_index([pd.Index([0, 1, 2, 3, 4]), ])
groupG.name = 'GROUP G'
groupH = potbig.iloc[[7, 15, 23, 31, 39], :]
groupH = groupH.set_index([pd.Index([0, 1, 2, 3, 4]), ])
groupH.name = 'GROUP H'

print("\nROUND 2\n")

for group in [groupA, groupB, groupC, groupD, groupE, groupF, groupG, groupH]:
    print(group.name, "\n")
    print(group)
    time.sleep(1)

    for k in (1, 2):

        b, c, d, e, f = 0, 1, 2, 3, 4

        for m in range(5):

            print("\n", "MATCHDAY", m + ((k - 1) * 5) + 1)

            for g in range(2):
                if g == 0:
                    t1 = c
                    t2 = d
                if g == 1:
                    t1 = e
                    t2 = f

                team1 = group.loc[t1, 'Country']
                team2 = group.loc[t2, 'Country']
                a1, d1 = group.loc[t1, 'Attack'], group.loc[t1, 'Defence']
                a2, d2 = group.loc[t2, 'Attack'], group.loc[t2, 'Defence']

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

                group.loc[t1, 'P'], group.loc[t2, 'P'] = group.loc[t1, 'P'] + 1, group.loc[t2, 'P'] + 1
                group.loc[t1, 'GF'], group.loc[t1, 'GA'] = group.loc[t1, 'GF'] + goals1, group.loc[t1, 'GA'] + goals2
                group.loc[t2, 'GF'], group.loc[t2, 'GA'] = group.loc[t2, 'GF'] + goals2, group.loc[t2, 'GA'] + goals1
                group.loc[t1, 'GD'] = group.loc[t1, 'GF'] - group.loc[t1, 'GA']
                group.loc[t2, 'GD'] = group.loc[t2, 'GF'] - group.loc[t2, 'GA']

                if goals1 > goals2:
                    group.loc[t1, 'Pts'] = group.loc[t1, 'Pts'] + 3
                    group.loc[t1, 'W'], group.loc[t2, 'L'] = group.loc[t1, 'W'] + 1, group.loc[t2, 'L'] + 1

                if goals1 < goals2:
                    group.loc[t2, 'Pts'] = group.loc[t2, 'Pts'] + 3
                    group.loc[t2, 'W'], group.loc[t1, 'L'] = group.loc[t2, 'W'] + 1, group.loc[t1, 'L'] + 1

                if goals1 == goals2:
                    group.loc[t1, 'Pts'] = group.loc[t1, 'Pts'] + 1
                    group.loc[t2, 'Pts'] = group.loc[t2, 'Pts'] + 1
                    group.loc[t1, 'D'], group.loc[t2, 'D'] = group.loc[t1, 'D'] + 1, group.loc[t2, 'D'] + 1

                time.sleep(0.3)

            nb, nc, nd, ne, nf = c, e, b, f, d

            b, c, d, e, f = nb, nc, nd, ne, nf

            time.sleep(0.3)

    time.sleep(1)
    group = group.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])
    group = group.reset_index()
    group = group.drop(['index'], axis=1)
    print("\n", group, "\n")

    round3 = group.iloc[0:2, :]
    pot_data = pd.concat([pot_data, round3])

    uc = input("Press enter to continue: ")  # uc = user continue

    print()

####### ROUND 3 ONWARDS BEWARE ############

pot_data = pot_data.iloc[40:, :]

groupwinner = pot_data.loc[0, :]

runnerup = pot_data.loc[1, :]
runnerup = runnerup.sort_values(by=['Pts'], ascending=False)
runnerup = runnerup.iloc[:4, :]

round3big = pd.concat([groupwinner, runnerup])
round3big = round3big.sort_values(by=['World_Rank'])

pot1 = round3big.iloc[:2, :]
pot2 = round3big.iloc[2:4, :]
pot3 = round3big.iloc[4:6, :]
pot4 = round3big.iloc[6:8, :]
pot5 = round3big.iloc[8:10, :]
pot6 = round3big.iloc[10:12, :]

pot1 = pot1.sample(frac=1)
pot2 = pot2.sample(frac=1)
pot3 = pot3.sample(frac=1)
pot4 = pot4.sample(frac=1)
pot5 = pot5.sample(frac=1)
pot6 = pot6.sample(frac=1)

round3big = pd.concat([pot1, pot2, pot3, pot4, pot5, pot6])
round3big[['P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']] = 0

groupA = round3big.iloc[[0, 2, 4, 6, 8, 10], :]
groupA = groupA.set_index([pd.Index([0, 1, 2, 3, 4, 5]), ])
groupB = round3big.iloc[[1, 3, 5, 7, 9, 11], :]
groupB = groupB.set_index([pd.Index([0, 1, 2, 3, 4, 5]), ])

qualified = pot_data.iloc[:1, :]

for group in [groupA, groupB]:
    print("############   ROUND 3  ############")
    print(group)
    # time.sleep(2)
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
            # time.sleep(0.3)
    # time.sleep(1)
    group = group.sort_values(by=['Pts'], ascending=False)
    group = group.reset_index()
    group = group.drop(['index'], axis=1)
    print("############   ROUND 3  ############")
    print(group)

    top2 = group.iloc[0:2, :]
    qualified = pd.concat([qualified, top2])
    round4 = group.iloc[2:3, :]
    pot_data = pd.concat([pot_data, round4])

    uc = input("Do you wish to continue, 1 if yes, 0 if no: ")  # uc = user continue
    if uc == 0:
        sys.exit

round4 = pot_data.iloc[16:, :]
round4 = round4.sample(frac=1)
round4 = round4.set_index([pd.Index([0, 1]), ])
pot_data = pot_data.iloc[16:, :]

print("############   ROUND 4  ############")
for a in range(1):
    team1 = round4.loc[(2 * a), 'Country']
    team2 = round4.loc[(2 * a + 1), 'Country']
    a1, d1 = round4.loc[(2 * a), 'Attack'], round4.loc[(2 * a), 'Defence']
    a2, d2 = round4.loc[(2 * a), 'Attack'], round4.loc[(2 * a), 'Defence']
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
        ict = round4.iloc[(2 * a):(2 * a + 1), :]

    if goals1 < goals2:
        winner = team2
        ict = round4.iloc[(2 * a + 1):(2 * a + 2), :]

    if goals1 == goals2:
        if agoals1 > agoals2:
            winner = team1
            ict = round4.iloc[(2 * a):(2 * a + 1), :]

        if agoals2 > agoals1:
            winner = team2
            ict = round4.iloc[(2 * a + 1):(2 * a + 2), :]

        if agoals1 == agoals2:
            time.sleep(1)
            Ber1 = bernoulli.rvs(p1, size=30)
            Ber2 = bernoulli.rvs(p2, size=30)
            goals1 = sum(Ber1) + goals1
            goals2 = sum(Ber2) + goals2

            if goals1 > goals2:
                winner = team1
                ict = round4.iloc[(2 * a):(2 * a + 1), :]

                print("ET:", team1, goals1, " - ", goals2, team2)

            if goals1 < goals2:
                winner = team2
                ict = round4.iloc[(2 * a + 1):(2 * a + 2), :]

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
                    ict = round4.iloc[(2 * a):(2 * a + 1), :]

                    print(team1, goals1, "(", pen1, ") - (", pen2, ")", goals2, team2)
                if pen1 < pen2:
                    winner = team2
                    ict = round4.iloc[(2 * a + 1):(2 * a + 2), :]

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
                                ict = round4.iloc[(2 * a):(2 * a + 1), :]

                                print(team1, goals1, "(", pen1, ") - (", pen2, ")", goals2, team2)
                                break
                            if pen1 < pen2:
                                winner = team2
                                ict = round4.iloc[(2 * a + 1):(2 * a + 2), :]

                                print(team1, goals1, "(", pen1, ") - (", pen2, ")", goals2, team2)
                                break

    time.sleep(1)
    print("############")

ict = ict[['Country', 'World_Rank']]
qualified = qualified[['Country', 'World_Rank']]    
qualified = qualified.iloc[1:, :]
print("\nQUALIFIED FOR WORLD CUP\n")
print(qualified)
print("\nQUALIFIED FOR INTERCONTINENTAL PLAYOFF\n")
print(ict, "\n")
uc = input("Press enter to exit: ")  # uc = user continue

