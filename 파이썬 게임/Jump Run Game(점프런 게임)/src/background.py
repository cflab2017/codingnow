import pygame

class Background:
    def __init__(self, screen_width, screen_height, image_path):
        self.image = pygame.image.load(image_path).convert()
        self.image = pygame.transform.scale(self.image, (screen_width, screen_height))
        self.rect = self.image.get_rect()
        self.screen_width = screen_width
        self.x = 0

    def update(self, game_speed):
        self.x -= game_speed
        if self.x <= -self.screen_width:
            self.x = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, 0))
        screen.blit(self.image, (self.x + self.screen_width, 0))
