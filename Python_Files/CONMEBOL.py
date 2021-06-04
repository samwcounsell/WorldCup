import pandas as pd
from Round_Simulation import CONMEBOL


def conmebol(time_delay, player_data, nation_data):
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

    input("End of CONMEBOL qualifiers, press enter to continue to the next Confederation: ")

    return player_data, nation_data, qualified, ict
