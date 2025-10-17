import pygame

class Key:
    def __init__(self, rect, text, normal_color, pressed_color, text_color):
        self.rect = rect
        self.text = text
        self.normal_color = normal_color
        self.pressed_color = pressed_color
        self.text_color = text_color
        self.is_pressed = False
        
        # try:
            # Attempt to load Malgun Gothic font as requested
        self.font = pygame.font.SysFont("malgungothic", 24)
        # except FileNotFoundError:
        #     # Fallback to default font if Malgun Gothic is not found
        #     self.font = pygame.font.Font(None, 24)

    def draw(self, screen):
        color = self.pressed_color if self.is_pressed else self.normal_color
        pygame.draw.rect(screen, color, self.rect, border_radius=3)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def set_pressed(self, pressed):
        self.is_pressed = pressed

class Keyboard:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.keys = {}
        self.key_colors = {
            "normal": (100, 100, 100), # Dark gray
            "pressed": (200, 200, 200), # Light gray
            "text": (255, 255, 255) # White text
        }
        self._create_keys()

    def _create_keys(self):
        # Define key dimensions and spacing
        key_width = 40
        key_height = 30
        padding = 5

        # Use the provided arrow_map for texts
        arrow_map = {
            "UP": "↑",
            "DOWN": "↓",
            "LEFT": "←",
            "RIGHT": "→",
            "SPACE": "SPACE"
        }

        # Calculate positions for arrow keys
        # Up arrow
        up_x = self.x + key_width + padding
        up_y = self.y
        up_rect = pygame.Rect(up_x, up_y, key_width, key_height)
        self.keys[pygame.K_UP] = Key(up_rect, arrow_map["UP"], self.key_colors["normal"], self.key_colors["pressed"], self.key_colors["text"])

        # Left arrow
        left_x = self.x
        left_y = self.y + key_height + padding
        left_rect = pygame.Rect(left_x, left_y, key_width, key_height)
        self.keys[pygame.K_LEFT] = Key(left_rect, arrow_map["LEFT"], self.key_colors["normal"], self.key_colors["pressed"], self.key_colors["text"])

        # Down arrow
        down_x = self.x + key_width + padding
        down_y = self.y + key_height + padding
        down_rect = pygame.Rect(down_x, down_y, key_width, key_height)
        self.keys[pygame.K_DOWN] = Key(down_rect, arrow_map["DOWN"], self.key_colors["normal"], self.key_colors["pressed"], self.key_colors["text"])

        # Right arrow
        right_x = self.x + 2 * (key_width + padding)
        right_y = self.y + key_height + padding
        right_rect = pygame.Rect(right_x, right_y, key_width, key_height)
        self.keys[pygame.K_RIGHT] = Key(right_rect, arrow_map["RIGHT"], self.key_colors["normal"], self.key_colors["pressed"], self.key_colors["text"])

        # Spacebar
        # Calculate spacebar width to span across the arrow keys
        # It should start at the left edge of the left arrow and end at the right edge of the right arrow
        space_start_x = left_x
        space_end_x = right_x + key_width
        space_width = space_end_x - space_start_x
        space_y = self.y + 2 * (key_height + padding)
        space_rect = pygame.Rect(space_start_x, space_y, space_width, key_height)
        self.keys[pygame.K_SPACE] = Key(space_rect, arrow_map["SPACE"], self.key_colors["normal"], self.key_colors["pressed"], self.key_colors["text"])

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.keys:
                self.keys[event.key].set_pressed(True)
        elif event.type == pygame.KEYUP:
            if event.key in self.keys:
                self.keys[event.key].set_pressed(False)

    def draw(self, screen):
        for key in self.keys.values():
            key.draw(screen)
