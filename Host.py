import random
import pandas as pd

#def host():
    # nations = ["England", "USA", "France", "Brazil", "China", "Australia", "South Africa", "India", "Japan", "Qatar"]
    #nations = ["Japan", "South Korea"]
    #host = random.choice(nations)
    #print(host)

    #return host

def host():
    possiblehosts = pd.read_csv(r"C:\Users\samwc\PycharmProjects\WorldCup\Host.csv")
    n = random.randint(0, 8)

    host = possiblehosts.loc[n, 'Country']
    print(host)
    hostdf = possiblehosts.iloc[n:n + 1, :]

    return host, hostdf




