import gymnasium as gym
import time
from stable_baselines3 import PPO
from env import PenEnv

env = PenEnv(render=True)

# Load the trained model
model = PPO.load("ppo_pendulum1")

# Run a few test episodes
obs, _ = env.reset()
for _ in range(1500):
    action, _ = model.predict(obs)  # Get action from trained model
    obs, reward, terminated, truncated, _ = env.step(action)
    time.sleep(0.02)  # Slow down for better visualization
    env.render()

    if terminated or truncated:
        obs, _ = env.reset()  # Reset if episode ends

env.close()
