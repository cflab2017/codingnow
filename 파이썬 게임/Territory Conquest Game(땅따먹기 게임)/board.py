"""
Game Board Class
Handles the game map, territory management, and capture logic.
"""

import pygame
from typing import List, Tuple, Set
import numpy as np
from constants import *


class Board:
    """Class to manage the game board."""
    
    def __init__(self, width: int, height: int):
        """
        Initializes the board.
        Args:
            width: Board width
            height: Board height
        """
        self.width = width
        self.height = height
        
        # 2D array for territory management (0: empty, 1: Player, 2-6: AI)
        self.territory_map = np.zeros((height, width), dtype=np.int8)
        
        # Surfaces for each player's territory
        self.territory_surfaces = {}
        for i in range(1, MAX_AI_COUNT + 2):
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            surface.fill((0, 0, 0, 0))
            self.territory_surfaces[i] = surface
        
        # Territory percentages for each player
        self.territory_percentages = {}
        
        # Background surface
        self.background_surface = pygame.Surface((width, height))
        self.background_surface.fill(BLACK)
        
        # Set up initial player territories (small areas in each corner)
        self._init_starting_territories()
    
    def _init_starting_territories(self) -> None:
        """Initialize starting territories - give each player a small starting area."""
        territory_size = 15

        # Define starting areas
        areas = {
            1: (slice(15, 15 + territory_size), slice(15, 15 + territory_size)),
            2: (slice(15, 15 + territory_size), slice(self.width - 30, self.width - 15)),
            3: (slice(self.height - 30, self.height - 15), slice(15, 15 + territory_size)),
            4: (slice(self.height - 30, self.height - 15), slice(self.width - 30, self.width - 15)),
        }

        colors = {
            1: PLAYER_TERRITORY_COLOR,
            2: AI_TERRITORY_COLORS[0],
            3: AI_TERRITORY_COLORS[1],
            4: AI_TERRITORY_COLORS[2],
        }

        for player_id, slices in areas.items():
            if player_id > MAX_AI_COUNT + 1: continue
            
            y_slice, x_slice = slices
            # Update map
            self.territory_map[y_slice, x_slice] = player_id
            
            # Draw on surface directly
            rect = pygame.Rect(x_slice.start, y_slice.start, x_slice.stop - x_slice.start, y_slice.stop - y_slice.start)
            self.territory_surfaces[player_id].fill(colors.get(player_id, WHITE), rect)

        print(f"Board initialized successfully")
        
        # Calculate initial percentages
        self._calculate_percentages()
    
    def get_territory_at(self, x: int, y: int) -> int:
        """
        Returns the owner of the territory at a specific position.
        Args:
            x, y: Position coordinates
        Returns:
            Territory owner (0: empty, 1: Player, 2-6: AI)
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.territory_map[y, x]
        return 0
    
    def is_in_own_territory(self, x: int, y: int, player_id: int) -> bool:
        """
        Checks if a player is inside their own territory.
        Args:
            x, y: Position coordinates
            player_id: Player ID
        Returns:
            Whether the player is inside their own territory
        """
        return self.get_territory_at(x, y) == player_id
    
    def claim_territory(self, path: List[Tuple[int, int]], player_id: int) -> bool:
        """
        Claims territory based on a path.
        Args:
            path: List of points in the drawn path [(x, y), ...]
            player_id: Player ID
        Returns:
            Whether the claim was successful
        """
        if len(path) < 3:
            return False

        start_territory = self.get_territory_at(path[0][0], path[0][1])
        end_territory = self.get_territory_at(path[-1][0], path[-1][1])

        if start_territory != player_id and end_territory != player_id:
            return False

        try:
            temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            temp_surface.fill((0, 0, 0, 0))
            
            pygame.draw.polygon(temp_surface, (255, 255, 255, 255), path)
            
            path_array = np.array(path)
            min_x, min_y = np.min(path_array, axis=0)
            max_x, max_y = np.max(path_array, axis=0)

            if player_id == 1:
                color = PLAYER_TERRITORY_COLOR
            else:
                color_idx = (player_id - 2) % len(AI_TERRITORY_COLORS)
                color = AI_TERRITORY_COLORS[color_idx]
            
            player_surface = self.territory_surfaces[player_id]

            # Calculate potential claimed area
            potential_claimed_pixels = 0
            for y in range(max(0, min_y), min(self.height, max_y + 1)):
                for x in range(max(0, min_x), min(self.width, max_x + 1)):
                    if temp_surface.get_at((x, y))[3] > 0:  # If pixel is part of the polygon
                        if self.territory_map[y, x] != player_id: # If it's not already owned by this player
                            potential_claimed_pixels += 1
            
            # Check AI claim limit
            if player_id > 1 and potential_claimed_pixels > MAX_AI_CLAIM_AREA:
                return False # Claim failed due to size limit

            # Now, actually claim the territory
            for y in range(max(0, min_y), min(self.height, max_y + 1)):
                for x in range(max(0, min_x), min(self.width, max_x + 1)):
                    if temp_surface.get_at((x, y))[3] > 0:  # Check alpha
                        if self.territory_map[y, x] != player_id:
                            self.territory_map[y, x] = player_id
                            player_surface.set_at((x, y), color)
            
            self._calculate_percentages()
            return True
                
        except Exception as e:
            print(f"Error while claiming territory: {e}")
            return False
    

    
    def _calculate_percentages(self) -> None:
        """Calculate the territory percentage for each player."""
        total_pixels = self.width * self.height
        
        for player_id in range(1, 7):  # 1: Player, 2-6: AI
            owned_pixels = np.sum(self.territory_map == player_id)
            percentage = (owned_pixels / total_pixels) * 100
            self.territory_percentages[player_id] = percentage
    
    def get_territory_percentage(self, player_id: int) -> float:
        """
        Returns the territory percentage for a specific player.
        Args:
            player_id: Player ID
        Returns:
            Territory percentage (0-100)
        """
        return self.territory_percentages.get(player_id, 0.0)
    
    def draw(self, surface: pygame.Surface) -> None:
        """
        Draws the board on the screen.
        Args:
            surface: The surface to draw on
        """
        # Draw background
        surface.blit(self.background_surface, (0, 0))
        
        # Draw each player's territory
        for player_id, territory_surface in self.territory_surfaces.items():
            surface.blit(territory_surface, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
    
    def is_position_valid(self, x: int, y: int) -> bool:
        """
        Checks if a position is valid (within map boundaries).
        Args:
            x, y: Position to check
        Returns:
            Whether the position is valid
        """
        return 0 <= x < self.width and 0 <= y < self.height
    
    def get_winner(self) -> int:
        """
        Returns the player who has captured the most territory.
        Returns:
            Winner ID (0: draw)
        """
        max_percentage = 0
        winner = 0
        
        for player_id, percentage in self.territory_percentages.items():
            if percentage > max_percentage:
                max_percentage = percentage
                winner = player_id
        
        return winner if max_percentage > 0 else 0
    
    def reset(self) -> None:
        """Reset the board."""
        self.territory_map = np.zeros((self.height, self.width), dtype=np.int8)
        self.territory_surfaces = {}
        self.territory_percentages = {}
        self._init_starting_territories()