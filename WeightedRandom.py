import random
import pandas as pd
from Commentary import goal, prematch
from Players import gs
from scipy.stats import binom, bernoulli
import time

df = pd.read_csv("AFCPlayers.csv")
df = df.set_index('Name')

# player_list = df['Name'].tolist()
player_list = df.index.tolist()
attack_list = df['Attack'].to_numpy()
total_attack = attack_list.sum()

team1 = "South Korea"
team2 = "Australia"
a1, d1, a2, d2 = 1.15, 1.1, 0.95, 1


# team1df = df[(df.Country == team1)]
# team2df = df[(df.Country == team2)]

# player_list1 = team1df['Name'].tolist()
# attack_list1 = team1df['Attack'].to_numpy()
# total_attack1 = attack_list1.sum()
# player_list2 = team2df['Name'].tolist()
# attack_list2 = team2df['Attack'].to_numpy()
# total_attack2 = attack_list2.sum()

# print(random.choices(player_list1, weights=attack_list1, k=1))

def TEST(team1, team2, a1, d1, a2, d2):
    p1 = 0.014 * (a1 / d2) * 1.2
    p2 = 0.014 * (a2 / d1)
    team1df = df[(df.Country == team1)]
    team2df = df[(df.Country == team2)]
    player_list1 = team1df.index.tolist()
    attack_list1 = team1df['Attack'].to_numpy()
    total_attack1 = attack_list1.sum()
    player_list2 = team2df.index.tolist()
    attack_list2 = team2df['Attack'].to_numpy()
    total_attack2 = attack_list2.sum()
    goals1 = 0
    goals2 = 0
    print("\n")
    prematch()
    for i in range(90):
        time.sleep(0.1)
        Ber1 = bernoulli.rvs(p1, size=1)
        Ber2 = bernoulli.rvs(p2, size=1)
        goals1 = goals1 + Ber1
        goals2 = goals2 + Ber2
        if (sum(Ber1) + sum(Ber2)) != 0:
            if sum(Ber1) == 1:
                line = goal()
                player = (random.choices(player_list1, weights=attack_list1, k=1))
                print("GOAL!", ','.join(player), i, "'", "Score: ", goals1, " - ", goals2)
                df.loc[player, 'Goals'] = df.loc[player, 'Goals'] + 1
                print(line, "\n")
            if sum(Ber2) == 1:
                line = goal()
                player = (random.choices(player_list2, weights=attack_list2, k=1))
                print("GOAL!", ','.join(player), i, "'", "Score: ", goals1, " - ", goals2)
                df.loc[player, 'Goals'] = df.loc[player, 'Goals'] + 1
                print(line, "\n")
        if i == 44:
            print("HALF TIME", goals1, " - ", goals2, "\n")
        if i == 89:
            print("FULL TIME", goals1, " - ", goals2)

yo = TEST(team1, team2, a1, d1, a2, d2)

#for i in range(100):
    #yo = TEST(team1, team2, a1, d1, a2, d2)

#print(df)
