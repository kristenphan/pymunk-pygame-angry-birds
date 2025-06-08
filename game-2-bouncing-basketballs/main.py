import pygame
import pymunk
import sys
import os
from pymunk import Vec2d
from pymunk import Space

class Ball():
    def __init__(self, position: Vec2d, radius: int, density: int, elasticity: float, image_file: str, space: Space):
        self.body = pymunk.Body()
        self.radius = radius
        self.body.position = position
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.density = 1
        self.shape.elasticity = 0.8
        self.image_file = image_file
        space.add(self.body, self.shape)
    
    def draw(self, display):
        # https://www.pygame.org/docs/ref/draw.html#pygame.draw.circle
        current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current directory
        image = pygame.image.load(f"{current_dir}/{self.image_file}")
        image = pygame.transform.scale(image, (self.radius * 3, self.radius * 3))  # Scale the image to fit the ball size

        display.blit(image, 
                     (int(self.body.position.x) - self.radius - 20, int(self.body.position.y) - self.radius - 20))
        
        # No need to draw th circle since we are using an image instead. Only use this for debugging.
        # pygame.draw.circle(
        #     display, 
        #     ball_color,
        #     (int(ball_body.position.x), int(ball_body.position.y)),
        #     ball_radius)  # Draw the ball at its current position

class Floor():
    def __init__(self, point_left: Vec2d, point_right: Vec2d, thickness: int, elasticity: float, color: tuple, space: Space):
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

def main():
    print("Hello from game-2!")
    pygame.init()
    display = pygame.display.set_mode((800, 800)) # 800x800 pixels
    pygame.display.set_caption("Game 2: Bouncing Basketball")
    clock = pygame.time.Clock()
    fps = 60
    space = pymunk.Space()
    space.gravity = 0, 1000  # Set gravity to pull objects downwards
    background_color = (255, 255, 255)  # White background


    ball_position = Vec2d(200, 200)  # Initial position of the ball
    ball_radius = 30
    ball_density = 1  # Density of the ball
    ball_elasticity = 0.8  # Elasticity of the ball
    ball_image_file = "image.png"  # Image file for the ball
    ball = Ball(position=ball_position,
                radius=ball_radius,
                density=ball_density,
                elasticity=ball_elasticity,
                image_file=ball_image_file,  
                space=space)    
    
    ball_2 = Ball(position=ball_position,
                radius=ball_radius,
                density=ball_density,
                elasticity=ball_elasticity,
                image_file=ball_image_file,  
                space=space)  
    
    floor_point_left = Vec2d(0, 600)  # Left point of the floor
    floor_point_right = Vec2d(800, 750)  # Right point of the floor
    floor_thickness = 5  # Thickness of the floor
    floor_elasticity = 0.8  # Elasticity of the floor
    floor_color = (0, 0, 0)  # Color of the floor: black
    floor = Floor(point_left=floor_point_left,
                point_right=floor_point_right,
                thickness=floor_thickness,
                elasticity=floor_elasticity, 
                color=floor_color,
                space=space)  
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)
        
        display.fill(background_color)  # Redraw the background as white
        ball.draw(display)  # Draw the ball
        ball_2.draw(display) # The 2 balls split up because physics does not allow them to overlap.
        floor.draw(display)  # Draw the floor

        pygame.display.update()
        pygame.display.flip() # Flip the display to convert Pymunk coordinates to Pygame coordinates
        clock.tick(fps)
        space.step(1 / fps)  # Update the Pymunk space

if __name__ == "__main__":
    main()