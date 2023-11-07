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
    try:
        # Try reading the file using default UTF-8 encoding
        df = pd.read_csv(csv)
        df_list.append(df)
    except UnicodeDecodeError:
        try:
            # If UTF-8 fails, try reading the file using UTF-16 encoding with tab separator
            df = pd.read_csv(file_path, sep='\t', encoding='utf-16')
            df_list.append(df)
        except Exception as e:
            print(f"Could not read file {csv} because of error: {e}")
    except Exception as e:
        print(f"Could not read file {csv} because of error: {e}")

# Concatenate all data into one DataFrame
big_df = pd.concat(df_list, ignore_index=True)
print(len(big_df.index), 'rows')

# Save the final result to a new CSV file
big_df.to_parquet('output1.parquet')
