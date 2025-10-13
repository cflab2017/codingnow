import pygame
from constants import *

class Snake:
    def __init__(self, x, y, color, direction=RIGHT):
        self.direction = direction
        dx, dy = -self.direction[0], -self.direction[1]
        self.body = [pygame.Rect(x + i * dx * GRID_SIZE, y + i * dy * GRID_SIZE, GRID_SIZE, GRID_SIZE) for i in range(3)]
        self.color = color
        self.alive = True

    @property
    def score(self):
        # Score is always equal to the snake's length
        return len(self.body)

    def move(self):
        if not self.alive:
            return

        head = self.body[0]
        new_x = head.x + self.direction[0] * GRID_SIZE
        new_y = head.y + self.direction[1] * GRID_SIZE

        # Wall wrapping
        if new_x >= SCREEN_WIDTH:
            new_x = 0
        elif new_x < 0:
            new_x = SCREEN_WIDTH - GRID_SIZE
        if new_y >= SCREEN_HEIGHT:
            new_y = UI_PANEL_HEIGHT
        elif new_y < UI_PANEL_HEIGHT:
            new_y = SCREEN_HEIGHT - GRID_SIZE

        new_head = pygame.Rect(new_x, new_y, GRID_SIZE, GRID_SIZE)
        
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        # Grows by 1 segment (for eating food)
        tail = self.body[-1]
        self.body.append(tail.copy())

    def grow_by(self, num_segments):
        # Grows by a specific number of segments
        if num_segments <= 0:
            return
        for _ in range(num_segments):
            tail = self.body[-1]
            self.body.append(tail.copy())

    def truncate(self, index):
        # Shortens the snake to the given index
        self.body = self.body[:index]

    def reset(self, x, y, direction):
        self.direction = direction
        dx, dy = -self.direction[0], -self.direction[1]
        self.body = [pygame.Rect(x + i * dx * GRID_SIZE, y + i * dy * GRID_SIZE, GRID_SIZE, GRID_SIZE) for i in range(3)]
        self.alive = True

    def check_self_collision(self):
        head = self.body[0]
        for segment in self.body[1:]:
            if head.colliderect(segment):
                self.alive = False

    def change_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def draw(self, surface):
        # Draw the head with eyes
        head = self.body[0]
        pygame.draw.rect(surface, self.color, head)
        pygame.draw.rect(surface, BLACK, head, 1)

        eye_radius = 3
        if self.direction == UP:
            eye1 = (head.centerx - 5, head.centery - 5)
            eye2 = (head.centerx + 5, head.centery - 5)
        elif self.direction == DOWN:
            eye1 = (head.centerx - 5, head.centery + 5)
            eye2 = (head.centerx + 5, head.centery + 5)
        elif self.direction == LEFT:
            eye1 = (head.centerx - 5, head.centery - 5)
            eye2 = (head.centerx - 5, head.centery + 5)
        else: # RIGHT
            eye1 = (head.centerx + 5, head.centery - 5)
            eye2 = (head.centerx + 5, head.centery + 5)
        
        pygame.draw.circle(surface, BLACK, eye1, eye_radius)
        pygame.draw.circle(surface, BLACK, eye2, eye_radius)

        # Draw the body
        for segment in self.body[1:]:
            pygame.draw.rect(surface, self.color, segment)
            pygame.draw.rect(surface, BLACK, segment, 1)