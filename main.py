from gymnasium import Env
from gymnasium.spaces import Discrete, Box
import numpy as np
import math
import pygame
import random

class ThreeVariableEnv(Env):
    def __init__(self, render=False):
        super().__init__()
        self.render_mode = render
        self.action_space = Discrete(3)  #decrease, stay, increase
        self.observation_space = Box(low=np.array([0, 180, 0]), high=np.array([360, 180, 800]), dtype=np.float32) 
        # pengulum angle, angular velocity, cart position

        self.state = np.array([270, 0, 400], dtype=np.float32)  
        self.pen_pos = [self.state[2], 300 + 150]
        self.tick_num = 0

        if render:
            pygame.init()
            self.screen = pygame.display.set_mode((800, 600))
            self.clock = pygame.time.Clock()

    def step(self, action):
        if action == 1:
            self.state[2] -= 6  # Decrease cart position
        elif action == 2:
            self.state[2] += 6  # Increase cart position
        # Action 2 does nothing (stay in place)

        
        
        dx = self.pen_pos[0] - self.state[2]
        dy = 300 - self.pen_pos[1]
        self.state[0] = math.degrees(math.atan2(dy, dx))
        reward = abs(self.state[1]) # Value from 0 to 1 based on how close the pengulum is to the top
        #print(reward, self.state[0], math.sin(math.radians(self.state[0])))

        mass = 1 # kg
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
        self.state[0] = min(359, self.state[1])
        self.state[0] = max(0, self.state[1])

        self.tick_num += 1
        return self.state, reward, terminated, False, {}

    def reset(self, seed=None, options=None):
        self.state = np.array([270, 0, 400], dtype=np.float32)  # Reset state
        self.tick_num = 0
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


if __name__ == "__main__":
    epsilon = 1.0  # Exploration rate
    epsilon_decay = 0.999
    epsilon_min = 0.01
    learning_rate = 0.1
    discount_factor = 0.99
    episodes = 10000

    env = ThreeVariableEnv(render=False)
    num_buckets = (360, 180, 800)  # Discretizing observation space
    num_actions = 3
    q_table = np.zeros(num_buckets + (num_actions,))
    # Training loop
    total_reward = 0
    for episode in range(episodes):
        print(episode, total_reward)
        state, _ = env.reset()
        state = env.discretize()
        done = False
        total_reward = 0

        was_seen = []
        while not done:
            if env.render_mode == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True

            env.render()
            #env.clock.tick(60)
            
            if random.uniform(0, 1) < epsilon:
                action = env.action_space.sample()  # Explore
            else:
                action = np.argmax(q_table[state])  # Exploit
            
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated
            next_state = env.discretize()
            total_reward += reward

            # Update Q-table
            best_next_action = np.argmax(q_table[next_state])
            was_seen.append((state, action, best_next_action))
            q_table[state + (action,)] += learning_rate * (reward + discount_factor * q_table[next_state + (best_next_action,)] - q_table[state + (action,)])
            state = next_state

         # Decay epsilon
        epsilon = max(epsilon_min, epsilon * epsilon_decay)
        
        if episode % 1000 == 0:
            print(f"Episode: {episode}, Total Reward: {total_reward}, Epsilon: {epsilon:.3f}")

    env.close()
    print("Training completed!")

    env = ThreeVariableEnv(render=True)
    for episode in range(10):
        state, _ = env.reset()
        state = env.discretize()
        done = False
        total_reward = 0

        while not done:
            env.render()
            action = np.argmax(q_table[state])  # Exploit
            
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            next_state = env.discretize()
            total_reward += reward

            # Update Q-table
            best_next_action = np.argmax(q_table[next_state])
            q_table[state + (action,)] += learning_rate * (reward + discount_factor * q_table[next_state + (best_next_action,)] - q_table[state + (action,)])
            state = next_state

            env.clock.tick(60)

