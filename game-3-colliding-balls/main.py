import pygame
import pymunk
import sys
import os
from pymunk import Vec2d
from pymunk import Space
import random

class Ball():
    def __init__(self, 
                 x: int, 
                 y: int,
                 collision_type: int,
                 space: Space, 
                 radius: int = 10,
                 density: int = 1, 
                 elasticity: float = 1,
                 color: tuple = (255, 0, 0)):
        self.body = pymunk.Body()
        self.radius = radius
        self.x = x
        self.y = y
        self.body.position = Vec2d(self.x, self.y)
        self.body.velocity = random.uniform(-800, 800), random.uniform(-800, 800)  # Random initial velocity for x- and y-axis
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.density = density
        self.shape.elasticity = elasticity
        self.shape.collision_type = collision_type
        self.color = color
        space.add(self.body, self.shape)
    
    def draw(self, display):
        # https://www.pygame.org/docs/ref/draw.html#pygame.draw.circle
        pygame.draw.circle(
            display, 
            self.color,
            (int(self.body.position.x), int(self.body.position.y)),
            self.radius)  # Draw the ball at its current position

class Floor():
    def __init__(self, 
                 point_left: Vec2d, 
                 point_right: Vec2d, 
                 thickness: int, 
                 elasticity: float, 
                 color: tuple, 
                 space: Space):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.point_left = point_left
        self.point_right = point_right
        self.thickness = thickness
        self.shape = pymunk.Segment(self.body, self.point_left, self.point_right, self.thickness)
        self.shape.elasticity = elasticity
        self.color = color
        space.add(self.body, self.shape)
    def draw(self, display):
        # https://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        pygame.draw.line(display, 
                         self.color, 
                         self.shape.a, 
                         self.shape.b, 
                         self.thickness) 
        
def collide(arbiter, space, data):
    print("Collision detected between balls!")	

def main():
    # 1. Set up Pymunk space
    print("Hello from game-3!")
    pygame.init()
    screen_size = 500  # Size of the game window
    display = pygame.display.set_mode((screen_size, screen_size)) # 800x800 pixels
    pygame.display.set_caption("Game 2: Colliding Balls")
    clock = pygame.time.Clock()
    fps = 60
    space = pymunk.Space()
    background_color = (255, 255, 255)  # White background

    # 2. Create balls
    ball_color = (163, 201, 166)  # Color of the ball: red
    ball_radius = 30
    balls = [Ball(x=random.randint(0, screen_size),
                  y=random.randint(0, screen_size),
                  collision_type=i,  # Unique collision type for each ball
                  radius=ball_radius,
                  color=ball_color,
                  space=space) for i in range(2)]  # Create two balls with different collision types
    
    floor_color = (255, 223, 211)
    floor_thickness = 20  # Thickness of the floor
    floor_elasticity = 0.8  # Elasticity of the floor
    corners = [(Vec2d(0, screen_size), Vec2d(screen_size, screen_size)),
               (Vec2d(0, 0), Vec2d(screen_size, 0)),
               (Vec2d(0, 0), Vec2d(0, screen_size)),
               (Vec2d(screen_size, 0), Vec2d(screen_size, screen_size))]
    
    # 3. Create floors acting as walls to contain the balls
    floors = [Floor(point_left=point_left, 
                      point_right=point_right, 
                      thickness=floor_thickness, 
                      elasticity=floor_elasticity, 
                      color=floor_color,  # Color of the floor: black
                      space=space) for point_left, point_right in corners]
    
    # 4. Set up collision handlers
    handler = space.add_collision_handler(0, 1)  # Collision handler for balls with collision type 0 and 1
    handler.separate = collide  # Function to call when a collision is detected

    # 4. Keep the game running unless the user interrupts it
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)

        # 5. Draw the background, balls, and floors
        display.fill(background_color)  # Redraw the background as white

        for ball in balls:
            ball.draw(display)

        for floor in floors:
            floor.draw(display)

        # 6. Update the display
        pygame.display.update()
        pygame.display.flip() # Flip the display to convert Pymunk coordinates to Pygame coordinates
        clock.tick(fps)
        space.step(1 / fps)  # Update the Pymunk space

if __name__ == "__main__":
    main()