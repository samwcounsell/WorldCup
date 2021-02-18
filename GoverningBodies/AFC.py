import pandas as pd
import time
from MatchSim import TLKO, GRP5, GRP6, GRP6HA

def afc():
    from Host import hosty

    pot_data = pd.read_csv("AFC.csv")
    pot_data = pot_data.sort_values(by=['World_Rank'])

    AFChosts = ["China", "India", "Japan", "Qatar", "South Korea", "Saudi Arabia"]
    host, hostdf = hosty()

    round1 = pot_data.iloc[34:46]
    round1 = round1.sample(frac=1)
    round1 = round1.set_index([pd.Index([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]), ])
    pot_data = pot_data.iloc[:34, :]

    print("\nWELCOME TO AFC WORLD CUP QUALIFYING\n")
    print("ROUND 1\n")

    a = 6
    pot_data = TLKO(a, round1, pot_data, 0.5)

    uc = input("Press enter to continue: ")  # uc = user continue

    pot_data = pot_data.sort_values(by=['World_Rank'])
    pot_data = pot_data.reset_index()
    pot_data = pot_data.drop(['index'], axis=1)

    pot1 = pot_data.iloc[:8, :]
    pot2 = pot_data.iloc[8:16, :]
    pot3 = pot_data.iloc[16:24, :]
    pot4 = pot_data.iloc[24:32, :]
    pot5 = pot_data.iloc[32:40, :]

    pot1 = pot1.sample(frac=1)
    pot2 = pot2.sample(frac=1)
    pot3 = pot3.sample(frac=1)
    pot4 = pot4.sample(frac=1)
    pot5 = pot5.sample(frac=1)

    potbig = pd.concat([pot1, pot2, pot3, pot4, pot5])

    groupA = potbig.iloc[[0, 8, 16, 24, 32], :]
    groupA = groupA.set_index([pd.Index([0, 1, 2, 3, 4]), ])
    groupA.name = 'GROUP A'
    groupB = potbig.iloc[[1, 9, 17, 25, 33], :]
    groupB = groupB.set_index([pd.Index([0, 1, 2, 3, 4]), ])
    groupB.name = 'GROUP B'
    groupC = potbig.iloc[[2, 10, 18, 26, 34], :]
    groupC = groupC.set_index([pd.Index([0, 1, 2, 3, 4]), ])
    groupC.name = 'GROUP C'
    groupD = potbig.iloc[[3, 11, 19, 27, 35], :]
    groupD = groupD.set_index([pd.Index([0, 1, 2, 3, 4]), ])
    groupD.name = 'GROUP D'
    groupE = potbig.iloc[[4, 12, 20, 28, 36], :]
    groupE = groupE.set_index([pd.Index([0, 1, 2, 3, 4]), ])
    groupE.name = 'GROUP E'
    groupF = potbig.iloc[[5, 13, 21, 29, 37], :]
    groupF = groupF.set_index([pd.Index([0, 1, 2, 3, 4]), ])
    groupF.name = 'GROUP F'
    groupG = potbig.iloc[[6, 14, 22, 30, 38], :]
    groupG = groupG.set_index([pd.Index([0, 1, 2, 3, 4]), ])
    groupG.name = 'GROUP G'
    groupH = potbig.iloc[[7, 15, 23, 31, 39], :]
    groupH = groupH.set_index([pd.Index([0, 1, 2, 3, 4]), ])
    groupH.name = 'GROUP H'

    print("\nROUND 2\n")

    for group in [groupA, groupB, groupC, groupD, groupE, groupF, groupG, groupH]:
        print(group.name, "\n")
        print(group.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False))
        time.sleep(1)

        group = GRP5(group)

        time.sleep(1)
        group = group.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])
        group = group.reset_index()
        group = group.drop(['index'], axis=1)
        print("\n", group.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False),
              "\n")

        round3 = group.iloc[0:2, :]
        pot_data = pd.concat([pot_data, round3])

        uc = input("Press enter to continue: ")  # uc = user continue

        print()

    ####### ROUND 3 ONWARDS BEWARE ############

    pot_data = pot_data.iloc[40:, :]

    groupwinner = pot_data.loc[0, :]

    runnerup = pot_data.loc[1, :]
    runnerup = runnerup.sort_values(by=['Pts'], ascending=False)
    hostcheck = pd.concat([groupwinner, runnerup])

    if host in AFChosts:
        hostcheck = hostcheck[hostcheck.Country != host]
    pot_data = hostcheck.iloc[:12, :]

    # runnerup = runnerup.iloc[:4, :]  # When using host feature # this line and the one below
    # pot_data = pd.concat([groupwinner, runnerup])

    pot_data = pot_data.sort_values(by=['World_Rank'])
    pot_data = pot_data.reset_index()
    pot_data = pot_data.drop(['index'], axis=1)

    pot1 = pot_data.iloc[:2, :]
    pot2 = pot_data.iloc[2:4, :]
    pot3 = pot_data.iloc[4:6, :]
    pot4 = pot_data.iloc[6:8, :]
    pot5 = pot_data.iloc[8:10, :]
    pot6 = pot_data.iloc[10:12, :]

    pot1 = pot1.sample(frac=1)
    pot2 = pot2.sample(frac=1)
    pot3 = pot3.sample(frac=1)
    pot4 = pot4.sample(frac=1)
    pot5 = pot5.sample(frac=1)
    pot6 = pot6.sample(frac=1)

    pot_data = pd.concat([pot1, pot2, pot3, pot4, pot5, pot6])
    pot_data[['P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']] = 0

    groupA = pot_data.iloc[[0, 2, 4, 6, 8, 10], :]
    groupA = groupA.set_index([pd.Index([0, 1, 2, 3, 4, 5]), ])
    groupA.name = 'GROUP A'
    groupB = pot_data.iloc[[1, 3, 5, 7, 9, 11], :]
    groupB = groupB.set_index([pd.Index([0, 1, 2, 3, 4, 5]), ])
    groupB.name = 'GROUP B'

    qualified = pot_data.iloc[:1, :]

    print("\nROUND 3\n")

    for group in [groupA, groupB]:
        print(group.name, "\n")
        print(group)
        # time.sleep(1)

        group = GRP6HA(group)
        # time.sleep(1)
        group = group.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])
        group = group.reset_index()
        group = group.drop(['index'], axis=1)
        print("\n", group.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False),
              "\n")

        top2 = group.iloc[0:2, :]
        qualified = pd.concat([qualified, top2])
        round4 = group.iloc[2:3, :]
        pot_data = pd.concat([pot_data, round4])

        uc = input("Press enter to continue: ")

    pot_data = pot_data.iloc[12:, :]
    pot_data = pot_data.set_index([pd.Index([0, 1]), ])

    print("\nROUND 4\n")

    ict = TLKO(1, pot_data, pot_data, 0.5)
    ict = ict.iloc[2:, :]
    qualified = qualified.iloc[1:, :]
    print("\nQUALIFIED FOR WORLD CUP\n")
    print(qualified.to_string(columns=['Country'], index=False))
    print("\nQUALIFIED FOR INTERCONTINENTAL PLAYOFF\n")
    print(ict.to_string(columns=['Country'], index=False), "\n")
    if host in AFChosts:
        print("\nQUALIFIED AS HOST\n")
        print(host)

    return qualified, ict



