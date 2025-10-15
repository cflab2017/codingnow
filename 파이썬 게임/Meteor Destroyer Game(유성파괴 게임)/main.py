import pygame
import sys
from config import *
from game import Game

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Meteor Destroyer")

    # Load assets
    try:
        assets = {
            "background": pygame.transform.scale(pygame.image.load("assets/background.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
            "launcher": pygame.transform.scale(pygame.image.load("assets/luncher.png"), (LAUNCHER_WIDTH, LAUNCHER_HEIGHT)),
            "meteor": pygame.transform.scale(pygame.image.load("assets/meteorite.png"), (METEOR_WIDTH, METEOR_HEIGHT)),
            "missile": pygame.transform.scale(pygame.image.load("assets/missile.png"), (MISSILE_WIDTH, MISSILE_HEIGHT)),
        }
    except pygame.error as e:
        print(f"Error loading assets: {e}")
        pygame.quit()
        sys.exit()

    clock = pygame.time.Clock()
    game = Game(assets)

    font = pygame.font.Font(None, 36)
    game_over_font = pygame.font.Font(None, 72)

    launch_angle = 90 # Initial angle (pointing up)

    while True:
        dt = clock.tick(60) / 1000.0 # Delta time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if game.game_over:
                    game = Game(assets) # Restart the game
                if event.key == pygame.K_SPACE:
                    game.fire_missile(launch_angle, MISSILE_SPEED_MAX)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            launch_angle += 2
        if keys[pygame.K_RIGHT]:
            launch_angle -= 2

        # Clamp the angle
        launch_angle = max(5, min(175, launch_angle))

        if not game.game_over:
            game.update(dt)

        screen.blit(assets["background"], (0, 0))

        if game.game_over:
            game_over_text = game_over_font.render("GAME OVER", True, WHITE)
            restart_text = font.render("Press any key to restart", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        else:
            # Draw launcher
            rotated_launcher = pygame.transform.rotate(assets["launcher"], launch_angle - 90)
            launcher_rect = rotated_launcher.get_rect(center=(LAUNCHER_X, SCREEN_HEIGHT - assets["launcher"].get_height() // 2))
            screen.blit(rotated_launcher, launcher_rect)

            # Draw reload timer on launcher
            if game.reload_cooldown > 0:
                reload_percentage = game.reload_cooldown / RELOAD_TIME
                gauge_width = assets["launcher"].get_width()
                gauge_height = 10
                gauge_x = launcher_rect.centerx - gauge_width // 2
                gauge_y = launcher_rect.top - gauge_height - 5
                pygame.draw.rect(screen, WHITE, (gauge_x, gauge_y, gauge_width, gauge_height), 1)
                pygame.draw.rect(screen, GREEN, (gauge_x, gauge_y, gauge_width * reload_percentage, gauge_height))

            game.draw(screen)

            # Draw UI
            score_text = font.render(f"Score: {game.score}", True, WHITE)
            level_text = font.render(f"Level: {game.level}", True, WHITE)
            screen.blit(score_text, (10, 10))
            screen.blit(level_text, (10, 50))

            # Draw HP Gauge
            hp_gauge_width = 200
            hp_gauge_height = 20
            hp_percentage = game.lives / PLAYER_LIVES
            pygame.draw.rect(screen, RED, (10, 90, hp_gauge_width * hp_percentage, hp_gauge_height))
            pygame.draw.rect(screen, WHITE, (10, 90, hp_gauge_width, hp_gauge_height), 2)
            hp_text = font.render("HP", True, WHITE)
            screen.blit(hp_text, (10 + (hp_gauge_width - hp_text.get_width()) // 2, 90 + (hp_gauge_height - hp_text.get_height()) // 2))

            # Draw XP Gauge
            xp_gauge_width = 200
            xp_gauge_height = 20
            xp_percentage = game.meteors_destroyed_this_level / METEORS_PER_LEVEL
            pygame.draw.rect(screen, BLUE, (10, 120, xp_gauge_width * xp_percentage, xp_gauge_height))
            pygame.draw.rect(screen, WHITE, (10, 120, xp_gauge_width, xp_gauge_height), 2)
            xp_text = font.render("EXP", True, WHITE)
            screen.blit(xp_text, (10 + (xp_gauge_width - xp_text.get_width()) // 2, 120 + (xp_gauge_height - xp_text.get_height()) // 2))

            if game.level_up_timer > 0:
                level_up_text = game_over_font.render("LEVEL UP!", True, WHITE)
                screen.blit(level_up_text, (SCREEN_WIDTH // 2 - level_up_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        
        pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5)

        pygame.display.flip()

if __name__ == '__main__':
    main()
