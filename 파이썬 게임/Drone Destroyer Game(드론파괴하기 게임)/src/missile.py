# src/missile.py

import pygame
import math
from src.config import MISSILE_RADIUS, YELLOW, GRAVITY, SCREEN_WIDTH, SCREEN_HEIGHT

class Missile:
    def __init__(self, x, y, angle, speed, image):
        self.x = x
        self.y = y
        self.angle = math.radians(angle) # Convert to radians
        self.speed = speed
        self.vel_x = self.speed * math.cos(self.angle)
        self.vel_y = -self.speed * math.sin(self.angle) # Negative because y-axis is inverted in pygame
        self.fired = False
        self.image = image
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

    def fire(self):
        self.fired = True

    def update(self):
        if self.fired:
            self.x += self.vel_x
            self.vel_y += GRAVITY # Apply gravity
            self.y += self.vel_y
            self.rect.x = self.x - MISSILE_RADIUS
            self.rect.y = self.y - MISSILE_RADIUS

    def draw(self, screen):
        if self.fired:
            self.rect.center = (int(self.x), int(self.y))
            screen.blit(self.image, self.rect)

    def is_offscreen(self):
        return self.x < 0 or self.x > SCREEN_WIDTH or self.y > SCREEN_HEIGHT
