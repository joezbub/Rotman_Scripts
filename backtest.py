import pandas as pd
import sys
import os
import importlib
import numpy as np
from position import PositionTracker
import matplotlib.pyplot as plt

class Algo:
    def __init__(self, name, algo, position):
        self.name = name
        self.algo = algo
        self.position = position
        self.state = {}

algos_path = 'algos/'
sys.path.insert(1, algos_path)
args = sys.argv

algos = []
for i in range(2, len(args)):
    if os.path.exists(algos_path + args[i] + ".py"):
        algos.append(Algo(args[i], importlib.import_module(args[i]), PositionTracker()))

df = pd.read_parquet(sys.argv[1] + 'clean.parquet')

def run_backtest(algos, df):
    dates = df[["datadate"]].to_numpy().flatten()
    tickers = df[["tic"]].to_numpy().flatten()
    prices = df[["adjpc"]].to_numpy().flatten()

    num_dates = len(np.unique(dates))
    pnls = np.empty((num_dates,len(algos)), np.float64)
    unqiue_date_ct = 0

    data = {}
    last_prices = {}

    def feed_data(date):
        nonlocal unqiue_date_ct
        nonlocal last_prices
        nonlocal data
        last_prices = {**last_prices, **data}
        for j, algo in enumerate(algos):
            ret = algo.algo.on_tick(unqiue_date_ct, data, algos[j].state, algos[j].position)
            print(date, unqiue_date_ct, algos[j].name, ret)
            pnls[unqiue_date_ct][j] = algos[j].position.place_trades(last_prices, ret)
        unqiue_date_ct += 1
        data = {}

    for i, date in np.ndenumerate(dates):
        if (i[0] > 0 and date != dates[i[0] - 1]):
            feed_data(date)
        data[tickers[i[0]]] = prices[i[0]]
    feed_data(dates[-1])

    return pnls

pnls = run_backtest(algos, df)

def calculate_sharpes(deltas):
    print(np.mean(deltas, axis=0))
    print(np.std(deltas, axis=0))
    return np.mean(deltas, axis=0) / np.std(deltas, axis=0)

def calculate_sortinos(deltas, T=0):
    def get_sortino(col, T):
        temp = np.minimum(0, col - T)**2
        temp_expectation = np.mean(temp)
        downside_dev = np.sqrt(temp_expectation)
        sortino_ratio = np.mean(col - T) / downside_dev
        return sortino_ratio
    sortinos = []
    for i in range(deltas.shape[1]):
        sortinos.append(get_sortino(deltas[:,i], T))
    return np.asarray(sortinos)

deltas = np.diff(pnls, axis=0)
sharpes = calculate_sharpes(deltas)
sortinos = calculate_sortinos(deltas)
# percent_deltas = deltas / pnls[:-1,:]
# percent_sharpes = np.mean(percent_deltas, axis=0) / np.std(percent_deltas, axis=0)
for i in range(len(algos)):
    print(algos[i].name)
print("FINAL PNLS", pnls[-1:, :])
print(sharpes)
print(sortinos)
# print(percent_sharpes)
for i in range(len(algos)):
    plt.plot(pnls[:,i], label=algos[i].name)
plt.legend(loc="upper left")
plt.title("PNL")
plt.show()

for i in range(len(algos)):
    plt.plot(deltas[:,i], label=algos[i].name)
plt.legend(loc="upper left")
plt.title("Deltas")
plt.show()