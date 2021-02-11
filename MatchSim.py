from scipy.stats import binom, bernoulli
import numpy as np
import pandas as pd
import time
import random
import sys

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