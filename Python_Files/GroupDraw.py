import pandas as pd


def GD4(i, n, df):
    a = df.iloc[[i, i + n, i + (2 * n), i + (3 * n)], :]
    a = a.set_index([pd.Index([0, 1, 2, 3]), ])
    return a


def GD5(i, n, df):
    a = df.iloc[[i, i + n, i + (2 * n), i + (3 * n), i + (4 * n)], :]
    a = a.set_index([pd.Index([0, 1, 2, 3, 4]), ])
    return a


def GD6(i, n, df):
    a = df.iloc[[i, i + n, i + (2 * n), i + (3 * n), i + (4 * n), i + (5 * n)], :]
    a = a.set_index([pd.Index([0, 1, 2, 3, 4, 5]), ])
    return a

