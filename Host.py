import random
import pandas as pd

possiblehosts = pd.read_csv(r"C:\Users\samwc\PycharmProjects\WorldCup\Host.csv")
n = random.randint(0, 20)

host = possiblehosts.loc[n, 'Country']
#print("\n", host)
hostdf = possiblehosts.iloc[n:n + 1, :]

def hosty():
    return host, hostdf




