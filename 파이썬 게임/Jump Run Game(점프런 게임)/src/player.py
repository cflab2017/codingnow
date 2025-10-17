import pygame

class Player:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Load player images
        self.run_images = [
            pygame.image.load("assets/player_0.png").convert_alpha(),
            pygame.image.load("assets/player_1.png").convert_alpha(),
            pygame.image.load("assets/player_2.png").convert_alpha(),
            pygame.image.load("assets/player_3.png").convert_alpha(),
        ]
        self.slide_image = pygame.image.load("assets/player_lie.png").convert_alpha()

        # Scale images (assuming all player images are roughly the same size)
        # Adjust scale factor as needed - Increased to 0.30 for 2x size
        scale_factor = 0.30
        self.run_images = [pygame.transform.scale_by(img, scale_factor) for img in self.run_images]
        self.slide_image = pygame.transform.scale_by(self.slide_image, scale_factor)

        self.current_image = self.run_images[0]
        self.rect = self.current_image.get_rect()
        self.rect.x = 50 # Player starting X position
        self.rect.y = self.screen_height - self.rect.height # Player starting Y position (on the ground)

        self.animation_index = 0
        self.animation_speed = 0.2 # Adjust for faster/slower animation

        self.is_jumping = False
        self.is_sliding = False
        self.jump_velocity = 0
        self.gravity = 1

        self.initial_y = self.rect.y # Store initial Y for ground level

        self.x_velocity = 0
        self.speed = 5 # Player horizontal movement speed

    def update(self):
        if self.is_sliding:
            self.current_image = self.slide_image
        elif self.is_jumping:
            self.rect.y += self.jump_velocity
            self.jump_velocity += self.gravity
            if self.rect.y >= self.initial_y: # Landed
                self.rect.y = self.initial_y
                self.is_jumping = False
                self.jump_velocity = 0
        else: # Running
            self.animation_index += self.animation_speed
            if self.animation_index >= len(self.run_images):
                self.animation_index = 0
            self.current_image = self.run_images[int(self.animation_index)]

        # Apply horizontal movement
        self.rect.x += self.x_velocity
        # Keep player within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width

    def jump(self):
        if not self.is_jumping and not self.is_sliding:
            self.is_jumping = True
            self.jump_velocity = -15 # Initial jump strength

    def slide(self):
        if not self.is_jumping and not self.is_sliding:
            self.is_sliding = True
            # Adjust player position for sliding (if slide image is shorter)
            # This might need fine-tuning based on actual image sizes
            self.rect.y += (self.current_image.get_height() - self.slide_image.get_height())
            # Set a timer for sliding duration if needed, or rely on key release

    def stop_slide(self):
        if self.is_sliding:
            self.is_sliding = False
            # Restore player position after sliding
            self.rect.y = self.initial_y

    def move_left(self):
        self.x_velocity = -self.speed

    def move_right(self):
        self.x_velocity = self.speed

    def stop_move_horizontal(self):
        self.x_velocity = 0

    def draw(self, screen):
        screen.blit(self.current_image, self.rect)