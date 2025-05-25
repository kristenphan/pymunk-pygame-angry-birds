import os
import sys

import math
import pygame 
import time
import pymunk
import pymunk.pygame_util
import random

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
    space.gravity = (0, 900)  # Use Vec2d to set gravity to pull objects downwards

    balls = []
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    ticks_to_next_ball = 10 # Number of ticks before adding a new ball

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)

            ticks_to_next_ball -= 1
            if ticks_to_next_ball <= 0:
                ticks_to_next_ball = 10
                ball_shape = add_ball(space)
                balls.append(ball_shape)
            
            screen.fill((255, 255, 255))  # Fill the screen with white color
            space.step(1/50.0)  # Step the physics simulation
            space.debug_draw(draw_options)  # Draw the space
            pygame.display.flip()
            clock.tick(60) # Set frame rate: 50 frames per second

def add_ball(space):
    """
    Return a circle shape that represents a ball in the space.
    """
    # BODY
    # A rigid body holds the physical properties of an object, such as its position, velocity, and mass.
    # It does not have a shape by itself. 

    # 1. Create ball's body at a starting position.
    body = pymunk.Body() 
    x = random.randint(100, 500)
    body.position = x, 50 

    # 2. Create a circle shape for the body
    radius = 25
    mass = 3
    shape = pymunk.Circle(body, radius)  

    # 3. All bodies must have their moment of inertia set. 
    # Moment of inertia is how an object responds to forces that try to make it rotate.
    # When a force hits an object at its center of mass, the object mostly just moves.
    # If it hits off-center, the object tends to rotate.
    # Easiest way to let Pymunk handle inertia calculation from mass.
    shape.mass = mass

    # 4. Make the ball roll by setting its friction.
    shape.friction = 1

    # 5. Add the body and shape to the space. 
    # The body must always be added to the space before or at the same time as any shapes attached to it. 
    space.add(body, shape)

    return shape

if __name__ == "__main__":
    sys.exit(main())