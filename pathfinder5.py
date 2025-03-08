from pathfinder4 import within_range, balance_pendulum, passed_top, increase_y_pos, increase_speed, reduce_speed
from env import calculate_next_state
import math


def rate_actions(state):
    return (1, 2, 3)

def crossed_angle(last_angle, current_angle, control_angle):
    last_angle %= 360
    current_angle %= 360
    control_angle %= 360
    if last_angle < 0:
        last_angle = 360 + last_angle
    if current_angle < 0:
        current_angle = 360 + current_angle
    if control_angle < 0:
        control_angle = 360 + control_angle
        
    if (last_angle - control_angle) * (current_angle - control_angle) < 0:
        return True
    return False

def find_required_velocity(state, mass=1, g=9.81, pen_l=1, dt=1/60):
    output = [0, 0]
    angle_adj = 0.1
    
    velocity = 0
    angle = 90 + angle_adj
    last_angle = 90 + angle_adj
    ticks = [0, 0]
    while not crossed_angle(last_angle, angle, state[0]):
        last_angle = angle
        torque = -mass * g * pen_l * math.cos(math.radians(angle))
        angular_acceleration = torque / (mass * pen_l * pen_l) #   -g * cos(angle)
        velocity += angular_acceleration * dt
        angle += math.degrees(velocity * dt)
        
        ticks[0] += 1
    output[0] = -velocity
    
    velocity = 0
    angle = 90 - angle_adj
    last_angle = 90 - angle_adj
    while not crossed_angle(last_angle, angle, state[0]):
        last_angle = angle
        torque = -mass * g * pen_l * math.cos(math.radians(angle))
        angular_acceleration = torque / (mass * pen_l * pen_l) #   -g * cos(angle)
        velocity += angular_acceleration * dt
        angle += math.degrees(velocity * dt)
        
        ticks[1] += 1
    output[1] = -velocity
    ticks = [ticks[0] * dt, ticks[1] * dt]
    return output, ticks
    
seen = {}
def func(state, action_history):
    if state in seen:
        return False, []
    seen[state] = True
    if balance_pendulum(state):
        return True, action_history
    
    action_list = rate_actions(state)
    for action in action_list:
        action_history.append(action)
        func(tuple(calculate_next_state(state, action)), action_history)
        action_history.pop(-1)
        
def prefered_direction(state):
    if state[2] > 400:
        return 1
    if state[2] < 400:
        return 2
    return 0
        
def basic_pathfinder(state):
    target_velocity, time_required = find_required_velocity(state)
    velocities = [calculate_next_state(list(state), 0)[1], calculate_next_state(list(state), 1)[1], calculate_next_state(list(state), 2)[1]]
    deviations = [min((abs(velocities[0] - target_velocity[0]), abs(velocities[0] - target_velocity[1]))), min((abs(velocities[1] - target_velocity[0]), abs(velocities[1] - target_velocity[1]))), min((abs(velocities[2] - target_velocity[0]), abs(velocities[2] - target_velocity[1])))]
    deviations = [abs(deviations[0]), abs(deviations[1]), abs(deviations[2])]
    
    time_required = min(time_required)
    action = deviations.index(min(deviations))
    weight1 = 0.25
    weight2 = 0
    weight3 = 0.005
    if deviations[action]  < weight1:
        print(action, "By min deviation")
        return action
    action, alt_y = increase_y_pos(state)
    if alt_y - math.sin(math.radians(state[0])) > weight2:
        print(action, "By y pos increase")
        return action
    
    if state[1] < 0:
        if state[1] < min(target_velocity):
            action = reduce_speed(state)
            print(action, "Reduce speed")
            return action
    if state[1] > 0:
        if state[1] > max(target_velocity):
            action = reduce_speed(state)
            print(action, "Reduce speed")
            return action
        
    
    pref_dir = prefered_direction(state)
    action, speeds = increase_speed(state)
    if abs(speeds[pref_dir] - speeds[action]) < weight3:
        print(pref_dir, "Returning prefered direction")
        return pref_dir
    
    print("Increase speed")
    return action
    
    


