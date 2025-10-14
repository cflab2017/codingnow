"""
Enemy AI Class
Handles AI behavior logic and competition with the player.
"""

import pygame
import random
import math
import time
from typing import List, Tuple, Optional
from player import Player
from constants import *


class Enemy(Player):
    """Class to manage AI enemy characters (inherits from Player)."""
    
    def __init__(self, x: int, y: int, player_id: int,
                 sound_line_draw: Optional[pygame.mixer.Sound] = None,
                 sound_player_death: Optional[pygame.mixer.Sound] = None,
                 sound_claim_territory: Optional[pygame.mixer.Sound] = None):
        """
        Initializes the AI enemy.
        Args:
            x, y: Starting position
            player_id: AI identifier (2-6)
            sound_line_draw: 선 그리기 사운드 객체
            sound_player_death: 플레이어 사망 사운드 객체
            sound_claim_territory: 영역 점령 사운드 객체
        """
        super().__init__(x, y, player_id, sound_line_draw, sound_player_death, sound_claim_territory)
        
        # AI-specific attributes
        self.ai_state = "explore"  # explore, attack, retreat, return_home"
        self.target_player = None
        self.state_timer = 0
        self.direction_change_timer = 0
        self.stuck_counter = 0
        self.last_positions = []
        
        # AI personality settings (randomly determined)
        self.aggression = random.uniform(0.3, 0.8)  # Aggressiveness
        self.caution = random.uniform(0.2, 0.7)    # Caution
        self.exploration = random.uniform(0.4, 0.9) # Exploration tendency
        
        # Target point
        self.target_x = x
        self.target_y = y
        
        # Desired direction for smoother turning
        self.target_dx = 0.0
        self.target_dy = 0.0
        self.turn_speed = AI_TURN_SPEED

        # Last safe position (where AI last left its territory)
        self.last_safe_x = float(x)
        self.last_safe_y = float(y)
        self.is_currently_in_territory = True # Track AI's current territory status
        
        # Start in a stopped state initially
        # self._set_random_direction()
    
    def update_ai(self, board, all_players: List[Player], dt: float) -> None:
        """
        Update AI logic.
        Args:
            board: The game board
            all_players: List of all players
        """
        if not self.is_alive:
            return
        
        # 2-second delay after game start
        if not hasattr(self, '_started_at'):
            self._started_at = time.time()
        
        if time.time() - self._started_at < 2.0:
            return  # Wait for 2 seconds
        
        # Set initial direction at the very beginning
        if not hasattr(self, '_ai_started'):
            self._set_random_direction()
            self._ai_started = True
        
        self.state_timer += 1
        self.direction_change_timer += 1
        
        # Record position (for detecting if stuck)
        current_pos = (int(self.x), int(self.y))
        self.last_positions.append(current_pos)
        if len(self.last_positions) > 30:
            self.last_positions.pop(0)
        
        # Detect if stuck
        if len(self.last_positions) >= 20:
            if self._is_stuck():
                self.stuck_counter += 1
                if self.stuck_counter > 30:  # Stuck for 30 consecutive frames
                    self._handle_stuck_state()
            else:
                self.stuck_counter = 0
        
        # Assess nearby danger
        danger_level = self._assess_danger(board, all_players)
        
        # Decide state
        self._decide_state(board, all_players, danger_level)
        
        # Execute action based on state
        self._execute_state_action(board, all_players)
        
        # Gradually update current direction towards target direction
        self._update_current_direction(dt)

        # Call parent class update
        super().update(board, dt)

        # Update last safe position if AI just left its territory
        if self.is_currently_in_territory and not self.is_in_territory:
            self.last_safe_x = self.x
            self.last_safe_y = self.y
            self.is_currently_in_territory = False
        elif not self.is_currently_in_territory and self.is_in_territory:
            self.is_currently_in_territory = True
    
    def _assess_danger(self, board, all_players: List[Player]) -> float:
        """
        Assess the danger level of the current position.
        Args:
            board: The game board
            all_players: List of all players
        Returns:
            Danger level (0.0 to 1.0)
        """
        danger = 0.0
        current_pos = (int(self.x), int(self.y))
        
        # Check distance to other players
        for player in all_players:
            if player.player_id != self.player_id and player.is_alive:
                player_pos = player.get_position()
                distance = self._distance(current_pos, player_pos)
                
                if distance < AI_PLAYER_DETECTION_RANGE:
                    # Danger increases as distance decreases
                    proximity_danger = 1.0 - (distance / AI_PLAYER_DETECTION_RANGE)
                    danger += proximity_danger * 0.5
                    
                    # Very dangerous if the opponent is drawing a trail nearby
                    if not player.is_in_territory and len(player.trail) > 0:
                        for trail_pos in player.trail[-10:]:  # Check recent trail only
                            trail_distance = self._distance(current_pos, trail_pos)
                            if trail_distance < 20:
                                danger += 0.8
        
        # Danger increases near screen boundaries
        margin = 50
        if (self.x < margin or self.x > GAME_WIDTH - margin or 
            self.y < margin or self.y > GAME_HEIGHT - margin):
            danger += 0.2
        
        # Danger increases near own trail
        if len(self.trail) > 10:
            for trail_pos in self.trail[:-5]:  # Exclude the last 5 points
                trail_distance = self._distance(current_pos, trail_pos)
                if trail_distance < 15:
                    danger += 0.4
                    break
        
        return min(danger, 1.0)
    
    def _decide_state(self, board, all_players: List[Player], danger_level: float) -> None:
        """
        Decide the AI's state.
        Args:
            board: The game board
            all_players: List of all players
            danger_level: Current danger level
        """
        # If it's dangerous, retreat or return home
        if danger_level > 0.6:
            if self.is_in_territory:
                self.ai_state = "retreat"
            else:
                self.ai_state = "return_home"
        
        # If outside territory and trail is getting too long, return home more aggressively
        elif not self.is_in_territory and len(self.trail) > MAX_TRAIL_LENGTH * 0.5: # Return home if trail is half max length
            self.ai_state = "return_home"
        
        # If AI has moved too far from its last safe point, return home
        if not self.is_in_territory and self._distance((self.x, self.y), (self.last_safe_x, self.last_safe_y)) > AI_MAX_MOVE_DISTANCE:
            self.ai_state = "return_home"
        
        # Occasionally act aggressively
        elif (self.state_timer > 180 and random.random() < self.aggression * 0.02 and
              self.is_in_territory):
            # If an enemy is nearby, switch to attack mode
            nearby_enemy = self._find_nearest_enemy(all_players)
            if nearby_enemy:
                self.target_player = nearby_enemy
                self.ai_state = "attack"
        
        # Default to exploring
        elif self.ai_state not in ["attack", "return_home"] or self.state_timer > 300:
            self.ai_state = "explore"
            self.state_timer = 0
    
    def _execute_state_action(self, board, all_players: List[Player]) -> None:
        """
        Execute action based on state.
        Args:
            board: The game board
            all_players: List of all players
        """
        if self.ai_state == "explore":
            self._explore_behavior()
        
        elif self.ai_state == "attack":
            self._attack_behavior(board, all_players)
        
        elif self.ai_state == "retreat":
            self._retreat_behavior(board)
        
        elif self.ai_state == "return_home":
            self._return_home_behavior(board)
        
        # Periodically change direction
        if (self.direction_change_timer > 60 and 
            random.random() < AI_DIRECTION_CHANGE_CHANCE):
            self._change_direction_slightly()
            self.direction_change_timer = 0
    
    def _explore_behavior(self) -> None:
        """Exploration behavior."""
        # Move towards the target point
        if self.direction_change_timer > 120 or self._distance((self.x, self.y), (self.target_x, self.target_y)) < 30:
            # Set a new target within MAX_EXPLORATION_DISTANCE from current position
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(50, MAX_EXPLORATION_DISTANCE)
            
            new_target_x = self.x + math.cos(angle) * distance
            new_target_y = self.y + math.sin(angle) * distance
            
            # Ensure target is within game boundaries
            self.target_x = max(0, min(GAME_WIDTH - 1, new_target_x))
            self.target_y = max(0, min(GAME_HEIGHT - 1, new_target_y))
            
            self.direction_change_timer = 0
        
        # Move towards the target
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        self.set_direction(dx, dy)
    
    def _attack_behavior(self, board, all_players: List[Player]) -> None:
        """Attack behavior."""
        if not self.target_player or not self.target_player.is_alive:
            self.ai_state = "explore"
            return
        
        target_pos = self.target_player.get_position()
        
        # Try to block the target's path
        if (not self.target_player.is_in_territory and 
            len(self.target_player.trail) > 0):
            
            # Aim for the middle of the target's trail
            trail = self.target_player.get_trail_copy()
            if len(trail) > 3:
                intercept_point = trail[len(trail) // 2]
                dx = intercept_point[0] - self.x
                dy = intercept_point[1] - self.y
                self.set_direction(dx, dy)
            else:
                # Track the target directly
                dx = target_pos[0] - self.x
                dy = target_pos[1] - self.y
                self.set_direction(dx, dy)
        else:
            # Move towards the target
            dx = target_pos[0] - self.x
            dy = target_pos[1] - self.y
            self.set_direction(dx, dy)
        
        # Give up if the target is too far
        if self._distance((self.x, self.y), target_pos) > AI_PLAYER_DETECTION_RANGE * 2:
            self.ai_state = "explore"
    
    def _retreat_behavior(self, board) -> None:
        """Retreat behavior."""
        # Move to the center of a safe area in own territory
        safe_x, safe_y = self._find_safe_territory_center(board)
        dx = safe_x - self.x
        dy = safe_y - self.y
        self.set_direction(dx, dy)
    
    def _return_home_behavior(self, board) -> None:
        """Return home behavior."""
        # Move to the nearest point in own territory
        home_x, home_y = self._find_nearest_own_territory(board)
        dx = home_x - self.x
        dy = home_y - self.y
        self.set_direction(dx, dy)
    
    def _find_nearest_enemy(self, all_players: List[Player]) -> Optional[Player]:
        """Find the nearest enemy."""
        nearest_enemy = None
        min_distance = float('inf')
        current_pos = (int(self.x), int(self.y))
        
        for player in all_players:
            if player.player_id != self.player_id and player.is_alive:
                player_pos = player.get_position()
                distance = self._distance(current_pos, player_pos)
                
                if distance < AI_PLAYER_DETECTION_RANGE and distance < min_distance:
                    min_distance = distance
                    nearest_enemy = player
        
        return nearest_enemy
    
    def _find_safe_territory_center(self, board) -> Tuple[int, int]:
        """Find the center of a safe area in own territory."""
        # Temporarily set to own territory near the center of the screen
        center_x, center_y = GAME_WIDTH // 2, GAME_HEIGHT // 2
        
        # Spiral out from the center to find own territory
        for radius in range(50, 200, 10):
            for angle in range(0, 360, 30):
                x = center_x + int(radius * math.cos(math.radians(angle)))
                y = center_y + int(radius * math.sin(math.radians(angle)))
                
                if board.is_position_valid(x, y) and board.is_in_own_territory(x, y, self.player_id):
                    return (x, y)
        
        # If not found, go near the starting position
        return self._get_starting_position()
    
    def _find_nearest_own_territory(self, board) -> Tuple[int, int]:
        """Find the nearest point in own territory."""
        current_pos = (int(self.x), int(self.y))
        min_distance = float('inf')
        nearest_pos = self._get_starting_position()
        
        # Find the nearest territory by simple grid sampling
        for x in range(0, GAME_WIDTH, 20):
            for y in range(0, GAME_HEIGHT, 20):
                if board.is_in_own_territory(x, y, self.player_id):
                    distance = self._distance(current_pos, (x, y))
                    if distance < min_distance:
                        min_distance = distance
                        nearest_pos = (x, y)
        
        return nearest_pos
    
    def _get_starting_position(self) -> Tuple[int, int]:
        """Return the starting position."""
        if self.player_id == 2:
            return (GAME_WIDTH - 22, 22)
        elif self.player_id == 3:
            return (22, GAME_HEIGHT - 22)
        elif self.player_id == 4:
            return (GAME_WIDTH - 22, GAME_HEIGHT - 22)
        else:
            return (GAME_WIDTH // 2, GAME_HEIGHT // 2)
    
    def _set_random_direction(self) -> None:
        """Set a random direction."""
        angle = random.uniform(0, 2 * math.pi)
        dx = math.cos(angle)
        dy = math.sin(angle)
        self.set_direction(dx, dy)
    
    def _change_direction_slightly(self) -> None:
        """Slightly change the current direction."""
        current_angle = math.atan2(self.dy, self.dx)
        angle_change = random.uniform(-math.pi/4, math.pi/4)  # Change by ±45 degrees
        new_angle = current_angle + angle_change
        
        dx = math.cos(new_angle)
        dy = math.sin(new_angle)
        self.set_direction(dx, dy)
    
    def _is_stuck(self) -> bool:
        """Check if the AI is stuck."""
        if len(self.last_positions) < 20:
            return False
        
        # If there is little change in the last 20 positions, consider it stuck
        recent_positions = self.last_positions[-20:]
        min_x = min(pos[0] for pos in recent_positions)
        max_x = max(pos[0] for pos in recent_positions)
        min_y = min(pos[1] for pos in recent_positions)
        max_y = max(pos[1] for pos in recent_positions)
        
        movement_range = max(max_x - min_x, max_y - min_y)
        return movement_range < 10
    
    def _handle_stuck_state(self) -> None:
        """Handle the stuck state."""
        # Change to a completely random direction
        self._set_random_direction()
        self.stuck_counter = 0
        self.last_positions.clear()
        
        # Also change state to explore
        self.ai_state = "explore"
        self.state_timer = 0
    
    def _distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """Calculate the distance between two points."""
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    def set_direction(self, dx: float, dy: float) -> None:
        """
        Set the desired direction of movement for the AI.
        Args:
            dx, dy: Desired movement vector
        """
        # Normalize the desired direction
        length = math.sqrt(dx**2 + dy**2)
        if length > 0:
            self.target_dx = (dx / length)
            self.target_dy = (dy / length)
        else:
            self.target_dx = 0
            self.target_dy = 0

    def _update_current_direction(self, dt: float) -> None:
        # Current direction vector
        current_angle = math.atan2(self.dy, self.dx)
        
        # Target direction vector
        target_angle = math.atan2(self.target_dy, self.target_dx)
        
        # Calculate the difference in angles
        angle_diff = target_angle - current_angle
        
        # Normalize angle_diff to be within [-pi, pi]
        if angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        elif angle_diff < -math.pi:
            angle_diff += 2 * math.pi
            
        # Determine the maximum angle change for this frame
        max_angle_change = math.radians(self.turn_speed) * dt
        
        # Apply the angle change gradually
        if abs(angle_diff) > max_angle_change:
            if angle_diff > 0:
                current_angle += max_angle_change
            else:
                current_angle -= max_angle_change
        else:
            current_angle = target_angle
            
        # Update dx, dy based on the new current_angle
        self.dx = math.cos(current_angle) * self.speed
        self.dy = math.sin(current_angle) * self.speed