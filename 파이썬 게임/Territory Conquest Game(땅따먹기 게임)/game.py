"""
Main Game Class
Integrates all game logic and handles the main loop.
"""

import pygame
import time
import random # Import random module
from typing import List, Optional
from constants import *
from board import Board
from player import Player
from enemy import Enemy
from ui import UI
from snake import Snake # Import Snake class


class Game:
    """Main game class - manages all game logic."""
    
    def __init__(self):
        """Initializes the game."""
        # Initialize Pygame
        pygame.init()
        pygame.mixer.init() # Initialize mixer
        
        # Screen settings
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Territory Conquest - Paper.io Style")
        
        # Clock settings
        self.clock = pygame.time.Clock()
        
        # Initialize game components
        self.board = Board(GAME_WIDTH, GAME_HEIGHT)
        self.ui = UI(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Initialize snake
        self.snakes = []
        self.snakes.append(Snake(GAME_WIDTH // 2, GAME_HEIGHT // 2)) # Create initial snake instance
        self.last_snake_spawn_time = time.time()
        
        # Sound effects
        self.sound_claim_territory = None
        self.sound_player_death = None
        self.sound_line_draw = None
        if SOUND_ENABLED:
            try:
                self.sound_claim_territory = pygame.mixer.Sound(SOUND_CLAIM_TERRITORY)
                self.sound_player_death = pygame.mixer.Sound(SOUND_PLAYER_DEATH)
                self.sound_line_draw = pygame.mixer.Sound(SOUND_LINE_DRAW)
            except pygame.error as e:
                print(f"Could not load sound: {e}")
                # If any sound fails to load, disable all sounds
                self.sound_claim_territory = None
                self.sound_player_death = None
                self.sound_line_draw = None
                # Note: SOUND_ENABLED is a module-level constant, cannot be changed directly here.
                # The checks `if self.sound_... and SOUND_ENABLED:` will handle this.
            except FileNotFoundError as e:
                print(f"Sound file not found: {e}")
                self.sound_claim_territory = None
                self.sound_player_death = None
                self.sound_line_draw = None
            except Exception as e:
                print(f"An unexpected error occurred while loading sound: {e}")
                self.sound_claim_territory = None
                self.sound_player_death = None
                self.sound_line_draw = None
        
        # Game state
        self.game_state = GAME_STATE_PLAYING
        self.running = True
        
        # Time management
        self.game_start_time = time.time()
        self.game_time_limit = GAME_TIME if not INFINITE_MODE else float('inf')
        
        # Initialize players
        self.all_players = []
        self._init_players()
        
        # Performance monitoring
        self.frame_count = 0
        self.last_fps_time = time.time()
        self.current_fps = 0
        
        # Rendering optimization
        self.last_ui_update = time.time()
        self.ui_update_interval = 0.1  # Update UI every 0.1 seconds
        
        # Game start message
        self.ui.add_status_message("Game Start! Conquer the territory!", 3.0)
    
    def _init_players(self) -> None:
        """Initialize players."""
        # Player (center of top-left starting area)
        player = Player(22, 22, 1, self.sound_line_draw, self.sound_player_death, self.sound_claim_territory)  # Pass sound objects
        self.all_players.append(player)
        
        # AIs (center of each starting area)
        ai_positions = [
            (GAME_WIDTH - 22, 22),      # AI 1 (top-right)
            (22, GAME_HEIGHT - 22),     # AI 2 (bottom-left)
            (GAME_WIDTH - 22, GAME_HEIGHT - 22)  # AI 3 (bottom-right)
        ]
        
        for i, (x, y) in enumerate(ai_positions[:MAX_AI_COUNT]):
            ai = Enemy(x, y, i + 2, self.sound_line_draw, self.sound_player_death, self.sound_claim_territory)  # Pass sound objects
            self.all_players.append(ai)
    
    def run(self) -> None:
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time (in seconds)
            
            self._handle_events()
            self._update(dt)
            self._draw()
            self._update_fps()
        
        pygame.quit()
    
    def _handle_events(self) -> None:
        """Handle events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                elif event.key == pygame.K_r:
                    self._restart_game()
                
                elif event.key == pygame.K_m:
                    self.ui.toggle_minimap()
                
                elif event.key == pygame.K_p or event.key == pygame.K_SPACE:
                    self.toggle_pause()
        
        # Handle player input (only when the game is playing)
        if self.game_state == GAME_STATE_PLAYING:
            keys = pygame.key.get_pressed()
            # Handle input for the player only
            for player in self.all_players:
                if player.player_id == 1 and player.is_alive:
                    player.handle_input(keys)
                    break  # Only one player, so exit
    
    def _update(self, dt: float) -> None:
        """Update game state."""
        # Update UI
        self.ui.update(dt)
        
        if self.game_state == GAME_STATE_PLAYING:
            self._update_game_playing(dt)
        elif self.game_state == GAME_STATE_GAME_OVER:
            self._update_game_over(dt)
        elif self.game_state == GAME_STATE_PAUSED:
            pass  # Do nothing when paused
    
    def _update_game_playing(self, dt: float) -> None:
        """Update while the game is in progress."""
        # Check time
        if not INFINITE_MODE:
            elapsed_time = time.time() - self.game_start_time
            if elapsed_time >= self.game_time_limit:
                self._end_game()
                return
        
        # Update players
        for player in self.all_players:
            if player.is_alive:
                if isinstance(player, Enemy):
                    player.update_ai(self.board, self.all_players, dt)
                else:
                    player.update(self.board, dt)
        
        # Snake spawning logic
        if time.time() - self.last_snake_spawn_time > SNAKE_SPAWN_INTERVAL and len(self.snakes) < MAX_SNAKES:
            spawn_x = random.randint(0, GAME_WIDTH - 1)
            spawn_y = random.randint(0, GAME_HEIGHT - 1)
            self.snakes.append(Snake(spawn_x, spawn_y))
            self.last_snake_spawn_time = time.time()

        # Update all snakes
        for snake in self.snakes:
            snake.update(self.board, dt)
        
        # Check for snake collisions
        self._check_snake_collisions()
        
        # Re-enable player collision checks
        self._check_player_collisions()
        
        # Check victory conditions
        self._check_victory_conditions()
    
    def _update_game_over(self, dt: float) -> None:
        """Update in game over state."""
        pass  # No specific processing for now
    
    def _check_player_collisions(self) -> None:
        """
        Check for collisions between players and handle bouncing.
        This method is for player-player and player-trail collisions.
        Snake collisions are handled in _check_snake_collisions.
        """
        alive_players = [p for p in self.all_players if p.is_alive]
        
        for i, player in enumerate(alive_players):
            if not player.is_alive:
                continue
            
            player_pos = player.get_position()
            
            # Check for collision with other players' trails
            for j, other_player in enumerate(alive_players):
                if i == j or not other_player.is_alive:
                    continue
                
                # Check for collision with another player's trail
                if other_player.is_position_on_trail(player_pos, tolerance=8):
                    # Bounce player off the trail
                    player.dx *= -1
                    player.dy *= -1
                    player.trail.clear() # Clear player's trail on bounce
                    player.trail_positions.clear()
                    break # Only bounce once per frame for trail collision
                
                # Check for direct collision between players
                other_pos = other_player.get_position()
                distance = ((player_pos[0] - other_pos[0])**2 + (player_pos[1] - other_pos[1])**2)**0.5
                if distance < 15:  # Direct collision
                    # Bounce both players
                    player.dx *= -1
                    player.dy *= -1
                    other_player.dx *= -1
                    other_player.dy *= -1
                    # Clear trails on direct collision
                    player.trail.clear()
                    player.trail_positions.clear()
                    other_player.trail.clear()
                    other_player.trail_positions.clear()
    
    def _check_snake_collisions(self) -> None:
        """
        Check for collisions between all snakes and players/player trails.
        """
        for snake in self.snakes:
            snake_head = snake.get_head_position()
            
            for player in self.all_players:
                if not player.is_alive:
                    continue
                
                # Collision with player's head
                player_head = player.get_position()
                if snake.check_collision_with_point(player_head, tolerance=10):
                    player.kill()
                    self._handle_player_death(player)
                    continue # Player is dead, no need to check trail
                
                # Collision with player's trail
                if player.is_position_on_trail(snake_head, tolerance=5):
                    player.kill()
                    self._handle_player_death(player)
                    continue

    def _handle_player_death(self, player: Player) -> None:
        """Handle player death."""
        if player.player_id == 1:
            self.ui.add_status_message("Player Died!", 2.0)
        else:
            self.ui.add_status_message(f"AI-{player.player_id-1} Died!", 2.0)
    
    def _check_victory_conditions(self) -> None:
        """Check victory conditions - changed to infinite mode."""
        # No victory condition check in infinite mode
        # Game ends only when the player presses ESC or R to restart
        pass
    
    def _end_game(self) -> None:
        """Handle game end."""
        self.game_state = GAME_STATE_GAME_OVER
        
        # Calculate final scores
        final_scores = {}
        for player in self.all_players:
            percentage = self.board.get_territory_percentage(player.player_id)
            final_scores[player.player_id] = percentage
        
        # Determine winner
        winner_id = self.board.get_winner()
        
        # Victory message
        if winner_id == 1:
            self.ui.add_status_message("Player Wins!", 5.0)
        elif winner_id > 1:
            self.ui.add_status_message(f"AI-{winner_id-1} Wins!", 5.0)
        else:
            self.ui.add_status_message("Draw!", 5.0)
        
        # Save final scores
        self.final_scores = final_scores
        self.winner_id = winner_id
    
    def _draw(self) -> None:
        """Draw the screen."""
        # Clear background
        self.screen.fill(BLACK)
        
        # Draw board
        self.board.draw(self.screen)
        
        # Draw players
        for player in self.all_players:
            player.draw(self.screen)
        
        # Draw all snakes
        for snake in self.snakes:
            snake.draw(self.screen)
        
        # Draw UI
        if self.game_state == GAME_STATE_PLAYING:
            self._draw_game_ui()
        elif self.game_state == GAME_STATE_GAME_OVER:
            self._draw_game_over_ui()
        elif self.game_state == GAME_STATE_PAUSED:
            self._draw_paused_ui()
        
        # Fade effect
        self.ui.draw_fade(self.screen)
        
        # Update screen
        pygame.display.flip()
    
    def _draw_game_ui(self) -> None:
        """Draw in-game UI - performance optimized."""
        current_time = time.time()
        
        # Don't update UI too frequently (performance improvement)
        if current_time - self.last_ui_update > self.ui_update_interval:
            self.last_ui_update = current_time
            
            # Calculate remaining time for snake spawn
            time_to_next_snake_spawn = max(0, SNAKE_SPAWN_INTERVAL - (current_time - self.last_snake_spawn_time))

            # Scoreboard
            self.ui.draw_scoreboard(self.screen, self.board, self.all_players, time_to_next_snake_spawn)
            
            # Minimap
            self.ui.draw_minimap(self.screen, self.board, self.all_players)
        else:
            # Use previous UI (fast rendering)
            time_to_next_snake_spawn = max(0, SNAKE_SPAWN_INTERVAL - (current_time - self.last_snake_spawn_time))
            self.ui.draw_scoreboard(self.screen, self.board, self.all_players, time_to_next_snake_spawn)
            self.ui.draw_minimap(self.screen, self.board, self.all_players)
        
        # Status messages (always display)
        self.ui.draw_status_messages(self.screen)
        
        # Controls help
        self.ui.draw_controls_help(self.screen)
        
        # UI separator line
        pygame.draw.line(self.screen, (100, 100, 100), (GAME_WIDTH, 0), (GAME_WIDTH, SCREEN_HEIGHT), 2)

        # FPS display (for development)
        fps_text = pygame.font.Font(None, 24).render(f"FPS: {self.current_fps}", True, WHITE)
        self.screen.blit(fps_text, (GAME_WIDTH + UI_MARGIN, SCREEN_HEIGHT - 30))
    
    def _draw_game_over_ui(self) -> None:
        """Draw game over UI."""
        # Display in-game UI as background
        self._draw_game_ui()
        
        # Game over screen
        self.ui.draw_game_over_screen(self.screen, self.winner_id, self.final_scores)
    
    def _draw_paused_ui(self) -> None:
        """Draw paused UI."""
        # Display in-game UI as background
        self._draw_game_ui()
        
        # Paused message
        font = pygame.font.Font(None, 72)
        paused_text = font.render("PAUSED", True, WHITE)
        text_rect = paused_text.get_rect(center=(GAME_WIDTH//2, GAME_HEIGHT//2))
        
        # Add background
        bg_rect = text_rect.inflate(40, 20)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), bg_rect)
        pygame.draw.rect(self.screen, WHITE, bg_rect, 3)
        
        self.screen.blit(paused_text, text_rect)
        
        # Display controls
        font_small = pygame.font.Font(None, 36)
        help_text = font_small.render("Press P or SPACE to resume", True, WHITE)
        help_rect = help_text.get_rect(center=(GAME_WIDTH//2, GAME_HEIGHT//2 + 80))
        self.screen.blit(help_text, help_rect)
    
    def _restart_game(self) -> None:
        """Restart the game."""
        # Reset game state
        self.game_state = GAME_STATE_PLAYING
        self.game_start_time = time.time()
        
        # Reset board
        self.board.reset()
        
        # Reset players
        self.all_players.clear()
        self._init_players()
        
        # UI message
        self.ui.add_status_message("Game Restarted!", 2.0)
        
        # Reset state
        self.final_scores = {}
        self.winner_id = 0
    
    def _update_fps(self) -> None:
        """Calculate and update FPS."""
        self.frame_count += 1
        current_time = time.time()
        
        if current_time - self.last_fps_time >= 1.0:  # Update every second
            self.current_fps = self.frame_count
            self.frame_count = 0
            self.last_fps_time = current_time
    
    def get_game_statistics(self) -> dict:
        """
        Return game statistics.
        Returns:
            Dictionary of game statistics
        """
        stats = {
            "game_time": time.time() - self.game_start_time,
            "alive_players": sum(1 for p in self.all_players if p.is_alive),
            "total_players": len(self.all_players),
            "current_leader": self.board.get_winner(),
            "territories": {}
        }
        
        for player in self.all_players:
            percentage = self.board.get_territory_percentage(player.player_id)
            stats["territories"][player.player_id] = {
                "percentage": percentage,
                "alive": player.is_alive,
                "is_player": player.player_id == 1
            }
        
        return stats
    
    def pause_game(self) -> None:
        """Pause the game."""
        if self.game_state == GAME_STATE_PLAYING:
            self.game_state = GAME_STATE_PAUSED
            self.ui.add_status_message("Game Paused", 1.0)
    
    def resume_game(self) -> None:
        """Resume the game."""
        if self.game_state == GAME_STATE_PAUSED:
            self.game_state = GAME_STATE_PLAYING
            self.ui.add_status_message("Game Resumed", 1.0)
    
    def toggle_pause(self) -> None:
        """Toggle pause."""
        if self.game_state == GAME_STATE_PLAYING:
            self.pause_game()
        elif self.game_state == GAME_STATE_PAUSED:
            self.resume_game()