# src/config.py

# Screen dimensions
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_SKY_BLUE = (100, 100, 150) # Background color
BLUE = (0, 0, 255) # Drone color
YELLOW = (255, 255, 0) # Missile color
RED = (255, 0, 0) # Explosion color
GREEN = (0, 255, 0) # Charge gauge color
PURPLE = (128, 0, 128) # XP gauge color

# Game physics
GRAVITY = 0.1 # Missile gravity effect

# Launcher settings
LAUNCHER_X = 50
LAUNCHER_Y = SCREEN_HEIGHT - 50
LAUNCHER_WIDTH = 20 * 2 # Half of current (20*2*2 / 2)
LAUNCHER_HEIGHT = 150 # Set directly to 150
BARREL_LENGTH = 40 # Set directly to 40
BARREL_WIDTH = 15 # Set directly to 15

# Missile settings
MISSILE_RADIUS = 5 * 3 # 3 times larger
MISSILE_INITIAL_SPEED = 10
MISSILE_MIN_SPEED = 5
MISSILE_MAX_SPEED = 30
MISSILE_INITIAL_ANGLE = 45 # degrees
MISSILE_MIN_ANGLE = 0
MISSILE_MAX_ANGLE = 90

# Drone settings
DRONE_WIDTH = 40 * 3 # 3 times larger
DRONE_HEIGHT = 20 * 3 # 3 times larger
DRONE_MIN_SPEED = 2
DRONE_MAX_SPEED = 7
DRONE_SPAWN_INTERVAL = 2000 # milliseconds
DRONE_DAMAGE = 10 # HP damage when a drone passes

# Explosion settings
EXPLOSION_MAX_RADIUS = 50
EXPLOSION_DURATION = 500 # milliseconds

# UI settings
FONT_SIZE = 24

# Gauge common settings
GAUGE_HEIGHT = 20
GAUGE_Y_POS = SCREEN_HEIGHT - GAUGE_HEIGHT - 10 # 10 pixels from bottom
GAUGE_PADDING = 20

# Charge system settings
CHARGE_MAX_TIME = 2000 # milliseconds, how long to hold space for max speed
CHARGE_GAUGE_WIDTH = 150
CHARGE_GAUGE_X = 10
CHARGE_GAUGE_Y = GAUGE_Y_POS

# XP and Leveling settings
INITIAL_XP_TO_LEVEL_UP = 500
XP_PER_DRONE = 50
XP_GAUGE_WIDTH = 150
XP_GAUGE_X = CHARGE_GAUGE_X + CHARGE_GAUGE_WIDTH + GAUGE_PADDING
XP_GAUGE_Y = GAUGE_Y_POS

# HP settings
MAX_HP = 100
HP_GAUGE_WIDTH = 150
HP_GAUGE_X = XP_GAUGE_X + XP_GAUGE_WIDTH + GAUGE_PADDING
HP_GAUGE_Y = GAUGE_Y_POS

# Image paths and sizes
ASSETS_DIR = "assets/"
DRONE_IMAGE_PATH = ASSETS_DIR + "drone.png"
MISSILE_IMAGE_PATH = ASSETS_DIR + "missile.png"
LAUNCHER_IMAGE_PATH = ASSETS_DIR + "launcher.png"
BARREL_IMAGE_PATH = ASSETS_DIR + "barrel.png"
BACKGROUND_IMAGE_PATH = ASSETS_DIR + "background.png"

# Desired image sizes (can be adjusted)
DRONE_IMAGE_SIZE = (DRONE_WIDTH, DRONE_HEIGHT)
MISSILE_IMAGE_SIZE = (MISSILE_RADIUS * 2, MISSILE_RADIUS * 2) # Diameter
LAUNCHER_IMAGE_SIZE = (LAUNCHER_WIDTH, LAUNCHER_HEIGHT) # Use the scaled LAUNCHER_WIDTH/HEIGHT
BARREL_IMAGE_SIZE = (BARREL_LENGTH, BARREL_WIDTH) # Use the scaled BARREL_LENGTH/WIDTH

# Key indicator settings
KEY_INDICATOR_SIZE = 40
KEY_INDICATOR_PADDING = 10
KEY_INDICATOR_START_X = SCREEN_WIDTH - (KEY_INDICATOR_SIZE * 4 + KEY_INDICATOR_PADDING * 3) - 10 # Right aligned
KEY_INDICATOR_START_Y = 225
