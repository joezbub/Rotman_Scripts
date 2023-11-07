import pandas as pd
import sys

df = pd.read_parquet(sys.argv[1])
print(len(df.index), 'rows originally')

current_stocks = df.loc[df['LINKENDDT'] == 'E']
print(current_stocks.head())
print(len(current_stocks.index), 'rows after removing inactive stocks')
# df.sort_values(['



