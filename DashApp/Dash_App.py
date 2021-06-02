import pandas as pd

World_Cup_Data = pd.read_csv('../Python_Files/Data_Set.csv')

# Ensuring pandas displays the whole data frame
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

print(World_Cup_Data)