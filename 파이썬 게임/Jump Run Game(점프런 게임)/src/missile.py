import pygame
import math

class Missile:
    def __init__(self, x, y, target_x, target_y, speed, image_path="assets/missile.png"):
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (20,70))
        self.image = self.original_image # Current image, will be rotated
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

        # Calculate direction vector towards target
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx**2 + dy**2)
        if distance == 0: # Avoid division by zero
            self.vx = 0
            self.vy = 0
        else:
            self.vx = (dx / distance) * self.speed
            self.vy = (dy / distance) * self.speed

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        # Calculate angle based on velocity vector
        angle = math.degrees(math.atan2(-self.vy, self.vx)) # -self.vy because pygame y-axis is inverted

        # Rotate the original image
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_offscreen(self, screen_width, screen_height):
        return (self.rect.right < 0 or self.rect.left > screen_width or
                self.rect.bottom < 0 or self.rect.top > screen_height)
