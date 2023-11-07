import pandas as pd
import os
import sys

args = sys.argv
paths = []
for i in range(1, len(args)):
    if os.path.exists(args[i]):
        paths.append(args[i])
print(paths)

df_list = []

for csv in paths:
    # Try reading the file using default UTF-8 encoding
    df = pd.read_csv(csv)
    df_list.append(df)

# Concatenate all data into one DataFrame
big_df = pd.concat(df_list, ignore_index=True)
print(len(big_df.index), 'rows')

# Save the final result to a new CSV file
big_df.to_parquet('nov7/output.parquet')
