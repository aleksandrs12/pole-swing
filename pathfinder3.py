import queue
from env import calculate_next_state

q = queue.Queue() # Bottom tree nodes

q.put((270, 0, 400, 0, 0, 0)) # Angle, angular velocity, cart position, depth, parent action, parent id in array
all_nodes = [(270, 0, 400, 0, 0, 0)]

def within_range(state):
    if abs(state[0]) < 2 and abs(state[1]) < 3:
        return True
    return False

depth = 0
seen = {}
while True:
    state = q.get()
    if state in seen:
        continue
    all_nodes.append(state)
    seen[state] = True
    if within_range(state):
        print('Path found!')
        print(state)
        break
    if state[3] > depth:
        depth = state[3]
        print(f'Depth: {depth}')
    state = list(state)
    state[5] = len(all_nodes) - 1
    state[4] = 3
    q.put(calculate_next_state(state, 3))
    state[4] = 1
    q.put(calculate_next_state(state, 1))
    state[4] = 2
    q.put(calculate_next_state(state, 2))

path = [5] * depth
next_id = len(all_nodes) - 1
for i in range(depth-1, 0, -1):
    path[i] = all_nodes[next_id][4]
    next_id = all_nodes[next_id][5]

print(path)