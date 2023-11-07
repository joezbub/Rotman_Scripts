def on_tick(date, data, state):
    if "A" not in state:
        state["A"] = 0
    state["A"] += 1
    print(date)
    return []