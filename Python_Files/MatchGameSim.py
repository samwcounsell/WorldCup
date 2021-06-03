from scipy.stats import binom, bernoulli
import numpy as np
import pandas as pd
import time
import random
import sys
from Commentary import goal, prematch


def match_simulation(leg, time_delay, player_data, team1, team2, a1, d1, a2, d2):
    if leg == 1:
        p1 = 0.014 * (a1 / d2) * 1.2
        p2 = 0.014 * (a2 / d1)
    if leg == 2:
        p1 = 0.014 * (a1 / d2)
        p2 = 0.014 * (a2 / d1) * 1.2

    team1player_data = player_data[(player_data.Country == team1)]
    team2player_data = player_data[(player_data.Country == team2)]
    player_list1 = team1player_data.index.tolist()
    attack_list1 = team1player_data['Attack'].to_numpy()
    assist_list1 = team1player_data['Passing'].to_numpy()
    player_list2 = team2player_data.index.tolist()
    attack_list2 = team2player_data['Attack'].to_numpy()
    assist_list2 = team2player_data['Passing'].to_numpy()

    goals1 = 0
    goals2 = 0

    # print("\n")
    prematch()
    if leg == 1:
        print(team1, "v", team2, "\n")
    if leg == 2:
        print(team2, "v", team1, "\n")
    for i in range(90):
        time.sleep(time_delay)
        Ber1 = bernoulli.rvs(p1, size=1)
        Ber2 = bernoulli.rvs(p2, size=1)
        goals1 = goals1 + Ber1
        goals2 = goals2 + Ber2

        if (sum(Ber1) + sum(Ber2)) != 0:
            if sum(Ber1) == 1:
                line = goal()
                player = (random.choices(player_list1, weights=attack_list1, k=1))
                assister = (random.choices(player_list1, weights=assist_list1, k=1))
                if leg == 1:
                    print("GOAL!", ','.join(player), i, "'", "Score: ", team1, goals1, " - ", goals2, team2)
                if leg == 2:
                    print("GOAL!", ','.join(player), i, "'", "Score: ", team2, goals2, " - ", goals1, team1)
                player_data.loc[player, 'Goals'], player_data.loc[assister, 'Assists'] = player_data.loc[
                                                                                             player, 'Goals'] + 1, \
                                                                                         player_data.loc[
                                                                                             assister, 'Assists'] + 1
                print(line, "\n")
            if sum(Ber2) == 1:
                line = goal()
                player = (random.choices(player_list2, weights=attack_list2, k=1))
                assister = (random.choices(player_list2, weights=assist_list2, k=1))
                if leg == 1:
                    print("GOAL!", ','.join(player), i, "'", "Score: ", team1, goals1, " - ", goals2, team2)
                if leg == 2:
                    print("GOAL!", ','.join(player), i, "'", "Score: ", team2, goals2, " - ", goals1, team1)
                player_data.loc[player, 'Goals'], player_data.loc[assister, 'Assists'] = player_data.loc[
                                                                                             player, 'Goals'] + 1, \
                                                                                         player_data.loc[
                                                                                             assister, 'Assists'] + 1
                print(line, "\n")
        if i == 44:
            if leg == 1:
                print("HALF TIME", team1, goals1, " - ", goals2, team2, "\n")
            if leg == 2:
                print("HALF TIME", team2, goals2, " - ", goals1, team1, "\n")
        if i == 89:
            if leg == 1:
                print("FULL TIME", team1, goals1, " - ", goals2, team2, "\n")
            if leg == 2:
                print("FULL TIME", team2, goals2, " - ", goals1, team1, "\n")

    return player_data, goals1, goals2


def match_simulation_30(leg, time_delay, player_data, team1, team2, a1, d1, a2, d2):
    if leg == 1:
        p1 = 0.014 * (a1 / d2) * 1.2
        p2 = 0.014 * (a2 / d1)
    if leg == 2:
        p1 = 0.014 * (a1 / d2)
        p2 = 0.014 * (a2 / d1) * 1.2

    team1player_data = player_data[(player_data.Country == team1)]
    team2player_data = player_data[(player_data.Country == team2)]
    player_list1 = team1player_data.index.tolist()
    attack_list1 = team1player_data['Attack'].to_numpy()
    assist_list1 = team1player_data['Passing'].to_numpy()
    player_list2 = team2player_data.index.tolist()
    attack_list2 = team2player_data['Attack'].to_numpy()
    assist_list2 = team1player_data['Passing'].to_numpy()
    goals1 = 0
    goals2 = 0
    print("\n")
    prematch()
    for i in range(30):
        time.sleep(time_delay)
        Ber1 = bernoulli.rvs(p1, size=1)
        Ber2 = bernoulli.rvs(p2, size=1)
        goals1 = goals1 + Ber1
        goals2 = goals2 + Ber2
        if (sum(Ber1) + sum(Ber2)) != 0:
            if sum(Ber1) == 1:
                line = goal()
                player = (random.choices(player_list1, weights=attack_list1, k=1))
                assister = (random.choices(player_list1, weights=assist_list1, k=1))
                if leg == 1:
                    print("GOAL!", ','.join(player), i, "'", "Score: ", team1, goals1, " - ", goals2, team2)
                if leg == 2:
                    print("GOAL!", ','.join(player), i, "'", "Score: ", team2, goals2, " - ", goals1, team1)
                player_data.loc[player, 'Goals'], player_data.loc[assister, 'Assists'] = player_data.loc[
                                                                                             player, 'Goals'] + 1, \
                                                                                         player_data.loc[
                                                                                             assister, 'Assists'] + 1
                print(line, "\n")
            if sum(Ber2) == 1:
                line = goal()
                player = (random.choices(player_list2, weights=attack_list2, k=1))
                assister = (random.choices(player_list2, weights=assist_list2, k=1))
                if leg == 1:
                    print("GOAL!", ','.join(player), i, "'", "Score: ", team1, goals1, " - ", goals2, team2)
                if leg == 2:
                    print("GOAL!", ','.join(player), i, "'", "Score: ", team2, goals2, " - ", goals1, team1)
                player_data.loc[player, 'Goals'], player_data.loc[assister, 'Assists'] = player_data.loc[
                                                                                             player, 'Goals'] + 1, \
                                                                                         player_data.loc[
                                                                                             assister, 'Assists'] + 1
                print(line, "\n")
        if i == 14:
            if leg == 1:
                print("HALF TIME", team1, goals1, " - ", goals2, team2, "\n")
            if leg == 2:
                print("HALF TIME", team2, goals2, " - ", goals1, team1, "\n")
        if i == 29:
            if leg == 1:
                print("FULL TIME", team1, goals1, " - ", goals2, team2, "\n")
            if leg == 2:
                print("FULL TIME", team2, goals2, " - ", goals1, team1, "\n")

    return player_data, goals1, goals2


def match_simulation_wc(time_delay, player_data, team1, team2, a1, d1, a2, d2):
    p1 = 0.014 * (a1 / d2)
    p2 = 0.014 * (a2 / d1)

    print("\nKICK OFF\n")

    team1player_data = player_data[(player_data.Country == team1)]
    team2player_data = player_data[(player_data.Country == team2)]
    player_list1 = team1player_data.index.tolist()
    attack_list1 = team1player_data['Attack'].to_numpy()
    assist_list1 = team1player_data['Passing'].to_numpy()
    player_list2 = team2player_data.index.tolist()
    attack_list2 = team2player_data['Attack'].to_numpy()
    assist_list2 = team2player_data['Passing'].to_numpy()

    goals1 = 0
    goals2 = 0

    # print("\n")
    prematch()

    print(team1, "v", team2, "\n")

    for i in range(90):
        time.sleep(time_delay)
        Ber1 = bernoulli.rvs(p1, size=1)
        Ber2 = bernoulli.rvs(p2, size=1)
        goals1 = goals1 + Ber1
        goals2 = goals2 + Ber2

        if (sum(Ber1) + sum(Ber2)) != 0:
            if sum(Ber1) == 1:
                line = goal()
                player = (random.choices(player_list1, weights=attack_list1, k=1))
                assister = (random.choices(player_list1, weights=assist_list1, k=1))

                print("GOAL!", ','.join(player), i, "'", "Score: ", team1, goals1, " - ", goals2, team2)

                player_data.loc[player, 'Goals'], player_data.loc[assister, 'Assists'] = player_data.loc[
                                                                                             player, 'Goals'] + 1, \
                                                                                         player_data.loc[
                                                                                             assister, 'Assists'] + 1
                player_data.loc[player, 'WC_Goals'], player_data.loc[assister, 'WC_Assists'] = player_data.loc[
                                                                                                   player, 'WC_Goals'] + 1, \
                                                                                               player_data.loc[
                                                                                                   assister, 'WC_Assists'] + 1
                print(line, "\n")
            if sum(Ber2) == 1:
                line = goal()
                player = (random.choices(player_list2, weights=attack_list2, k=1))
                assister = (random.choices(player_list2, weights=assist_list2, k=1))

                print("GOAL!", ','.join(player), i, "'", "Score: ", team1, goals1, " - ", goals2, team2)

                player_data.loc[player, 'Goals'], player_data.loc[assister, 'Assists'] = player_data.loc[
                                                                                             player, 'Goals'] + 1, \
                                                                                         player_data.loc[
                                                                                             assister, 'Assists'] + 1
                player_data.loc[player, 'WC_Goals'], player_data.loc[assister, 'WC_Assists'] = player_data.loc[
                                                                                                   player, 'WC_Goals'] + 1, \
                                                                                               player_data.loc[
                                                                                                   assister, 'WC_Assists'] + 1
                print(line, "\n")
        if i == 44:
            print("HALF TIME", team1, goals1, " - ", goals2, team2, "\n")

        if i == 89:
            print("FULL TIME", team1, goals1, " - ", goals2, team2, "\n")

    return player_data, goals1, goals2


def match_simulation_30_wc(time_delay, player_data, team1, team2, a1, d1, a2, d2, goals1, goals2):
    p1 = 0.014 * (a1 / d2) * 1.2
    p2 = 0.014 * (a2 / d1)

    team1player_data = player_data[(player_data.Country == team1)]
    team2player_data = player_data[(player_data.Country == team2)]
    player_list1 = team1player_data.index.tolist()
    attack_list1 = team1player_data['Attack'].to_numpy()
    assist_list1 = team1player_data['Passing'].to_numpy()
    player_list2 = team2player_data.index.tolist()
    attack_list2 = team2player_data['Attack'].to_numpy()
    assist_list2 = team1player_data['Passing'].to_numpy()
    et_goals1 = 0
    et_goals2 = 0
    print("\nEXTRA TIME KICK OFF\n")
    for i in range(30):
        time.sleep(time_delay)
        Ber1 = bernoulli.rvs(p1, size=1)
        Ber2 = bernoulli.rvs(p2, size=1)
        goals1 = goals1 + Ber1
        goals2 = goals2 + Ber2
        if (sum(Ber1) + sum(Ber2)) != 0:
            if sum(Ber1) == 1:
                line = goal()
                player = (random.choices(player_list1, weights=attack_list1, k=1))
                assister = (random.choices(player_list1, weights=assist_list1, k=1))
                print("GOAL!", ','.join(player), i, "'", "Score: ", team1, goals1 + et_goals1, " - ",
                      goals2 + et_goals2, team2)
                player_data.loc[player, 'Goals'], player_data.loc[assister, 'Assists'] = player_data.loc[
                                                                                             player, 'Goals'] + 1, \
                                                                                         player_data.loc[
                                                                                             assister, 'Assists'] + 1
                player_data.loc[player, 'WC_Goals'], player_data.loc[assister, 'WC_Assists'] = player_data.loc[
                                                                                                   player, 'WC_Goals'] + 1, \
                                                                                               player_data.loc[
                                                                                                   assister, 'WC_Assists'] + 1
                print(line, "\n")
            if sum(Ber2) == 1:
                line = goal()
                player = (random.choices(player_list2, weights=attack_list2, k=1))
                assister = (random.choices(player_list2, weights=assist_list2, k=1))
                print("GOAL!", ','.join(player), i, "'", "Score: ", team1, goals1 + et_goals1, " - ",
                      goals2 + et_goals2, team2)
                player_data.loc[player, 'Goals'], player_data.loc[assister, 'Assists'] = player_data.loc[
                                                                                             player, 'Goals'] + 1, \
                                                                                         player_data.loc[
                                                                                             assister, 'Assists'] + 1
                player_data.loc[player, 'WC_Goals'], player_data.loc[assister, 'WC_Assists'] = player_data.loc[
                                                                                             player, 'WC_Goals'] + 1, \
                                                                                         player_data.loc[
                                                                                             assister, 'WC_Assists'] + 1
                print(line, "\n")
        if i == 14:
            print("ET HALF TIME", team1, goals1 + et_goals1, " - ", goals2 + et_goals2, team2, "\n")
        if i == 29:
            print("ET FULL TIME", team1, goals1 + et_goals1, " - ", goals2 + et_goals2, team2, "\n")

    return player_data, et_goals1, et_goals2
