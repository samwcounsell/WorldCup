import random
import pandas as pd

def host():
    possiblehosts = pd.read_csv(r"C:\Users\samwc\PycharmProjects\WorldCup\Host.csv")
    n = random.randint(0, 16)

    host = possiblehosts.loc[n, 'Country']
    print("\n", host)
    hostdf = possiblehosts.iloc[n:n + 1, :]

    return host, hostdf




