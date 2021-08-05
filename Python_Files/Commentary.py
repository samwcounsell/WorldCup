import random, webbrowser, time
import pandas as pd
from Stadiums import stadium

comm = pd.read_csv("Commentary.csv")
r, c = comm.shape


def prematch():
    from Host import host_selector
    host, hostdf = host_selector()
    a, b, c, link = stadium(host)
    b = int(float(b))
    x = random.uniform(0.85, 1)
    att = round(b * x)
    print("Welcome to today's game here at the", a, "in", c)
    print("Today's attendance is", att, "\n")


def prefinal():
    from Host import host_selector
    host, hostdf = host_selector()
    a, b, c, link = stadium(host)
    b = int(float(b))
    x = random.uniform(0.85, 1)
    att = round(b * x)
    print("Welcome to today's game here at the", a, "in", c)
    time.sleep(1)
    webbrowser.open(link)
    print("Today's attendance is", att, "\n")


def goal():
    n = random.randint(0, r - 1)
    line = comm.loc[n, 'Goal']
    return line
