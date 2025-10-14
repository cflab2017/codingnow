# 🎯 Territory Conquest Game - Paper.io Style

A real-time territory conquest game implemented with Python Pygame. Expand your area by drawing lines of your own color, and compete with AI enemies to conquer the largest territory!

## 📜 Game Overview and Rules

-   **Territory Expansion**: Players move around the map, drawing lines of their own color.
-   **Claiming Land**: When a line you've drawn connects back to your already claimed territory, the enclosed area within that line becomes your territory.
-   **Game Over Conditions**:
    -   If you touch your own line or an enemy's line while drawing (when outside your claimed territory), it's game over.
    -   If you collide with a snake, or if a snake collides with your unfinished line, it's game over.
    -   Attempting to move outside the map boundaries will stop your movement.
-   **Victory Condition**: Conquer the largest area within the time limit, or eliminate all enemies to win. (Currently in infinite mode)
-   **Competition**: Compete against multiple AI opponents to see who can claim the most land.

## 🎮 Controls

-   **WASD or Arrow Keys**: Player movement
-   **R Key**: Restart game
-   **M Key**: Toggle minimap (on/off)
-   **P or Space Key**: Pause/Resume game
-   **ESC Key**: Exit game

## 🐍 Snake

-   New snakes appear on the map at regular intervals.
-   Snakes have their own head and tongue, and are larger than regular game entities.
-   Snakes cannot invade already claimed territory; they bounce off.
-   If you collide with a snake, or if a snake touches your unfinished line, it's game over.

## 🚀 Key Features

-   **Real-time Territory Conquest**: Smooth movement and area-filling animations.
-   **AI Competitors**: AI enemies with various behavior patterns, including wall avoidance and player detection.
-   **Dynamic UI**: Real-time scoreboard, minimap, game status messages, and snake spawn timer.
-   **Collision Detection**: Precise collision detection between players, players and lines, and with snakes.

## 🛠️ How to Run

1.  **Install Required Libraries**:
    ```bash
    pip install pygame numpy
    ```
    Or if you have a `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the Game**:
    ```bash
    python main.py
    ```

## 💡 Improvement Ideas (Future Expansion)

-   **Sound Effects**: Add sound effects for line creation, successful territory claims, player death, and background music. (Currently, only the code is implemented; actual `.wav` files are needed.)
-   **Level System**: Add various maps with obstacles or special structures.
-   **Power-up Items**: Introduce items like speed boosts or shields to diversify gameplay.
-   **Multiplayer**: Implement online or local multiplayer functionality.
-   **Scoreboard**: Feature to save and display high scores.
