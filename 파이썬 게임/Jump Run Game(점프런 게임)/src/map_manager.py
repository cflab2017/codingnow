import pygame
import random
from src.drone import Drone # Import Drone class
from src.missile import Missile # Import Missile class
from src.explosion import Explosion # Import Explosion class
from src.item import Heart # Import Heart class

class MapManager:
    def __init__(self, screen_width, screen_height, game_speed):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.game_speed = game_speed
        self.ground_segments = [] # List to hold continuous ground segments
        self.obstacles = [] # List to hold various obstacles (drones)
        self.active_missiles = [] # New list to hold all active missiles
        self.active_explosions = [] # New list to hold all active explosions
        self.active_items = [] # New list to hold all active items (hearts)

        # Load images
        self.ground_image = pygame.image.load("assets/dirt.png").convert_alpha()

        # Scale images
        self.ground_height = 50 # Height of the continuous ground
        self.ground_image = pygame.transform.scale(self.ground_image, (self.screen_width, self.ground_height))

        self.last_ground_x = 0 # Keep track of the x-position of the last generated ground segment

        # Generate initial continuous ground
        self._generate_initial_ground()

    def _generate_initial_ground(self):
        # Create two ground segments side-by-side to cover the screen and beyond
        # This ensures continuous scrolling without gaps
        rect1 = self.ground_image.get_rect()
        rect1.x = 0
        rect1.y = self.screen_height - self.ground_height
        self.ground_segments.append({"type": "ground", "image": self.ground_image, "rect": rect1})

        rect2 = self.ground_image.get_rect()
        rect2.x = self.screen_width # Place the second segment immediately after the first
        rect2.y = self.screen_height - self.ground_height
        self.ground_segments.append({"type": "ground", "image": self.ground_image, "rect": rect2})
        
    def _add_drone_obstacle(self):
        drone = Drone(self.screen_width, self.screen_height, self.game_speed)
        self.obstacles.append({"type": "drone", "object": drone, "rect": drone.rect})


    def update(self, player_rect): # Pass player_rect to update drones
        # Move existing ground segments
        for segment in self.ground_segments:
            segment["rect"].x -= self.game_speed

        # Loop ground segments for continuous scrolling
        if self.ground_segments[0]["rect"].right <= 0:
            # If the first segment is completely off-screen, move it to the end
            self.ground_segments[0]["rect"].x = self.ground_segments[1]["rect"].right
            # Swap their order so the one that just moved is now the second one
            self.ground_segments.append(self.ground_segments.pop(0))

        # Update and move existing obstacles (drones)
        for obstacle in self.obstacles:
            if obstacle["type"] == "drone":
                new_missile = obstacle["object"].update(player_rect) # Update drone and get new missile if fired
                if new_missile:
                    self.active_missiles.append(new_missile)
                    # Removed debug print
                obstacle["rect"] = obstacle["object"].rect # Update rect from drone object

        # Remove off-screen obstacles (drones)
        self.obstacles = [obstacle for obstacle in self.obstacles if obstacle["rect"].right > 0]

        # Generate new obstacles (only drones now)
        if random.random() < 0.015: # Small chance to generate a new obstacle
            self._add_drone_obstacle()

        # Generate new heart items
        if random.random() < 0.001: # Increased chance to generate a heart for testing
            # Position heart at a height reachable by jumping
            # Assuming player.initial_y is the ground level for the player's feet
            # Player's max jump height is roughly 120 pixels above initial_y
            # So, hearts should appear between player.initial_y - 120 and player.initial_y - 50
            # We need to pass player's initial_y to MapManager or calculate it here.
            # For now, let's use a fixed range relative to screen_height that is jumpable.
            heart_y = random.randint(self.screen_height - self.ground_height - 150, self.screen_height - self.ground_height - 80) # Adjust range as needed
            self.active_items.append(Heart(self.screen_width + 20, heart_y, self.game_speed))

        # Update active missiles
        for missile in self.active_missiles:
            missile.update()
        
        # Filter out missiles that are off-screen or hit the ground, and create explosions for ground hits
        missiles_to_keep = []
        for missile in self.active_missiles:
            ground_rect = pygame.Rect(0, self.screen_height - self.ground_height, self.screen_width, self.ground_height)
            if missile.is_offscreen(self.screen_width, self.screen_height):
                pass # Missile is off-screen, just discard it
            elif missile.rect.colliderect(ground_rect):
                self.active_explosions.append(Explosion(missile.rect.centerx, missile.rect.centery))
            else:
                missiles_to_keep.append(missile)
        self.active_missiles = missiles_to_keep

        # Update active explosions
        explosions_to_keep = []
        for explosion in self.active_explosions:
            explosion.update()
            if not explosion.done:
                explosions_to_keep.append(explosion)
        self.active_explosions = explosions_to_keep

        # Update active items
        items_to_keep = []
        for item in self.active_items:
            item.update()
            if not item.is_offscreen(self.screen_width):
                items_to_keep.append(item)
        self.active_items = items_to_keep


    def draw(self, screen):
        # Draw ground segments
        for segment in self.ground_segments:
            screen.blit(segment["image"], segment["rect"])
        # Draw obstacles (drones)
        for obstacle in self.obstacles:
            if obstacle["type"] == "drone":
                obstacle["object"].draw(screen)
        # Draw active missiles
        for missile in self.active_missiles:
            missile.draw(screen)
        # Draw active explosions
        for explosion in self.active_explosions:
            explosion.draw(screen)
        # Draw active items (hearts)
        for item in self.active_items:
            item.draw(screen)

    def get_current_ground_y(self, player_x):
        # Player is always on the continuous ground
        return self.screen_height - self.ground_height
    
    def check_obstacle_collision(self, player_rect):
        # Check collision with drones
        for obstacle in self.obstacles:
            if obstacle["type"] == "drone":
                if player_rect.colliderect(obstacle["rect"]):
                    return True
        # Check collision with active missiles
        for missile in self.active_missiles:
            if player_rect.colliderect(missile.rect):
                self.active_missiles.remove(missile) # Remove missile after collision
                return True
        return False