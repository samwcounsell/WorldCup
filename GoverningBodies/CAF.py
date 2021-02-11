from scipy.stats import binom, bernoulli
import numpy as np
import pandas as pd
import time
import random
import sys
from MatchSim import TLKO

pot_data = pd.read_csv(r"C:\Users\samwc\PycharmProjects\WorldCup\CAF.csv")
#pot_data = pd.read_csv(r"")

pot_data = pot_data.sort_values(by=['World_Rank'])
round1 = pot_data.iloc[26:54]
round1 = round1.sample(frac=1)
round1 = round1.reset_index()
round1 = round1.drop(['index'], axis=1)

pot_data = pot_data.iloc[:28, :]

print("\nWELCOME TO CAF WORLD CUP QUALIFYING\n")
print("ROUND 1\n")

a = 14
pot_data = TLKO(a, round1, pot_data)
print(pot_data)

