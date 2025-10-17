# Jump Run

## Description

"Jump Run" is a 2D running game created using Python and Pygame. The player character automatically runs from left to right, and the player must avoid obstacles. The game speed increases over time, making it more challenging.

## Game Rules

-   **Controls:**
    -   `Spacebar`: Jump
    -   `↓ (Down Arrow Key)`: Slide
-   **Objective:** Survive as long as possible by avoiding obstacles.
-   **Game Over:** The game ends upon collision with an obstacle.
-   **Score:** The score is calculated based on survival time or the number of obstacles avoided.

## Items

-   **Heart:** Increases life when acquired.

## Code Structure

```
.
├── main.py         # Main game loop and initial setup
├── assets/         # Image files used in the game
│   ├── bg.png
│   ├── dirt.png
│   ├── drone.png
│   ├── explosion_0.png
│   ├── explosion_1.png
│   ├── explosion_2.png
│   ├── explosion_3.png
│   ├── heart.png
│   ├── lava.png
│   ├── missile.png
│   ├── platform.png
│   ├── player_0.png
│   ├── player_1.png
│   ├── player_2.png
│   ├── player_3.png
│   └── player_lie.png
├── src/            # Main game logic (modularized)
│   ├── background.py   # Handles background scrolling
│   ├── drone.py        # Logic for drone obstacles
│   ├── explosion.py    # Explosion animation effect
│   ├── ground.py       # Logic for the ground
│   ├── item.py         # Logic for items
│   ├── keyboard.py     # On-screen keyboard UI
│   ├── lava.py         # Logic for lava obstacles
│   ├── map_manager.py  # Map generation and management
│   ├── missile.py      # Logic for missile obstacles
│   └── player.py       # Logic for the player character
└── readme_kr.md      # Game description (Korean)
└── readme_en.md      # Game description (English)
```
