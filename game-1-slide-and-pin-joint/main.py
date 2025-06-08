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

    # Use Vec2d to set gravity to pull objects downwards
    # Vec2d: y is positive downwards, x is positive to the right.
    # Higher y means objects accelerate faster.
    # https://www.pymunk.org/en/latest/pymunk.html#pymunk.Space.gravity
    space.gravity = (0, 900)  

    balls = []
    ticks_to_next_ball = 10 # Number of ticks before adding a new ball
    lines = add_static_l(space)

    # Use Pymunk's debugging utilities as a quick way to draw the space instead of using Pygame.
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    # Keep the game running until the user closes it
    while True:
        # Process all user events such as keyboard, mouse, and window events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)

        # Spawn a new ball every 10 ticks of the loop
        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 10
            ball_shape = add_ball(space)
            # balls.append(ball_shape)
        
        # Fill the screen with white color
        screen.fill((255, 255, 255))  

        # Step the physics simulation  
        space.step(1/50.0)              

        # Draw the space
        # Simplier than using Pygame's drawing functions, but ignores shape colors.
        space.debug_draw(draw_options)  

        # Update the display with what you just drew
        pygame.display.flip()           

        # Set frame rate: 20 frames per second (controls how fast the while loop runs)
        # Higher fps means the balls are spawned more frequently.
        clock.tick(20)                 

def add_ball(space):
    """
    Return a circle shape that represents a ball in the space.
    """
    # BODY
    # A rigid body holds the physical properties of an object, such as its position, velocity, and mass.
    # It does not have a shape by itself. 

    # 1. Create ball's body at a starting position.
    # Default body type is dynamic, meaning it can move and be affected by forces.
    # https://www.pymunk.org/en/latest/_modules/pymunk/body.html#Body
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
    # https://www.pymunk.org/en/latest/pymunk.html#pymunk.Shape.mass
    shape.mass = mass

    # 4. Make the ball roll by setting its friction.
    shape.friction = 1

    # 5. Add the body and shape to the space. 
    # The body must always be added to the space before or at the same time as any shapes attached to it. 
    # https://www.pymunk.org/en/latest/_modules/pymunk/space.html#Space.add
    space.add(body, shape)

    return shape

def add_static_l(space):
    """
    Add two static vertical and horizontal lines
    forming an L shape to the space for the balls to land on.
    """
    # Static body does not move
    # https://www.pymunk.org/en/latest/_modules/pymunk/body.html#Body
    body = pymunk.Body(body_type=pymunk.Body.STATIC)        
    body.position = (300, 300)                              # Position of the static body

    # Create two segments (lines) to form an L shape
    # Horizontal line from (-150, 0) to (255, 0) with thickness 5
    line1 = pymunk.Segment(body, (-150, 100), (255, 100), 5)    # Horizontal line

    # # Vertical line
    line2 = pymunk.Segment(body, (-150, 100), (-150, 50), 5)        
    line1.friction = 1                                  # Friction for the horizontal line
    line2.friction = 1              
    space.add(body, line1, line2)                       # Add the static body and lines to the space  

if __name__ == "__main__":
    sys.exit(main())