import pandas as pd
import random

stadiums = pd.read_csv("Stadiums.csv")
r, c = stadiums.shape

def stadium(host):
    #hostnation = "Japan"
    n = random.randint(0, 5)
    ground = stadiums.loc[4 * n, host]
    capacity = stadiums.loc[4 * n + 1, host]
    city = stadiums.loc[4 * n + 2, host]
    link = stadiums.loc[4 * n + 3, host]
    return ground, capacity, city, link






