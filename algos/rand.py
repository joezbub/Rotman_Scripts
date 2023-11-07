import random

def on_tick(date, data, state):
    keys = list(data.keys())
    return [(random.choice(keys), 1)]