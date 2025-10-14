import pygame
from constants import *

class FloatingText:
    def __init__(self, x, y, text, color):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.lifespan = 40  # How long the text stays on screen (in frames)
        self.y_speed = -1 # How fast it moves up
        self.font = pygame.font.Font(None, 24)

    def update(self):
        self.y += self.y_speed
        self.lifespan -= 1

    def draw(self, surface):
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        surface.blit(text_surface, text_rect)
