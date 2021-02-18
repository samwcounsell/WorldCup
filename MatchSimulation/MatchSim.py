from scipy.stats import binom, bernoulli
import numpy as np
import pandas as pd
import time
import random
import sys

from MatchGameSim import TLGRP90, TLGRP90HA

def TLKO(alpha, beta, gamma, tao):
    for a in range(alpha):
        time.sleep(tao)
        print("MATCH", a + 1)
        team1 = beta.loc[(2 * a), 'Country']
        team2 = beta.loc[(2 * a + 1), 'Country']
        a1, d1 = beta.loc[(2 * a), 'Attack'], beta.loc[(2 * a), 'Defence']
        a2, d2 = beta.loc[(2 * a + 1), 'Attack'], beta.loc[(2 * a + 1), 'Defence']
        for leg in (1, 2):
            time.sleep(tao * 0.5)
            if leg == 1:
                p1 = 0.014 * (a1 / d2)
                p2 = 0.014 * (a2 / d1) * 0.8
                Ber1 = bernoulli.rvs(p1, size=90)
                Ber2 = bernoulli.rvs(p2, size=90)
                hgoals1 = sum(Ber1)
                agoals2 = sum(Ber2)
                print(team1, hgoals1, " - ", agoals2, team2)
                time.sleep(tao)

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
                time.sleep(tao)
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
                    time.sleep(tao)
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

            nb, nc, nd, ne, nf = c, e, b, f, d

            b, c, d, e, f = nb, nc, nd, ne, nf

            time.sleep(0.3)
    return alpha


def GRP6(alpha):
    for k in (1, 2):

        a, b, c, d, e, f = 0, 1, 2, 3, 4, 5

        for m in range(5):

            print("\n", "MATCHDAY", m + ((k - 1) * 5) + 1)

            for g in range(3):
                if g == 0:
                    t1 = a
                    t2 = b
                if g == 1:
                    t1 = c
                    t2 = d
                if g == 2:
                    t1 = e
                    t2 = f

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

            nb, nc, nd, ne, nf = c, e, b, f, d
            b, c, d, e, f = nb, nc, nd, ne, nf

            time.sleep(0.3)
    return alpha


def GRP8(alpha):
    for k in (1, 2):

        a, b, c, d, e, f, g, h = 0, 1, 2, 3, 4, 5, 6, 7

        for m in range(7):

            print("\n", "MATCHDAY", m + ((k - 1) * 5) + 1)

            for n in range(4):
                if n == 0:
                    t1 = a
                    t2 = b
                if n == 1:
                    t1 = c
                    t2 = d
                if n == 2:
                    t1 = e
                    t2 = f
                if n == 3:
                    t1 = g
                    t2 = h

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

            nb, nc, nd, ne, nf, ng, nh = c, e, b, g, d, h, f
            b, c, d, e, f, g, h = nb, nc, nd, ne, nf, ng, nh

            time.sleep(0.3)
    return alpha


#def GRP10(alpha):
#    for k in (1, 2):
#
#        a, b, c, d, e, f, g, h, i, j = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
#
#        for m in range(9):
#
#            print("\n", "MATCHDAY", m + ((k - 1) * 9) + 1)
#
#            for l in range(5):
#                if l == 0:
#                    t1 = a
#                    t2 = b
#                if l == 1:
#                    t1 = c
#                    t2 = d
#                if l == 2:
#                    t1 = e
#                    t2 = f
#                if l == 3:
#                    t1 = g
#                    t2 = h
#                if l == 4:
#                    t1 = i
#                    t2 = j
#
#                team1 = alpha.loc[t1, 'Country']
#                team2 = alpha.loc[t2, 'Country']
#                a1, d1 = alpha.loc[t1, 'Attack'], alpha.loc[t1, 'Defence']
#                a2, d2 = alpha.loc[t2, 'Attack'], alpha.loc[t2, 'Defence']
#
#                goals1, goals2 = TLGRP90HA(k, a1, d1, a2, d2)
#
#                print(team1, goals1, " - ", goals2, team2)
#
#                alpha.loc[t1, 'P'], alpha.loc[t2, 'P'] = alpha.loc[t1, 'P'] + 1, alpha.loc[t2, 'P'] + 1
#                alpha.loc[t1, 'GF'], alpha.loc[t1, 'GA'] = alpha.loc[t1, 'GF'] + goals1, alpha.loc[t1, 'GA'] + goals2
#                alpha.loc[t2, 'GF'], alpha.loc[t2, 'GA'] = alpha.loc[t2, 'GF'] + goals2, alpha.loc[t2, 'GA'] + goals1
#                alpha.loc[t1, 'GD'] = alpha.loc[t1, 'GF'] - alpha.loc[t1, 'GA']
#                alpha.loc[t2, 'GD'] = alpha.loc[t2, 'GF'] - alpha.loc[t2, 'GA']
#
#                if goals1 > goals2:
#                    alpha.loc[t1, 'Pts'] = alpha.loc[t1, 'Pts'] + 3
#                    alpha.loc[t1, 'W'], alpha.loc[t2, 'L'] = alpha.loc[t1, 'W'] + 1, alpha.loc[t2, 'L'] + 1
#
#                if goals1 < goals2:
#                    alpha.loc[t2, 'Pts'] = alpha.loc[t2, 'Pts'] + 3
#                    alpha.loc[t2, 'W'], alpha.loc[t1, 'L'] = alpha.loc[t2, 'W'] + 1, alpha.loc[t1, 'L'] + 1
#
#                if goals1 == goals2:
#                    alpha.loc[t1, 'Pts'] = alpha.loc[t1, 'Pts'] + 1
#                    alpha.loc[t2, 'Pts'] = alpha.loc[t2, 'Pts'] + 1
#                    alpha.loc[t1, 'D'], alpha.loc[t2, 'D'] = alpha.loc[t1, 'D'] + 1, alpha.loc[t2, 'D'] + 1
#
#                time.sleep(0.3)
#
#            nb, nc, nd, ne, nf, ng, nh, ni, nj = c, e, b, g, d, i, f, j, h
#            b, c, d, e, f, g, h, i, j = nb, nc, nd, ne, nf, ng, nh, ni, nj
#
#            time.sleep(0.3)
#    return alpha

def CONMEBOL(alpha):
    for k in (1, 2):

        for m in range(9):

            print("\n", "MATCHDAY", m + ((k - 1) * 9) + 1)
            if k == 1:
                if m == 0:
                    a, b, c, d, e, f, g, h, i, j = 0, 8, 1, 4, 3, 5, 6, 2, 7, 9
                if m == 1:
                    a, b, c, d, e, f, g, h, i, j = 2, 3, 4, 6, 5, 7, 8, 1, 9, 0
                if m == 2:
                    a, b, c, d, e, f, g, h, i, j = 1, 0, 3, 4, 5, 9, 7, 6, 8, 2
                if m == 3:
                    a, b, c, d, e, f, g, h, i, j = 0, 3, 2, 7, 4, 8, 6, 5, 9, 1
                if m == 4:
                    a, b, c, d, e, f, g, h, i, j = 1, 3, 4, 9, 5, 2, 7, 0, 8, 6
                if m == 5:
                    a, b, c, d, e, f, g, h, i, j = 0, 5, 2, 4, 3, 7, 6, 1, 9, 8
                if m == 6:
                    a, b, c, d, e, f, g, h, i, j = 0, 6, 2, 1, 3, 9, 5, 4, 7, 8
                if m == 7:
                    a, b, c, d, e, f, g, h, i, j = 1, 7, 4, 0, 6, 3, 8, 5, 9, 2
                if m == 8:
                    a, b, c, d, e, f, g, h, i, j = 2, 0, 4, 7, 5, 1, 8, 3, 9, 6
            if k == 2:
                if m == 0:
                    a, b, c, d, e, f, g, h, i, j = 0, 9, 1, 8, 3, 2, 6, 4, 7, 5
                if m == 1:
                    a, b, c, d, e, f, g, h, i, j = 0, 1, 2, 8, 4, 3, 6, 7, 9, 5
                if m == 2:
                    a, b, c, d, e, f, g, h, i, j = 1, 9, 3, 0, 5, 6, 7, 2, 8, 4
                if m == 3:
                    a, b, c, d, e, f, g, h, i, j = 0, 7, 2, 5, 3, 1, 6, 8, 9, 5
                if m == 4:
                    a, b, c, d, e, f, g, h, i, j = 1, 6, 4, 2, 5, 0, 7, 3, 8, 9
                if m == 5:
                    a, b, c, d, e, f, g, h, i, j = 1, 2, 4, 5, 6, 0, 8, 7, 9, 3
                if m == 6:
                    a, b, c, d, e, f, g, h, i, j = 0, 4, 2, 9, 3, 6, 5, 8, 7, 1
                if m == 7:
                    a, b, c, d, e, f, g, h, i, j = 0, 2, 1, 5, 3, 8, 6, 9, 7, 4
                if m == 8:
                    a, b, c, d, e, f, g, h, i, j = 2, 6, 4, 1, 5, 3, 8, 0, 9, 7

            for l in range(5):
                if l == 0:
                    t1 = a
                    t2 = b
                if l == 1:
                    t1 = c
                    t2 = d
                if l == 2:
                    t1 = e
                    t2 = f
                if l == 3:
                    t1 = g
                    t2 = h
                if l == 4:
                    t1 = i
                    t2 = j

                team1 = alpha.loc[t1, 'Country']
                team2 = alpha.loc[t2, 'Country']
                a1, d1 = alpha.loc[t1, 'Attack'], alpha.loc[t1, 'Defence']
                a2, d2 = alpha.loc[t2, 'Attack'], alpha.loc[t2, 'Defence']

                goals1, goals2 = TLGRP90AH(k, a1, d1, a2, d2)

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

        time.sleep(0.3)

    return alpha

def GRP6HA(alpha):
    for k in (1, 2):

        for m in range(5):

            print("\n", "MATCHDAY", m + ((k - 1) * 5) + 1)
            if k == 1:
                if m == 0:
                    a, b, c, d, e, f = 2, 1, 0, 5, 4, 3
                if m == 1:
                    a, b, c, d, e, f = 3, 0, 1, 4, 5, 2
                if m == 2:
                    a, b, c, d, e, f = 4, 2, 0, 1, 5, 3
                if m == 3:
                    a, b, c, d, e, f = 1, 3, 2, 0, 4, 5
                if m == 4:
                    a, b, c, d, e, f = 0, 4, 5, 1, 3, 2
            else:
                if m == 0:
                    a, b, c, d, e, f = 4, 0, 1, 5, 2, 3
                if m == 1:
                    a, b, c, d, e, f = 3, 1, 0, 2, 5, 4
                if m == 2:
                    a, b, c, d, e, f = 2, 4, 1, 0, 3, 5
                if m == 3:
                    a, b, c, d, e, f = 0, 3, 4, 1, 2, 5
                if m == 4:
                    a, b, c, d, e, f = 1, 2, 5, 0, 3, 4

            for g in range(3):
                if g == 0:
                    t1 = a
                    t2 = b
                if g == 1:
                    t1 = c
                    t2 = d
                if g == 2:
                    t1 = e
                    t2 = f

                team1 = alpha.loc[t1, 'Country']
                team2 = alpha.loc[t2, 'Country']
                a1, d1 = alpha.loc[t1, 'Attack'], alpha.loc[t1, 'Defence']
                a2, d2 = alpha.loc[t2, 'Attack'], alpha.loc[t2, 'Defence']

                goals1, goals2 = TLGRP90HA(k, a1, d1, a2, d2)

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

            time.sleep(0.3)
    return alpha

def GRP4HA(alpha):
    for k in (1, 2):

        for m in range(3):

            print("\n", "MATCHDAY", m + ((k - 1) * 3) + 1)
            if k == 1:
                if m == 0:
                    a, b, c, d = 0, 1, 2, 3
                if m == 1:
                    a, b, c, d = 1, 2, 3, 0
                if m == 2:
                    a, b, c, d = 2, 0, 1, 3
            else:
                if m == 0:
                    a, b, c, d = 0, 2, 3, 1
                if m == 1:
                    a, b, c, d = 2, 1, 0, 3
                if m == 2:
                    a, b, c, d = 3, 2, 0, 1

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

                goals1, goals2 = TLGRP90HA(k, a1, d1, a2, d2)

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

            time.sleep(0.3)
    return alpha

def GRP4WC(alpha):
    for k in (1, 2):

        for m in range(3):

            print("\n", "MATCHDAY", m + ((k - 1) * 3) + 1)
            if k == 1:
                if m == 0:
                    a, b, c, d = 0, 1, 2, 3
                if m == 1:
                    a, b, c, d = 3, 0, 1, 2
                if m == 2:
                    a, b, c, d = 2, 0, 1, 3

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

                goals1, goals2 = TLGRP90HA(k, a1, d1, a2, d2)

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

            time.sleep(0.3)
    return alpha

def GRP8HA(alpha):
    for k in (1, 2):

        for m in range(7):

            print("\n", "MATCHDAY", m + ((k - 1) * 7) + 1)
            if k == 1:
                if m == 0:
                    a, b, c, d, e, f, g, h = 0, 1, 2, 3, 4, 5, 6, 7
                if m == 1:
                    a, b, c, d, e, f, g, h = 5, 7, 4, 6, 1, 3, 0, 2
                if m == 2:
                    a, b, c, d, e, f, g, h = 4, 3, 0, 7, 6, 2, 1, 5
                if m == 3:
                    a, b, c, d, e, f, g, h = 2, 5, 6, 1, 0, 4, 7, 3
                if m == 4:
                    a, b, c, d, e, f, g, h = 6, 0, 3, 5, 2, 7, 4, 1
                if m == 5:
                    a, b, c, d, e, f, g, h = 1, 2, 7, 4, 3, 0, 5, 6
                if m == 6:
                    a, b, c, d, e, f, g, h = 3, 6, 5, 0, 7, 1, 2, 4
            else:
                if m == 0:
                    a, b, c, d, e, f, g, h = 0, 6, 1, 4, 5, 3, 7, 2
                if m == 1:
                    a, b, c, d, e, f, g, h = 1, 0, 3, 2, 7, 6, 5, 4
                if m == 2:
                    a, b, c, d, e, f, g, h = 2, 1, 6, 5, 0, 3, 4, 7
                if m == 3:
                    a, b, c, d, e, f, g, h = 3, 1, 7, 5, 2, 0, 6, 4
                if m == 4:
                    a, b, c, d, e, f, g, h = 4, 0, 1, 6, 5, 2, 3, 7
                if m == 5:
                    a, b, c, d, e, f, g, h = 5, 1, 2, 6, 7, 0, 3, 4
                if m == 6:
                    a, b, c, d, e, f, g, h = 6, 3, 0, 5, 1, 7, 4, 2

            for n in range(4):
                if n == 0:
                    t1 = a
                    t2 = b
                if n == 1:
                    t1 = c
                    t2 = d
                if n == 2:
                    t1 = e
                    t2 = f
                if n == 3:
                    t1 = g
                    t2 = h

                team1 = alpha.loc[t1, 'Country']
                team2 = alpha.loc[t2, 'Country']
                a1, d1 = alpha.loc[t1, 'Attack'], alpha.loc[t1, 'Defence']
                a2, d2 = alpha.loc[t2, 'Attack'], alpha.loc[t2, 'Defence']

                goals1, goals2 = TLGRP90HA(k, a1, d1, a2, d2)

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

            time.sleep(0.3)
    return alpha
