from scipy.stats import binom, bernoulli
import numpy as np
import pandas as pd
import time
import random
import sys
from Commentary import prematch, goal
from MatchGameSim import match_simulation, match_simulation_30, match_simulation_wc, \
    match_simulation_30_wc


def TLKO_simulation(number_of_matches, time_delay, player_data, nation_data, active_data, section_data):
    for a in range(number_of_matches):
        et_goals1, et_goals2 = 0, 0
        time.sleep(time_delay)
        print("MATCH", a + 1, "\n")
        team1 = active_data.loc[(2 * a), 'Country']
        team2 = active_data.loc[(2 * a + 1), 'Country']
        a1, d1 = active_data.loc[(2 * a), 'Attack'], active_data.loc[(2 * a), 'Defence']
        a2, d2 = active_data.loc[(2 * a + 1), 'Attack'], active_data.loc[(2 * a + 1), 'Defence']

        for leg in (1, 2):
            if leg == 1:
                player_data, hgoals1, agoals2 = match_simulation(leg, time_delay, player_data, team1, team2, a1, d1, a2,
                                                                 d2)
            if leg == 2:
                player_data, agoals1, hgoals2 = match_simulation(leg, time_delay, player_data, team1, team2, a1, d1, a2,
                                                                 d2)

        if hgoals1 + agoals1 > hgoals2 + agoals2:
            df = active_data.iloc[(2 * a):(2 * a + 1), :]
            section_data = pd.concat([section_data, df])

        if hgoals1 + agoals1 < hgoals2 + agoals2:
            df = active_data.iloc[(2 * a + 1):(2 * a + 2), :]
            section_data = pd.concat([section_data, df])

        if hgoals1 + agoals1 == hgoals2 + agoals2:
            if agoals1 > agoals2:
                df = active_data.iloc[(2 * a):(2 * a + 1), :]
                section_data = pd.concat([section_data, df])

            if agoals2 > agoals1:
                df = active_data.iloc[(2 * a + 1):(2 * a + 2), :]
                section_data = pd.concat([section_data, df])

            if agoals1 == agoals2:
                time.sleep(time_delay)
                player_data, et_goals1, et_goals2 = match_simulation_30(leg, time_delay, player_data, team1, team2, a1,
                                                                        d1, a2, d2)

                if et_goals1 > et_goals2:
                    df = active_data.iloc[(2 * a):(2 * a + 1), :]
                    section_data = pd.concat([section_data, df])
                    print("ET:", team1, hgoals1 + agoals1 + et_goals1, " - ", hgoals2 + agoals2 + et_goals2, team2)

                if et_goals1 < et_goals2:
                    df = active_data.iloc[(2 * a + 1):(2 * a + 2), :]
                    section_data = pd.concat([section_data, df])
                    print("ET:", team1, hgoals1 + agoals1 + et_goals1, " - ", hgoals2 + agoals2 + et_goals2, team2)

                if et_goals1 == et_goals2:
                    print("ET:", team1, hgoals1 + agoals1 + et_goals1, " - ", hgoals2 + agoals2 + et_goals2, team2)
                    time.sleep(time_delay)
                    Ber1 = bernoulli.rvs(0.7, size=5)
                    Ber2 = bernoulli.rvs(0.7, size=5)
                    pen1 = sum(Ber1)
                    pen2 = sum(Ber2)

                    if pen1 > pen2:
                        df = active_data.iloc[(2 * a):(2 * a + 1), :]
                        section_data = pd.concat([section_data, df])
                        print("\n", team1, hgoals1 + agoals1 + et_goals1, "(", pen1, ") - (", pen2, ")",
                              hgoals2 + agoals2 + et_goals2, team2, "\n")
                    if pen1 < pen2:
                        df = active_data.iloc[(2 * a + 1):(2 * a + 2), :]
                        section_data = pd.concat([section_data, df])
                        print("\n", team1, hgoals1 + agoals1 + et_goals1, "(", pen1, ") - (", pen2, ")",
                              hgoals2 + agoals2 + et_goals2, team2, "\n")
                    if pen1 == pen2:
                        for b in range(100):
                            Ber1 = bernoulli.rvs(0.7, size=1)
                            Ber2 = bernoulli.rvs(0.7, size=1)
                            pen1 = sum(Ber1) + pen1
                            pen2 = sum(Ber2) + pen2
                            if pen1 != pen2:
                                if pen1 > pen2:
                                    df = active_data.iloc[(2 * a):(2 * a + 1), :]
                                    section_data = pd.concat([section_data, df])
                                    print(team1, hgoals1 + agoals1 + et_goals1, "(", pen1, ") - (", pen2, ")",
                                          hgoals2 + agoals2 + et_goals2, team2)
                                    break
                                if pen1 < pen2:
                                    df = active_data.iloc[(2 * a + 1):(2 * a + 2), :]
                                    section_data = pd.concat([section_data, df])
                                    print(team1, hgoals1 + agoals1 + et_goals1, "(", pen1, ") - (", pen2, ")",
                                          hgoals2 + agoals2 + et_goals2, team2)
                                    break

        nation_data.loc[team1, 'total_GF'], nation_data.loc[team1, 'total_GA'], = \
            nation_data.loc[team1, 'total_GF'] + hgoals1 + agoals1 + et_goals1, nation_data.loc[
                team1, 'total_GA'] + hgoals2 + agoals2 + et_goals2
        nation_data.loc[team2, 'total_GF'], nation_data.loc[team2, 'total_GA'], = \
            nation_data.loc[team2, 'total_GF'] + hgoals2 + agoals2 + et_goals2, nation_data.loc[
                team2, 'total_GA'] + hgoals1 + agoals1 + et_goals1
        nation_data.loc[team1, 'total_P'], nation_data.loc[team2, 'total_P'] = \
            nation_data.loc[team1, 'total_P'] + 2, nation_data.loc[team2, 'total_P'] + 2

        player_data.loc[player_data.Country == team1, 'P'], player_data.loc[player_data.Country == team2, 'P'] = \
            player_data.loc[player_data.Country == team1, 'P'] + 2, \
            player_data.loc[player_data.Country == team2, 'P'] + 2

        print("AGGREGATE", team1, hgoals1 + agoals1, " - ", hgoals2 + agoals2, team2)

        if hgoals1 + agoals1 == hgoals2 + agoals2:
            if agoals1 > agoals2:
                print(team1, "go through on away goals")
            if agoals1 < agoals2:
                print(team2, "go through on away goals")

        print()
        print()

    return player_data, nation_data, section_data


def GRP5(time_delay, player_data, nation_data, group_data):
    for leg in (1, 2):

        b, c, d, e, f = 0, 1, 2, 3, 4

        for m in range(5):

            print("\n", "MATCHDAY", m + ((leg - 1) * 5) + 1)

            for g in range(2):
                if g == 0:
                    t1 = c
                    t2 = d
                if g == 1:
                    t1 = e
                    t2 = f

                team1 = group_data.loc[t1, 'Country']
                team2 = group_data.loc[t2, 'Country']
                a1, d1 = group_data.loc[t1, 'Attack'], group_data.loc[t1, 'Defence']
                a2, d2 = group_data.loc[t2, 'Attack'], group_data.loc[t2, 'Defence']

                player_data, goals1, goals2 = match_simulation(leg, time_delay, player_data, team1, team2, a1, d1, a2,
                                                               d2)

                nation_data.loc[team1, 'total_GF'], nation_data.loc[team1, 'total_GA'] = \
                    nation_data.loc[team1, 'total_GF'] + goals1, nation_data.loc[team1, 'total_GA'] + goals2
                nation_data.loc[team2, 'total_GF'], nation_data.loc[team2, 'total_GA'] = \
                    nation_data.loc[team2, 'total_GF'] + goals2, nation_data.loc[team2, 'total_GA'] + goals1
                nation_data.loc[team1, 'total_P'], nation_data.loc[team2, 'total_P'] = \
                    nation_data.loc[team1, 'total_P'] + 1, nation_data.loc[team2, 'total_P'] + 1

                player_data.loc[player_data.Country == team1, 'P'], player_data.loc[player_data.Country == team2, 'P'] = \
                    player_data.loc[player_data.Country == team1, 'P'] + 1, \
                    player_data.loc[player_data.Country == team2, 'P'] + 1

                print(team1, goals1, " - ", goals2, team2)

                group_data.loc[t1, 'P'], group_data.loc[t2, 'P'] = group_data.loc[t1, 'P'] + 1, group_data.loc[
                    t2, 'P'] + 1
                group_data.loc[t1, 'GF'], group_data.loc[t1, 'GA'] = group_data.loc[t1, 'GF'] + goals1, group_data.loc[
                    t1, 'GA'] + goals2
                group_data.loc[t2, 'GF'], group_data.loc[t2, 'GA'] = group_data.loc[t2, 'GF'] + goals2, group_data.loc[
                    t2, 'GA'] + goals1
                group_data.loc[t1, 'GD'] = group_data.loc[t1, 'GF'] - group_data.loc[t1, 'GA']
                group_data.loc[t2, 'GD'] = group_data.loc[t2, 'GF'] - group_data.loc[t2, 'GA']

                if goals1 > goals2:
                    group_data.loc[t1, 'Pts'] = group_data.loc[t1, 'Pts'] + 3
                    group_data.loc[t1, 'W'], group_data.loc[t2, 'L'] = group_data.loc[t1, 'W'] + 1, group_data.loc[
                        t2, 'L'] + 1

                if goals1 < goals2:
                    group_data.loc[t2, 'Pts'] = group_data.loc[t2, 'Pts'] + 3
                    group_data.loc[t2, 'W'], group_data.loc[t1, 'L'] = group_data.loc[t2, 'W'] + 1, group_data.loc[
                        t1, 'L'] + 1

                if goals1 == goals2:
                    group_data.loc[t1, 'Pts'] = group_data.loc[t1, 'Pts'] + 1
                    group_data.loc[t2, 'Pts'] = group_data.loc[t2, 'Pts'] + 1
                    group_data.loc[t1, 'D'], group_data.loc[t2, 'D'] = group_data.loc[t1, 'D'] + 1, group_data.loc[
                        t2, 'D'] + 1

                time.sleep(time_delay * 3)

            nb, nc, nd, ne, nf = c, e, b, f, d

            b, c, d, e, f = nb, nc, nd, ne, nf

            time.sleep(time_delay * 3)
    return player_data, nation_data, group_data


def CONMEBOL(time_delay, player_data, nation_data, group_data):
    for leg in (1, 2):

        for m in range(9):



            print("\n", "MATCHDAY", m + ((leg - 1) * 9) + 1)
            if leg == 1:
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
            if leg == 2:
                if m == 0:
                    a, b, c, d, e, f, g, h, i, j = 0, 9, 1, 8, 3, 2, 6, 4, 7, 5
                if m == 1:
                    a, b, c, d, e, f, g, h, i, j = 0, 1, 2, 8, 4, 3, 6, 7, 9, 5
                if m == 2:
                    a, b, c, d, e, f, g, h, i, j = 1, 9, 3, 0, 5, 6, 7, 2, 8, 4
                if m == 3:
                    a, b, c, d, e, f, g, h, i, j = 0, 7, 2, 5, 3, 1, 6, 8, 9, 4
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

                team1 = group_data.loc[t1, 'Country']
                team2 = group_data.loc[t2, 'Country']
                a1, d1 = group_data.loc[t1, 'Attack'], group_data.loc[t1, 'Defence']
                a2, d2 = group_data.loc[t2, 'Attack'], group_data.loc[t2, 'Defence']

                player_data, goals1, goals2 = match_simulation(leg, time_delay, player_data, team1, team2, a1, d1, a2,
                                                               d2)
                nation_data.loc[team1, 'total_GF'], nation_data.loc[team1, 'total_GA'] = \
                    nation_data.loc[team1, 'total_GF'] + goals1, nation_data.loc[team1, 'total_GA'] + goals2
                nation_data.loc[team2, 'total_GF'], nation_data.loc[team2, 'total_GA'] = \
                    nation_data.loc[team2, 'total_GF'] + goals2, nation_data.loc[team2, 'total_GA'] + goals1
                nation_data.loc[team1, 'total_P'], nation_data.loc[team2, 'total_P'] = \
                    nation_data.loc[team1, 'total_P'] + 1, nation_data.loc[team2, 'total_P'] + 1

                player_data.loc[player_data.Country == team1, 'P'], player_data.loc[player_data.Country == team2, 'P'] = \
                    player_data.loc[player_data.Country == team1, 'P'] + 1, \
                    player_data.loc[player_data.Country == team2, 'P'] + 1

                print(team1, goals1, " - ", goals2, team2)

                group_data.loc[t1, 'P'], group_data.loc[t2, 'P'] = group_data.loc[t1, 'P'] + 1, group_data.loc[
                    t2, 'P'] + 1
                group_data.loc[t1, 'GF'], group_data.loc[t1, 'GA'] = group_data.loc[t1, 'GF'] + goals1, \
                                                                     group_data.loc[t1, 'GA'] + goals2
                group_data.loc[t2, 'GF'], group_data.loc[t2, 'GA'] = group_data.loc[t2, 'GF'] + goals2, \
                                                                     group_data.loc[t2, 'GA'] + goals1
                group_data.loc[t1, 'GD'] = group_data.loc[t1, 'GF'] - group_data.loc[t1, 'GA']
                group_data.loc[t2, 'GD'] = group_data.loc[t2, 'GF'] - group_data.loc[t2, 'GA']

                if goals1 > goals2:
                    group_data.loc[t1, 'Pts'] = group_data.loc[t1, 'Pts'] + 3
                    group_data.loc[t1, 'W'], group_data.loc[t2, 'L'] = group_data.loc[t1, 'W'] + 1, \
                                                                       group_data.loc[t2, 'L'] + 1

                if goals1 < goals2:
                    group_data.loc[t2, 'Pts'] = group_data.loc[t2, 'Pts'] + 3
                    group_data.loc[t2, 'W'], group_data.loc[t1, 'L'] = group_data.loc[t2, 'W'] + 1, \
                                                                       group_data.loc[t1, 'L'] + 1

                if goals1 == goals2:
                    group_data.loc[t1, 'Pts'] = group_data.loc[t1, 'Pts'] + 1
                    group_data.loc[t2, 'Pts'] = group_data.loc[t2, 'Pts'] + 1
                    group_data.loc[t1, 'D'], group_data.loc[t2, 'D'] = group_data.loc[t1, 'D'] + 1, \
                                                                       group_data.loc[t2, 'D'] + 1

                time.sleep(time_delay * 3)

        time.sleep(time_delay * 3)

    return player_data, nation_data, group_data


def GRP6HA(time_delay, player_data, nation_data, group_data):
    for leg in (1, 2):

        for m in range(5):

            print("\n", "MATCHDAY", m + ((leg - 1) * 5) + 1)
            if leg == 1:
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

                team1 = group_data.loc[t1, 'Country']
                team2 = group_data.loc[t2, 'Country']
                a1, d1 = group_data.loc[t1, 'Attack'], group_data.loc[t1, 'Defence']
                a2, d2 = group_data.loc[t2, 'Attack'], group_data.loc[t2, 'Defence']

                player_data, goals1, goals2 = match_simulation(leg, time_delay, player_data, team1, team2, a1, d1, a2,
                                                               d2)

                nation_data.loc[team1, 'total_GF'], nation_data.loc[team1, 'total_GA'] = \
                    nation_data.loc[team1, 'total_GF'] + goals1, nation_data.loc[team1, 'total_GA'] + goals2
                nation_data.loc[team2, 'total_GF'], nation_data.loc[team2, 'total_GA'] = \
                    nation_data.loc[team2, 'total_GF'] + goals2, nation_data.loc[team2, 'total_GA'] + goals1
                nation_data.loc[team1, 'total_P'], nation_data.loc[team2, 'total_P'] = \
                    nation_data.loc[team1, 'total_P'] + 1, nation_data.loc[team2, 'total_P'] + 1

                player_data.loc[player_data.Country == team1, 'P'], player_data.loc[player_data.Country == team2, 'P'] = \
                    player_data.loc[player_data.Country == team1, 'P'] + 1, \
                    player_data.loc[player_data.Country == team2, 'P'] + 1

                print(team1, goals1, " - ", goals2, team2)

                group_data.loc[t1, 'P'], group_data.loc[t2, 'P'] = group_data.loc[t1, 'P'] + 1, group_data.loc[
                    t2, 'P'] + 1
                group_data.loc[t1, 'GF'], group_data.loc[t1, 'GA'] = group_data.loc[t1, 'GF'] + goals1, group_data.loc[
                    t1, 'GA'] + goals2
                group_data.loc[t2, 'GF'], group_data.loc[t2, 'GA'] = group_data.loc[t2, 'GF'] + goals2, group_data.loc[
                    t2, 'GA'] + goals1
                group_data.loc[t1, 'GD'] = group_data.loc[t1, 'GF'] - group_data.loc[t1, 'GA']
                group_data.loc[t2, 'GD'] = group_data.loc[t2, 'GF'] - group_data.loc[t2, 'GA']

                if goals1 > goals2:
                    group_data.loc[t1, 'Pts'] = group_data.loc[t1, 'Pts'] + 3
                    group_data.loc[t1, 'W'], group_data.loc[t2, 'L'] = group_data.loc[t1, 'W'] + 1, group_data.loc[
                        t2, 'L'] + 1

                if goals1 < goals2:
                    group_data.loc[t2, 'Pts'] = group_data.loc[t2, 'Pts'] + 3
                    group_data.loc[t2, 'W'], group_data.loc[t1, 'L'] = group_data.loc[t2, 'W'] + 1, group_data.loc[
                        t1, 'L'] + 1

                if goals1 == goals2:
                    group_data.loc[t1, 'Pts'] = group_data.loc[t1, 'Pts'] + 1
                    group_data.loc[t2, 'Pts'] = group_data.loc[t2, 'Pts'] + 1
                    group_data.loc[t1, 'D'], group_data.loc[t2, 'D'] = group_data.loc[t1, 'D'] + 1, group_data.loc[
                        t2, 'D'] + 1

                time.sleep(time_delay * 3)

            time.sleep(time_delay * 3)
    return player_data, nation_data, group_data


def GRP4HA(time_delay, player_data, nation_data, group_data):
    for leg in (1, 2):

        for m in range(3):

            print("\n", "MATCHDAY", m + ((leg - 1) * 3) + 1)
            if leg == 1:
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

                team1 = group_data.loc[t1, 'Country']
                team2 = group_data.loc[t2, 'Country']
                a1, d1 = group_data.loc[t1, 'Attack'], group_data.loc[t1, 'Defence']
                a2, d2 = group_data.loc[t2, 'Attack'], group_data.loc[t2, 'Defence']

                player_data, goals1, goals2 = match_simulation(leg, time_delay, player_data, team1, team2, a1, d1, a2,
                                                               d2)

                nation_data.loc[team1, 'total_GF'], nation_data.loc[team1, 'total_GA'] = \
                    nation_data.loc[team1, 'total_GF'] + goals1, nation_data.loc[team1, 'total_GA'] + goals2
                nation_data.loc[team2, 'total_GF'], nation_data.loc[team2, 'total_GA'] = \
                    nation_data.loc[team2, 'total_GF'] + goals2, nation_data.loc[team2, 'total_GA'] + goals1
                nation_data.loc[team1, 'total_P'], nation_data.loc[team2, 'total_P'] = \
                    nation_data.loc[team1, 'total_P'] + 1, nation_data.loc[team2, 'total_P'] + 1

                player_data.loc[player_data.Country == team1, 'P'], player_data.loc[player_data.Country == team2, 'P'] = \
                    player_data.loc[player_data.Country == team1, 'P'] + 1, \
                    player_data.loc[player_data.Country == team2, 'P'] + 1

                print(team1, goals1, " - ", goals2, team2)

                group_data.loc[t1, 'P'], group_data.loc[t2, 'P'] = group_data.loc[t1, 'P'] + 1, group_data.loc[
                    t2, 'P'] + 1
                group_data.loc[t1, 'GF'], group_data.loc[t1, 'GA'] = group_data.loc[t1, 'GF'] + goals1, group_data.loc[
                    t1, 'GA'] + goals2
                group_data.loc[t2, 'GF'], group_data.loc[t2, 'GA'] = group_data.loc[t2, 'GF'] + goals2, group_data.loc[
                    t2, 'GA'] + goals1
                group_data.loc[t1, 'GD'] = group_data.loc[t1, 'GF'] - group_data.loc[t1, 'GA']
                group_data.loc[t2, 'GD'] = group_data.loc[t2, 'GF'] - group_data.loc[t2, 'GA']

                if goals1 > goals2:
                    group_data.loc[t1, 'Pts'] = group_data.loc[t1, 'Pts'] + 3
                    group_data.loc[t1, 'W'], group_data.loc[t2, 'L'] = group_data.loc[t1, 'W'] + 1, group_data.loc[
                        t2, 'L'] + 1

                if goals1 < goals2:
                    group_data.loc[t2, 'Pts'] = group_data.loc[t2, 'Pts'] + 3
                    group_data.loc[t2, 'W'], group_data.loc[t1, 'L'] = group_data.loc[t2, 'W'] + 1, group_data.loc[
                        t1, 'L'] + 1

                if goals1 == goals2:
                    group_data.loc[t1, 'Pts'] = group_data.loc[t1, 'Pts'] + 1
                    group_data.loc[t2, 'Pts'] = group_data.loc[t2, 'Pts'] + 1
                    group_data.loc[t1, 'D'], group_data.loc[t2, 'D'] = group_data.loc[t1, 'D'] + 1, group_data.loc[
                        t2, 'D'] + 1

                time.sleep(time_delay * 3)

            time.sleep(time_delay * 3)
    return player_data, nation_data, group_data


def GRP8HA(time_delay, player_data, nation_data, group_data):
    for leg in (1, 2):

        for m in range(7):

            print("\n", "MATCHDAY", m + ((leg - 1) * 7) + 1)
            if leg == 1:
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

                team1 = group_data.loc[t1, 'Country']
                team2 = group_data.loc[t2, 'Country']
                a1, d1 = group_data.loc[t1, 'Attack'], group_data.loc[t1, 'Defence']
                a2, d2 = group_data.loc[t2, 'Attack'], group_data.loc[t2, 'Defence']

                player_data, goals1, goals2 = match_simulation(leg, time_delay, player_data, team1, team2, a1, d1, a2,
                                                               d2)

                nation_data.loc[team1, 'total_GF'], nation_data.loc[team1, 'total_GA'] = \
                    nation_data.loc[team1, 'total_GF'] + goals1, nation_data.loc[team1, 'total_GA'] + goals2
                nation_data.loc[team2, 'total_GF'], nation_data.loc[team2, 'total_GA'] = \
                    nation_data.loc[team2, 'total_GF'] + goals2, nation_data.loc[team2, 'total_GA'] + goals1
                nation_data.loc[team1, 'total_P'], nation_data.loc[team2, 'total_P'] = \
                    nation_data.loc[team1, 'total_P'] + 1, nation_data.loc[team2, 'total_P'] + 1

                player_data.loc[player_data.Country == team1, 'P'], player_data.loc[player_data.Country == team2, 'P'] = \
                    player_data.loc[player_data.Country == team1, 'P'] + 1, \
                    player_data.loc[player_data.Country == team2, 'P'] + 1

                print(team1, goals1, " - ", goals2, team2)

                group_data.loc[t1, 'P'], group_data.loc[t2, 'P'] = group_data.loc[t1, 'P'] + 1, group_data.loc[
                    t2, 'P'] + 1
                group_data.loc[t1, 'GF'], group_data.loc[t1, 'GA'] = group_data.loc[t1, 'GF'] + goals1, group_data.loc[
                    t1, 'GA'] + goals2
                group_data.loc[t2, 'GF'], group_data.loc[t2, 'GA'] = group_data.loc[t2, 'GF'] + goals2, group_data.loc[
                    t2, 'GA'] + goals1
                group_data.loc[t1, 'GD'] = group_data.loc[t1, 'GF'] - group_data.loc[t1, 'GA']
                group_data.loc[t2, 'GD'] = group_data.loc[t2, 'GF'] - group_data.loc[t2, 'GA']

                if goals1 > goals2:
                    group_data.loc[t1, 'Pts'] = group_data.loc[t1, 'Pts'] + 3
                    group_data.loc[t1, 'W'], group_data.loc[t2, 'L'] = group_data.loc[t1, 'W'] + 1, group_data.loc[
                        t2, 'L'] + 1

                if goals1 < goals2:
                    group_data.loc[t2, 'Pts'] = group_data.loc[t2, 'Pts'] + 3
                    group_data.loc[t2, 'W'], group_data.loc[t1, 'L'] = group_data.loc[t2, 'W'] + 1, group_data.loc[
                        t1, 'L'] + 1

                if goals1 == goals2:
                    group_data.loc[t1, 'Pts'] = group_data.loc[t1, 'Pts'] + 1
                    group_data.loc[t2, 'Pts'] = group_data.loc[t2, 'Pts'] + 1
                    group_data.loc[t1, 'D'], group_data.loc[t2, 'D'] = group_data.loc[t1, 'D'] + 1, group_data.loc[
                        t2, 'D'] + 1

                time.sleep(time_delay * 3)

            time.sleep(time_delay * 3)
    return player_data, nation_data, group_data


def WorldCupGroupStage(time_delay, player_data, nation_data, group_names):
    for round in range(3):
        for part in range(4):

            print("\n", "World Cup Group Stage Day", (round + 1) * (part + 1), "\n")
            for ind_grp in range(2):

                group = group_names[(part * 2) + ind_grp]

                for g in range(2):

                    if round == 0:
                        a, b, c, d = 0, 1, 2, 3
                    if round == 1:
                        a, b, c, d = 1, 2, 3, 0
                    if round == 2:
                        a, b, c, d = 2, 0, 1, 3

                    if g == 0:
                        t1 = a
                        t2 = b
                    if g == 1:
                        t1 = c
                        t2 = d

                    team1 = group.loc[t1, 'Country']
                    team2 = group.loc[t2, 'Country']

                    a1, d1 = group.loc[t1, 'Attack'], group.loc[t1, 'Defence']
                    a2, d2 = group.loc[t2, 'Attack'], group.loc[t2, 'Defence']

                    player_data, goals1, goals2 = match_simulation_wc(time_delay, player_data, team1, team2, a1, d1,
                                                                      a2,
                                                                      d2)

                    nation_data.loc[team1, 'total_GF'], nation_data.loc[team1, 'total_GA'] = \
                        nation_data.loc[team1, 'total_GF'] + goals1, nation_data.loc[team1, 'total_GA'] + goals2
                    nation_data.loc[team2, 'total_GF'], nation_data.loc[team2, 'total_GA'] = \
                        nation_data.loc[team2, 'total_GF'] + goals2, nation_data.loc[team2, 'total_GA'] + goals1
                    nation_data.loc[team1, 'total_P'], nation_data.loc[team2, 'total_P'] = \
                        nation_data.loc[team1, 'total_P'] + 1, nation_data.loc[team2, 'total_P'] + 1

                    player_data.loc[player_data.Country == team1, 'P'], player_data.loc[
                        player_data.Country == team2, 'P'] = \
                        player_data.loc[player_data.Country == team1, 'P'] + 1, \
                        player_data.loc[player_data.Country == team2, 'P'] + 1
                    player_data.loc[player_data.Country == team1, 'WC_P'], player_data.loc[
                        player_data.Country == team2, 'WC_P'] = \
                        player_data.loc[player_data.Country == team1, 'WC_P'] + 1, \
                        player_data.loc[player_data.Country == team2, 'WC_P'] + 1

                    print(team1, goals1, " - ", goals2, team2)

                    group.loc[t1, 'P'], group.loc[t2, 'P'] = group.loc[t1, 'P'] + 1, group.loc[
                        t2, 'P'] + 1
                    group.loc[t1, 'GF'], group.loc[t1, 'GA'] = group.loc[t1, 'GF'] + goals1, \
                                                               group.loc[
                                                                   t1, 'GA'] + goals2
                    group.loc[t2, 'GF'], group.loc[t2, 'GA'] = group.loc[t2, 'GF'] + goals2, \
                                                               group.loc[
                                                                   t2, 'GA'] + goals1
                    group.loc[t1, 'GD'] = group.loc[t1, 'GF'] - group.loc[t1, 'GA']
                    group.loc[t2, 'GD'] = group.loc[t2, 'GF'] - group.loc[t2, 'GA']

                    if goals1 > goals2:
                        group.loc[t1, 'Pts'] = group.loc[t1, 'Pts'] + 3
                        group.loc[t1, 'W'], group.loc[t2, 'L'] = group.loc[t1, 'W'] + 1, group.loc[
                            t2, 'L'] + 1

                    if goals1 < goals2:
                        group.loc[t2, 'Pts'] = group.loc[t2, 'Pts'] + 3
                        group.loc[t2, 'W'], group.loc[t1, 'L'] = group.loc[t2, 'W'] + 1, group.loc[
                            t1, 'L'] + 1

                    if goals1 == goals2:
                        group.loc[t1, 'Pts'] = group.loc[t1, 'Pts'] + 1
                        group.loc[t2, 'Pts'] = group.loc[t2, 'Pts'] + 1
                        group.loc[t1, 'D'], group.loc[t2, 'D'] = group.loc[t1, 'D'] + 1, group.loc[
                            t2, 'D'] + 1

                    time.sleep(time_delay * 3)

                time.sleep(time_delay * 3)

                group = group.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])
                # group = group.reset_index()
                # group = group.drop(['index'], axis=1)

                group_names[(part * 2) + ind_grp] = group

                print("\n", group.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'],
                                            index=False),
                      "\n")

                uc = input("Press enter to continue: ")  # uc = user continue

    return player_data, nation_data, group_names


def TLKO_simulation_wc_16(number_of_matches, time_delay, player_data, nation_data, active_data, section_data):
    for a in range(number_of_matches):
        et_goals1, et_goals2 = 0, 0
        time.sleep(time_delay)
        print("MATCH", a + 1, "\n")

        if (a % 2) == 0:
            team1 = active_data.loc[(2 * a), 'Country']
            team2 = active_data.loc[(2 * a + 3), 'Country']
            a1, d1 = active_data.loc[(2 * a), 'Attack'], active_data.loc[(2 * a), 'Defence']
            a2, d2 = active_data.loc[(2 * a + 3), 'Attack'], active_data.loc[(2 * a + 3), 'Defence']

            player_data, goals1, goals2 = match_simulation_wc(time_delay, player_data, team1, team2, a1, d1, a2, d2)

            if goals1 > goals2:
                df = active_data.iloc[(2 * a):(2 * a) + 1, :]
                section_data = pd.concat([section_data, df])

            if goals1 < goals2:
                df = active_data.iloc[(2 * a + 3):(2 * a) + 4, :]
                section_data = pd.concat([section_data, df])

            if goals1 == goals2:
                player_data, et_goals1, et_goals2 = match_simulation_30_wc(time_delay, player_data, team1, team2, a1,
                                                                           d1, a2, d2, goals1, goals2)
                if et_goals1 > et_goals2:
                    df = active_data.iloc[(2 * a):(2 * a) + 1, :]
                    section_data = pd.concat([section_data, df])
                    print("ET:", team1, goals1 + et_goals1, " - ", goals2 + et_goals2, team2)

                if et_goals1 < et_goals2:
                    df = active_data.iloc[(2 * a + 3):(2 * a) + 4, :]
                    section_data = pd.concat([section_data, df])
                    print("ET:", team1, goals1 + et_goals1, " - ", goals2 + et_goals2, team2)

                if et_goals1 == et_goals2:
                    print("ET:", team1, goals1 + et_goals1, " - ", goals2 + et_goals2, team2)
                    time.sleep(time_delay)
                    Ber1 = bernoulli.rvs(0.7, size=5)
                    Ber2 = bernoulli.rvs(0.7, size=5)
                    pen1 = sum(Ber1)
                    pen2 = sum(Ber2)

                    if pen1 > pen2:
                        df = active_data.iloc[(2 * a):(2 * a) + 1, :]
                        section_data = pd.concat([section_data, df])
                        print("\n", team1, goals1 + et_goals1, "(", pen1, ") - (", pen2, ")",
                              goals2 + et_goals2, team2, "\n")
                    if pen1 < pen2:
                        df = active_data.iloc[(2 * a + 3):(2 * a) + 4, :]
                        section_data = pd.concat([section_data, df])
                        print("\n", team1, goals1 + et_goals1, "(", pen1, ") - (", pen2, ")",
                              goals2 + et_goals2, team2, "\n")
                    if pen1 == pen2:
                        for b in range(100):
                            Ber1 = bernoulli.rvs(0.7, size=1)
                            Ber2 = bernoulli.rvs(0.7, size=1)
                            pen1 = sum(Ber1) + pen1
                            pen2 = sum(Ber2) + pen2
                            if pen1 != pen2:
                                if pen1 > pen2:
                                    df = active_data.iloc[(2 * a):(2 * a) + 1, :]
                                    section_data = pd.concat([section_data, df])
                                    print("\n", team1, goals1 + et_goals1, "(", pen1, ") - (", pen2, ")",
                                          goals2 + et_goals2, team2)
                                    break
                                if pen1 < pen2:
                                    df = active_data.iloc[(2 * a + 3):(2 * a) + 4, :]
                                    section_data = pd.concat([section_data, df])
                                    print("\n", team1, goals1 + et_goals1, "(", pen1, ") - (", pen2, ")",
                                          goals2 + et_goals2, team2)
                                    break

            print(team1, goals1, " - ", goals2, team2)
            print()
            print()

        if (a % 2) != 0:
            team1 = active_data.loc[(2 * a) - 1, 'Country']
            team2 = active_data.loc[2 * a, 'Country']
            a1, d1 = active_data.loc[(2 * a) - 1, 'Attack'], active_data.loc[(2 * a) - 1, 'Defence']
            a2, d2 = active_data.loc[2 * a, 'Attack'], active_data.loc[2 * a, 'Defence']
            player_data, goals1, goals2 = match_simulation_wc(time_delay, player_data, team1, team2, a1, d1, a2, d2)

            if goals1 > goals2:
                df = active_data.iloc[(2 * a) - 1:2 * a, :]
                section_data = pd.concat([section_data, df])

            if goals1 < goals2:
                df = active_data.iloc[2 * a:(2 * a) + 1, :]
                section_data = pd.concat([section_data, df])

            if goals1 == goals2:
                player_data, et_goals1, et_goals2 = match_simulation_30_wc(time_delay, player_data, team1, team2, a1,
                                                                           d1, a2, d2, goals1, goals2)
                if et_goals1 > et_goals2:
                    df = active_data.iloc[(2 * a) - 1:2 * a, :]
                    section_data = pd.concat([section_data, df])
                    print("ET:", team1, goals1 + et_goals1, " - ", goals2 + et_goals2, team2)

                if et_goals1 < et_goals2:
                    df = active_data.iloc[2 * a:(2 * a) + 1, :]
                    section_data = pd.concat([section_data, df])
                    print("ET:", team1, goals1 + et_goals1, " - ", goals2 + et_goals2, team2)

                if et_goals1 == et_goals2:
                    print("ET:", team1, goals1 + et_goals1, " - ", goals2 + et_goals2, team2)
                    time.sleep(time_delay)
                    Ber1 = bernoulli.rvs(0.7, size=5)
                    Ber2 = bernoulli.rvs(0.7, size=5)
                    pen1 = sum(Ber1)
                    pen2 = sum(Ber2)

                    if pen1 > pen2:
                        df = active_data.iloc[(2 * a) - 1:2 * a, :]
                        section_data = pd.concat([section_data, df])
                        print("\n", team1, goals1 + et_goals1, "(", pen1, ") - (", pen2, ")",
                              goals2 + et_goals2, team2, "\n")
                    if pen1 < pen2:
                        df = active_data.iloc[2 * a:(2 * a) + 1, :]
                        section_data = pd.concat([section_data, df])
                        print("\n", team1, goals1 + et_goals1, "(", pen1, ") - (", pen2, ")",
                              goals2 + et_goals2, team2, "\n")
                    if pen1 == pen2:
                        for b in range(100):
                            Ber1 = bernoulli.rvs(0.7, size=1)
                            Ber2 = bernoulli.rvs(0.7, size=1)
                            pen1 = sum(Ber1) + pen1
                            pen2 = sum(Ber2) + pen2
                            if pen1 != pen2:
                                if pen1 > pen2:
                                    df = active_data.iloc[(2 * a) - 1:2 * a, :]
                                    section_data = pd.concat([section_data, df])
                                    print("\n", team1, goals1 + et_goals1, "(", pen1, ") - (", pen2, ")",
                                          goals2 + et_goals2, team2)
                                    break
                                if pen1 < pen2:
                                    df = active_data.iloc[2 * a:(2 * a) + 1, :]
                                    section_data = pd.concat([section_data, df])
                                    print("\n", team1, goals1 + et_goals1, "(", pen1, ") - (", pen2, ")",
                                          goals2 + et_goals2, team2)
                                    break

            print(team1, goals1, " - ", goals2, team2)
            print()
            print()

        nation_data.loc[team1, 'total_GF'], nation_data.loc[team1, 'total_GA'] = \
            nation_data.loc[team1, 'total_GF'] + goals1, nation_data.loc[team1, 'total_GA'] + goals2
        nation_data.loc[team2, 'total_GF'], nation_data.loc[team2, 'total_GA'] = \
            nation_data.loc[team2, 'total_GF'] + goals2, nation_data.loc[team2, 'total_GA'] + goals1
        nation_data.loc[team1, 'total_P'], nation_data.loc[team2, 'total_P'] = \
            nation_data.loc[team1, 'total_P'] + 1, nation_data.loc[team2, 'total_P'] + 1

        player_data.loc[player_data.Country == team1, 'P'], player_data.loc[player_data.Country == team2, 'P'] = \
            player_data.loc[player_data.Country == team1, 'P'] + 1, \
            player_data.loc[player_data.Country == team2, 'P'] + 1
        player_data.loc[player_data.Country == team1, 'WC_P'], player_data.loc[player_data.Country == team2, 'WC_P'] = \
            player_data.loc[player_data.Country == team1, 'WC_P'] + 1, \
            player_data.loc[player_data.Country == team2, 'WC_P'] + 1

    return player_data, nation_data, section_data


def TLKO_simulation_wc_late(number_of_matches, time_delay, player_data, nation_data, active_data, section_data):
    for a in range(number_of_matches):
        et_goals1, et_goals2 = 0, 0
        time.sleep(time_delay)
        print("MATCH", a + 1, "\n")

        if number_of_matches > 1:
            if a == 0:
                x, y = 0, 2
            if a == 1:
                x, y = 1, 3
            if a == 2:
                x, y = 4, 6
            if a == 3:
                x, y = 5, 7

        else:
            x, y = 0, 1

        team1 = active_data.loc[x, 'Country']
        team2 = active_data.loc[y, 'Country']
        a1, d1 = active_data.loc[x, 'Attack'], active_data.loc[x, 'Defence']
        a2, d2 = active_data.loc[y, 'Attack'], active_data.loc[y, 'Defence']

        player_data, goals1, goals2 = match_simulation_wc(time_delay, player_data, team1, team2, a1, d1, a2, d2)

        if goals1 > goals2:
            df = active_data.iloc[x:x + 1, :]
            section_data = pd.concat([section_data, df])

        if goals1 < goals2:
            df = active_data.iloc[y:y + 1, :]
            section_data = pd.concat([section_data, df])

        if goals1 == goals2:
            player_data, et_goals1, et_goals2 = match_simulation_30_wc(time_delay, player_data, team1, team2, a1,
                                                                       d1, a2, d2, goals1, goals2)
            if et_goals1 > et_goals2:
                df = active_data.iloc[x:x + 1, :]
                section_data = pd.concat([section_data, df])
                print("ET:", team1, goals1 + et_goals1, " - ", goals2 + et_goals2, team2)

            if et_goals1 < et_goals2:
                df = active_data.iloc[y:y + 1, :]
                section_data = pd.concat([section_data, df])
                print("ET:", team1, goals1 + et_goals1, " - ", goals2 + et_goals2, team2)

            if et_goals1 == et_goals2:
                print("ET:", team1, goals1 + et_goals1, " - ", goals2 + et_goals2, team2)
                time.sleep(time_delay)
                Ber1 = bernoulli.rvs(0.7, size=5)
                Ber2 = bernoulli.rvs(0.7, size=5)
                pen1 = sum(Ber1)
                pen2 = sum(Ber2)

                if pen1 > pen2:
                    df = active_data.iloc[x:x + 1, :]
                    section_data = pd.concat([section_data, df])
                    print("\n", team1, goals1 + et_goals1, "(", pen1, ") - (", pen2, ")",
                          goals2 + et_goals2, team2, "\n")
                if pen1 < pen2:
                    df = active_data.iloc[y:y + 1, :]
                    section_data = pd.concat([section_data, df])
                    print("\n", team1, goals1 + et_goals1, "(", pen1, ") - (", pen2, ")",
                          goals2 + et_goals2, team2, "\n")
                if pen1 == pen2:
                    for b in range(100):
                        Ber1 = bernoulli.rvs(0.7, size=1)
                        Ber2 = bernoulli.rvs(0.7, size=1)
                        pen1 = sum(Ber1) + pen1
                        pen2 = sum(Ber2) + pen2
                        if pen1 != pen2:
                            if pen1 > pen2:
                                df = active_data.iloc[x:x + 1, :]
                                section_data = pd.concat([section_data, df])
                                print("\n", team1, goals1 + et_goals1, "(", pen1, ") - (", pen2, ")",
                                      goals2 + et_goals2, team2)
                                break
                            if pen1 < pen2:
                                df = active_data.iloc[y:y + 1, :]
                                section_data = pd.concat([section_data, df])
                                print("\n", team1, goals1 + et_goals1, "(", pen1, ") - (", pen2, ")",
                                      goals2 + et_goals2, team2)
                                break

            print(team1, goals1, " - ", goals2, team2, "\n", "\n")

        nation_data.loc[team1, 'total_GF'], nation_data.loc[team1, 'total_GA'] = \
            nation_data.loc[team1, 'total_GF'] + goals1, nation_data.loc[team1, 'total_GA'] + goals2
        nation_data.loc[team2, 'total_GF'], nation_data.loc[team2, 'total_GA'] = \
            nation_data.loc[team2, 'total_GF'] + goals2, nation_data.loc[team2, 'total_GA'] + goals1
        nation_data.loc[team1, 'total_P'], nation_data.loc[team2, 'total_P'] = \
            nation_data.loc[team1, 'total_P'] + 1, nation_data.loc[team2, 'total_P'] + 1

        player_data.loc[player_data.Country == team1, 'P'], player_data.loc[player_data.Country == team2, 'P'] = \
            player_data.loc[player_data.Country == team1, 'P'] + 1, \
            player_data.loc[player_data.Country == team2, 'P'] + 1
        player_data.loc[player_data.Country == team1, 'WC_P'], player_data.loc[player_data.Country == team2, 'WC_P'] = \
            player_data.loc[player_data.Country == team1, 'WC_P'] + 1, \
            player_data.loc[player_data.Country == team2, 'WC_P'] + 1

    return player_data, nation_data, section_data
