import gymnasium as gym
import time
from stable_baselines3 import PPO
from env import PenEnv

# Create the environment (No rendering during training)
env = PenEnv(render=False)

# Create the PPO model
model = PPO("MlpPolicy", env, verbose=1)
print('Env loaded')

# Train the model
model.learn(total_timesteps=10000000)

# Save the trained model
model.save("ppo_pendulum1")
env.close()  # Close the training environment

# ===========================
# 🎥 Render the trained model
# ===========================

# Reload the environment with rendering enabled
env = gym.make('Pendulum-v1', render_mode="human")

# Load the trained model
model = PPO.load("ppo_pendulum")

# Run a few test episodes
obs, _ = env.reset()
for _ in range(500):
    action, _ = model.predict(obs)  # Get action from trained model
    obs, reward, terminated, truncated, _ = env.step(action)
    time.sleep(0.02)  # Slow down for better visualization

    if terminated or truncated:
        obs, _ = env.reset()  # Reset if episode ends

env.close()
