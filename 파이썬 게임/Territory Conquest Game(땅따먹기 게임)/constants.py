"""
Constants definition file for the Territory Conquest game
Manages all game settings centrally
"""

# Screen Settings
GAME_WIDTH = 800
GAME_HEIGHT = 800
UI_WIDTH = 280
SCREEN_WIDTH = GAME_WIDTH + UI_WIDTH
SCREEN_HEIGHT = GAME_HEIGHT
FPS = 60

# Color Definitions (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 100, 100)
BLUE = (100, 100, 255)
GREEN = (100, 255, 100)
YELLOW = (255, 255, 100)
PURPLE = (255, 100, 255)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

# Player Colors
PLAYER_COLOR = BLUE
PLAYER_TRAIL_COLOR = (150, 150, 255)
PLAYER_TERRITORY_COLOR = (100, 100, 255, 100)  # Semi-transparent

# AI Colors
AI_COLORS = [RED, GREEN, YELLOW, PURPLE, ORANGE, CYAN]
AI_TRAIL_COLORS = [(255, 150, 150), (150, 255, 150), (255, 255, 150), 
                   (255, 150, 255), (255, 200, 100), (150, 255, 255)]
AI_TERRITORY_COLORS = [(255, 100, 100, 100), (100, 255, 100, 100), (255, 255, 100, 100),
                       (255, 100, 255, 100), (255, 165, 0, 100), (0, 255, 255, 100)]

# Snake Settings
SNAKE_COLOR = (100, 200, 100) # Greenish color
SNAKE_SPEED = 120 # pixels per second
SNAKE_SEGMENT_SIZE = 15
SNAKE_INITIAL_LENGTH = 5
SNAKE_UPDATE_INTERVAL = 0.1 # How often the snake moves a segment
SNAKE_SPAWN_INTERVAL = 30 # seconds
MAX_SNAKES = 5

# Game Settings
PLAYER_SPEED = 150  # pixels per second
AI_SPEED = 100  # pixels per second
TRAIL_WIDTH = 3
TERRITORY_ALPHA = 100

# Game Rules
GAME_TIME = 300  # seconds (5 minutes)
INFINITE_MODE = True  # True for infinite mode

# AI Settings
MAX_AI_COUNT = 3
AI_DIRECTION_CHANGE_CHANCE = 0.02  # 2% chance to change direction
AI_PLAYER_DETECTION_RANGE = 100
MAX_AI_CLAIM_AREA = 500 # Max pixels an AI can claim in one go
MAX_EXPLORATION_DISTANCE = 200 # Max distance AI will explore from current position
AI_MAX_MOVE_DISTANCE = 300 # Max distance AI will move from its safe point before returning home
AI_TURN_SPEED = 5.0  # Degrees per second for AI turning

# UI Settings
SCORE_FONT_SIZE = 24
UI_FONT_SIZE = 18
UI_MARGIN = 10

# Sound Settings
SOUND_ENABLED = True
SOUND_CLAIM_TERRITORY = "assets/sounds/claim.wav"
SOUND_PLAYER_DEATH = "assets/sounds/death.wav"
SOUND_LINE_DRAW = "assets/sounds/line.wav"

# Performance Optimization
MAX_TRAIL_LENGTH = 1000  # Max trail length
COLLISION_CHECK_DISTANCE = 5  # Collision check distance

# Game States
GAME_STATE_MENU = 0
GAME_STATE_PLAYING = 1
GAME_STATE_GAME_OVER = 2
GAME_STATE_PAUSED = 3