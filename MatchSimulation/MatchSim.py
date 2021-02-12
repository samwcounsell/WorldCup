from scipy.stats import binom, bernoulli
import numpy as np
import pandas as pd
import time
import random
import sys

from MatchGameSim import TLGRP90

def TLKO(alpha, beta, gamma):
    for a in range(alpha):
        print("MATCH", a + 1)
        team1 = beta.loc[(2 * a), 'Country']
        team2 = beta.loc[(2 * a + 1), 'Country']
        a1, d1 = beta.loc[(2 * a), 'Attack'], beta.loc[(2 * a), 'Defence']
        a2, d2 = beta.loc[(2 * a), 'Attack'], beta.loc[(2 * a), 'Defence']
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
            df = beta.iloc[(2 * a):(2 * a + 1), :]
            gamma = pd.concat([gamma, df])

        if goals1 < goals2:
            winner = team2
            df = beta.iloc[(2 * a + 1):(2 * a + 2), :]
            gamma = pd.concat([gamma, df])

        if goals1 == goals2:
            if agoals1 > agoals2:
                winner = team1
                df = beta.iloc[(2 * a):(2 * a + 1), :]
                gamma = pd.concat([gamma, df])

            if agoals2 > agoals1:
                winner = team2
                df = beta.iloc[(2 * a + 1):(2 * a + 2), :]
                gamma = pd.concat([gamma, df])

            if agoals1 == agoals2:
                time.sleep(0.7)
                Ber1 = bernoulli.rvs(p1, size=30)
                Ber2 = bernoulli.rvs(p2, size=30)
                goals1 = sum(Ber1) + goals1
                goals2 = sum(Ber2) + goals2

                if goals1 > goals2:
                    winner = team1
                    df = beta.iloc[(2 * a):(2 * a + 1), :]
                    gamma = pd.concat([gamma, df])
                    print("ET:", team1, goals1, " - ", goals2, team2)

                if goals1 < goals2:
                    winner = team2
                    df = beta.iloc[(2 * a + 1):(2 * a + 2), :]
                    gamma = pd.concat([gamma, df])
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
                        df = beta.iloc[(2 * a):(2 * a + 1), :]
                        gamma = pd.concat([gamma, df])
                        print(team1, goals1, "(", pen1, ") - (", pen2, ")", goals2, team2)
                    if pen1 < pen2:
                        winner = team2
                        df = beta.iloc[(2 * a + 1):(2 * a + 2), :]
                        gamma = pd.concat([gamma, df])
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
                                    df = beta.iloc[(2 * a):(2 * a + 1), :]
                                    gamma = pd.concat([gamma, df])
                                    print(team1, goals1, "(", pen1, ") - (", pen2, ")", goals2, team2)
                                    break
                                if pen1 < pen2:
                                    winner = team2
                                    df = beta.iloc[(2 * a + 1):(2 * a + 2), :]
                                    gamma = pd.concat([gamma, df])
                                    print(team1, goals1, "(", pen1, ") - (", pen2, ")", goals2, team2)
                                    break

        time.sleep(0.7)
        print()

    return gamma


###GROUPS###

def GRP4(alpha):
    for k in (1, 2):

        a, b, c, d,  = 0, 1, 2, 3

        for m in range(3):

            print("\n", "MATCHDAY", m + ((k - 1) * 3) + 1)

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

                time.sleep(0.3)

            nb, nc, nd = c, d, b

            b, c, d = nb, nc, nd

            time.sleep(0.3)
    return alpha


def GRP5(alpha):
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

                team1 = alpha.loc[t1, 'Country']
                team2 = alpha.loc[t2, 'Country']
                a1, d1 = alpha.loc[t1, 'Attack'], alpha.loc[t1, 'Defence']
                a2, d2 = alpha.loc[t2, 'Attack'], alpha.loc[t2, 'Defence']

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

                time.sleep(0.3)

            nb, nc, nd, ne, nf = c, e, b, f, d

            b, c, d, e, f = nb, nc, nd, ne, nf

            time.sleep(0.3)
    return alpha
