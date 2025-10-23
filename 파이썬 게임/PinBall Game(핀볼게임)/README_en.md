# Pinball Game

A simple pinball game implemented with Pygame.

## Game Description
This game implements the basic elements of a classic pinball game using the Pygame library. Players control the flippers to hit the ball, aiming for bumpers and other objects to score points.

## How to Play (Controls)
*   **Left Flipper**: `Left Arrow` key
*   **Right Flipper**: `Right Arrow` key
*   **Launch Ball**: `Spacebar` (Hold to pull the spring, release to launch the ball.)
*   **Quit Game**: `ESC` key
*   **Restart Game**: `R` key (When game is over)

## Code Structure
The project consists of the following main files and folders:
*   `main.py`: The main executable file for the game. It contains the game loop, initialization, object creation, and update/drawing logic.
*   `src/`: This folder contains Python scripts that modularize various components of the game.
    *   `src/ball.py`: Defines the Ball object. Handles physics, collision detection, and particle generation.
    *   `src/bumper.py`: Defines the Bumper object. Handles scoring on collision, flashing, and scaling animations.
    *   `src/flipper.py`: Defines the Flipper object. Handles rotation based on key input and collision with the ball.
    *   `src/spring.py`: Defines the Spring object. Manages the ball launching mechanism.
    *   `src/wall.py`: Defines the Wall object. Handles collision with the ball.
    *   `src/gate.py`: Defines the Gate object.
    *   `src/blackhole.py`: Defines the BlackHole object. Causes game over if the ball falls into it.
    *   `src/keyboard.py`: Defines an object for visually displaying keyboard input status.
    *   `src/particle.py`: Defines the ParticleEmitter system. Creates visual effects on collision.
*   `assets/`: This folder stores game assets such as images and sound files.
    *   `assets/ball.png`: Ball image.
    *   `assets/background.png`: Game background image.
    *   `assets/*.png`: Various planet bumper images.
    *   `assets/bounce.wav`: Collision sound effect.
    *   `assets/hit.wav`: (May not be currently used)

## Game Rules
*   Score points by hitting bumpers and other objects with the ball.
*   The game ends if the ball falls into the black hole.
*   Press `R` to restart the game.
*   Press `ESC` to quit the game.
