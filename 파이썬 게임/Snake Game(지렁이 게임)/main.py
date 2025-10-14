import pygame
import sys

# Import winsound only on Windows
if sys.platform == "win32":
    import winsound

from constants import *
from snake import Snake
from food import Food
from effects import FloatingText

def play_sound(sound_type):
    if sys.platform != "win32":
        return # Do nothing on non-Windows systems
    
    if sound_type == "eat":
        winsound.Beep(1200, 50) # frequency, duration
    elif sound_type == "collide":
        winsound.Beep(500, 100)
    elif sound_type == "defeat":
        winsound.Beep(300, 200)
    elif sound_type == "win":
        winsound.Beep(1500, 150)

def draw_grid(surface):
    for y in range(UI_PANEL_HEIGHT, SCREEN_HEIGHT, GRID_SIZE):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, (50, 50, 50), rect, 1)

def draw_gauge(surface, x, y, width, height, color, current_value, max_value):
    if current_value < 0:
        current_value = 0
    if current_value > max_value:
        current_value = max_value
    
    fill_width = (current_value / max_value) * width if max_value > 0 else 0
    
    background_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, (50, 50, 50), background_rect)
    
    fill_rect = pygame.Rect(x, y, fill_width, height)
    pygame.draw.rect(surface, color, fill_rect)
    
    pygame.draw.rect(surface, WHITE, background_rect, 2)

def show_start_screen(surface):
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    title_text = font.render("2-Player Snake", True, WHITE)
    p1_text = small_font.render("Player 1: WASD", True, BLUE)
    p2_text = small_font.render("Player 2: Arrow Keys", True, ORANGE)
    start_text = small_font.render("Press any key to start", True, WHITE)

    surface.fill(BLACK)
    surface.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))
    surface.blit(p1_text, (SCREEN_WIDTH // 2 - p1_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    surface.blit(p2_text, (SCREEN_WIDTH // 2 - p2_text.get_width() // 2, SCREEN_HEIGHT // 2))
    surface.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT * 3 // 4))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_game_over_screen(surface, winner, score1, score2):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))

    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    
    if winner == "Draw":
        winner_text = font.render("Draw!", True, WHITE)
    else:
        winner_text = font.render(f"{winner} Wins!", True, WHITE)

    score1_text = small_font.render(f"Player 1 Score: {score1}", True, BLUE)
    score2_text = small_font.render(f"Player 2 Score: {score2}", True, ORANGE)
    restart_text = small_font.render("Press 'R' to Restart or 'Q' to Quit", True, WHITE)

    surface.blit(winner_text, (SCREEN_WIDTH // 2 - winner_text.get_width() // 2, SCREEN_HEIGHT // 4))
    surface.blit(score1_text, (SCREEN_WIDTH // 2 - score1_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    surface.blit(score2_text, (SCREEN_WIDTH // 2 - score2_text.get_width() // 2, SCREEN_HEIGHT // 2))
    surface.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT * 3 // 4))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    waiting = False

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("2-Player Snake Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    show_start_screen(screen)

    while True:
        snake1 = Snake(100, 100 + UI_PANEL_HEIGHT, BLUE, RIGHT)
        snake2 = Snake(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100, ORANGE, LEFT)
        snakes = [snake1, snake2]
        food = Food()
        food.spawn(snakes)
        floating_texts = []

        running = True
        winner_info = None

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        snake1.change_direction(UP)
                    elif event.key == pygame.K_s:
                        snake1.change_direction(DOWN)
                    elif event.key == pygame.K_a:
                        snake1.change_direction(LEFT)
                    elif event.key == pygame.K_d:
                        snake1.change_direction(RIGHT)
                    
                    if event.key == pygame.K_UP:
                        snake2.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        snake2.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake2.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake2.change_direction(RIGHT)

            if not running: continue

            snake1.move()
            snake2.move()

            for effect in floating_texts:
                effect.update()
            floating_texts = [e for e in floating_texts if e.lifespan > 0]

            if snake1.alive and snake1.body[0].colliderect(food.rect):
                play_sound("eat")
                floating_texts.append(FloatingText(food.rect.centerx, food.rect.centery, f"+{food.value}", BLUE))
                snake1.grow_by(food.value)
                food.spawn(snakes)
            
            if snake2.alive and snake2.body[0].colliderect(food.rect):
                play_sound("eat")
                floating_texts.append(FloatingText(food.rect.centerx, food.rect.centery, f"+{food.value}", ORANGE))
                snake2.grow_by(food.value)
                food.spawn(snakes)

            # --- Collision and Victory Condition Logic ---
            snake1.check_self_collision()
            snake2.check_self_collision()

            if not snake1.alive or not snake2.alive:
                play_sound("defeat")
                winner = "Player 2" if not snake1.alive else "Player 1"
                winner_info = (winner, snake1.score, snake2.score)
                running = False

            if running:
                s1_head, s2_head = snake1.body[0], snake2.body[0]
                if s1_head.colliderect(s2_head):
                    play_sound("collide")
                    snake1.reset(100, 100 + UI_PANEL_HEIGHT, RIGHT)
                    snake2.reset(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100, LEFT)
                else:
                    s1_hit_s2 = False
                    for index, segment in enumerate(snake2.body[1:], 1):
                        if s1_head.colliderect(segment):
                            play_sound("collide")
                            transferred_length = len(snake2.body) - index
                            snake1.grow_by(transferred_length)
                            snake2.truncate(index)
                            if len(snake2.body) <= 1:
                                snake2.alive = False
                            s1_hit_s2 = True
                            break
                    if not s1_hit_s2:
                        for index, segment in enumerate(snake1.body[1:], 1):
                            if s2_head.colliderect(segment):
                                play_sound("collide")
                                transferred_length = len(snake1.body) - index
                                snake2.grow_by(transferred_length)
                                snake1.truncate(index)
                                if len(snake1.body) <= 1:
                                    snake1.alive = False
                                break
            
            if running and (not snake1.alive or not snake2.alive):
                play_sound("defeat")
                winner = "Player 2" if not snake1.alive else "Player 1"
                winner_info = (winner, snake1.score, snake2.score)
                running = False

            WIN_LENGTH = 10
            if running and (snake1.score >= WIN_LENGTH or snake2.score >= WIN_LENGTH):
                play_sound("win")
                winner = ""
                if snake1.score >= WIN_LENGTH and snake2.score >= WIN_LENGTH:
                    winner = "Player 1" if snake1.score > snake2.score else "Player 2"
                    if snake1.score == snake2.score: winner = "Draw"
                elif snake1.score >= WIN_LENGTH:
                    winner = "Player 1"
                else:
                    winner = "Player 2"
                winner_info = (winner, snake1.score, snake2.score)
                running = False

            # --- Drawing ---
            screen.fill((30, 30, 30))
            game_area = pygame.Rect(0, UI_PANEL_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - UI_PANEL_HEIGHT)
            screen.fill(BLACK, game_area)

            draw_grid(screen)
            snake1.draw(screen)
            snake2.draw(screen)
            food.draw(screen)

            for effect in floating_texts:
                effect.draw(screen)

            score1_text = font.render(f"P1: {snake1.score}", True, WHITE)
            score2_text = font.render(f"P2: {snake2.score}", True, ORANGE)
            screen.blit(score1_text, (10, 10))
            screen.blit(score2_text, (SCREEN_WIDTH - score2_text.get_width() - 10, 10))

            GAUGE_WIDTH, GAUGE_HEIGHT = 150, 15
            draw_gauge(screen, 10, 35, GAUGE_WIDTH, GAUGE_HEIGHT, BLUE, snake1.score, WIN_LENGTH)
            draw_gauge(screen, SCREEN_WIDTH - GAUGE_WIDTH - 10, 35, GAUGE_WIDTH, GAUGE_HEIGHT, ORANGE, snake2.score, WIN_LENGTH)

            pygame.display.flip()
            clock.tick(10)
        
        if winner_info:
            show_game_over_screen(screen, winner_info[0], winner_info[1], winner_info[2])

if __name__ == '__main__':
    main()
