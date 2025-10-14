"""
플레이어 클래스
플레이어 이동, 선 그리기, 영역 점령을 처리
"""

import pygame
import math
from typing import List, Tuple, Optional
from constants import *


class Player:
    """플레이어 캐릭터를 관리하는 클래스"""
    
    def __init__(self, x: int, y: int, player_id: int = 1, 
                 sound_line_draw: Optional[pygame.mixer.Sound] = None,
                 sound_player_death: Optional[pygame.mixer.Sound] = None,
                 sound_claim_territory: Optional[pygame.mixer.Sound] = None):
        """
        플레이어 초기화
        Args:
            x, y: 시작 위치
            player_id: 플레이어 식별자 (1: 플레이어, 2-6: AI)
            sound_line_draw: 선 그리기 사운드 객체
            sound_player_death: 플레이어 사망 사운드 객체
            sound_claim_territory: 영역 점령 사운드 객체
        """
        self.x = float(x)
        self.y = float(y)
        self.player_id = player_id
        
        # Sound objects
        self.sound_line_draw = sound_line_draw
        self.sound_player_death = sound_player_death
        self.sound_claim_territory = sound_claim_territory
        
        # 이동 관련
        self.dx = 0.0
        self.dy = 0.0
        self.speed = PLAYER_SPEED if player_id == 1 else AI_SPEED
        
        # 상태 관리
        self.is_alive = True
        self.is_in_territory = True  # Whether the player is in their own territory
        self.was_in_territory = True # Track previous territory state
        
        # 경로 관리 (그려지는 선)
        self.trail = []  # [(x, y), ...] 형태의 경로
        self.trail_positions = []  # 더 세밀한 위치 기록
        
        # 색상 설정
        if player_id == 1:
            self.color = PLAYER_COLOR
            self.trail_color = PLAYER_TRAIL_COLOR
        else:
            color_idx = (player_id - 2) % len(AI_COLORS)
            self.color = AI_COLORS[color_idx]
            self.trail_color = AI_TRAIL_COLORS[color_idx]
        
        # 충돌 감지용 히트박스
        self.hitbox_radius = 8

    
    def update(self, board, dt: float) -> None:
        """
        Updates the player state.
        Args:
            board: The game board object
            dt: Delta time (time between frames)
        """
        if not self.is_alive:
            return

        # Store previous integer position
        prev_x, prev_y = int(self.x), int(self.y)

        # Update position (using dt)
        self.x += self.dx * dt
        self.y += self.dy * dt

        # Check screen boundaries
        self._handle_boundary_collision()

        current_x, current_y = int(self.x), int(self.y)

        # Check for collision with enemy territory
        territory_owner = board.get_territory_at(current_x, current_y)
        if territory_owner != 0 and territory_owner != self.player_id:
            # Bounce off enemy territory
            self.x = prev_x  # Revert position
            self.y = prev_y
            self.dx *= -1  # Reverse direction
            self.dy *= -1
            # Also clear trail if any, as player is forced back
            self.trail.clear()
            self.trail_positions.clear()
            return # Skip further updates for this frame to prevent immediate re-collision

        # Check if the current position is in own territory
        self.was_in_territory = self.is_in_territory # Update the attribute
        self.is_in_territory = board.is_in_own_territory(current_x, current_y, self.player_id)

        # Just left territory, start a new trail
        if self.was_in_territory and not self.is_in_territory:
            self.trail.clear()
            self.trail_positions.clear()
            # Add the last inside point to start the trail smoothly
            self.trail.append((prev_x, prev_y))
            self.trail_positions.append((prev_x, prev_y))

        # If outside territory or moving outside
        if not self.is_in_territory:
            # Add to trail only if far enough from the last point (for a smooth trail)
            if not self.trail or self._distance((current_x, current_y), self.trail[-1]) > 1.0:
                self.trail.append((current_x, current_y))
                self.trail_positions.append((current_x, current_y))
                if self.sound_line_draw and SOUND_ENABLED:
                    self.sound_line_draw.play()
                
                # Limit max trail length
                if len(self.trail) > MAX_TRAIL_LENGTH:
                    self.trail.pop(0)
                    self.trail_positions.pop(0)

        # If returning to territory from outside
        elif not self.was_in_territory and self.is_in_territory:
            if len(self.trail) > 2:
                self.trail.append((current_x, current_y))
                if board.claim_territory(self.trail, self.player_id):
                    if self.player_id == 1:
                        print("Territory claimed!")
                    if self.sound_claim_territory and SOUND_ENABLED:
                        self.sound_claim_territory.play()
            
            # Always clear the trail when re-entering territory
            self.trail.clear()
            self.trail_positions.clear()

        # Collision check
        self._check_collisions(board)
    
    def _check_boundaries(self) -> bool:
        """화면 경계 체크"""
        if self.x < 0 or self.x >= GAME_WIDTH or self.y < 0 or self.y >= GAME_HEIGHT:
            return False
        return True
    
    def _handle_boundary_collision(self) -> None:
        """Handle boundary collision - stop at the edge."""
        # X-axis boundary
        if self.x < 0:
            self.x = 0
            self.dx = 0  # Stop X movement at the left wall
        elif self.x >= GAME_WIDTH:
            self.x = GAME_WIDTH - 1
            self.dx = 0  # Stop X movement at the right wall
        
        # Y-axis boundary
        if self.y < 0:
            self.y = 0
            self.dy = 0  # Stop Y movement at the top wall
        elif self.y >= GAME_HEIGHT:
            self.y = GAME_HEIGHT - 1
            self.dy = 0  # Stop Y movement at the bottom wall
    
    def _check_collisions(self, board) -> None:
        """Collision check."""
        if not self.is_alive:
            return
        
        current_pos = (int(self.x), int(self.y))
        
        # Collision with own trail (after a safe distance) - disabled
        # if len(self.trail) > self.safe_distance_frames:
        #     for i, trail_pos in enumerate(self.trail[:-self.safe_distance_frames]):
        #         if self._distance(current_pos, trail_pos) < self.hitbox_radius:
        #             print(f"Player {self.player_id} died: hit own trail")
        #             self.is_alive = False
        #             return
        
        # Collision with other players' trails is handled in the Game class
    
    def _distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """Calculate the distance between two points."""
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    def set_direction(self, dx: float, dy: float) -> None:
        """
        Set the direction of movement.
        Args:
            dx, dy: Movement vector
        """
        # Normalize
        length = math.sqrt(dx**2 + dy**2)
        if length > 0:
            self.dx = (dx / length) * self.speed
            self.dy = (dy / length) * self.speed
        else:
            self.dx = 0
            self.dy = 0
    
    def handle_input(self, keys) -> None:
        """
        Handle keyboard input (used by player only).
        Args:
            keys: Pygame keys state
        """
        if self.player_id != 1:  # Ignore if not the player
            return
        
        dx, dy = 0, 0
        
        # WASD or Arrow key input
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:  # Use elif
            dx = 1
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:  # Use elif
            dy = 1
        
        # Stop if no input
        if dx == 0 and dy == 0:
            self.dx = 0
            self.dy = 0
        else:
            self.set_direction(dx, dy)
    
    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the player on the screen.
        Args:
            surface: The surface to draw on
        """
        if not self.is_alive:
            return
        
        # Draw trail (line)
        if len(self.trail) > 1:
            pygame.draw.lines(surface, self.trail_color, False, self.trail, TRAIL_WIDTH)
        
        # Draw player character
        player_pos = (int(self.x), int(self.y))
        
        # Outline
        pygame.draw.circle(surface, WHITE, player_pos, self.hitbox_radius + 2)
        
        # Body
        pygame.draw.circle(surface, self.color, player_pos, self.hitbox_radius)
        
        # Direction indicator (small line)
        if abs(self.dx) > 0.1 or abs(self.dy) > 0.1:
            direction_length = 15
            end_x = player_pos[0] + (self.dx / self.speed) * direction_length
            end_y = player_pos[1] + (self.dy / self.speed) * direction_length
            pygame.draw.line(surface, WHITE, player_pos, (int(end_x), int(end_y)), 2)
    
    def reset_position(self, x: int, y: int) -> None:
        """
        Reset position.
        Args:
            x, y: New position
        """
        self.x = float(x)
        self.y = float(y)
        self.dx = 0
        self.dy = 0
        self.is_alive = True
        self.is_in_territory = True
        self.trail.clear()
        self.trail_positions.clear()

    
    def get_position(self) -> Tuple[int, int]:
        """Return current position."""
        return (int(self.x), int(self.y))
    
    def get_trail_copy(self) -> List[Tuple[int, int]]:
        """Return a copy of the current trail."""
        return self.trail.copy()
    
    def is_position_on_trail(self, pos: Tuple[int, int], tolerance: int = 5) -> bool:
        """
        Check if a specific position is on this player's trail.
        Args:
            pos: Position to check
            tolerance: Allowed tolerance
        Returns:
            Whether the position is on the trail
        """
        for trail_pos in self.trail:
            if self._distance(pos, trail_pos) <= tolerance:
                return True
        return False
    
    def get_territory_percentage(self, board) -> float:
        """Return the current territory percentage."""
        return board.get_territory_percentage(self.player_id)
    
    def kill(self) -> None:
        """Handle player death."""
        self.is_alive = False
        self.trail.clear()
        self.trail_positions.clear()
        if self.sound_player_death and SOUND_ENABLED:
            self.sound_player_death.play()
    
    def respawn(self, x: int, y: int) -> None:
        """
        Respawn the player (if needed).
        Args:
            x, y: Respawn position
        """
        self.reset_position(x, y)