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
- Pymunk (top, left corner) and Pygame (bottom, left corner) have different coordinate systems. To resolve this, define coordinates according to Pymunk and flip the Pygame display `pygame.display.flip()`
    - Example: [slide-and-joint/main.py](game-1-slide-and-joint/main.py)
### Pymunk
- [Docs](https://www.pymunk.org/en/latest/installation.html)
- Built on top of a 2D physics library Munk2D written in C. 
- Key concepts
    - Body
        - A rigid body holds the physical properties of an object: mass, position, rotation, velocity, etc. 
        - It does not have a shape by itself. 
        - Example bodies: a football with a shape of circle in 2D, a wooden plank.
        - Examples: 
            - L-shaped body: [slide-and-joint/main.py](game-1-slide-and-joint/main.py)
    - Shape
        - By attching shapes to bodies, you can define the body's shape. 
        - You can attach multiple shapes to a single body to define a complex shape, or none if the body does not require a shape. 
        - 
        - Example shapes: circle, poly, segment (aka. line). 
            - [pymunk.Shape](https://www.pymunk.org/en/latest/pymunk.html#pymunk.Shape)
                - You usually don't want to create instances of this class directly but use one of the specialized spaces instead (`Circle`, `Poly`, or `Segment`)
            - [Segment](https://www.pymunk.org/en/latest/pymunk.html#pymunk.Segment)
                - A segment is a line shape connecting 2 points.
            - [Circle]()
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
    - Arbiter
        - https://www.pymunk.org/en/latest/pymunk.html#pymunk.Arbiter
        - An arbiter object encapsulates a pair of colliding shapes and all of the data about their collision. 
            - The space creates the arbiter objects when a collision starts, and persists until those shapes are no longer colliding.
            - Data points include elasticity (are the 2 shapes bouncing off each other), surface velocity (a running treadmill), etc.
        - A collision handler is a set of 4 function callbacks for the different collision events that Pymunk recognizes
            - `begin(): bool`
                - When 2 shapes start touching each other for the first time. 
                - `True`: When Pymunk should process the collision normally. 
                - `False`: When Pymunk should ignore the collision. 
            - `pre_solve(): bool`
                - Two shapes are touching during this step.
                - Used when you want to update the arbiter object. 
                - `True`: When Pymunk should process the collision normally. 
                - `False`: When Pymunk should ignore the collision. 
            - `post_solve()`
                - Two shapes are touching and their collision repsonse has been processed. 
                - For example, create a sound after collision or calculate damage. 
            - `separate()`
                - Like `post_solve()`, but two shapes have separated for the first time. 
- Physics properties
    - Friction
        - https://www.pymunk.org/en/latest/pymunk.html#pymunk.Circle.friction
        - friction = 0 is frictionless (Can slide forever).
        - Examples: 
            - PinJoint and SlideJoint: [slide-and-joint/main.py](game-1-slide-and-joint/main.py)
    - Gravity
        - https://www.pymunk.org/en/latest/pymunk.html#pymunk.Space.gravity
        - Use Vec2d to set gravity to pull objects downwards
            - y is positive downwards, x is positive to the right.
            - (0, 900) pulls downwards with acceleration 900 pixels/second^2.
        - Examples: 
        - PinJoint and SlideJoint: [slide-and-joint/main.py](game-1-slide-and-joint/main.py)
    - Mass & density
        - When a body does not have a mass (or density on the body's shape), Pymunk often has issues doing its calculation. 
        - You should only either set the mass and moment of inertia for a body, or (recommended) set the shape's density and let Pymunk calculate the mass and inertia based on the shape. 
    - Velocity
        - A body can have a linear velocity at the center of its gravity.
            - https://www.pymunk.org/en/latest/pymunk.html#pymunk.Body.velocity
            - Example: [game-3-colliding-balls/main.py](game-3-colliding-balls/main.py)
### Pygame
- Instead of having to write custom functions to draw the spcae in Pygame, can use Pymunk's debugging capabilities to draw space with default colors. 
- Example drawing functions:
    - `pygame.draw.line`
        - https://www.pygame.org/docs/ref/draw.html#pygame.draw.line
    - `pygame.draw.circle`
        - https://www.pygame.org/docs/ref/draw.html#pygame.draw.circle
- Examples: 
    - PinJoint and SlideJoint: [slide-and-joint/main.py](game-1-slide-and-joint/main.py)

## Resources
- https://python-poetry.org/docs/basic-usage/#using-poetry-run

