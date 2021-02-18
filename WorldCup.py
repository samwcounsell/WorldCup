from Host import hosty
from AFC import afc
from CAF import caf
from CONCACAF import concacaf
from CONMBEOL import conmebol
from OFC import ofc
from UEFA import uefa

import pandas as pd

host, hostdf = hosty()

afc, ict1 = afc()
caf = caf()
concacaf, ict2 = concacaf()
conmebol, ict3 = conmebol()
ict4 = ofc()
uefa = uefa()

teams = hostdf
teams = pd.concat([teams, afc])
teams = pd.concat([teams, caf])
teams = pd.concat([teams, concacaf])
teams = pd.concat([teams, conmebol])
teams = pd.concat([teams, uefa])
ict = pd.concat([ict1, ict2, ict3, ict4])

print(teams, "\n", ict)
