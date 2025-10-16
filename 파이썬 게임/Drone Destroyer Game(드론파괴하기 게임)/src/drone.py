# src/drone.py

import pygame
import random
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, DRONE_WIDTH, DRONE_HEIGHT, DRONE_MIN_SPEED, DRONE_MAX_SPEED, BLUE

class Drone:
    def __init__(self, image):
        self.x = SCREEN_WIDTH
        self.y = random.randint(50, SCREEN_HEIGHT - 150) # Avoid launcher area
        self.speed = random.uniform(DRONE_MIN_SPEED, DRONE_MAX_SPEED)
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        self.x -= self.speed
        self.rect.x = self.x

    def draw(self, screen):
        self.rect.topleft = (int(self.x), int(self.y))
        screen.blit(self.image, self.rect)

    def is_offscreen(self):
        return self.x < -DRONE_WIDTH
