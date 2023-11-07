import pandas as pd
import sys

df = pd.read_parquet(sys.argv[1] + 'output.parquet')
print(len(df.index), 'rows originally')

df['adjpc'] = df['prccd'] / df['ajexdi']
df = df.drop(columns=['LIID', 'iid', 'adrrc']).sort_values(['datadate', 'tic']).reset_index(drop=True).dropna(subset=['adjpc'])

print(df)
df.to_parquet(sys.argv[1] + 'clean.parquet')
