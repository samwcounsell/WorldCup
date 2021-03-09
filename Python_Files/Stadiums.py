import pandas as pd
import random

stadiums = pd.read_csv(r"C:\Users\samwc\PycharmProjects\WorldCup\Stadiums.csv")
r, c = stadiums.shape

def stadium():
    hostnation = "Japan"
    n = random.randint(0, 5)
    ground = stadiums.loc[3 * n, hostnation]
    capacity = stadiums.loc[3 * n + 1, hostnation]
    city = stadiums.loc[3 * n + 2, hostnation]
    return ground, capacity, city




