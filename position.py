from collections import defaultdict

class PositionTracker:
    def __init__(self):
        self.cash = 1000000
        self.positions = defaultdict(int)

    def place_trades(self, data, trades):
        self.cash *= 1.00015
        for trade in trades:
            self.positions[trade[0]] += trade[1]
            self.cash -= data[trade[0]] * trade[1]
        
        holding_value = 0
        for ticker in self.positions:
            holding_value += self.positions[ticker] * data[ticker]
        return self.cash + holding_value
