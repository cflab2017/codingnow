import pygame
from src.background import Background
from src.keyboard import Keyboard
from src.player import Player
from src.map_manager import MapManager
from src.explosion import Explosion # Import Explosion class

# Game settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GAME_SPEED = 3  # Initial game speed (reduced for slower gameplay)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Jump Run")
    clock = pygame.time.Clock()

    # Game state variables
    hp = 100
    game_over = False
    score = 0 # Initialize score
    player_explosions = [] # List to hold explosions for player collisions

    # Fonts for displaying text
    font = pygame.font.Font(None, 36) # For lives and game over messages

    # Load background
    background = Background(SCREEN_WIDTH, SCREEN_HEIGHT, "assets/bg.png")

    # Initialize keyboard display
    keyboard = Keyboard(10, 10) # Position the keyboard at (10, 10)

    # Initialize MapManager
    map_manager = MapManager(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_SPEED)

    # Initialize player
    player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
    # Adjust player's initial_y to be on top of the ground
    player.initial_y = map_manager.get_current_ground_y(player.rect.x) - player.rect.height
    player.rect.y = player.initial_y

    def reset_game():
        nonlocal hp, game_over, score
        hp = 100
        game_over = False
        score = 0
        player.rect.x = 50 # Reset player position
        player.rect.y = player.initial_y # Reset player position
        player.is_jumping = False
        player.is_sliding = False
        player.jump_velocity = 0
        player.x_velocity = 0
        map_manager.__init__(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_SPEED) # Reinitialize map
        player_explosions.clear() # Clear player explosions


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keyboard.handle_event(event) # Handle keyboard events

            if not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.jump()
                    elif event.key == pygame.K_DOWN:
                        player.slide()
                    elif event.key == pygame.K_LEFT:
                        player.move_left()
                    elif event.key == pygame.K_RIGHT:
                        player.move_right()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        player.stop_slide()
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        player.stop_move_horizontal()
            else: # Game Over state
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: # Press 'R' to restart
                        reset_game()


        if not game_over:
            # Update game elements
            background.update(GAME_SPEED)
            map_manager.update(player.rect) # Pass player.rect to update drones and their missiles
            player.update()

            # Update player's initial_y based on current ground
            player.initial_y = map_manager.get_current_ground_y(player.rect.x) - player.rect.height
            if not player.is_jumping and not player.is_sliding and player.rect.y > player.initial_y:
                player.rect.y = player.initial_y # Snap to ground if falling and not jumping/sliding

            # Check for collision with obstacles (drones or their missiles)
            if map_manager.check_obstacle_collision(player.rect):
                player_explosions.append(Explosion(player.rect.centerx, player.rect.centery)) # Create explosion at player position
                hp -= 10 # Decrement HP on collision
                if hp <= 0:
                    game_over = True
                else:
                    # Reset player position after losing HP (optional, can be removed for continuous damage)
                    player.rect.x = 50
                    player.rect.y = player.initial_y
                    player.is_jumping = False
                    player.is_sliding = False
                    player.jump_velocity = 0
                    player.x_velocity = 0

            # Score (placeholder for now, will be implemented properly later)
            score += 1 # Increment score for survival

            # Check for collision with heart items
            items_to_remove = []
            for item in map_manager.active_items:
                if player.rect.colliderect(item.rect):
                    hp = min(100, hp + 10) # Increase HP, max 100
                    items_to_remove.append(item)
            for item in items_to_remove:
                map_manager.active_items.remove(item)

        # Update player explosions
        explosions_to_keep = []
        for explosion in player_explosions:
            explosion.update()
            if not explosion.done:
                explosions_to_keep.append(explosion)
        player_explosions = explosions_to_keep

        # Draw game elements
        screen.fill((255, 255, 255))
        background.draw(screen)
        map_manager.draw(screen) # Draw map segments and obstacles
        player.draw(screen)
        keyboard.draw(screen)

        # Draw player explosions
        for explosion in player_explosions:
            explosion.draw(screen)

        # Draw HP Gauge
        hp_bar_width = 200
        hp_bar_height = 20
        hp_bar_x = SCREEN_WIDTH - hp_bar_width - 10
        hp_bar_y = 10

        # Background of HP bar
        pygame.draw.rect(screen, (200, 200, 200), (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height), 0)
        # Current HP
        current_hp_width = int(hp_bar_width * (hp / 100))
        pygame.draw.rect(screen, (255, 0, 0), (hp_bar_x, hp_bar_y, current_hp_width, hp_bar_height), 0)
        # HP bar border
        pygame.draw.rect(screen, (0, 0, 0), (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height), 2)

        # Display HP text inside the gauge
        hp_text = font.render(f"HP: {hp}", True, (255, 255, 255)) # White text for HP
        screen.blit(hp_text, (hp_bar_x + (hp_bar_width // 2) - (hp_text.get_width() // 2), hp_bar_y + (hp_bar_height // 2) - (hp_text.get_height() // 2)))

        # Display score
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 40))


        if game_over:
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            restart_text = font.render("Press R to Restart", True, (0, 0, 0))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))



        # Draw a white border around the screen
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5)

        pygame.display.flip()
        clock.tick(FPS) # Moved inside the loop

    pygame.quit()

if __name__ == "__main__":
    main()