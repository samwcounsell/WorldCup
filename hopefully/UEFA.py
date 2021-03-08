import pandas as pd
from MatchSim import TLKO_simulation, GRP5, GRP6HA
from GroupDraw import GD5, GD6


def uefa(time_delay, player_data, nation_data):
    from Host import host_selector
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]

    pot = pd.read_csv("UEFA.csv")

    UEFAhosts = ["France", "England", "Spain", "Italy", "Germany", "Russia"]
    host, hostdf = host_selector()
    print(host)

    if host in UEFAhosts:
        pot = pot[pot.Country != host]

    pot1 = pot.iloc[:10, :]
    pot2 = pot.iloc[10:20, :]
    pot3 = pot.iloc[20:30, :]
    pot4 = pot.iloc[30:40, :]
    pot5 = pot.iloc[40:50, :]
    pot6 = pot.iloc[50:, :]

    pot1 = pot1.sample(frac=1)
    pot2 = pot2.sample(frac=1)
    pot3 = pot3.sample(frac=1)
    pot4 = pot4.sample(frac=1)
    pot = pd.concat([pot1, pot2, pot3, pot4, pot5, pot6])

    print("\nWELCOME TO UEFA WORLD CUP QUALIFYING")
    print("\nROUND 1")

    if host in UEFAhosts:
        for i in range(4):
            group6 = GD6(i, 10, pot)
            print("\nGroup", alphabet[i])
            print("\n", group6.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False),
                  "\n")

            player_data, nation_data, group6 = GRP6HA(time_delay, player_data, nation_data, group6)
            group6 = group6.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])
            group6 = group6.reset_index()
            group6 = group6.drop(['index'], axis=1)
            round2 = group6.iloc[0:2, :]
            pot = pd.concat([pot, round2])

            print("\n", group6.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False),
                  "\n")

            uc = input("Press enter to continue: ")  # uc = user continue

        for i in range(6):
            group5 = GD5(i + 4, 10, pot)
            print("\nGroup", alphabet[i + 4])
            print("\n", group5.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False),
                  "\n")

            player_data, nation_data, group5 = GRP6HA(time_delay, player_data, nation_data, group5)
            group5 = group5.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])
            group5 = group5.reset_index()
            group5 = group5.drop(['index'], axis=1)
            round2 = group5.iloc[0:2, :]
            pot = pd.concat([pot, round2])

            print("\n", group5.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False),
                  "\n")

            uc = input("Press enter to continue: ")  # uc = user continue
        pot = pot.iloc[54:, :]

    if host not in UEFAhosts:
        for i in range(5):
            group6 = GD6(i, 10, pot)
            print("\nGroup", alphabet[i])
            print("\n", group6.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False),
                  "\n")

            player_data, nation_data, group6 = GRP6HA(time_delay, player_data, nation_data, group6)
            group6 = group6.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])
            group6 = group6.reset_index()
            group6 = group6.drop(['index'], axis=1)
            round2 = group6.iloc[0:2, :]
            pot = pd.concat([pot, round2])

            print("\n", group6.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False),
                  "\n")

            uc = input("Press enter to continue: ")  # uc = user continue

        for i in range(5):
            group5 = GD5(i + 5, 10, pot)
            print("\nGroup", alphabet[i + 4])
            print("\n", group5.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False),
                  "\n")

            player_data, nation_data, group5 = GRP5(time_delay, player_data, nation_data, group5)
            group5 = group5.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])
            group5 = group5.reset_index()
            group5 = group5.drop(['index'], axis=1)
            round2 = group5.iloc[0:2, :]
            pot = pd.concat([pot, round2])

            print("\n", group5.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False),
                  "\n")

            uc = input("Press enter to continue: ")  # uc = user continue
        pot = pot.iloc[55:, :]

    print(pot[['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']])
    pot[['P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']] = 0

    potbig = pot.loc[0, :]
    runnerup = pot.loc[1, :]

    # Round2

    for i in range(2):
        group = GD5(i, 2, runnerup)
        print("\nGroup", alphabet[i])
        print("\n", group.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False),
              "\n")

        player_data, nation_data, group = GRP6HA(time_delay, player_data, nation_data, group)
        group = group.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])
        group = group.reset_index()
        group = group.drop(['index'], axis=1)
        round3 = group.iloc[0:2, :]
        potbig = pd.concat([potbig, round3])

        print("\n", group.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False),
              "\n")

        uc = input("Press enter to continue: ")  # uc = user continue

    # print(potbig[['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']], "\n")
    qualified = potbig.loc[0, :]
    playoff = potbig.loc[1, :]

    playoff = playoff.reset_index()
    playoff = playoff.drop(['index'], axis=1)

    print("\n")

    player_data, nation_data, qualified = TLKO_simulation(1, time_delay, player_data, nation_data, playoff, qualified)
    print("QUALIFIED FOR THE WORLD CUP\n")
    print(qualified.to_string(columns=['Country'], index=False))
    if host in UEFAhosts:
        print("\nQUALIFIED AS HOST\n")
        print(host)

    return player_data, nation_data, qualified
