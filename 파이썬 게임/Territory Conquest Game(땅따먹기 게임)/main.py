"""
Territory Conquest Game - Paper.io Style
Main execution file

How to run:
python main.py

Controls:
- WASD or Arrow Keys: Player movement
- R: Restart game
- M: Toggle minimap
- ESC: Exit game

Game Rules:
1. Draw lines with your color to expand your territory
2. When your line connects back to your territory, claim the enclosed area
3. If you touch an enemy or your own line while drawing, it's game over
4. Goal: Conquer the largest territory within the time limit
"""

import sys
import os

# Add the current script's directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    import pygame
    import numpy as np
except ImportError as e:
    print("Required libraries are not installed.")
    print("Please install them with the following command:")
    print("pip install pygame numpy")
    sys.exit(1)

from game import Game


def print_game_info():
    """Print game information."""
    print("=" * 60)
    print("🎯 Territory Conquest Game - Paper.io Style")
    print("=" * 60)
    print("📜 Game Rules:")
    print("  • Draw lines with your color to expand your territory")
    print("  • When your line connects to your territory, claim the enclosed area")
    print("  • If you touch an enemy or your own line while drawing, game over!")
    print("  • Conquer the largest territory within the time limit")
    print()
    print("🎮 Controls:")
    print("  • WASD or Arrow Keys: Player movement")
    print("  • R Key: Restart game")
    print("  • M Key: Toggle minimap")
    print("  • ESC Key: Exit game")
    print()
    print("🤖 Compete with AI enemies to become the territory king!")
    print("=" * 60)


def main():
    """Main function."""
    # Print game information
    print_game_info()
    
    try:
        # Create a game instance
        print("Initializing game...")
        game = Game()
        print("Game started!")
        print()
        
        # Run the game
        game.run()
        
        print("Game ended.")
        
        # Print game statistics
        if hasattr(game, 'final_scores') and game.final_scores:
            print("\n🏆 Final Results:")
            print("-" * 30)
            
            # Sort scores
            sorted_scores = sorted(game.final_scores.items(), 
                                 key=lambda x: x[1], reverse=True)
            
            for rank, (player_id, score) in enumerate(sorted_scores, 1):
                if player_id == 1:
                    name = "Player"
                    emoji = "👤"
                else:
                    name = f"AI-{player_id-1}"
                    emoji = "🤖"
                
                print(f"  {rank}. {emoji} {name}: {score:.1f}%")
            
            # Display winner
            winner_id = getattr(game, 'winner_id', 0)
            if winner_id == 1:
                print("\n🎉 Congratulations! Player wins!")
            elif winner_id > 1:
                print(f"\n😅 AI-{winner_id-1} wins! Try again!")
            else:
                print("\n🤝 It's a draw!")
        
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\n❌ An error occurred while running the game: {e}")
        print("If errors persist, please check:")
        print("1. pygame and numpy are properly installed")
        print("2. All game files are in the same folder")
        print("3. Python version is 3.6 or higher")
        
        # Print debugging information
        print(f"\nPython version: {sys.version}")
        try:
            print(f"Pygame version: {pygame.version.ver}")
            print(f"NumPy version: {np.__version__}")
        except:
            pass
        
        return 1
    
    return 0


def check_dependencies():
    """Check dependencies."""
    try:
        import pygame
        import numpy as np
        return True
    except ImportError:
        return False


if __name__ == "__main__":
    # Check dependencies
    if not check_dependencies():
        print("❌ Required libraries are not installed.")
        print("\n📦 Installation method:")
        print("pip install pygame numpy")
        print("\nAlternatively:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # Run the main function
    sys.exit(main())