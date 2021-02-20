import random
import pandas as pd
from Stadiums import stadium

comm = pd.read_csv("Commentary.csv")
r, c = comm.shape

def prematch():
    from Host import hosty
    host, hostdf = hosty()
    a, b, c = stadium()
    b = int(float(b))
    x = random.uniform(0.85, 1)
    att = round(b * x)
    print("Welcome to today's game here at the", a, "in", c)
    print("Today's attendance is", att, "\n")



def goal():
    n = random.randint(0, r - 1)
    line = comm.loc[n, 'Goal']
    return line
