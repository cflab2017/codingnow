import pygame
import math
import random
from config import *
from data_structures import *

class GameObject:
    def __init__(self, x, y, vx, vy, radius, id, image):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.id = id
        self.image = image
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rect.center = (self.x, self.y)

class Meteor(GameObject):
    def __init__(self, x, y, vx, vy, id, image, radius=METEOR_RADIUS):
        super().__init__(x, y, vx, vy, radius, id, image)

    def update(self, dt):
        super().update(dt)
        # Bounce off the sides
        if self.x - self.radius < 0 or self.x + self.radius > SCREEN_WIDTH:
            self.vx = -self.vx
            self.x = max(self.radius, min(self.x, SCREEN_WIDTH - self.radius))

class Missile(GameObject):
    def __init__(self, x, y, vx, vy, id, image, radius=MISSILE_RADIUS):
        super().__init__(x, y, vx, vy, radius, id, image)
        self.state = "flying"

    def draw(self, screen):
        # Rotate the missile to face the direction of travel
        angle = math.degrees(math.atan2(-self.vy, self.vx)) - 90
        rotated_image = pygame.transform.rotate(self.image, angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, rotated_rect)

    def update(self, dt):
        # Apply gravity
        self.vy += GRAVITY * dt
        super().update(dt)

class Game:
    def __init__(self, assets):
        self.assets = assets
        self.meteors = []
        self.missiles = []
        self.score = 0
        self.level = 1
        self.lives = PLAYER_LIVES
        self.meteors_destroyed_this_level = 0
        self.reload_cooldown = 0
        self.meteor_spawn_timer = 0
        self.game_over = False
        self.id_counter = 0
        self.time = 0.0
        self.level_up_timer = 0

    def get_observation(self):
        launcher_state = LauncherState(x=LAUNCHER_X, y=0)
        meteor_states = [MeteorState(id=m.id, x=m.x, y=m.y, vx=m.vx, vy=m.vy, radius=m.radius) for m in self.meteors]
        missile_states = [MissileState(id=m.id, state=m.state, x=m.x, y=m.y, vx=m.vx, vy=m.vy) for m in self.missiles]

        return Observation(
            time=self.time,
            launcher=launcher_state,
            meteors=meteor_states,
            missiles=missile_states,
            g=GRAVITY,
            ammo=-1, # Infinite ammo
            reload_cooldown=self.reload_cooldown
        )

    def spawn_meteor(self):
        self.id_counter += 1
        x = random.randint(0, SCREEN_WIDTH)
        y = 0
        # Increase meteor speed with level
        vx = random.randint(-50, 50) * (1 + self.level * 0.1)
        vy = random.randint(50, 150) * (1 + self.level * 0.1)
        meteor = Meteor(x, y, vx, vy, self.id_counter, self.assets["meteor"])
        self.meteors.append(meteor)

    def fire_missile(self, angle_deg, speed):
        if self.reload_cooldown <= 0:
            self.id_counter += 1
            angle_rad = math.radians(angle_deg)
            vx = speed * math.cos(angle_rad)
            vy = -speed * math.sin(angle_rad) # Negative because pygame y-axis is inverted
            missile = Missile(LAUNCHER_X, LAUNCHER_Y - 50, vx, vy, self.id_counter, self.assets["missile"])
            self.missiles.append(missile)
            self.score -= 1
            self.reload_cooldown = RELOAD_TIME

    def level_up(self):
        self.level += 1
        self.meteors_destroyed_this_level = 0
        self.level_up_timer = 2 # Show level up message for 2 seconds

    def update(self, dt):
        if self.game_over:
            return
        
        self.time += dt

        if self.reload_cooldown > 0:
            self.reload_cooldown -= dt
        
        if self.level_up_timer > 0:
            self.level_up_timer -= dt

        # Increase spawn rate with level
        self.meteor_spawn_timer -= dt
        if self.meteor_spawn_timer <= 0:
            self.spawn_meteor()
            spawn_time = random.uniform(1.0, 3.0) / (1 + self.level * 0.1)
            self.meteor_spawn_timer = max(0.5, spawn_time) # Ensure spawn time doesn't get too low

        for meteor in self.meteors[:]:
            meteor.update(dt)
            if meteor.y > SCREEN_HEIGHT:
                self.meteors.remove(meteor)
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True

        for missile in self.missiles:
            missile.update(dt)

        self.check_collisions()

    def draw(self, screen):
        for meteor in self.meteors:
            meteor.draw(screen)

        for missile in self.missiles:
            missile.draw(screen)

    def check_collisions(self):
        # Basic collision detection
        for missile in self.missiles[:]:
            for meteor in self.meteors[:]:
                if missile.rect.colliderect(meteor.rect):
                    self.missiles.remove(missile)
                    self.meteors.remove(meteor)
                    self.score += 100
                    self.meteors_destroyed_this_level += 1
                    if self.meteors_destroyed_this_level >= METEORS_PER_LEVEL:
                        self.level_up()
                    break
