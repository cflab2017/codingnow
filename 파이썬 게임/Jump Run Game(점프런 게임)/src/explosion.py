import pygame

class Explosion:
    def __init__(self, x, y):
        self.images = []
        # Load explosion animation frames (assuming you have explosion_0.png, explosion_1.png, etc.)
        # For now, let's use a placeholder or a single image if no animation frames are available.
        # If you have actual explosion images, replace this with a loop to load them.
        try:
            for i in range(4): # Assuming 4 frames for explosion animation
                img = pygame.image.load(f"assets/explosion_{i}.png").convert_alpha()
                self.images.append(pygame.transform.scale_by(img, 0.5)) # Scale as needed
        except pygame.error:
            # Fallback if explosion animation images are not found
            print("Explosion animation frames not found. Using a placeholder.")
            self.images.append(pygame.image.load("assets/missile.png").convert_alpha()) # Using missile as placeholder
            self.images = [pygame.transform.scale_by(img, 0.5) for img in self.images]


        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 0.2 # Speed of animation
        self.done = False # Flag to indicate if animation is complete

    def update(self):
        self.index += self.animation_speed
        if self.index >= len(self.images):
            self.done = True
        else:
            self.image = self.images[int(self.index)]

    def draw(self, screen):
        if not self.done:
            screen.blit(self.image, self.rect)
