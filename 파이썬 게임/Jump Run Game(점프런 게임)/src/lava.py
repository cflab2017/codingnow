import pygame

class Lava:
    def __init__(self, screen_width, screen_height, image_path="assets/lava.png", height=50):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.height = height
        
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (screen_width, height))
        self.rect = self.image.get_rect()
        # Position the lava at the bottom of the screen
        self.rect.y = screen_height - height

    def draw(self, screen):
        screen.blit(self.image, self.rect)