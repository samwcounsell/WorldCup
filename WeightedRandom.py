import random
import pandas as pd
from Commentary import goal, prematch
from scipy.stats import bernoulli
import time

player_data = pd.read_csv("AFCPlayers.csv")
player_data = player_data.set_index('Name')

# player_list = player_data['Name'].tolist()
player_list = player_data.index.tolist()
attack_list = player_data['Attack'].to_numpy()
total_attack = attack_list.sum()

team1 = "Pakistan"
team2 = "India"
a1, d1, a2, d2 = 1.15, 1.1, 0.95, 1
k = 2


# Inputs: player_data, number of legs, teams, attack/defense ratings
def Home_And_Away(player_data, k, team1, team2, a1, d1, a2, d2):
    # The * 1.2 gives the home team and advantage, calculates goal scoring chances
    if k == 1:
        p1 = 0.014 * (a1 / d2) * 1.2
        p2 = 0.014 * (a2 / d1)
    if k == 2:
        p1 = 0.014 * (a1 / d2)
        p2 = 0.014 * (a2 / d1) * 1.2

    # Getting the required match data in list form
    team1player_data = player_data[(player_data.Country == team1)]
    team2player_data = player_data[(player_data.Country == team2)]
    player_list1 = team1player_data.index.tolist()
    attack_list1 = team1player_data['Attack'].to_numpy()
    player_list2 = team2player_data.index.tolist()
    attack_list2 = team2player_data['Attack'].to_numpy()

    # Resetting goals to 0 - 0
    goals1 = 0
    goals2 = 0
    print("\n")

    # Calling the prematch commentary
    prematch()

    # Simulating the actual game
    for i in range(90):

        time.sleep(0.1)
        Ber1 = bernoulli.rvs(p1, size=1)
        Ber2 = bernoulli.rvs(p2, size=1)
        goals1 = goals1 + Ber1
        goals2 = goals2 + Ber2

        # What happens if there is a goal
        if (sum(Ber1) + sum(Ber2)) != 0:

            if sum(Ber1) == 1:
                # Calls the commentary line for after a goal
                goal_scorer = goal()

                # Uses a weighted sum to choose goal scorer
                player = (random.choices(player_list1, weights=attack_list1, k=1))

                # Print goal scorer, ','.join(player) converts player to string so no square brackets
                print("GOAL!", ','.join(player), i, "'", "Score: ", goals1, " - ", goals2)

                # Adds a goal to the players overall tally in player_data
                player_data.loc[player, 'Goals'] = player_data.loc[player, 'Goals'] + 1
                print(goal_scorer, "\n")

            if sum(Ber2) == 1:
                goal_scorer = goal()
                player = (random.choices(player_list2, weights=attack_list2, k=1))
                print("GOAL!", ','.join(player), i, "'", "Score: ", goals1, " - ", goals2)
                player_data.loc[player, 'Goals'] = player_data.loc[player, 'Goals'] + 1
                print(goal_scorer, "\n")

        # Displaying half/full time
        if i == 44:
            print("HALF TIME", goals1, " - ", goals2, "\n")
        if i == 89:
            print("FULL TIME", goals1, " - ", goals2)

    # Return: player_data, the number of goals scored
    return player_data, goals1, goals2


Test_Match = Home_And_Away(player_data, k, team1, team2, a1, d1, a2, d2)
