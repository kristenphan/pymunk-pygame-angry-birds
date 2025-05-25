import os
import sys

import math
import pygame 
import time
import pymunk

def main():
    # Intialize Pygame and create a screen of size 600x600 pixels
    pygame.init()
    screen = pygame.display.set_mode((600, 600))    
    pygame.display.set_caption("Game 1: Slide & Pin Joint")
    clock = pygame.time.Clock()

    # SPACE:
    # A basic simulation unit in Pymunk.
    # You add bodies, shapes, and joints to a space, and then update the space as a whole. 
    space = pymunk.Space()
    space.gravity = (0, 900)  # Set gravity to pull objects downwards

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)
            screen.fill((255, 255, 255))  # Fill the screen with white color
            space.step(1/50.0)  # Step the physics simulation
            pygame.display.flip()
            clock.tick(50)

if __name__ == "__main__":
    sys.exit(main())