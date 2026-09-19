# Asteroids [![MIT License](https://img.shields.io/badge/license-MIT-22c55e.svg)](LICENSE)

Python version of the classic Asteroids arcade game. Pilot a ship, dodge
incoming asteroids, shoot them, and split larger rocks into smaller ones.

## Motivation

This project rebuilds an arcade classic as a focused exercise in real-time
game loops, movement, collision detection, procedural spawning, and pixel-art
presentation with Pygame.

## Features

- Player-controlled ship with rotation, forward/reverse movement, and shooting.
- Random asteroid spawning from the edges of the screen.
- Asteroids split into smaller asteroids when hit.
- Collision detection between the player, shots, and asteroids.
- JSONL runtime logs for game state and notable events.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) for dependency management

## Usage

Install dependencies:

```bash
uv sync
```

Run the game:

```bash
uv run python main.py
```

Controls:

- `Up Arrow`: move forward
- `Down Arrow`: move backward
- `Left Arrow`: rotate left
- `Right Arrow`: rotate right
- `Space`: shoot

## Preview

![Asteroids gameplay](assets/preview/preview.gif)
