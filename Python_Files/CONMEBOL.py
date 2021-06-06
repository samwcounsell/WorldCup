import pandas as pd
from Round_Simulation import CONMEBOL


def conmebol(time_delay, player_data, nation_data, awards_data):
    from Host import host_selector

    pot_data = pd.read_csv("CONMEBOL.csv")
    pot_data = pot_data.sort_values(by=['World_Rank'])

    conmebol_hosts = ["Brazil", "Argentina"]
    host, host_df = host_selector()

    group = pot_data
    print("\n", group.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False), "\n")

    player_data, nation_data, group = CONMEBOL(time_delay, player_data, nation_data, group)
    group = group.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])
    group = group.reset_index()
    group = group.drop(['index'], axis=1)

    print("\n", group.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False), "\n")

    if host in conmebol_hosts:
        group = group[group.Country != host]

    qualified = group.iloc[:4, :]
    ict = group.iloc[4:5, :]

    print("QUALIFIED FOR THE WORLD CUP FROM SOUTH AMERICA\n")
    print(qualified.to_string(columns=['Country'], index=False, header=False))
    print("\nQUALIFIED FOR INTERCONTINENTAL PLAYOFF\n")
    print(ict.to_string(columns=['Country'], index=False, header=False), "\n")
    if host in conmebol_hosts:
        print("\nQUALIFIED AS HOST\n")
        print(host)

    # The Awards
    conmebol_player_data = player_data.loc[player_data['Confederation'] == 'CONMEBOL']

    # Ordering data frame for the Golden Boot winner
    conmebol_player_data = conmebol_player_data.sort_values(by=['Goals', 'Assists'], ascending=False)
    conmebol_player_data = conmebol_player_data.reset_index()
    # Isolating the Golden Boot winner
    conmebol_Golden_Boot = conmebol_player_data.loc[0, 'Name']
    conmebol_player_data = conmebol_player_data.set_index('Name')
    conmebol_GBN = conmebol_player_data.loc[conmebol_Golden_Boot, 'Goals']

    # Ordering data frame for the Golden Playmaker winner
    conmebol_player_data = conmebol_player_data.sort_values(by=['Assists', 'Goals'], ascending=False)
    conmebol_player_data = conmebol_player_data.reset_index()
    # Isolating the Golden Playmaker winner
    conmebol_Golden_Playmaker = conmebol_player_data.loc[0, 'Name']
    conmebol_player_data = conmebol_player_data.set_index('Name')
    conmebol_GPN = conmebol_player_data.loc[conmebol_Golden_Playmaker, 'Assists']
    
    # Updating the Award Winners database
    conmebol_award_1 = conmebol_Golden_Boot + " with " + str(conmebol_GBN) + " Goals"
    conmebol_award_2 = conmebol_Golden_Playmaker + " with " + str(conmebol_GPN) + " Assists"
    awards_data.at['CONMEBOL Golden Boot'] = conmebol_award_1
    awards_data.at['CONMEBOL Golden Playmaker'] = conmebol_award_2

    # Displaying the Award Winners
    print("\nAWARDS")
    print("\nThe CONMEBOL Golden Boot Winner is", conmebol_Golden_Boot, "with", conmebol_GBN, "Goals")
    print("\nThe CONMEBOL Golden Playmaker Winner is", conmebol_Golden_Playmaker, "with", conmebol_GPN, "Assists")

    input("\nEnd of CONMEBOL qualifiers, press enter to continue to the next Confederation: ")

    return player_data, nation_data, qualified, ict, awards_data
