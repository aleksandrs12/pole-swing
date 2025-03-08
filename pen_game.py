import pygame
import sys
import math
#from pathfinder4 import get_action
from pathfinder5 import basic_pathfinder

# Initialize Pygame
pygame.init()

# Set up display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Game")

def calculate_distance(p1, p2):
    """Calculate Euclidean distance between two points."""
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game loop
clock = pygame.time.Clock()
running = True

angle = 270
cart_position = 400
angular_velocity = 0
pen_pos = [cart_position, 300 + 150]

depth = 0

while running:
    depth += 1
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    # Game logic here
    screen.fill(WHITE)
    pygame.draw.circle(screen, (0, 0, 0), (cart_position, 300), 50)
    pygame.draw.circle(screen, (0, 0, 0), (pen_pos[0], pen_pos[1]), 20)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        cart_position -= 6
    if keys[pygame.K_d]:
        cart_position += 6

    action = 0
    action = basic_pathfinder((angle, angular_velocity, cart_position))
    if action == 1:
        cart_position -= 1
    elif action == 2:
        cart_position += 1
    if cart_position > 800:
        cart_position = 800
    if cart_position < 0 or cart_position > 800:
        pen_pos[0] = 400 - (cart_position - pen_pos[0])
        cart_position = 400

    dx = pen_pos[0] - cart_position
    dy = 300 - pen_pos[1]
    angle = math.degrees(math.atan2(dy, dx))
    
    #angle = round(angle * 12) / 12
    #angular_velocity = round(angular_velocity * 16) / 16
    
    

    mass = 5 # kg
    pen_l = 1 # m
    g = 9.81  # gravitational acceleration in m/s²
    dt = 1/60  # time step (60 FPS)
    # Calculate angle between pen_pos and cart position
    

    # Calculate forces and acceleration
    torque = -mass * g * pen_l * math.cos(math.radians(angle))
    angular_acceleration = torque / (mass * pen_l * pen_l)
    angular_velocity += angular_acceleration * dt
    angle += math.degrees(angular_velocity * dt)

    pen_pos = [cart_position + math.cos(math.radians(angle)) * 150, 300 - math.sin(math.radians(angle)) * 150]





    
    # Add drawing code here
    
    # Update display
    pygame.display.flip()
    
    # Control frame rate
    clock.tick(60)

# Quit game
pygame.quit()
sys.exit()