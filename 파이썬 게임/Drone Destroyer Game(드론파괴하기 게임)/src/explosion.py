# src/explosion.py

import pygame
from src.config import EXPLOSION_MAX_RADIUS, EXPLOSION_DURATION

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_time = pygame.time.get_ticks()
        self.radius = 0
        self.alpha = 255

    def update(self):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        progress = elapsed_time / EXPLOSION_DURATION

        if progress < 1:
            self.radius = int(EXPLOSION_MAX_RADIUS * progress)
            self.alpha = int(255 * (1 - progress)) # Fade out
        else:
            self.radius = EXPLOSION_MAX_RADIUS
            self.alpha = 0

    def draw(self, screen):
        if self.alpha > 0:
            s = pygame.Surface((EXPLOSION_MAX_RADIUS * 2, EXPLOSION_MAX_RADIUS * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 165, 0, self.alpha), (EXPLOSION_MAX_RADIUS, EXPLOSION_MAX_RADIUS), self.radius)
            screen.blit(s, (self.x - EXPLOSION_MAX_RADIUS, self.y - EXPLOSION_MAX_RADIUS))

    def is_finished(self):
        return self.alpha <= 0
