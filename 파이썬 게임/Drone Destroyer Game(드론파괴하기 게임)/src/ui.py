# src/ui.py

import pygame
from src.config import (WHITE, GREEN, PURPLE, RED, BLUE, BLACK, INITIAL_XP_TO_LEVEL_UP, MAX_HP,
                        CHARGE_GAUGE_X, CHARGE_GAUGE_WIDTH,
                        XP_GAUGE_X, XP_GAUGE_WIDTH,
                        HP_GAUGE_X, HP_GAUGE_WIDTH,
                        GAUGE_Y_POS, GAUGE_HEIGHT,
                        KEY_INDICATOR_SIZE, KEY_INDICATOR_PADDING, KEY_INDICATOR_START_X, KEY_INDICATOR_START_Y)

class UI:
    def __init__(self, font):
        self.font = font

    def draw(self, screen, score, level, angle, speed, keys):
        score_text = self.font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        level_text = self.font.render(f"Level: {level}", True, WHITE)
        screen.blit(level_text, (10, 40))

        angle_text = self.font.render(f"Angle: {angle:.1f}", True, WHITE)
        screen.blit(angle_text, (10, 70))

        speed_text = self.font.render(f"Speed: {speed:.1f}", True, WHITE)
        screen.blit(speed_text, (10, 100))

        self.draw_key_indicators(screen, keys)

    def draw_key_indicators(self, screen, keys):
        key_positions = {
            'UP': (KEY_INDICATOR_START_X + KEY_INDICATOR_SIZE + KEY_INDICATOR_PADDING, KEY_INDICATOR_START_Y),
            'DOWN': (KEY_INDICATOR_START_X + KEY_INDICATOR_SIZE + KEY_INDICATOR_PADDING, KEY_INDICATOR_START_Y + KEY_INDICATOR_SIZE + KEY_INDICATOR_PADDING),
            'LEFT': (KEY_INDICATOR_START_X, KEY_INDICATOR_START_Y + KEY_INDICATOR_SIZE + KEY_INDICATOR_PADDING),
            'RIGHT': (KEY_INDICATOR_START_X + 2 * (KEY_INDICATOR_SIZE + KEY_INDICATOR_PADDING), KEY_INDICATOR_START_Y + KEY_INDICATOR_SIZE + KEY_INDICATOR_PADDING),
            'SPACE': (KEY_INDICATOR_START_X, KEY_INDICATOR_START_Y + 2 * (KEY_INDICATOR_SIZE + KEY_INDICATOR_PADDING) + 10)
        }
        
        key_sizes = {
            'SPACE': (3 * KEY_INDICATOR_SIZE + 2 * KEY_INDICATOR_PADDING, KEY_INDICATOR_SIZE)
        }

        key_map = {
            pygame.K_UP: "UP",
            pygame.K_DOWN: "DOWN",
            pygame.K_LEFT: "LEFT",
            pygame.K_RIGHT: "RIGHT",
            pygame.K_SPACE: "SPACE"
        }
        
        arrow_map = {
            "UP": "↑",
            "DOWN": "↓",
            "LEFT": "←",
            "RIGHT": "→",
            "SPACE": "SPACE"
        }

        for key_code, key_name in key_map.items():
            is_pressed = keys[key_code]
            
            pos = key_positions[key_name]
            size = key_sizes.get(key_name, (KEY_INDICATOR_SIZE, KEY_INDICATOR_SIZE))
            
            # Create a new surface for the key with per-pixel alpha
            key_surface = pygame.Surface(size, pygame.SRCALPHA)

            # 70% transparent -> 30% opaque (alpha = 255 * 0.3 = 76.5)
            alpha = 77
            
            # Set background color with alpha
            if is_pressed:
                bg_color = (0, 0, 0, alpha) # Black with alpha
            else:
                bg_color = (255, 255, 255, alpha) # White with alpha
            
            key_surface.fill(bg_color)

            # Draw border (fully opaque)
            pygame.draw.rect(key_surface, WHITE, key_surface.get_rect(), 1)

            # Set text color
            text_color = WHITE if is_pressed else BLACK

            # Draw key text
            key_text_surface = self.font.render(arrow_map[key_name], True, text_color)
            text_rect = key_text_surface.get_rect(center=key_surface.get_rect().center)
            key_surface.blit(key_text_surface, text_rect)

            # Blit the semi-transparent surface onto the main screen
            screen.blit(key_surface, pos)

    def draw_charge_gauge(self, screen, charge_level):
        # Background for the gauge
        pygame.draw.rect(screen, WHITE, (CHARGE_GAUGE_X, GAUGE_Y_POS, CHARGE_GAUGE_WIDTH, GAUGE_HEIGHT), 2) # White outline
        # Fill level
        fill_width = int(CHARGE_GAUGE_WIDTH * charge_level)
        pygame.draw.rect(screen, PURPLE, (CHARGE_GAUGE_X, GAUGE_Y_POS, fill_width, GAUGE_HEIGHT))
        # Text inside gauge
        power_text = self.font.render("POWER", True, WHITE)
        text_rect = power_text.get_rect(center=(CHARGE_GAUGE_X + CHARGE_GAUGE_WIDTH / 2, GAUGE_Y_POS + GAUGE_HEIGHT / 2))
        screen.blit(power_text, text_rect)

    def draw_xp_gauge(self, screen, xp, level):
        # Background for the XP gauge
        pygame.draw.rect(screen, WHITE, (XP_GAUGE_X, GAUGE_Y_POS, XP_GAUGE_WIDTH, GAUGE_HEIGHT), 2) # White outline
        # Fill level
        xp_progress = (xp % INITIAL_XP_TO_LEVEL_UP) / INITIAL_XP_TO_LEVEL_UP
        fill_width = int(XP_GAUGE_WIDTH * xp_progress)
        pygame.draw.rect(screen, BLUE, (XP_GAUGE_X, GAUGE_Y_POS, fill_width, GAUGE_HEIGHT))
        # Text inside gauge
        exp_label = self.font.render("EXP", True, WHITE)
        text_rect = exp_label.get_rect(center=(XP_GAUGE_X + XP_GAUGE_WIDTH / 2, GAUGE_Y_POS + GAUGE_HEIGHT / 2))
        screen.blit(exp_label, text_rect)

    def draw_hp_gauge(self, screen, hp):
        # Background for the HP gauge
        pygame.draw.rect(screen, WHITE, (HP_GAUGE_X, GAUGE_Y_POS, HP_GAUGE_WIDTH, GAUGE_HEIGHT), 2) # White outline
        # Fill level
        hp_progress = hp / MAX_HP
        fill_width = int(HP_GAUGE_WIDTH * hp_progress)
        pygame.draw.rect(screen, RED, (HP_GAUGE_X, GAUGE_Y_POS, fill_width, GAUGE_HEIGHT))
        # Text inside gauge
        hp_label = self.font.render("HP", True, WHITE)
        text_rect = hp_label.get_rect(center=(HP_GAUGE_X + HP_GAUGE_WIDTH / 2, GAUGE_Y_POS + GAUGE_HEIGHT / 2))
        screen.blit(hp_label, text_rect)
