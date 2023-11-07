import pandas as pd
import sys
import os
import importlib
import numpy as np
from position import PositionTracker

algos_path = 'algos/'
sys.path.insert(1, algos_path)
args = sys.argv
names = []
algos = []
states = []
positions = []
for i in range(2, len(args)):
    if os.path.exists(algos_path + args[i] + ".py"):
        names.append(args[i])
        algos.append(importlib.import_module(args[i]))
        states.append({})
        positions.append(PositionTracker())

df = pd.read_parquet(sys.argv[1] + 'clean.parquet')

dates = df[["datadate"]].to_numpy().flatten()
tickers = df[["tic"]].to_numpy().flatten()
prices = df[["adjpc"]].to_numpy().flatten()

num_dates = len(np.unique(dates))
pnls = np.empty((num_dates,len(algos)), np.float64)
unqiue_date_ct = 0

data = {}
for i, date in np.ndenumerate(dates):
    if (i[0] > 0 and date != dates[i[0] - 1]) or i[0] == len(dates) - 1:
        for j, algo in enumerate(algos):
            ret = algo.on_tick(dates[i[0] - 1], data, states[j])
            print(names[j], ret)
            pnls[unqiue_date_ct][j] = positions[j].place_trades(data, ret)
        unqiue_date_ct += 1
        data = {}
    data[tickers[i[0]]] = prices[i[0]]
    
    