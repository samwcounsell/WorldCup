import pandas as pd
import time
from MatchSim import TLKO_simulation, GRP5, GRP6HA
from GroupDraw import GD5

# Start of alphabet is defined to name groups within the function
alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]


def afc(time_delay, player_data, nation_data, test):
    # Importing host inside function so as to not generate a new host
    from Host import host_selector

    # Reading in the AFC teams and sorting by world rank
    afc_data = pd.read_csv("AFC.csv")
    afc_data = afc_data.sort_values(by=['World_Rank'])

    # Listing possible AFC hosts, then calling the host nation
    AFChosts = ["China", "India", "Japan", "Qatar", "South Korea", "Saudi Arabia", "Australia"]
    host, hostdf = host_selector()

    # Pulling last 12 teams to play in round 1, then removing them from the main data set
    round1 = afc_data.iloc[34:46]
    round1 = round1.sample(frac=1)
    round1 = round1.set_index([pd.Index([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]), ])
    afc_data = afc_data.iloc[:34, :]

    print("\nWELCOME TO AFC WORLD CUP QUALIFYING\n")
    print("ROUND 1\n")

    # Running the two-leg knockout function, inputs: number of matches, dataset of participating teams, dataset to
    # attach winners to, time delay
    player_data, nation_data, afc_data = TLKO_simulation(6, time_delay, player_data, nation_data, round1, afc_data)

    # Checking the user wants to continue
    if test != "Y":
        input("Press enter to continue: ")

    # Resorting the teams by world rank, the reindexing
    afc_data = afc_data.sort_values(by=['World_Rank'])
    afc_data = afc_data.reset_index()
    afc_data = afc_data.drop(['index'], axis=1)

    # Drawing the 5 pots, then frac = 1 randomises the teams so the draw is random
    pot1 = afc_data.iloc[:8, :]
    pot2 = afc_data.iloc[8:16, :]
    pot3 = afc_data.iloc[16:24, :]
    pot4 = afc_data.iloc[24:32, :]
    pot5 = afc_data.iloc[32:40, :]
    pot1 = pot1.sample(frac=1)
    pot2 = pot2.sample(frac=1)
    pot3 = pot3.sample(frac=1)
    pot4 = pot4.sample(frac=1)
    pot5 = pot5.sample(frac=1)

    potbig = pd.concat([pot1, pot2, pot3, pot4, pot5])

    print("\nROUND 2\n")

    # Simulating the 8 groups of 5 teams, hence i in range 8
    for i in range(8):
        # Calling the group draw function which draws the current group
        group = GD5(i, 8, potbig)
        print("\nGroup", alphabet[i])
        print(group.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False))

        # Running the matches for the current group, the function returns the final group table
        player_data, nation_data, group = GRP5(time_delay, player_data, nation_data, group)

        # Sorting the group by points, then goal difference etc
        time.sleep(time_delay * 5)
        group = group.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])

        # Reindexing the group again, so we can pull the top two teams
        group = group.reset_index()
        group = group.drop(['index'], axis=1)
        print("\n", group.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False),
              "\n")

        # Pulling the winner and runner up and attaching them to the main data frame
        round3 = group.iloc[0:2, :]
        afc_data = pd.concat([afc_data, round3])

        if test != "Y":
            input("Press enter to continue: ")

        print()

    # Removing the 40 teams that went into the previous stage, leaving us with only the top 2 from each group
    afc_data = afc_data.iloc[40:, :]

    # Separating the group winners
    groupwinner = afc_data.loc[0, :]
    print(groupwinner)

    # Selecting then sorting the runners up and then rejoining them to the winners
    runnerup = afc_data.loc[1, :]
    runnerup = runnerup.sort_values(by=['Pts'], ascending=False)
    hostcheck = pd.concat([groupwinner, runnerup])
    print(hostcheck)

    # Making sure the host doesn't qualify by removing them if they're in the dataset, then selecting the winners and
    # 4 best runners up to move onto round 3
    if host in AFChosts:
        hostcheck = hostcheck[hostcheck.Country != host]
    afc_data = hostcheck.iloc[:12, :]

    # Sorting and reindexing again
    afc_data = afc_data.sort_values(by=['World_Rank'])
    afc_data = afc_data.reset_index()
    afc_data = afc_data.drop(['index'], axis=1)

    # Redrawing and randomising pots
    pot1 = afc_data.iloc[:2, :]
    pot2 = afc_data.iloc[2:4, :]
    pot3 = afc_data.iloc[4:6, :]
    pot4 = afc_data.iloc[6:8, :]
    pot5 = afc_data.iloc[8:10, :]
    pot6 = afc_data.iloc[10:12, :]
    pot1 = pot1.sample(frac=1)
    pot2 = pot2.sample(frac=1)
    pot3 = pot3.sample(frac=1)
    pot4 = pot4.sample(frac=1)
    pot5 = pot5.sample(frac=1)
    pot6 = pot6.sample(frac=1)

    # Rejoining pots, resetting stats for the next group stage
    afc_data = pd.concat([pot1, pot2, pot3, pot4, pot5, pot6])
    afc_data[['P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']] = 0

    # Drawing the 2 groups of 6, then setting the index
    groupA = afc_data.iloc[[0, 2, 4, 6, 8, 10], :]
    groupA = groupA.set_index([pd.Index([0, 1, 2, 3, 4, 5]), ])
    groupA.name = 'GROUP A'
    groupB = afc_data.iloc[[1, 3, 5, 7, 9, 11], :]
    groupB = groupB.set_index([pd.Index([0, 1, 2, 3, 4, 5]), ])
    groupB.name = 'GROUP B'

    # Making a dummy one row data frame to attach winners to
    qualified = afc_data.iloc[:1, :]

    print(groupA, groupB)

    print("\nROUND 3\n")

    # Running round 3, function not used to draw groups as it is only 2 groups
    for group_data in [groupA, groupB]:
        print(group_data.name, "\n")
        print(group_data)
        time.sleep(time_delay * 5)

        # Running the matches for the current group_data, as seen in round 2
        player_data, nation_data, group_data = GRP6HA(time_delay, player_data, nation_data, group_data)
        time.sleep(time_delay * 5)

        # Sorting and then displaying current group_data, as seen in round 2
        group_data = group_data.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])
        group_data = group_data.reset_index()
        group_data = group_data.drop(['index'], axis=1)
        print("\n", group_data.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False),
              "\n")

        # Top 2 become winners and qualify straight to world cup, they are attached to dummy data frame
        winners = group_data.iloc[0:2, :]
        qualified = pd.concat([qualified, winners])

        # 3rd place teams get reattached to main data frame for round 4
        round4 = group_data.iloc[2:3, :]
        afc_data = pd.concat([afc_data, round4])

        if test != "Y":
            input("Press enter to continue: ")

    # Cutting main data frame down to only round 4 teams and reindexing
    afc_data = afc_data.iloc[12:, :]
    afc_data = afc_data.set_index([pd.Index([0, 1]), ])

    print("\nROUND 4\n")

    # ict(Inter-continental team) runs the two-legged knockout, as seen in round 1, then leaves only the winner in
    # the data frame
    player_data, nation_data, ict = TLKO_simulation(1, time_delay, player_data, nation_data, afc_data, afc_data)
    ict = ict.iloc[2:, :]

    # Removing the dummy row from the data frame leaving the teams qualified directly for the world cup
    qualified = qualified.iloc[1:, :]

    # Printing all the qualified teams, checks for host and displays them if they're in AFC
    print("\nQUALIFIED FOR WORLD CUP\n")
    print(qualified.to_string(columns=['Country'], index=False))
    print("\nQUALIFIED FOR INTERCONTINENTAL PLAYOFF\n")
    print(ict.to_string(columns=['Country'], index=False))
    if host in AFChosts:
        print("\nQUALIFIED AS HOST\n")
        print(host)

    # Returns the team data for the qualified and ict team to the main world cup

    # AFC Plotly Test

    # player_data = player_data.sort_values(by=['Goals'], ascending=False)
    # player_data['Goals_Per_Game'] = player_data['Goals'] / player_data['P']
    # player_data['Assists_Per_Game'] = player_data['Assists'] / player_data['P']
    # player_data = player_data.sort_values(by=['Goals_Per_Game'], ascending=False)
    # print(player_data.to_string(columns=['P', 'Goals', 'Goals_Per_Game']))

    # nation_data = nation_data.sort_values(by=['total_GF'], ascending=False)
    # nation_data['GF_Per_Game'] = nation_data['total_GF'] / nation_data['total_P']
    # nation_data['GA_Per_Game'] = nation_data['total_GA'] / nation_data['total_P']
    # nation_data = nation_data.sort_values(by=['GF_Per_Game'], ascending=False)
    # print(nation_data)

    # afc_player_data = player_data[player_data['Confederation'] == 'AFC']
    # afc_player_table_data = afc_player_data.reset_index()
    # afc_nation_data = nation_data[nation_data['Confederation'] == 'AFC']
    # print(afc_player_data.to_string(columns=['P', 'Goals', 'Assists', 'Goals_Per_Game', 'Assists_Per_Game']))

    input("\nEnd of AFC qualifiers, press enter to continue to the next Confederation: ")

    return player_data, nation_data, qualified, ict
