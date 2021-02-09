from scipy.stats import binom, bernoulli
import numpy as np
import pandas as pd
import time
import random

# imports the AFC nations csv and sorts it by world rank
#afcpot_data = pd.read_csv(r"C:\Users\samwc\PycharmProjects\WorldCup\AFC.csv")  # Sam file location
#afcpot_data = pd.read_csv(r"/Users/keanerussell/Documents/Documents/Home/Python/AFC.csv")  # Keane file location
afcpot_data = afcpot_data.sort_values(by=['World_Rank'])

# Round 1

# selects the 12 lowest ranked teams, randomises the order and renames the rows from 0:11, this can be made prettier but I cba yet
afcround1 = afcpot_data.iloc[34:46]
afcround1 = afcround1.sample(frac=1)
afcround1 = afcround1.set_index([pd.Index([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]), ])
# cuts the 12 lowest ranked teams from the original dataframe
afcpot_data = afcpot_data.iloc[:34, :]

# a in range 6 represents the 6 knockout matches, the matches are played by teams with row name 0v1, 2v3, 4v5..., hence why we randomise the order of the dataframe
for a in range(6):
    team1 = afcround1.loc[(2 * a), 'Country']  # pulls team with row names 0,2,4,6,8,10 (2 x a = (0,1,2,3,4,5))
    team2 = afcround1.loc[
        (2 * a + 1), 'Country']  # pulls team with row names 1,3,5,7,9,11 ((2 x a) = (0,1,2,3,4,5) + 1)
    a1, d1 = afcround1.loc[(2 * a), 'Attack'], afcround1.loc[(2 * a), 'Defence']
    a2, d2 = afcround1.loc[(2 * a), 'Attack'], afcround1.loc[(2 * a), 'Defence']
    p1 = 0.014 * (a1 / d2)  # probability of team1 scoring each minute
    p2 = 0.014 * (a2 / d1)
    Ber1 = bernoulli.rvs(p1, size=90)  # bernoulli run 90 times, once per minute, if result is a 1 the team scored
    Ber2 = bernoulli.rvs(p2, size=90)
    goals1 = sum(Ber1)  # adds up all the goals to get the final score for team1
    goals2 = sum(Ber2)
    print(team1, goals1, " - ", goals2, team2)  # prints result

    # if team1 wins it adds team1 back to the data frame, once this happens for all 6 games, the data frame becomes 40 rows, which is how many teams
    # are in then next round (34 auto-qualify + 6 winners of these matches)
    if goals1 > goals2:
        winner = team1
        df = afcround1.iloc[(2 * a):(2 * a + 1), :]
        afcpot_data = pd.concat([afcpot_data, df])

    if goals1 < goals2:
        winner = team2
        df = afcround1.iloc[(2 * a + 1):(2 * a + 2), :]
        afcpot_data = pd.concat([afcpot_data, df])

    # if goals are level after 90 minutes, does 30 minutes of extra time
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

        # if goals are level after extra time each team takes 5 penalties
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

            # if penalites are level are 5, teams enter sudden death, the loop only breaks if one team scores and the other does not
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

# Round 2

# Reorders the teams by World Rank, using reset.index adds an extra index column that the .drop removes
afcpot_data = afcpot_data.sort_values(by=['World_Rank'])
afcpot_data = afcpot_data.reset_index()
afcpot_data = afcpot_data.drop(['index'], axis=1)
# print(afcpot_data)

# Splits the dataframe into 5 pots
afcpot1 = afcpot_data.iloc[:8, :]
afcpot2 = afcpot_data.iloc[8:16, :]
afcpot3 = afcpot_data.iloc[16:24, :]
afcpot4 = afcpot_data.iloc[24:32, :]
afcpot5 = afcpot_data.iloc[32:40, :]

# Randomises all the pots
afcpot1 = afcpot1.sample(frac=1)
afcpot2 = afcpot2.sample(frac=1)
afcpot3 = afcpot3.sample(frac=1)
afcpot4 = afcpot4.sample(frac=1)
afcpot5 = afcpot5.sample(frac=1)

# Puts all the pots back together
afcpotbig = pd.concat([afcpot1, afcpot2, afcpot3, afcpot4, afcpot5])

# Draws the 8 groups, since it's now ordered by pots (which have been randomised) it is taking one random team from each pot to form a group
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

# Runs the 8 groups, the loops in order from out to in: for group (each group), for k (home and away legs), for i,j (the two teams playing each match)
# So the most inner loop is just a match simulated between team i and team j, for all the specified combinations of i and j, these games are played twice
# when k == 1, the LHS team is home, k == 2 the RHS team is home, this is done for each group from group A to group F
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
                # print(team1, "xG/m", format(p1, ".4f"), " xG/norm", format((p1 / 0.014), ".4f"), "xG_total",
                # format((p1 * 90), ".4f"), "sd", format(((p1 * (1 - p1) * 90) ** 0.5), ".4f"))
                # print(team2, "xG/m", format(p2, ".4f"), " xG/norm", format((p2 / 0.014), ".4f"), "xG_total",
                # format((p2 * 90), ".4f"), "sd", format(((p2 * (1 - p2) * 90) ** 0.5), ".4f"))
            time.sleep(0.3)
    time.sleep(1)
    print("################")
