# Rotman_Scripts

## Instructions

Merge csvs by running `python merge_csvs.py arg1 arg2 arg3...` where the args are the paths to the csv files. This creates an output parquet file (compressed dataframe).

Clean the dataframe from above by running `python organize_data.py nov7/` where nov7/ is the path to the folder containing the parquet file. This program will sort the df by date and ticker and drop garbage rows. It will produce a clean.parquet file in that folder. 