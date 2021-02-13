import pandas as pd


def GD4(i, n, df):
    a = df.iloc[[i, i + n, i + (2 * n), i + (3 * n)], :]
    a = a.set_index([pd.Index([0, 1, 2, 3]), ])
    return a
