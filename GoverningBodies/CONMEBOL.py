from scipy.stats import binom, bernoulli
import numpy as np
import pandas as pd
import time
import random
import sys
from MatchSim import TLKO
from MatchSim import GRP10
from GroupDraw import GD4

# pot_data = pd.read_csv(r"C:\Users\samwc\PycharmProjects\WorldCup\CONMEBOL.csv")
pot_data = pd.read_csv(r"/Users/keanerussell/Documents/Documents/Home/Python/CONMEBOL.csv")
pot_data = pot_data.sort_values(by=['World_Rank'])

group = pot_data
print("\n", group, "\n")

group = GRP10(group)
group = group.sort_values(['Pts', 'GD', 'GF', 'GA'], ascending=[False, False, False, True])
group = group.reset_index()
group = group.drop(['index'], axis=1)

print("\n", group, "\n")

top4 = group.iloc[0:4, :]
qualified = pd.concat([group, top4])
ict = group.iloc[4:5, :]
ict = pd.concat([group, ict])

qualified = qualified.iloc[10:, :]
ict = ict.iloc[10:, :]
ict = ict[['Country', 'World_Rank']]
qualified = qualified[['Country', 'World_Rank']]
print("\nQUALIFIED FOR WORLD CUP\n")
print(qualified)
print("\nQUALIFIED FOR INTERCONTINENTAL PLAYOFF\n")
print(ict, "\n")
