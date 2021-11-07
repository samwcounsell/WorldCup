import pandas as pd
from Round_Simulation import TLKO_simulation, GRP5, GRP8HA
from Group_Draws import GD5


def concacaf_f(time_delay, player_data, nation_data, awards_data, test, runs, host):
    from Host import host_selector

    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]

    pot_data = pd.read_csv("CONCACAF.csv")
    CONCACAFhosts = ["Mexico", "USA"]
    #host, hostdf = host_selector()

    round1 = pot_data.iloc[5:36]
    top5 = pot_data.iloc[:5, :]

    print("\nWELCOME TO CONCACAF WORLD CUP QUALIFYING\n")
    print("ROUND 1")

    pot1 = round1.iloc[:6, :]
    pot2 = round1.iloc[6:12, :]
    pot3 = round1.iloc[12:18, :]
    pot4 = round1.iloc[18:24, :]
    pot5 = round1.iloc[24:30, :]

    pot1 = pot1.sample(frac=1)
    pot2 = pot2.sample(frac=1)
    pot3 = pot3.sample(frac=1)
    pot4 = pot4.sample(frac=1)
    pot5 = pot5.sample(frac=1)
    pot = pd.concat([pot1, pot2, pot3, pot4, pot5])
    pot = pot.reset_index()
    pot = pot.drop(['index'], axis=1)

    for i in range(6):
        group = GD5(i, 6, pot)
        print("\nGroup", alphabet[i])
        print(group.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False), "\n")

        player_data, nation_data, group = GRP5(time_delay, player_data, nation_data, group)
        group = group.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])
        group = group.reset_index()
        group = group.drop(['index'], axis=1)
        winner = group.iloc[0:1, :]
        pot = pd.concat([pot, winner])

        print("\n", group.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False),
              "\n")

        if test != "Y":
            input("Press enter to continue: ")

    pot = pot.iloc[30:, :]
    # print(pot)
    pot = pot.reset_index()
    pot = pot.drop(['index'], axis=1)

    print("\nROUND 2\n")

    a = 3
    player_data, nation_data, round2 = TLKO_simulation(a, time_delay, player_data, nation_data, pot, pot)
    round2 = round2.iloc[6:, :]
    # print(round2)

    round3 = pd.concat([top5, round2])
    round3 = round3.reset_index()
    round3 = round3.drop(['index'], axis=1)
    round3[['P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']] = 0

    if test != "Y":
        input("Press enter to continue: ")

    print("\nROUND 3\n")

    print(round3.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False))

    player_data, nation_data, group = GRP8HA(time_delay, player_data, nation_data, round3)

    group = group.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])
    group = group.reset_index()
    group = group.drop(['index'], axis=1)
    print("\n", group.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False), "\n")

    if host in CONCACAFhosts:
        group = group[group.Country != host]

    qualified = group.iloc[:3, :]
    print("\nQUALIFIED FOR THE WORLD CUP NORTH AND CENTRAL AMERICA")
    print("\n", qualified.to_string(columns=['Country'], index=False, header=False))
    print("\nQUALIFIED FOR INTERCONTINENTAL PLAYOFF")
    ict = group.iloc[3:4, :]
    print("\n", ict.to_string(columns=['Country'], index=False, header=False))
    if host in CONCACAFhosts:
        print("\nQUALIFIED AS HOST\n")
        print(host)

    # The Awards
    concacaf_player_data = player_data.loc[player_data['Confederation'] == 'CONCACAF']

    # Ordering data frame for the Golden Boot winner
    concacaf_player_data = concacaf_player_data.sort_values(by=['Goals', 'Assists'], ascending=False)
    concacaf_player_data = concacaf_player_data.reset_index()
    # Isolating the Golden Boot winner
    concacaf_Golden_Boot = concacaf_player_data.loc[0, 'Name']
    concacaf_player_data = concacaf_player_data.set_index('Name')
    concacaf_GBN = concacaf_player_data.loc[concacaf_Golden_Boot, 'Goals']

    # Ordering data frame for the Golden Playmaker winner
    concacaf_player_data = concacaf_player_data.sort_values(by=['Assists', 'Goals'], ascending=False)
    concacaf_player_data = concacaf_player_data.reset_index()
    # Isolating the Golden Playmaker winner
    concacaf_Golden_Playmaker = concacaf_player_data.loc[0, 'Name']
    concacaf_player_data = concacaf_player_data.set_index('Name')
    concacaf_GPN = concacaf_player_data.loc[concacaf_Golden_Playmaker, 'Assists']
    
    # Updating the Award Winners database
    concacaf_award_1 = concacaf_Golden_Boot + " with " + str(concacaf_GBN) + " Goals"
    concacaf_award_2 = concacaf_Golden_Playmaker + " with " + str(concacaf_GPN) + " Assists"
    awards_data.at['CONCACAF Golden Boot'] = concacaf_award_1
    awards_data.at['CONCACAF Golden Playmaker'] = concacaf_award_2

    # Displaying the Award Winners
    print("\nAWARDS")
    print("\nThe CONCACAF Golden Boot Winner is", concacaf_Golden_Boot, "with", concacaf_GBN, "Goals")
    print("\nThe CONCACAF Golden Playmaker Winner is", concacaf_Golden_Playmaker, "with", concacaf_GPN, "Assists")

    if runs == 1:
        input("\nEnd of CONCACAF qualifiers, press enter to continue to the next Confederation: ")

    return player_data, nation_data, qualified, ict, awards_data
