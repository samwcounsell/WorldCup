from scipy.stats import binom, bernoulli
import numpy as np
import pandas as pd
import time
import random
import sys


def TLGRP90(k, a1, d1, a2, d2):
    if k == 1:  # the * 1.2 gives the home team and advantage
        p1 = 0.014 * (a1 / d2) * 1.2
        p2 = 0.014 * (a2 / d1)
    if k == 2:  # the * 1.2 gives the home team and advantage
        p1 = 0.014 * (a1 / d2)
        p2 = 0.014 * (a2 / d1) * 1.2

    Ber1 = bernoulli.rvs(p1, size=90)
    Ber2 = bernoulli.rvs(p2, size=90)
    goals1 = sum(Ber1)
    goals2 = sum(Ber2)
    return goals1, goals2
