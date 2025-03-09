import math

    
def discretize(state):
    return (round(state[0] * 3) / 3, round(state[1] * 4) / 4, round(state[2] / 100) * 100)
    
    
def calculate_next_state(state, action):
    mass = 1 # kg
    pen_l = 1 # m
    g = 9.81  # gravitational acceleration in m/s²
    dt = 1/60  # time step (60 FPS)
    
    pen_pos = [state[2] + math.cos(math.radians(state[0])) * 150 * pen_l, 300 - math.sin(math.radians(state[0])) * 150 * pen_l]
    
    if action == 1:
        state[2] -= 4  # Decrease cart position
    elif action == 2:
        state[2] += 4  # Increase cart position
    
    if state[2] > 800:
        state[2] = 800
        
    if state[2] < 0:
        state[2] = 0
    # Action 2 does nothing (stay in place)
        
    dx = pen_pos[0] - state[2]
    dy = 300 - pen_pos[1]
    state[0] = math.degrees(math.atan2(dy, dx))
    reward = (math.sin(math.radians(state[0])) + 1) / 2 # Value from 0 to 1 based on how close the pengulum is to the top
    #print(reward, state[0], math.sin(math.radians(state[0])))
    
    # Calculate angle between pen_pos and cart position
    
    # Calculate forces and acceleration
    torque = -mass * g * pen_l * math.cos(math.radians(state[0]))
    angular_acceleration = torque / (mass * pen_l * pen_l) #   -g * cos(angle)
    state[1] += angular_acceleration * dt
    state[0] += math.degrees(state[1] * dt)
    state[0] %= 360
    
    state[2] = max(0, state[2])
    state[2] = min(799, state[2])
    state[1] = min(59, state[1])
    state[1] = max(-59, state[1])
    state[0] = min(359, state[0])
    state[0] = max(0, state[0])

    #state[3] += 1
    return state