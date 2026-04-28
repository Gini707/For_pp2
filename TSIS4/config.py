WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 20
GRID_COLS = WINDOW_WIDTH // CELL_SIZE
GRID_ROWS = WINDOW_HEIGHT // CELL_SIZE

FPS = 60
BASE_SPEED = 8
SPEED_INCREMENT = 1
LEVEL_UP_SCORE = 5

FOOD_DISAPPEAR_TIME = 7000
POWERUP_FIELD_TIME = 8000
POWERUP_EFFECT_TIME = 5000

OBSTACLE_START_LEVEL = 3
OBSTACLES_PER_LEVEL = 5

BLACK       = (0, 0, 0)
WHITE       = (255, 255, 255)
GRAY        = (40, 40, 40)
LIGHT_GRAY  = (80, 80, 80)
GREEN       = (0, 200, 0)
DARK_GREEN  = (0, 140, 0)
RED         = (220, 50, 50)
DARK_RED    = (120, 0, 0)
YELLOW      = (230, 200, 0)
ORANGE      = (230, 130, 0)
BLUE        = (50, 100, 220)
CYAN        = (0, 200, 220)
PURPLE      = (160, 50, 220)
PINK        = (220, 80, 160)
BG_COLOR    = (10, 10, 20)
GRID_COLOR  = (20, 20, 35)
BORDER_COLOR = (60, 60, 80)

FOOD_COLORS = {
    "normal":  (0, 200, 80),
    "bonus":   (230, 180, 0),
    "poison":  (120, 0, 0),
}

POWERUP_COLORS = {
    "speed":  (0, 200, 220),
    "slow":   (160, 50, 220),
    "shield": (230, 200, 0),
}

FOOD_POINTS = {
    "normal": 1,
    "bonus":  3,
}

import json
import os

SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "snake_color": [0, 200, 0],
    "grid_overlay": True,
    "sound": True,
}


def load_settings() -> dict:
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
                for key, val in DEFAULT_SETTINGS.items():
                    data.setdefault(key, val)
                return data
        except (json.JSONDecodeError, IOError):
            pass
    return dict(DEFAULT_SETTINGS)


def save_settings(settings: dict):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)


DB_CONFIG = {
    "host":     "localhost",
    "port":     "5432",
    "dbname":   "snake_game",
    "user":     "postgres",
    "password": "1234",
}