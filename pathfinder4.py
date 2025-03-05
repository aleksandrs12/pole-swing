from env import calculate_next_state
import math

positions = [(270, 0, 400)]

def within_range(state):
    if abs(state[0] - 90) < 2:
        return True
    return False

def reduce_speed(state):
    speeds = [0, 0, 0]
    speeds[0] = calculate_next_state(list(state), 0)
    speeds[1] = calculate_next_state(list(state), 1)
    speeds[2] = calculate_next_state(list(state), 2)
    return speeds.index(min(speeds))

def increase_speed(state):
    speeds = [0, 0, 0]
    speeds[0] = calculate_next_state(list(state), 0)
    speeds[1] = calculate_next_state(list(state), 1)
    speeds[2] = calculate_next_state(list(state), 2)
    return speeds.index(max(speeds))

def increase_y_pos(state):
    alt_y = [0, 0, 0]
    alt_y[0] = math.sin(math.radians(calculate_next_state(list(state), 0)[0]))
    alt_y[1] = math.sin(math.radians(calculate_next_state(list(state), 1)[0]))
    alt_y[2] = math.sin(math.radians(calculate_next_state(list(state), 2)[0]))
    return alt_y.index(max(alt_y)), max(alt_y)

def dir_changed(state1, state2):
    if state1[1] * state2[1] < 0:
        return True

def get_action(state):
    alt_state = list(state)
    while not within_range(alt_state) and alt_state[1] != 0:
        last_state = list(alt_state)
        alt_state = calculate_next_state(list(alt_state), 0)
        if dir_changed(last_state, alt_state):
            alt_state[1] = 0
            break

    if within_range(alt_state) and alt_state[1] == 0:
        return 0
    elif within_range(state):
        return reduce_speed(state)
    
    weight1 = 0.05
    alt_y_action, alt_y = increase_y_pos(state)
    if alt_y - math.sin(math.radians(state[0])) > weight1:
        print(alt_y, math.sin(math.radians(state[0])))
        return alt_y_action
    return increase_speed(state)
