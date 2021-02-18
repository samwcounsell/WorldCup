from scipy.stats import binom, bernoulli
import numpy as np
import pandas as pd
import time
import random
import sys
from MatchSim import TLKO
from MatchSim import CONMEBOL
from GroupDraw import GD4

def conmebol():
    from Host import hosty

    pot_data = pd.read_csv(r"C:\Users\samwc\PycharmProjects\WorldCup\CONMEBOL.csv")
    # pot_data = pd.read_csv(r"/Users/keanerussell/Documents/Documents/Home/Python/CONMEBOL.csv")
    pot_data = pot_data.sort_values(by=['World_Rank'])

    CONMEBOLhosts = ["Brazil", "Argentina"]
    host, hostdf = hosty()

    group = pot_data
    print("\n", group.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False), "\n")

    group = CONMEBOL(group)
    group = group.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])
    group = group.reset_index()
    group = group.drop(['index'], axis=1)

    print("\n", group.to_string(columns=['Country', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'], index=False), "\n")

    if host in CONMEBOLhosts:
        group = group[group.Country != host]

    qualified = group.iloc[:4, :]
    ict = group.iloc[4:5, :]

    print("QUALIFIED FOR THE WORLD CUP\n")
    print(qualified.to_string(columns=['Country'], index=False))
    print("\nQUALIFIED FOR INTERCONTINENTAL PLAYOFF\n")
    print(ict.to_string(columns=['Country'], index=False), "\n")
    if host in CONMEBOLhosts:
        print("\nQUALIFIED AS HOST\n")
        print(host)

    return (qualified, ict)

