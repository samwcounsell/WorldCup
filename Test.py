from scipy.stats import binom, bernoulli
import numpy as np
import pandas as pd
import random

team_data = pd.read_csv(r"C:\Users\samwc\PycharmProjects\WorldCup\team_data.csv")

for i,j in zip((0, 1, 0, 1, 0, 2), (2, 3, 3, 2, 1, 3)):
     if i != j:
        team1 = team_data.loc[i, 'Country']
        team2 = team_data.loc[j, 'Country']
        
        a1, d1 = team_data.loc[i, 'Attack'], team_data.loc[i, 'Defence']
        a2, d2 = team_data.loc[j, 'Attack'], team_data.loc[j, 'Defence']
        
        p1 = 0.014 * (a1 / d2)
        q1 = 1 - p1
        p2 = 0.014 * (a2 / d1)
        q2 = 1 - p2
          
        quantile = np.arange(0.01, 1, 0.1)
     
        Ber1 = bernoulli.rvs(p1, q1, size=90)
        Ber2 = bernoulli.rvs(p2, q2, size=90)
     
        goals1 = sum(Ber1)
        goals2 = sum(Ber2)
     
        print(team1, goals1, " - ", goals2, team2)
        print(team1, "xG/m", format(p1, ".4f"), " xG/norm", format((p1 / 0.014), ".4f"), "xG_total", format((p1 * 90), ".4f"))
        print(team2, "xG/m", format(p2, ".4f"), " xG/norm", format((p2 / 0.014), ".4f"), "xG_total", format((p2 * 90), ".4f"))
