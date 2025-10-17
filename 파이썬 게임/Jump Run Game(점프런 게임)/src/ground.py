import pygame

class Ground:
    def __init__(self, screen_width, screen_height, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()
        # Scale the ground image to fit the screen width and a reasonable height
        self.image = pygame.transform.scale(self.image, (screen_width, 50)) # Example height, adjust as needed
        self.rect = self.image.get_rect()
        self.screen_width = screen_width
        self.x = 0
        self.y = screen_height - self.rect.height # Position at the bottom of the screen

    def update(self, game_speed):
        self.x -= game_speed
        if self.x <= -self.screen_width:
            self.x = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        screen.blit(self.image, (self.x + self.screen_width, self.y))
