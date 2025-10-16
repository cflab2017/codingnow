# src/ai_launcher.py

import pygame
import math
import random
from src.config import (
    SCREEN_WIDTH, LAUNCHER_WIDTH, LAUNCHER_HEIGHT, BARREL_LENGTH, BARREL_WIDTH,
    AI_LAUNCHER_COLOR, AI_LAUNCHER_FIRE_INTERVAL, AI_MISSILE_SPEED, GRAVITY,
    MISSILE_MIN_ANGLE, MISSILE_MAX_ANGLE
)
from src.missile import Missile

class AILauncher:
    def __init__(self, x, y, launcher_image, missile_image):
        self.x = x
        self.y = y
        self.launcher_image = launcher_image
        self.missile_image = missile_image # Store missile image
        self.rect = self.launcher_image.get_rect(bottomleft=(self.x, self.y))
        self.angle = 45 # Initial angle
        self.last_fire_time = pygame.time.get_ticks()

    def find_target(self, drones):
        # Simple AI: target the closest drone that is not too far to the left
        if not drones:
            return None
        
        # Filter drones that are within a reasonable range for the AI to target
        targetable_drones = [d for d in drones if d.x > self.x + LAUNCHER_WIDTH]
        if not targetable_drones:
            return None

        # Find the closest drone horizontally
        target_drone = min(targetable_drones, key=lambda drone: abs(drone.x - self.x))
        return target_drone

    def calculate_angle(self, target_drone, missile_speed):
        # Calculate the angle needed to hit the target, considering gravity
        # This is a simplified projectile motion calculation
        dx = target_drone.x - (self.x + LAUNCHER_WIDTH / 2)
        dy = target_drone.y - (self.y - LAUNCHER_HEIGHT / 2)

        # Quadratic formula for projectile motion to find angle
        # A * tan(theta)^2 + B * tan(theta) + C = 0
        # A = -g * dx^2 / (2 * v0^2 * cos(theta)^2) = -g * dx^2 / (2 * v0^2) * (1 + tan(theta)^2)
        # B = dx * tan(theta)
        # C = dy

        # Simplified for direct angle calculation (ignoring air time for now)
        # angle = atan2(dy, dx) - this is for direct line of sight

        # Let's use a simpler approach for now: aim directly at the drone's current position
        # and add a small lead based on drone speed and missile speed
        
        # Estimate time to target (simplified)
        time_to_target = dx / missile_speed # Assuming horizontal speed is missile_speed * cos(angle)
        
        # Predict drone's future position
        predicted_target_y = target_drone.y - target_drone.speed * time_to_target
        
        # Recalculate dy with predicted position
        dy_predicted = predicted_target_y - (self.y - LAUNCHER_HEIGHT / 2)

        # Calculate angle
        angle_rad = math.atan2(-dy_predicted, dx) # Negative dy because Pygame y-axis is inverted
        angle_deg = math.degrees(angle_rad)

        # Adjust angle to be within valid range (0-90 degrees for upward launch)
        # The AI launcher fires from right to left, so angle should be between 90 and 180
        # Or, if we consider the angle relative to the launcher's forward direction (left), then 0-90
        # Let's assume 0-90 degrees relative to horizontal, pointing left
        
        # Clamp angle to valid range
        clamped_angle = max(MISSILE_MIN_ANGLE, min(MISSILE_MAX_ANGLE, angle_deg))
        return clamped_angle

    def update(self, drones, missiles_list):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fire_time > AI_LAUNCHER_FIRE_INTERVAL:
            target_drone = self.find_target(drones)
            if target_drone:
                # Calculate angle and fire
                self.angle = self.calculate_angle(target_drone, AI_MISSILE_SPEED)
                new_missile = Missile(
                    self.x + LAUNCHER_WIDTH / 2,
                    self.y - LAUNCHER_HEIGHT / 2,
                    self.angle, # Angle for AI launcher
                    AI_MISSILE_SPEED,
                    self.missile_image # Pass the missile image
                )
                # AI missiles should fly right to left, so adjust velocity
                # The angle is relative to the horizontal, so cos(angle) is for horizontal component
                # and sin(angle) is for vertical component.
                # Since it's firing left, vel_x should be negative.
                # vel_y is negative for upward trajectory (Pygame y-axis inverted)
                new_missile.vel_x = -AI_MISSILE_SPEED * math.cos(math.radians(self.angle))
                new_missile.vel_y = -AI_MISSILE_SPEED * math.sin(math.radians(self.angle))
                new_missile.fire()
                missiles_list.append(new_missile)
                self.last_fire_time = current_time

    def draw(self, screen):
        # Draw launcher base
        screen.blit(self.launcher_image, self.rect)
