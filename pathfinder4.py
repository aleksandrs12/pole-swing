from env import calculate_next_state
import math

positions = [(270, 0, 400)]

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
    speeds[0] = calculate_next_state(list(state), 0)[1]
    speeds[1] = calculate_next_state(list(state), 1)[1]
    speeds[2] = calculate_next_state(list(state), 2)[1]
    print(speeds, speeds.index(min(speeds)))
    return speeds.index(min(speeds))

def increase_speed(state):
    speeds = [0, 0, 0]
    speeds[0] = calculate_next_state(list(state), 0)[1]
    speeds[1] = calculate_next_state(list(state), 1)[1]
    speeds[2] = calculate_next_state(list(state), 2)[1]
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
    
class Position:
    def __init__(self, state, parent_id, parent_action):
        self.state = state
        self.parent_id = parent_id
        self.parent_action = parent_action

def balance_pendulum(state):
    if abs(state[0] - 90) < 3 and abs(state[1]) < 2:
        return True

def find_path(depth_limit, state):
    positions = [Position(tuple(state), -1, -1)]
    seen = {}
    depth = 0
    next_id_start = 0
    while depth < depth_limit:
        depth += 1
        print(depth)
        current_id_start = next_id_start
        next_id_start = len(positions) - 1
        for n in range(current_id_start, len(positions)):
            if tuple(positions[n].state) in seen:
                continue
            seen[tuple(positions[n].state)] = True
            if balance_pendulum(positions[n].state):
                return True, positions
            for i in range(3):
                positions.append(Position(tuple(calculate_next_state(list(positions[n].state), i)), n, i))
    max_vel = -99
    for n in range(len(positions)):
        if positions[n].state[1] > max_vel:
            max_vel = positions[n].state[1]
            print(max_vel)
    return False, positions

def get_path(depth_limit, state):
    path_found, positions = find_path(depth_limit, state)
    if not path_found:
        print('Path not found!')
        return -1
    action = -1
    pos = positions[-1]
    while pos.parent_id != 0:
        action = pos.parent_action
        pos = positions[pos.parent_id]
    return action

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
    if passed_top(alt_state):
        print('Decrease')
        return reduce_speed(state)
    
    print('Increase')
    weight1 = 0.025
    alt_y_action, alt_y = increase_y_pos(state)
    if alt_y - math.sin(math.radians(state[0])) > weight1:
        return alt_y_action
    
    return increase_speed(state)
