from env import calculate_next_state
import math

def within_range(state):
    if abs(state[0] - 90) < 2:
        return True
    return False

def passed_top(state):
    if abs(state[0] - 90) - abs(state[1]) < 0:
        return True
    return False

def reduce_speed(state):
    speeds = [0, 0, 0]
    speeds[0] = abs(calculate_next_state(list(state), 0)[1])
    speeds[1] = abs(calculate_next_state(list(state), 1)[1])
    speeds[2] = abs(calculate_next_state(list(state), 2)[1])
    print(speeds, speeds.index(min(speeds)))
    return speeds.index(min(speeds))

def increase_speed(state):
    speeds = [0, 0, 0]
    speeds[0] = abs(calculate_next_state(list(state), 0)[1])
    speeds[1] = abs(calculate_next_state(list(state), 1)[1])
    speeds[2] = abs(calculate_next_state(list(state), 2)[1])
    return speeds.index(max(speeds)), speeds

def increase_y_pos(state):
    alt_y = [0, 0, 0]
    alt_y[0] = math.sin(math.radians(calculate_next_state(list(state), 0)[0]))
    alt_y[1] = math.sin(math.radians(calculate_next_state(list(state), 1)[0]))
    alt_y[2] = math.sin(math.radians(calculate_next_state(list(state), 2)[0]))
    return alt_y.index(max(alt_y)), max(alt_y)

def dir_changed(state1, state2):
    if state1[1] * state2[1] < 0:
        return True
    

def balance_pendulum(state):
    if abs(state[0] - 90) < 3 and abs(state[1]) < 2:
        return True

