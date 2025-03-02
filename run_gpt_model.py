import gymnasium as gym
import time
from stable_baselines3 import PPO

env = gym.make('Pendulum-v1', render_mode="human")

# Load the trained model
model = PPO.load("ppo_pendulum")

# Run a few test episodes
obs, _ = env.reset()
for _ in range(1500):
    action, _ = model.predict(obs)  # Get action from trained model
    obs, reward, terminated, truncated, _ = env.step(action)
    time.sleep(0.02)  # Slow down for better visualization

    if terminated or truncated:
        obs, _ = env.reset()  # Reset if episode ends

env.close()
