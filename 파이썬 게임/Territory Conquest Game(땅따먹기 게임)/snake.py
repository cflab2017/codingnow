"""
Snake Class
Represents a snake entity that moves around the game board.
"""

import pygame
import random
import math
from typing import List, Tuple
from constants import *

class Snake:
    """
    A simple snake entity that moves around the game board.
    Collides with players and their trails.
    """
    
    def __init__(self, x: int, y: int):
        """
        Initializes the snake.
        Args:
            x, y: Starting position of the snake's head.
        """
        self.x = float(x)
        self.y = float(y)
        self.speed = SNAKE_SPEED
        self.color = SNAKE_COLOR
        self.segment_size = SNAKE_SEGMENT_SIZE
        
        # Snake body segments
        self.body: List[Tuple[int, int]] = []
        for _ in range(SNAKE_INITIAL_LENGTH):
            self.body.append((int(self.x), int(self.y)))
        
        # Movement direction (dx, dy)
        self.dx = 0.0
        self.dy = 0.0
        self._set_random_direction()
        
        self.last_move_time = pygame.time.get_ticks()
        self.move_interval_ms = int(SNAKE_UPDATE_INTERVAL * 1000)
        
    def _set_random_direction(self) -> None:
        """Sets a random initial direction for the snake."""
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.dx, self.dy = random.choice(directions)
        
    def update(self, board, dt: float) -> None:
        """
        Updates the snake's position and body.
        Args:
            board: The game board object.
            dt: Delta time (time between frames).
        """
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_move_time > self.move_interval_ms:
            self.last_move_time = current_time
            
            # Calculate potential new head position
            potential_new_x = self.x + self.dx * self.segment_size
            potential_new_y = self.y + self.dy * self.segment_size
            
            # Check for collision with claimed territory
            # Convert potential new position to board coordinates
            board_x = int(potential_new_x)
            board_y = int(potential_new_y)

            if board.is_position_valid(board_x, board_y) and board.get_territory_at(board_x, board_y) != 0:
                # Bounce off claimed territory
                self.dx *= -1
                self.dy *= -1
                # Recalculate potential new position with reversed direction
                potential_new_x = self.x + self.dx * self.segment_size
                potential_new_y = self.y + self.dy * self.segment_size
                # Also change direction randomly to avoid getting stuck
                self._change_direction()

            # Simple boundary handling: bounce off walls
            if potential_new_x < 0 or potential_new_x >= GAME_WIDTH:
                self.dx *= -1
                potential_new_x = self.x + self.dx * self.segment_size # Re-calculate with new direction
            if potential_new_y < 0 or potential_new_y >= GAME_HEIGHT:
                self.dy *= -1
                potential_new_y = self.y + self.dy * self.segment_size # Re-calculate with new direction
            
            self.x = potential_new_x
            self.y = potential_new_y
            
            # Add new head position and remove tail segment
            self.body.insert(0, (int(self.x), int(self.y)))
            if len(self.body) > SNAKE_INITIAL_LENGTH:
                self.body.pop()
            
            # Occasionally change direction
            if random.random() < 0.1: # 10% chance to change direction
                self._change_direction()
                
    def _change_direction(self) -> None:
        """Changes the snake's direction randomly, avoiding immediate reversal."""
        possible_directions = []
        if self.dx == 0: # Moving vertically
            possible_directions.append((1, 0)) # Right
            possible_directions.append((-1, 0)) # Left
        elif self.dy == 0: # Moving horizontally
            possible_directions.append((0, 1)) # Down
            possible_directions.append((0, -1)) # Up
        
        if possible_directions:
            self.dx, self.dy = random.choice(possible_directions)
            
    def draw(self, surface: pygame.Surface) -> None:
        """
        Draws the snake on the screen.
        Args:
            surface: The surface to draw on.
        """
        if not self.body:
            return

        # Draw head with a distinct color
        head_color = (255, 255, 0) # Yellow for head
        head_segment = self.body[0]
        head_x, head_y = head_segment[0], head_segment[1]
        pygame.draw.rect(surface, head_color, (head_x, head_y, self.segment_size, self.segment_size))

        # Draw eyes
        eye_radius = 2
        eye_color = BLACK
        # Calculate eye positions based on direction
        if self.dx == 1: # Moving right
            eye1_pos = (head_x + self.segment_size - eye_radius * 2, head_y + eye_radius * 2)
            eye2_pos = (head_x + self.segment_size - eye_radius * 2, head_y + self.segment_size - eye_radius * 2)
        elif self.dx == -1: # Moving left
            eye1_pos = (head_x + eye_radius * 2, head_y + eye_radius * 2)
            eye2_pos = (head_x + eye_radius * 2, head_y + self.segment_size - eye_radius * 2)
        elif self.dy == 1: # Moving down
            eye1_pos = (head_x + eye_radius * 2, head_y + self.segment_size - eye_radius * 2)
            eye2_pos = (head_x + self.segment_size - eye_radius * 2, head_y + self.segment_size - eye_radius * 2)
        elif self.dy == -1: # Moving up
            eye1_pos = (head_x + eye_radius * 2, head_y + eye_radius * 2)
            eye2_pos = (head_x + self.segment_size - eye_radius * 2, head_y + eye_radius * 2)
        else: # Default (e.g., stopped or initial state)
            eye1_pos = (head_x + self.segment_size // 4, head_y + self.segment_size // 4)
            eye2_pos = (head_x + self.segment_size * 3 // 4, head_y + self.segment_size // 4)

        pygame.draw.circle(surface, eye_color, eye1_pos, eye_radius)
        pygame.draw.circle(surface, eye_color, eye2_pos, eye_radius)

        # Draw tongue
        tongue_length = self.segment_size // 2
        tongue_color = RED
        if self.dx == 1: # Moving right
            tongue_start = (head_x + self.segment_size, head_y + self.segment_size // 2)
            tongue_end = (head_x + self.segment_size + tongue_length, head_y + self.segment_size // 2)
        elif self.dx == -1: # Moving left
            tongue_start = (head_x, head_y + self.segment_size // 2)
            tongue_end = (head_x - tongue_length, head_y + self.segment_size // 2)
        elif self.dy == 1: # Moving down
            tongue_start = (head_x + self.segment_size // 2, head_y + self.segment_size)
            tongue_end = (head_x + self.segment_size // 2, head_y + self.segment_size + tongue_length)
        elif self.dy == -1: # Moving up
            tongue_start = (head_x + self.segment_size // 2, head_y)
            tongue_end = (head_x + self.segment_size // 2, head_y - tongue_length)
        else:
            tongue_start = (head_x + self.segment_size, head_y + self.segment_size // 2)
            tongue_end = (head_x + self.segment_size + tongue_length, head_y + self.segment_size // 2)
        
        pygame.draw.line(surface, tongue_color, tongue_start, tongue_end, 2)

        # Draw body segments
        for segment in self.body[1:]:
            pygame.draw.rect(surface, self.color, (segment[0], segment[1], self.segment_size, self.segment_size))
            
    def get_head_position(self) -> Tuple[int, int]:
        """Returns the current head position of the snake."""
        return (int(self.x), int(self.y))
        
    def get_body_segments(self) -> List[Tuple[int, int]]:
        """Returns all body segments of the snake."""
        return self.body
    
    def check_collision_with_point(self, point: Tuple[int, int], tolerance: int = 5) -> bool:
        """
        Checks if the snake's head collides with a given point.
        Args:
            point: The point to check collision against.
            tolerance: The collision tolerance.
        Returns:
            True if collision, False otherwise.
        """
        head_x, head_y = self.get_head_position()
        point_x, point_y = point
        
        distance = math.sqrt((head_x - point_x)**2 + (head_y - point_y)**2)
        return distance < (self.segment_size / 2 + tolerance)
