# drone_game.py

import pygame
import sys
import math

from src.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, DARK_SKY_BLUE, BLACK, WHITE,
    LAUNCHER_X, LAUNCHER_Y, LAUNCHER_WIDTH, LAUNCHER_HEIGHT,
    MISSILE_RADIUS, MISSILE_INITIAL_SPEED, MISSILE_MIN_SPEED, MISSILE_MAX_SPEED,
    MISSILE_INITIAL_ANGLE, MISSILE_MIN_ANGLE, MISSILE_MAX_ANGLE,
    GRAVITY, DRONE_WIDTH, DRONE_HEIGHT, DRONE_MIN_SPEED, DRONE_MAX_SPEED,
    DRONE_SPAWN_INTERVAL, EXPLOSION_MAX_RADIUS, EXPLOSION_DURATION, FONT_SIZE, CHARGE_MAX_TIME,
    BARREL_LENGTH, BARREL_WIDTH,
    DRONE_DAMAGE, XP_PER_DRONE, INITIAL_XP_TO_LEVEL_UP, MAX_HP,
    DRONE_IMAGE_PATH, MISSILE_IMAGE_PATH, LAUNCHER_IMAGE_PATH,
    DRONE_IMAGE_SIZE, MISSILE_IMAGE_SIZE, LAUNCHER_IMAGE_SIZE,
    BARREL_IMAGE_PATH, BARREL_IMAGE_SIZE,
    BACKGROUND_IMAGE_PATH
)
from src.missile import Missile
from src.drone import Drone
from src.explosion import Explosion
from src.ui import UI

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Drone Destroyer")

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Game variables
score = 0
xp = 0
level = 1
hp = MAX_HP
game_over = False
launcher_angle = MISSILE_INITIAL_ANGLE
launcher_speed = MISSILE_INITIAL_SPEED
last_player_fire_time = pygame.time.get_ticks()

# Fonts
font = pygame.font.SysFont("malgungothic", FONT_SIZE)

# Load images
drone_image = pygame.image.load(DRONE_IMAGE_PATH).convert_alpha()
drone_image = pygame.transform.scale(drone_image, DRONE_IMAGE_SIZE)

missile_image = pygame.image.load(MISSILE_IMAGE_PATH).convert_alpha()
missile_image = pygame.transform.scale(missile_image, MISSILE_IMAGE_SIZE)
missile_image = pygame.transform.rotate(missile_image, -90) # Rotate 90 degrees right (clockwise)

launcher_image = pygame.image.load(LAUNCHER_IMAGE_PATH).convert_alpha()
launcher_image = pygame.transform.scale(launcher_image, LAUNCHER_IMAGE_SIZE)

barrel_image = pygame.image.load(BARREL_IMAGE_PATH).convert_alpha()
barrel_image = pygame.transform.scale(barrel_image, BARREL_IMAGE_SIZE)

background_image = pygame.image.load(BACKGROUND_IMAGE_PATH).convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Game state
missiles = []
drones = []
explosions = []

# UI instance
game_ui = UI(font)

# Drone spawn timer
last_drone_spawn_time = pygame.time.get_ticks()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r:
                # Reset game
                score = 0
                xp = 0
                level = 1
                hp = MAX_HP
                game_over = False
                missiles = []
                drones = []
                explosions = []
                launcher_angle = MISSILE_INITIAL_ANGLE
                launcher_speed = MISSILE_INITIAL_SPEED
            if not game_over: # Only process these if game is not over
                pass # Event handling for K_SPACE, K_LEFT, K_RIGHT, K_UP, K_DOWN moved outside

    if not game_over:
        # Handle continuous speed adjustment with K_LEFT/K_RIGHT
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            launcher_speed = min(MISSILE_MAX_SPEED, launcher_speed + 1)
        if keys[pygame.K_LEFT]:
            launcher_speed = max(MISSILE_MIN_SPEED, launcher_speed - 1)
        if keys[pygame.K_UP]:
            launcher_angle = min(MISSILE_MAX_ANGLE, launcher_angle + 1)
        if keys[pygame.K_DOWN]:
            launcher_angle = max(MISSILE_MIN_ANGLE, launcher_angle - 1)

        # Continuous firing with K_SPACE
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - last_player_fire_time > 200: # Fire every 200ms
                                    # Missile originates from inside the launcher, at the base of the barrel
                                    missile_start_x = LAUNCHER_X + launcher_rect.width / 2
                                    missile_start_y = LAUNCHER_Y - LAUNCHER_HEIGHT
                
                                    new_missile = Missile(missile_start_x, missile_start_y, launcher_angle, launcher_speed, missile_image)
                                    new_missile.fire()
                                    missiles.append(new_missile)
                                    last_player_fire_time = current_time

        # Spawn drones
        current_time = pygame.time.get_ticks()
        if current_time - last_drone_spawn_time > DRONE_SPAWN_INTERVAL:
            drones.append(Drone(drone_image))
            last_drone_spawn_time = current_time

    if not game_over:
        # Spawn drones
        current_time = pygame.time.get_ticks()
        if current_time - last_drone_spawn_time > DRONE_SPAWN_INTERVAL:
            drones.append(Drone(drone_image))
            last_drone_spawn_time = current_time

        # Update game elements
        for missile in missiles:
            missile.update()
        for drone in drones:
            drone.update()
            # Check if drone passed the launcher (off-screen to the left)
            if drone.is_offscreen():
                hp -= DRONE_DAMAGE
                drones.remove(drone) # Remove drone after it deals damage
                if hp <= 0:
                    game_over = True



        for explosion in explosions:
            explosion.update()

        # Collision detection
        for missile in missiles[:]: # Iterate over a copy to allow removal
            for drone in drones[:]:
                if missile.fired and missile.rect.colliderect(drone.rect):
                    explosions.append(Explosion(drone.x + DRONE_WIDTH / 2, drone.y + DRONE_HEIGHT / 2))
                    score += 100
                    xp += XP_PER_DRONE
                    # Level up logic
                    if xp >= INITIAL_XP_TO_LEVEL_UP * level: # XP required for next level increases
                        level += 1
                        # Optionally, reset xp or carry over remainder
                        # For simplicity, let's just keep accumulating xp for now
                    missiles.remove(missile)
                    drones.remove(drone)
                    break # Missile can only hit one drone

        # Remove off-screen missiles and drones, and finished explosions
        missiles = [m for m in missiles if not m.is_offscreen()]
        drones = [d for d in drones if not d.is_offscreen()]
        explosions = [e for e in explosions if not e.is_finished()]

        # Update charge level based on launcher_speed
        charge_level = (launcher_speed - MISSILE_MIN_SPEED) / (MISSILE_MAX_SPEED - MISSILE_MIN_SPEED)

    # Drawing
    screen.blit(background_image, (0, 0))

    # Draw launcher base
    launcher_rect = launcher_image.get_rect(bottomleft=(LAUNCHER_X, LAUNCHER_Y))
    screen.blit(launcher_image, launcher_rect)

    # Draw launcher barrel
    rotated_barrel = pygame.transform.rotate(barrel_image, launcher_angle)
    # Adjust center to be at the top of the launcher
    barrel_rect = rotated_barrel.get_rect(midleft=(LAUNCHER_X + launcher_rect.width / 2, LAUNCHER_Y - LAUNCHER_HEIGHT))
    screen.blit(rotated_barrel, barrel_rect)

    for missile in missiles:
        missile.draw(screen)
    for drone in drones:
        drone.draw(screen)

    for explosion in explosions:
        explosion.draw(screen)

    # Draw UI
    game_ui.draw(screen, score, level, launcher_angle, launcher_speed, keys)
    game_ui.draw_charge_gauge(screen, charge_level)
    game_ui.draw_xp_gauge(screen, xp, level)
    game_ui.draw_hp_gauge(screen, hp)

    if game_over:
        game_over_text = font.render("GAME OVER! Press R to Restart", True, WHITE)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(game_over_text, text_rect)

    # Draw white border around the screen
    pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5) # 5 pixels thick border

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()
