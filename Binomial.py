from scipy.stats import binom, bernoulli
import numpy as np
import random

rn = random.sample(set([0, 1, 2]), 2)
rn1 = rn[0]
rn2 = rn[1]

#team_data = pd.read_csv(r"C:\Users\samwc\PycharmProjects\WorldCup\team_data.csv")
#team_data = pd.read_csv(r" ")

team1 = team_data.loc[rn1, 'Country']
team2 = team_data.loc[rn2, 'Country']

# teams attack and defense rating
a1, d1 = team_data.loc[rn1, 'Attack'], team_data.loc[rn1, 'Defence']
a2, d2 = team_data.loc[rn2, 'Attack'], team_data.loc[rn2, 'Defence']

# teams attack and defense rating
a1, d1 = 1.2, 0.9
a2, d2 = 0.8, 1.1

# calculating the chance of each team scoring
p1 = 0.014 * (a1 / d2)
q1 = 1 - p1
p2 = 0.014 * (a2 / d1)
q2 = 1 - p2

# No idea tbh
quantile = np.arange(0.01, 1, 0.1)

# Bernoulli distributions, this is the match being played, each minute is then displayed
Ber1 = bernoulli.rvs(p1, q1, size=90)
Ber2 = bernoulli.rvs(p2, q2, size=90)
print("Random Variates : \n", Ber1)
print("Random Variates : \n", Ber2)

# counts goals scored and displays result
goals1 = sum(Ber1)
goals2 = sum(Ber2)
print(team1, goals1, " - ", goals2, team2)

# prints chance of teams scoring each minute and the chance compared a completely basic match
print(team1, "xG/m", format(p1, ".4f"), " xG/norm", format((p1 / 0.014), ".4f"), "xG_total", format((p1 * 90), ".4f"))
print(team2, "xG/m", format(p2, ".4f"), " xG/norm", format((p2 / 0.014), ".4f"), "xG_total", format((p2 * 90), ".4f"))

#from scipy.stats import binom
#import matplotlib.pyplot as plt

#n = 90
#p = 0.014

#r_values = list(range(n + 1))

#dist = [binom.pmf(r, n, p) for r in r_values]

#plt.bar(r_values, dist)
#plt.show()
