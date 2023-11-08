from collections import defaultdict

class PositionTracker:
    def __init__(self):
        self.cash = 1000000
        self.positions = defaultdict(float)

    def place_trades(self, data, trades):
        self.cash *= 1.00015
        for trade in trades:
            self.positions[trade] += trades[trade]
            self.cash -= data[trade] * trades[trade]
        
        holding_value = 0
        for ticker in self.positions:
            holding_value += self.positions[ticker] * data[ticker]
        return self.cash + holding_value
