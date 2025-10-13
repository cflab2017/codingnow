# 2-Player Snake Game

This is a variant of the classic snake game where two players compete on a single keyboard.

## Features

- 2-player local versus gameplay
- Unique "Cut and Absorb" collision system
- Multiple victory and defeat conditions
- Special food items with different scores (strawberry shape)
- Simple visual and sound effects

## How to Play

### Requirements

- The `pygame` library must be installed.
  ```
  pip install pygame
  ```

### Running the Game

- Enter the following command in your terminal to run the game:
  ```
  python main.py
  ```

### Controls

- **Player 1 (Blue):** `W`, `A`, `S`, `D`
- **Player 2 (Orange):** Arrow Keys (`↑`, `↓`, `←`, `→`)

## Game Rules

### Objective

The goal is to be the last snake standing by defeating the opponent or being the first to reach a length of 10.

### Movement

- Snakes move continuously and wrap around the screen edges when they hit a wall.

### Food

- **Red Strawberry:** Increases length by 1.
- **Yellow Strawberry:** Increases length by 2 (rare).
- A text effect appears at the location of the food when it is eaten.

### Collision Rules

1.  **Head vs. Body (Cut & Absorb):**
    - If you hit the opponent's body with your head, their snake is "cut" at the point of impact.
    - The length of the severed tail part is added to your snake's length.

2.  **Head vs. Head (Draw):**
    - If both snakes' heads collide head-on, both snakes are reset to the default length (3 blocks).

3.  **Self-Collision (Defeat):**
    - If you hit your own body with your head, you are immediately defeated.

## Victory Conditions

You win if you are the first to meet any of the following conditions:

1.  **Reach Length 10:** Your snake's length becomes 10 or more.
2.  **Annihilate Opponent:** You win by cutting the opponent's snake down to a length of 1.
3.  **Opponent Self-Destructs:** You win if the other player is defeated by hitting their own body.

## UI

- The top UI panel displays the current length (score) for each player.
- A gauge below the score shows the progress towards the victory length of 10.
- When the game ends, the final results are shown on a semi-transparent overlay on top of the last game screen.