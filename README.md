# Snake Game with AI Adversary

This is a Python implementation of the classic Snake game with an AI-controlled adversary snake.

## Features
- Player-controlled snake using arrow keys
- AI-controlled adversary snake
- Score tracking
- Collision detection
- Game over screen

## Requirements
- Python 3.6+
- Pygame

## Installation
```bash
pip install pygame
```

## How to Run
```bash
python main.py
```

## Controls
- Arrow Up: Move Up
- Arrow Down: Move Down
- Arrow Left: Move Left
- Arrow Right: Move Right

## Game Rules
1. Control your snake (green) to collect food (red)
2. Avoid collisions with:
   - Walls
   - Your own body
   - AI snake (blue)
3. Game ends on collision
4. Score increases when food is collected