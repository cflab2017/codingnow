"""
UI Class
Manages the scoreboard, minimap, and game UI.
"""

import pygame
from typing import List, Dict, Optional
from constants import *


class UI:
    """Class to manage the game UI."""
    
    def __init__(self, screen_width: int, screen_height: int):
        """
        Initializes the UI.
        Args:
            screen_width: Screen width
            screen_height: Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Initialize font
        pygame.font.init()
        self.score_font = pygame.font.Font(None, SCORE_FONT_SIZE)
        self.ui_font = pygame.font.Font(None, UI_FONT_SIZE)
        
        # UI Colors
        self.ui_bg_color = (0, 0, 0, 128)  # Semi-transparent black
        self.ui_text_color = WHITE
        self.ui_border_color = (100, 100, 100)
        
        # Minimap settings
        self.minimap_size = 150
        self.minimap_x = GAME_WIDTH + UI_MARGIN

        self.show_minimap = True
        
        # Scoreboard position
        self.scoreboard_x = GAME_WIDTH + UI_MARGIN
        self.scoreboard_y = UI_MARGIN
        
        # Game status messages
        self.status_messages = []
        self.message_timer = 0
        
        # Fade effect
        self.fade_alpha = 0
        self.fade_direction = 0  # 0: None, 1: Fade-in, -1: Fade-out
    
    def update(self, dt: float) -> None:
        """
        Updates the UI.
        Args:
            dt: Delta time
        """
        # Update status message timer
        if self.message_timer > 0:
            self.message_timer -= 1  # Decrease per frame
            if self.message_timer <= 0:
                if self.status_messages:
                    self.status_messages.pop(0)
        
        # Update fade effect
        if self.fade_direction != 0:
            fade_speed = 3
            if self.fade_direction == 1:  # Fade-in
                self.fade_alpha += fade_speed
                if self.fade_alpha >= 255:
                    self.fade_alpha = 255
                    self.fade_direction = 0
            else:  # Fade-out
                self.fade_alpha -= fade_speed
                if self.fade_alpha <= 0:
                    self.fade_alpha = 0
                    self.fade_direction = 0
    
    def draw_scoreboard(self, surface: pygame.Surface, board, all_players: List, time_to_next_snake_spawn: float) -> None:
        """
        Draws the scoreboard.
        Args:
            surface: The surface to draw on
            board: The game board
            all_players: List of all players
            time_to_next_snake_spawn: Time until the next snake spawns
        """
        # Scoreboard background
        scoreboard_width = UI_WIDTH - 2 * UI_MARGIN
        scoreboard_height = 120 + len(all_players) * 25
        
        # Background rectangle
        bg_surface = pygame.Surface((scoreboard_width, scoreboard_height), pygame.SRCALPHA)
        bg_surface.fill(self.ui_bg_color)
        surface.blit(bg_surface, (self.scoreboard_x, self.scoreboard_y))
        
        # Border
        pygame.draw.rect(surface, self.ui_border_color, 
                        (self.scoreboard_x, self.scoreboard_y, scoreboard_width, scoreboard_height), 2)
        
        # Title
        title_text = self.score_font.render("Territory Status", True, self.ui_text_color)
        surface.blit(title_text, (self.scoreboard_x + UI_MARGIN, self.scoreboard_y + UI_MARGIN))
        
        # Display score for each player
        y_offset = self.scoreboard_y + 40
        
        # Sort player info by territory percentage
        player_scores = []
        for player in all_players:
            if player.is_alive:
                percentage = board.get_territory_percentage(player.player_id)
                player_scores.append((player, percentage))
        
        player_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Display info for each player
        for i, (player, percentage) in enumerate(player_scores):
            # Rank display
            rank_text = f"#{i+1}"
            
            # Player name
            if player.player_id == 1:
                name = "Player"
                color = PLAYER_COLOR
            else:
                name = f"AI-{player.player_id-1}"
                color_idx = (player.player_id - 2) % len(AI_COLORS)
                color = AI_COLORS[color_idx]
            
            # Territory percentage display
            score_text = f"{rank_text} {name}: {percentage:.1f}%"
            
            # Survival status display
            if not player.is_alive:
                score_text += " (Dead)"
                text_color = (128, 128, 128)  # Gray
            else:
                text_color = self.ui_text_color
            
            text_surface = self.ui_font.render(score_text, True, text_color)
            surface.blit(text_surface, (self.scoreboard_x + UI_MARGIN, y_offset))
            
            # Player color display (small rectangle)
            if player.is_alive:
                color_rect = pygame.Rect(self.scoreboard_x + scoreboard_width - 30, y_offset + 2, 20, 14)
                pygame.draw.rect(surface, color, color_rect)
                pygame.draw.rect(surface, WHITE, color_rect, 1)
            
            y_offset += 25

        # Draw snake spawn timer below minimap
        if self.show_minimap:
            minimap_y = self.scoreboard_y + scoreboard_height + UI_MARGIN * 4
            timer_y = minimap_y + self.minimap_size + UI_MARGIN
        else:
            timer_y = y_offset + UI_MARGIN * 2 # If minimap is hidden, place it below scoreboard

        timer_text = f"Next Snake: {int(time_to_next_snake_spawn)}s"
        # Use a larger font for the snake spawn timer
        large_font = pygame.font.Font(None, SCORE_FONT_SIZE + 10) # 10 points larger than score font
        timer_surface = large_font.render(timer_text, True, self.ui_text_color)
        surface.blit(timer_surface, (self.scoreboard_x + UI_MARGIN, timer_y))

    def draw_game_timer(self, surface: pygame.Surface, remaining_time: float) -> None:
        """
        Draws the game timer.
        Args:
            surface: The surface to draw on
            remaining_time: Remaining time (in seconds)
        """
        if INFINITE_MODE:
            return
        
        # Timer position (top center of the screen)
        timer_x = self.screen_width // 2 - 50
        timer_y = UI_MARGIN
        
        # Timer background
        timer_bg = pygame.Surface((100, 30), pygame.SRCALPHA)
        timer_bg.fill(self.ui_bg_color)
        surface.blit(timer_bg, (timer_x, timer_y))
        
        # Border
        pygame.draw.rect(surface, self.ui_border_color, (timer_x, timer_y, 100, 30), 2)
        
        # Time text
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        time_text = f"{minutes:02d}:{seconds:02d}"
        
        # Display in red if time is low
        if remaining_time < 30:
            text_color = RED
        elif remaining_time < 60:
            text_color = YELLOW
        else:
            text_color = self.ui_text_color
        
        timer_surface = self.ui_font.render(time_text, True, text_color)
        text_rect = timer_surface.get_rect(center=(timer_x + 50, timer_y + 15))
        surface.blit(timer_surface, text_rect)
    
    def draw_minimap(self, surface: pygame.Surface, board, all_players: List) -> None:
        """
        Draws the minimap.
        Args:
            surface: The surface to draw on
            board: The game board
            all_players: List of all players
        """
        if not self.show_minimap:
            return
        
        # Minimap background
        scoreboard_height = 120 + len(all_players) * 25
        minimap_y = self.scoreboard_y + scoreboard_height + UI_MARGIN * 4

        minimap_surface = pygame.Surface((self.minimap_size, self.minimap_size), pygame.SRCALPHA)
        minimap_surface.fill((0, 0, 0, 180))
        
        # Scaling ratio
        scale_x = self.minimap_size / GAME_WIDTH
        scale_y = self.minimap_size / GAME_HEIGHT
        
        # Territory display (simple pixel sampling)
        sample_rate = 8  # Sample every 8 pixels
        for x in range(0, GAME_WIDTH, sample_rate):
            for y in range(0, GAME_HEIGHT, sample_rate):
                territory = board.get_territory_at(x, y)
                if territory > 0:
                    # Convert to minimap coordinates
                    mini_x = int(x * scale_x)
                    mini_y = int(y * scale_y)
                    
                    # Set territory color
                    if territory == 1:
                        color = PLAYER_COLOR
                    else:
                        color_idx = (territory - 2) % len(AI_COLORS)
                        color = AI_COLORS[color_idx]
                    
                    # Display as a small rectangle
                    mini_rect = pygame.Rect(mini_x, mini_y, 2, 2)
                    pygame.draw.rect(minimap_surface, color, mini_rect)
        
        # Player position display
        for player in all_players:
            if player.is_alive:
                pos = player.get_position()
                mini_x = int(pos[0] * scale_x)
                mini_y = int(pos[1] * scale_y)
                
                # Player color
                if player.player_id == 1:
                    color = WHITE
                else:
                    color = WHITE
                
                # Display as a small circle
                pygame.draw.circle(minimap_surface, color, (mini_x, mini_y), 3)
                pygame.draw.circle(minimap_surface, BLACK, (mini_x, mini_y), 3, 1)
        
        # Draw minimap surface
        surface.blit(minimap_surface, (self.minimap_x, minimap_y))
        
        # Minimap border
        pygame.draw.rect(surface, self.ui_border_color, 
                        (self.minimap_x, minimap_y, self.minimap_size, self.minimap_size), 2)
        
        # Minimap title
        title = self.ui_font.render("Minimap", True, self.ui_text_color)
        surface.blit(title, (self.minimap_x, minimap_y - 20))
    
    def draw_status_messages(self, surface: pygame.Surface) -> None:
        """Display status messages."""
        if not self.status_messages:
            return
        
        message = self.status_messages[0]
        text_surface = self.score_font.render(message, True, WHITE)
        
        # Display in the center of the screen
        text_rect = text_surface.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2))
        
        # Add background
        bg_rect = text_rect.inflate(40, 20)
        bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 180))
        
        surface.blit(bg_surface, bg_rect)
        pygame.draw.rect(surface, WHITE, bg_rect, 2)
        surface.blit(text_surface, text_rect)
    
    def draw_game_over_screen(self, surface: pygame.Surface, winner_id: int, 
                             final_scores: Dict[int, float]) -> None:
        """
        Draws the game over screen.
        Args:
            surface: The surface to draw on
            winner_id: Winner ID
            final_scores: Dictionary of final scores
        """
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = pygame.font.Font(None, 48).render("GAME OVER!", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(self.screen_width // 2, GAME_HEIGHT // 2 - 150))
        surface.blit(game_over_text, game_over_rect)
        
        # Winner display
        if winner_id == 1:
            winner_text = "Player Wins!"
            color = PLAYER_COLOR
        elif winner_id > 1:
            winner_text = f"AI-{winner_id-1} Wins!"
            color_idx = (winner_id - 2) % len(AI_COLORS)
            color = AI_COLORS[color_idx]
        else:
            winner_text = "Draw!"
            color = WHITE
        
        winner_surface = pygame.font.Font(None, 36).render(winner_text, True, color)
        winner_rect = winner_surface.get_rect(center=(self.screen_width // 2, GAME_HEIGHT // 2 - 100))
        surface.blit(winner_surface, winner_rect)
        
        # Final score display
        y_offset = GAME_HEIGHT // 2
        score_title = self.score_font.render("Final Scores:", True, WHITE)
        score_title_rect = score_title.get_rect(center=(self.screen_width // 2, y_offset))
        surface.blit(score_title, score_title_rect)
        
        # Sort scores in descending order
        sorted_scores = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
        
        y_offset += 40
        for rank, (player_id, score) in enumerate(sorted_scores, 1):
            if player_id == 1:
                name = "Player"
            else:
                name = f"AI-{player_id-1}"
            
            score_text = f"{rank}. {name}: {score:.1f}%"
            score_surface = self.ui_font.render(score_text, True, WHITE)
            score_rect = score_surface.get_rect(center=(self.screen_width // 2, y_offset))
            surface.blit(score_surface, score_rect)
            
            y_offset += 25
        
        # Restart instructions
        restart_text = self.ui_font.render("Press R to Restart, ESC to Exit", True, WHITE)
        restart_rect = restart_text.get_rect(center=(self.screen_width // 2, GAME_HEIGHT - 50))
        surface.blit(restart_text, restart_rect)
    
    def draw_controls_help(self, surface: pygame.Surface) -> None:
        """Display controls help."""
        help_x = GAME_WIDTH + UI_MARGIN
        help_y = self.screen_height - 150
        
        help_lines = [
            "Controls:",
            "WASD/Arrow Keys: Move",
            "P/Space: Pause",
            "R: Restart",
            "M: Toggle Minimap",
            "ESC: Exit"
        ]
        
        for i, line in enumerate(help_lines):
            help_surface = self.ui_font.render(line, True, (200, 200, 200))
            surface.blit(help_surface, (help_x, help_y + i * 18))
    
    def add_status_message(self, message: str, duration: float = 3.0) -> None:
        """
        Adds a status message.
        Args:
            message: The message to display
            duration: The duration to display for (in seconds)
        """
        self.status_messages.append(message)
        self.message_timer = duration * 60  # Convert to frames (assuming 60 FPS)
    
    def start_fade_in(self) -> None:
        """Start fade-in."""
        self.fade_direction = 1
        self.fade_alpha = 0
    
    def start_fade_out(self) -> None:
        """Start fade-out."""
        self.fade_direction = -1
        self.fade_alpha = 0
    
    def draw_fade(self, surface: pygame.Surface) -> None:
        """Draw fade effect."""
        if self.fade_alpha > 0:
            fade_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            fade_surface.fill((0, 0, 0, self.fade_alpha))
            surface.blit(fade_surface, (0, 0))
    
    def toggle_minimap(self) -> None:
        """Toggle minimap display."""
        self.show_minimap = not self.show_minimap