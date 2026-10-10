import pandas as pd
import sys

df = pd.read_csv('stat_analysis/data.csv')
print(df.iloc[int(sys.argv[1])])