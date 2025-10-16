# Drone Destroyer Game

## 🎮 Game Description

"Drone Destroyer" is a 2D arcade game developed using Python and the Pygame library. Players control a launcher on the left side of the screen to fire missiles and destroy drones flying in from the right. Missiles follow a parabolic trajectory influenced by gravity, and hitting a drone results in an explosion effect and points.

## 🕹️ Controls

*   **↑ (Up Arrow) / ↓ (Down Arrow) Keys**: Adjust missile launch angle
*   **← (Left Arrow) / → (Right Arrow) Keys**: Adjust missile launch speed
*   **Spacebar**: Launch missile
*   **R Key**: Restart game
*   **ESC Key or Close Window**: Exit game

## 📁 Code Structure

The project is organized into the following main files and directories:

*   `drone_game.py`: Contains the main game logic, initialization, event handling, and game loop.
*   `src/config.py`: Defines general game settings such as screen dimensions, colors, and FPS.
*   `src/missile.py`: Defines the Missile class, handling its physics (gravity, velocity), movement, and rendering.
*   `src/drone.py`: Defines the Drone class, managing drone spawning, movement, rendering, and collision detection with missiles.
*   `src/explosion.py`: Defines the Explosion class, responsible for the animation and visual effects of explosions upon impact.
*   `src/ui.py`: Manages and renders in-game user interface (UI) elements, including score, launch angle, and speed display.
*   `src/ai_launcher.py`: (Optional) May contain logic related to an AI launcher. Currently not implemented.
*   `assets/`: Stores image files used in the game, such as the background, launcher, drones, and missiles.

## 🚀 How to Run

1.  **Install Pygame**: If you don't have Pygame installed, use the following command:
    ```bash
pip install pygame
    ```
2.  **Run the Game**: Navigate to the project's root directory and execute the following command to start the game:
    ```bash
python drone_game.py
    ```