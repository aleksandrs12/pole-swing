from pathfinder4 import within_range, balance_pendulum, passed_top, increase_y_pos, increase_speed, reduce_speed
from env import calculate_next_state
import math

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
        
def prefered_direction(state):
    if state[2] > 400:
        return 1
    if state[2] < 400:
        return 2
    return 0

def find_required_energy(state, mass=1, g=9.81, pen_l=1, dt=1/60):
    absolute_speed = math.pi * pen_l * 2 * (state[1] / 360 /dt) # calculate the absolute speed of the pendulum (it seems like state[1] is per tick so i had to adjust per that)
    potential_energy = mass * g * pen_l * ((math.sin(math.radians(state[0])) + 1) / 2) # pretty obvious
    kinetic_energy = 0.5 * mass * (absolute_speed ** 2) / 2 # pretty obvious except that i had to divide by 2, prob has to do with the fact i converted sinus to a value between 0 and 1
    necessary_energy = mass * g * pen_l * ((math.sin(math.radians(90)) + 1) / 2)
    energy_deficit = necessary_energy - (potential_energy + kinetic_energy)
    #print("Energy deficit: ", energy_deficit)
    
    return energy_deficit

def find_energy_distribution(state, action_update_frequency=1, mass=1, g=9.81, pen_l=1, dt=1/60):
    absolute_speed = math.pi * pen_l * 2 * (state[1] / 360 /dt) # calculate the absolute speed of the pendulum (it seems like state[1] is per tick so i had to adjust per that)
    potential_energy = mass * g * pen_l * ((math.sin(math.radians(state[0])) + 1) / 2) # pretty obvious
    kinetic_energy = 0.5 * mass * (absolute_speed ** 2) / 2 # pretty obvious except that i had to divide by 2, prob has to do with the fact i converted sinus to a value between 0 and 1
    if potential_energy == 0:
        return 1
    k_potential = potential_energy / (potential_energy + kinetic_energy) / 1.3 + (1 - (1/1.3))
    
    return k_potential

def find_Nth_state(state, action, n, mass=1, g=9.81, pen_l=1, dt=1/60):
    for i in range(n):
        state = calculate_next_state(list(state), action)
    return state

def apply_coefficients(arr, coeffs):
    return [arr[i] * coeffs[i] for i in range(len(arr))]

def min_angle_deviation(state):
    deviations = [(calculate_next_state(state, 0)[0] - 90) % 360, (calculate_next_state(state, 1)[0] - 90) % 360, (calculate_next_state(state, 2)[0] - 90) % 360]
    deviations = list(map(abs, deviations))
    action = deviations.index(min(deviations))
    return action

def action_energy(state, action_update_frequency=1):
    energy_deficit = find_required_energy(state)
    deficits = [find_Nth_state(state, 0, action_update_frequency), find_Nth_state(state, 1, action_update_frequency), find_Nth_state(state, 2, action_update_frequency)]
    deficits = list(map(find_required_energy, deficits))
    deficits = list(map(abs, deficits))
    print(deficits)
    if math.sin(math.radians(state[0])) > 0.98 and abs(energy_deficit) < 0.1:
        target_velocity, time_required = find_required_velocity(state, pen_l=1)
        velocities = [calculate_next_state(list(state), 0)[1], calculate_next_state(list(state), 1)[1], calculate_next_state(list(state), 2)[1]]
        deviations = [min((abs(velocities[0] - target_velocity[0]), abs(velocities[0] - target_velocity[1]))), min((abs(velocities[1] - target_velocity[0]), abs(velocities[1] - target_velocity[1]))), min((abs(velocities[2] - target_velocity[0]), abs(velocities[2] - target_velocity[1])))]
        deviations = [abs(deviations[0]), abs(deviations[1]), abs(deviations[2])]
        return deviations.index(min(deviations))
    print(deficits)
    action = deficits.index(min(deficits))
    return action


        
def basic_pathfinder(state):
    target_velocity, time_required = find_required_velocity(state, pen_l=1)
    velocities = [calculate_next_state(list(state), 0)[1], calculate_next_state(list(state), 1)[1], calculate_next_state(list(state), 2)[1]]
    deviations = [min((abs(velocities[0] - target_velocity[0]), abs(velocities[0] - target_velocity[1]))), min((abs(velocities[1] - target_velocity[0]), abs(velocities[1] - target_velocity[1]))), min((abs(velocities[2] - target_velocity[0]), abs(velocities[2] - target_velocity[1])))]
    deviations = [abs(deviations[0]), abs(deviations[1]), abs(deviations[2])]
    
    time_required = min(time_required)
    action = deviations.index(min(deviations))
    weight1 = 0.25
    weight2 = 0
    weight3 = 0.005
    if deviations[action]  < weight1:
        #print(action, "By min deviation")
        return action
    
    if state[1] < 0:
        if state[1] < min(target_velocity):
            action = reduce_speed(state)
            #print(action, "Reduce speed")
            return action
    if state[1] > 0:
        if state[1] > max(target_velocity):
            action = reduce_speed(state)
            #print(action, "Reduce speed")
            return action
        
        
    action, alt_y = increase_y_pos(state)
    if alt_y - math.sin(math.radians(state[0])) > weight2:
        #print(action, "By y pos increase")
        return action
    
    #print("Increase speed")
    action = increase_speed(state)
    return action
    
    


