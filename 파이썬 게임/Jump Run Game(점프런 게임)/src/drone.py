import pygame
import random
from src.missile import Missile # Import Missile class

class Drone:
    def __init__(self, screen_width, screen_height, game_speed, image_path="assets/drone.png"):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.game_speed = game_speed
        
        self.image = pygame.image.load(image_path).convert_alpha()
        # Scale drone image (adjust scale factor as needed)
        scale_factor = 0.1 # Example scale factor
        self.image = pygame.transform.scale_by(self.image, scale_factor)
        self.rect = self.image.get_rect()

        # Initial position (off-screen to the right, random height)
        self.rect.x = screen_width + 50 # Start a bit off-screen
        self.rect.y = random.randint(screen_height // 4, screen_height // 3) # Random height in upper quarter to third

        self.fire_cooldown = 1000 # Reverted cooldown to original value
        self.last_fire_time = pygame.time.get_ticks() # Last time a missile was fired

    def update(self, player_rect):
        self.rect.x -= self.game_speed * 1.5 # Drone moves faster than background

        # Fire missile if cooldown is over and drone is in the firing zone
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fire_time > self.fire_cooldown: # Convert frames to milliseconds
            if self.rect.x > self.screen_width * 0.5: # Adjust firing range
                self.last_fire_time = current_time
                new_missile = self.fire(player_rect) # Get the new missile
                return new_missile # Return the new missile
        return None # No missile fired

    def fire(self, player_rect):
        missile_speed = 7.2 # Decreased by 10%
        new_missile = Missile(self.rect.centerx, self.rect.centery, player_rect.centerx, player_rect.centery, missile_speed)
        return new_missile # Return the missile

    def draw(self, screen):
        screen.blit(self.image, self.rect)
