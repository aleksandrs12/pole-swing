from env import calculate_next_state
import math
import sys


sys.setrecursionlimit(300000)

seen = {}
winning_strat = []
state = [270, 0, 400]

def within_range(state):
    if state[1] < 3 and math.sin(math.radians(state[0])) > 0.85:
        return True
    return False

def rec(state, history):
    global winning_strat
    global seen
    print(state)
    if within_range(state):
        print(1, state)
        winning_strat = history
        return True
    if tuple(state) in seen:
        return False
    seen[tuple(state)] = True
    
    history.append(0)
    if rec(list(calculate_next_state(state, 0)), history):
        return True
    history.pop(-1)
    history.append(1)
    if rec(list(calculate_next_state(state, 1)), history):
        return True
    history.pop(-1)
    history.append(2)
    if rec(list(calculate_next_state(state, 2)), history):
        return True
    return False
    
rec(state, [])
print(winning_strat)