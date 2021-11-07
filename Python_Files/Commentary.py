import random, webbrowser, time
import pandas as pd
from Stadiums import stadium
from pygame import mixer

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


def prefinal(runs):
    from Host import host_selector
    host, hostdf = host_selector()
    a, b, c, link = stadium(host)
    b = int(float(b))
    x = random.uniform(0.85, 1)
    att = round(b * x)
    print("Welcome to today's game here at the", a, "in", c, "\n")
    if runs == 1:
        input("Press enter to take a tour of the stadium: \n")
        webbrowser.open(link)
        input("Now you have taken a tour of the stadium, press enter to continue: ")
    print("Today's attendance is", att, "\n")


def goal():
    n = random.randint(0, r - 1)
    line = comm.loc[n, 'Goal']
    return line


def celebration(player, runs):
    # Easter Egg 1
    if runs == 1:
        if ''.join(player) == 'Sebastian Giovinco':
            mixer.init()
            mixer.music.load('AudioFiles/giovinco.mp3')
            mixer.music.play()
            time.sleep(12)

    if runs == 1:
        if ''.join(player) == 'Krzystof Piatek':
            mixer.init()
            mixer.music.load('AudioFiles/piatek.mp3')
            mixer.music.play()
            time.sleep(2)