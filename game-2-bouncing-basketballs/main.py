import pygame
import pymunk
import sys
import os

print("Hello from game-2!")
pygame.init()
display = pygame.display.set_mode((800, 800)) # 800x800 pixels
pygame.display.set_caption("Game 2: Bouncing Basketball")
clock = pygame.time.Clock()
fps = 60
space = pymunk.Space()

ball_body = pymunk.Body()
ball_body.position = 400, 50  # Set the initial position of the ball. Otherwise, default is (0, 0) top left corner per Pygame.
ball_radius = 30
ball_shape = pymunk.Circle(ball_body, ball_radius)  # Create a circle with radius 10
ball_shape.density = 1  # Set the density of the shape
ball_shape.elasticity = 0.8 # Without segment and ball elasticity, the ball would roll off the segment instead of bouncing off it. 1 = perfect elasticity, 0 = no elasticity
space.gravity = 0, 1000  # Set gravity to pull objects downwards

space.add(ball_body, ball_shape)  # Add the body and shape to the space

segment_body = pymunk.Body(body_type=pymunk.Body.STATIC)  # Create a static body for the segment. Density is indefinite by default, not not moving. 
segment_point_left = pymunk.Vec2d(0, 500)  # Starting point of the segment
segment_point_right = pymunk.Vec2d(800, 700)  # Ending point of the segment
segment_thickness = 5  # Thickness of the segment

# https://www.pymunk.org/en/latest/pymunk.html#pymunk.Segment
segment_shape = pymunk.Segment(segment_body, segment_point_left, segment_point_right, segment_thickness)  # Create a segment with a thickness of 5
segment_shape.elasticity = 0.8 # Without segment and ball elasticity, the ball would roll off the segment instead of bouncing off it.
space.add(segment_body, segment_shape)  # Add the segment to the space

background_color = (255, 255, 255)  # White background
ball_color = (255, 0, 0)  # Color of the circle (ball): red
segment_color = (0, 0, 0)  # Color of the segment: black

current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current directory
image = pygame.image.load(f"{current_dir}/image.png")
image = pygame.transform.scale(image, (ball_radius * 3, ball_radius * 3))  # Scale the image to fit the ball size

def game():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)
        

        display.fill(background_color)  # Redraw the background as white

        # https://www.pygame.org/docs/ref/draw.html#pygame.draw.circle
        display.blit(image, (int(ball_body.position.x) - ball_radius - 20, int(ball_body.position.y) - ball_radius - 20))
        
        # No need to draw th circle since we are using an image instead
        # pygame.draw.circle(
        #     display, 
        #     ball_color,
        #     (int(ball_body.position.x), int(ball_body.position.y)),
        #     ball_radius)  # Draw the ball at its current position

        # https://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        pygame.draw.line(display, 
                         segment_color, 
                         segment_shape.a, 
                         segment_shape.b, 
                         segment_thickness) 

        pygame.display.update()
        pygame.display.flip() # Flip the display to convert Pymunk coordinates to Pygame coordinates
        clock.tick(fps)
        space.step(1 / fps)  # Update the Pymunk space

game()
pygame.quit()