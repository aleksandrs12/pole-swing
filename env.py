from gymnasium import Env
from gymnasium.spaces import Discrete, Box
import numpy as np
import math
import pygame
import random

class PenEnv(Env):
    def __init__(self, render=False):
        super().__init__()
        self.render_mode = render
        self.action_space = Discrete(3)  #decrease, stay, increase
        self.observation_space = Box(low=np.array([0, 180, 0]), high=np.array([360, 180, 800]), dtype=np.float32) 
        # pengulum angle, angular velocity, cart position

        self.state = np.array([270, 0, 400], dtype=np.float32)  
        self.pen_pos = [self.state[2], 300 + 150]
        self.tick_num = 0
        self.total_reward = 0

        if render:
            pygame.init()
            self.screen = pygame.display.set_mode((800, 600))
            self.clock = pygame.time.Clock()

    def step(self, action):
        if action == 1:
            self.state[2] -= 1  # Decrease cart position
        elif action == 2:
            self.state[2] += 1  # Increase cart position
        # Action 2 does nothing (stay in place)

        
        
        dx = self.pen_pos[0] - self.state[2]
        dy = 300 - self.pen_pos[1]
        self.state[0] = math.degrees(math.atan2(dy, dx))
        reward = (math.sin(math.radians(self.state[0])) + 1) / 2 # Value from 0 to 1 based on how close the pengulum is to the top
        self.total_reward += reward
        #print(reward, self.state[0], math.sin(math.radians(self.state[0])))

        mass = 5 # kg
        pen_l = 1 # m
        g = 9.81  # gravitational acceleration in m/s²
        dt = 1/60  # time step (60 FPS)
        # Calculate angle between pen_pos and cart position
        

        # Calculate forces and acceleration
        torque = -mass * g * pen_l * math.cos(math.radians(self.state[0]))
        angular_acceleration = torque / (mass * pen_l * pen_l)
        self.state[1] += angular_acceleration * dt
        self.state[0] += math.degrees(self.state[1] * dt)
        self.state[0] %= 360

        self.pen_pos = [self.state[2] + math.cos(math.radians(self.state[0])) * 150, 300 - math.sin(math.radians(self.state[0])) * 150]

        # Termination if any variable reaches 0 or 100
        terminated = self.state[2] <= 0 or self.state[2] >= 800 or self.state[1] > 360 or self.state[1] < -360 or self.tick_num / 60 > 15
        self.state[2] = max(0, self.state[2])
        self.state[2] = min(799, self.state[2])
        self.state[1] = min(59, self.state[1])
        self.state[1] = max(-59, self.state[1])
        self.state[0] = min(359, self.state[0])
        self.state[0] = max(0, self.state[0])

        self.tick_num += 1
        return self.state, reward, terminated, False, {}

    def reset(self, seed=None, options=None):
        self.state = np.array([270, 0, 400], dtype=np.float32)  # Reset state
        print(f'Reward: {round(self.total_reward * 100) / 100} / {round(self.total_reward/(self.tick_num+1) * 1000) / 1000}')
        self.tick_num = 0
        self.total_reward = 0
        return self.state, {}

    def render(self):
        #print(f"State: {self.state}")
        if self.render_mode:
            self.screen.fill((255, 255, 255))
            pygame.draw.circle(self.screen, (0, 0, 0), (round(self.state[2]), 300), 50)
            pygame.draw.circle(self.screen, (0, 0, 0), (round(self.pen_pos[0]), round(self.pen_pos[1])), 20)
            pygame.display.flip()

    
    def discretize(self):
        return (round(self.state[0]), round(self.state[1]), round(self.state[2]))
    
def discretize(state):
    return (round(state[0] * 3) / 3, round(state[1] * 4) / 4, round(state[2] / 100) * 100)
    
    
def calculate_next_state(state, action):
    pen_pos = [state[2] + math.cos(math.radians(state[0])) * 150, 300 - math.sin(math.radians(state[0])) * 150]
    
    if action == 1:
        state[2] -= 4  # Decrease cart position
    elif action == 2:
        state[2] += 4  # Increase cart position
    
    if state[2] > 800:
        state[2] = 800
    # Action 2 does nothing (stay in place)
        
    dx = pen_pos[0] - state[2]
    dy = 300 - pen_pos[1]
    state[0] = math.degrees(math.atan2(dy, dx))
    reward = (math.sin(math.radians(state[0])) + 1) / 2 # Value from 0 to 1 based on how close the pengulum is to the top
    #print(reward, state[0], math.sin(math.radians(state[0])))
    
    mass = 1 # kg
    pen_l = 1 # m
    g = 9.81  # gravitational acceleration in m/s²
    dt = 1/60  # time step (60 FPS)
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