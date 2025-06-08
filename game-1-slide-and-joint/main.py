import os
import sys

import math
import pygame 
import time
import pymunk
import pymunk.pygame_util
import random

def main():
    # 1. Intialize Pygame and create a screen of size 600x600 pixels
    pygame.init()
    screen = pygame.display.set_mode((600, 600))    
    pygame.display.set_caption("Game 1: Slide & Pin Joint")
    clock = pygame.time.Clock()


    # 2. Create a Pymunk space.
    # SPACE:
    # Space is a basic simulation unit in Pymunk.
    # You add bodies, shapes, and joints to a space, and then update the space as a whole. 
    space = pymunk.Space()


    # 3. Set gravity to pull objects downwards using Vec2d.
    # Vec2d: y is positive downwards, x is positive to the right.
    # Higher y means objects accelerate faster.
    # https://www.pymunk.org/en/latest/pymunk.html#pymunk.Space.gravity
    space.gravity = (0, 900)  

    # 4. Create a list to hold the balls that will be added to the space.
    balls = []
    ticks_to_next_ball = 10 # Number of ticks before adding a new ball

    # 5. Add a rorating L shape with 2 joints to the space.
    add_rorating_l(space)

    # 6. Set up Pymunk's debugging utilities as a quick way to draw the space instead of using Pygame.
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    # 7. Keep the game running until the user closes it
    while True:
        # 8. Process all user events such as keyboard, mouse, and window events to stop the game.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)

        # 9. Spawn a new ball every 10 ticks of the loop
        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 10
            ball_shape = add_ball(space)
            balls.append(ball_shape)
        
        # 10. Fill the screen with white color
        screen.fill((255, 255, 255))  

        # 11. Remove balls that have fallen below the screen
        # to avoid consuming too much memory and cpu.
        balls_to_remove = []  # List to keep track of balls to remove
        for ball in balls:
            if ball.body.position.y > 550:  # If the ball goes below the screen
                balls_to_remove.append(ball)  # Mark it for removal
        
        for ball in balls_to_remove:
            space.remove(ball, ball.body)
            balls.remove(ball)  # Remove the ball from the list

        # 12. Draw the space with balls and L shape.

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
    x = random.randint(120, 350)
    body.position = x, 50 

    # 2. Create a circle shape for the body
    mass = 3    
    radius = 25
    shape = pymunk.Circle(body, radius, (0, 0))  

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

def add_rorating_l(space):
    """
    Add two static vertical and horizontal lines
    forming an L shape.
    The L shape can rotate as the balls to land on it.
    """
    # 1. Create an L-shaped body 
    # Create a body for the L shape.
    # https://www.pymunk.org/en/latest/_modules/pymunk/body.html#Body
    l_body = pymunk.Body(10, 100000) 
    l_body.position = (300, 300)       
    
    # Create two segments (line shapes attached to the body) to form an L shape
    # Horizontal line from (-150, 0) to (255, 0) with thickness 5 relative to the body position
    horizontal_line = pymunk.Segment(l_body, (-150, 0), (250, 0), 5)    

    # # Vertical line
    vertical_line = pymunk.Segment(l_body, (-150, 0), (-150, -50), 5)   

    # Friction for the horizontal line     
    horizontal_line.friction = 1                                  
    vertical_line.friction = 1    

    horizontal_line.mass = 8
    vertical_line.mass = 1

    # 2. Create a body representing the center of the horizontal line (aka. rotation center body)
    rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)  # Create a body for the rotation center
    rotation_center_body.position = (300, 300)  # Set its position
    
    # 3. Create a body representing the rotation limit
    rotation_limit_body = pymunk.Body(body_type=pymunk.Body.STATIC)  # Create a body for the rotation limit
    rotation_limit_body.position = (200, 300)  # Set its position

    # 4. Create a PinJoint to connect the L-shaped body to the rotation center body.
    rotation_center_joint = pymunk.PinJoint(
        l_body, rotation_center_body, (0,0), (0,0)
    )    

    # 5. Create a SlideJoint to limit the rotation of the L-shaped body.
    joint_limit = 25
    rotation_limit_joint = pymunk.SlideJoint(l_body, rotation_limit_body, (-100, 0), (0, 0), 0, joint_limit) 

    # 6.Add the L-shaped body with segments, one PinJoint, one SlideJoint.
    # The joints control how the L-shaped body rotates and slides as the balls hit it.           
    space.add(horizontal_line, vertical_line, l_body, rotation_center_joint, rotation_limit_joint)                   

if __name__ == "__main__":
    sys.exit(main())