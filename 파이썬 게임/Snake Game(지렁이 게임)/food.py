import pygame
import random
from constants import *

class Food:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, GRID_SIZE, GRID_SIZE)
        self.value = 1
        self.color = RED

    def spawn(self, snakes):
        # Randomly determine the type of food
        if random.random() < 0.2: # 20% chance for special food
            self.value = 2
            self.color = YELLOW
        else: # 80% chance for regular food
            self.value = 1
            self.color = RED
        
        # Randomize position
        self.randomize_position(snakes)

    def randomize_position(self, snakes):
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE + UI_PANEL_HEIGHT
            self.rect.topleft = (x, y)
            
            on_snake = False
            for snake in snakes:
                for segment in snake.body:
                    if self.rect.colliderect(segment):
                        on_snake = True
                        break
                if on_snake:
                    break
            
            if not on_snake:
                break

    def draw(self, surface):
        # Draw a simplified strawberry shape
        # Body (main ellipse, using self.color which is red or yellow)
        body_rect = self.rect.inflate(-2, -2)
        body_rect.y += 1
        pygame.draw.ellipse(surface, self.color, body_rect)

        # Leaves (two green triangles)
        leaf_y = body_rect.top + 4
        
        # Left leaf
        pygame.draw.polygon(surface, GREEN, [
            (self.rect.centerx, body_rect.top),
            (self.rect.left, leaf_y),
            (self.rect.centerx - 2, leaf_y)
        ])
        # Right leaf
        pygame.draw.polygon(surface, GREEN, [
            (self.rect.centerx, body_rect.top),
            (self.rect.right, leaf_y),
            (self.rect.centerx + 2, leaf_y)
        ])