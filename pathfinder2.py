from env import calculate_next_state
import math

positions = [(270, 0, 400)]

def within_range(state):
    if abs(state[0] - 90) < 2 and abs(state[1]) < 0.25:
        return True
    return False

seen = {}
path_found = False
max_sin = -1
depth = 0
while not path_found:
    if depth % 10 == 0:
        print(depth)
    depth += 1
    for n in range(len(positions)):
        if positions[n] in seen:
            continue
        seen[positions[n]] = True
        if within_range(positions[n]):
            path_found = True
            print('Path found!')
            print(positions[n])
        a = math.sin(math.radians(positions[n][0]))
        if a > max_sin:
            max_sin = a
            print(f'New max sin: {max_sin}, array length: {len(positions)}')
            
        tempo = calculate_next_state(list(positions[n]), 0)
        if not tempo in seen:
            positions.append(tempo)
        tempo = calculate_next_state(list(positions[n]), 1)
        if not tempo in seen:
            positions.append(tempo)
        positions[n] = calculate_next_state(list(positions[n]), 2)
        
        
