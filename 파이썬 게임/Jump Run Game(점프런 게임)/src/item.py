import pygame

class Heart:
    def __init__(self, x, y, game_speed, image_path="assets/heart.png"):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (20,20)) # Scale as needed
        # self.image = pygame.transform.scale_by(self.image, 0.5) # Scale as needed
        self.rect = self.image.get_rect(center=(x, y))
        self.game_speed = game_speed

    def update(self):
        self.rect.x -= self.game_speed # Move from right to left

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_offscreen(self, screen_width):
        return self.rect.right < 0
