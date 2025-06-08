# Using Pymunk and Pygame to build Angry Birds

## How to run project locally
```
# Install poetry
curl -sSL https://install.python-poetry.org | python3 -

# Define dependencies in pyproject.toml and add dependencies interactively in terminal or "poetry add {package-name}={version}"
poetry init

# Run python program (with virtual env activated)
poetry run python3 main.py

# Create poetry.lock & show dependency tree
poetry lock
poetry show --tree

# Show Pymunk example games (packaged along with the wheel)
poetry run python3 -m pymunk.examples -l

# Run Pymunk example game
poetry run python3 -m pymunk.examples.breakout

# Run games built by Kristen
poetry run python3 game-1-slide-and-joint/main.py
```

## About Pymunk and Pygame
- Pymunk is for physics logics while Pygame is for rendering. 
### Pymunk
- [Docs](https://www.pymunk.org/en/latest/installation.html)
- Built on top of a 2D physics library Munk2D written in C. 
- Key concepts
    - Rigid body
        - A rigid body holds the physical properties of an object: mass, position, rotation, velocity, etc. 
        - It does not have a shape by itself. 
        - Example bodies: a football with a shape of circle in 2D, a wooden plank.
        - Examples:
            - L-shaped body: [slide-and-joint/main.py](game-1-slide-and-joint/main.py)
    - Collision shape
        - By attching shapes to bodies, you can define the body's shape. 
        - You can attach multiple shapes to a single body to define a complex shape, or none if the body does not require a shape. 
        - Example shapes: circle, square, segment (aka. line). 
            -  [Segment](https://www.pymunk.org/en/latest/pymunk.html#pymunk.Segment)
                - A segment is a line shape connecting 2 points.
        - Examples:
            - Segments and circles: [slide-and-joint/main.py](game-1-slide-and-joint/main.py)
    - Constraint/ joint
        - https://www.pymunk.org/en/latest/pymunk.constraints.html
        - You can attach joints between 2 bodies to constrain their behavior. 
        - Constraints can be simple joints that allow bodies to pivot around each other like bones in your body, or they can be more abstract like gear joint or motors. 
        - Examples: 
            - PinJoint and SlideJoint: [slide-and-joint/main.py](game-1-slide-and-joint/main.py)
    - Space
        - A space is the basic simulation unit in Munk2D. 
        - You add bodies, shapes, and joints to a shape, and then update the space as a whole. 
- Physics properties
    - Friction
        - https://www.pymunk.org/en/latest/pymunk.html#pymunk.Circle.friction
        - friction = 0 is frictionless (Can slide forever).
    - Gravity
        - https://www.pymunk.org/en/latest/pymunk.html#pymunk.Space.gravity
        - Use Vec2d to set gravity to pull objects downwards
            - y is positive downwards, x is positive to the right.
            - (0, 900) pulls downwards with acceleration 900 pixels/second^2.
    
### Pygame

## Resources
- https://python-poetry.org/docs/basic-usage/#using-poetry-run

