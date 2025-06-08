# angry-birds-finland
Built with Python

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
```

## Resources
- https://python-poetry.org/docs/basic-usage/#using-poetry-run

