import random
import pandas as pd

possible_hosts = pd.read_csv("Host.csv")
n = random.randint(0, 20)

host = possible_hosts.loc[n, 'Country']

host_df = possible_hosts.iloc[n:n + 1, :]

def host_selector():
    return host, host_df




