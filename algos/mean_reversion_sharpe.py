import numpy as np
from collections import defaultdict

analyze_period = 20
trade_period = 3
stocks = 10
portfolio_size = 1000000

def calculate_sharpe(prices):
    deltas = np.diff(prices)
    return np.mean(deltas) / np.std(deltas)

def on_tick(index, data, state, positions):
    for ticker in data:
        if ticker not in state:
            state[ticker] = []
        state[ticker].append(data[ticker])
        if len(state[ticker]) > analyze_period * 10:
            state[ticker].pop(0)

    if index % trade_period != 0:
        return {}

    trades = defaultdict(float)
    # unwind current positions
    for ticker in positions.positions:
        curr_pos = positions.positions[ticker]
        if curr_pos != 0:
            trades[ticker] = -curr_pos

    sharpes = []
    for ticker in data:
        if len(state[ticker]) > 2 * analyze_period:
            sharpes.append((ticker, calculate_sharpe(state[ticker]) - calculate_sharpe(state[ticker][-analyze_period:])))
    sorted_sharpes = sorted(sharpes, key=lambda tup: tup[1], reverse=True)
    for i in range(min(len(sorted_sharpes), stocks)):
        ticker = sorted_sharpes[i][0]
        trades[ticker] += (portfolio_size / stocks) / data[ticker]
    return trades
                
        
    

        