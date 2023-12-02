"""
    Side default value setting for game
"""

NAME_WINDOW: str = "Wumpus Game"  # Window game name
ICON_NAME: str = r"./Assets/Images/icon.png"  # Icon window pygame
FPS: int = 100  # FPS game
WIDTH: int = 1100  # Width main screen
HEIGHT: int = 680  # Height main screen

# DEFINE COLOR
BLACK: tuple = (0, 0, 0)
WHITE: tuple = (255, 255, 255)
BLUE: tuple = (0, 0, 255)
GREEN: tuple = (0, 255, 0)
RED: tuple = (255, 0, 0)
PURPLE: tuple = (255, 0, 255)
YELLOW: tuple = (255, 255, 0)
ORANGE: tuple = (255, 165, 0)
GREY: tuple = (200, 200, 200)
# --- End Define Color

# Board game default setting
NUMBER_CELL: int = 10  # default 10 row and 10 col
SPACING_CELL: int = 1
CELL_SIZE: int = 60
MARGIN: object = {
    "TOP": 0,
    "LEFT": 0
}

# IMAGE
CELL_IMAGE = r"Assets/Images/floor.png"
CELL_GOLD_IMAGE = r"Assets/Images/floor_gold.png"
GOLD_IMAGE = r"Assets/Images/gold.png"
PIT_IMAGE = r"Assets/Images/hole.png"
WUMPUS_IMAGE = r"Assets/Images/wumpus.png"
BREEZE_IMAGE = r"Assets/Images/breeze.png"
STENCH_IMAGE = r"Assets/Images/smell.png"

ARROW_IMAGE = [r"Assets/Images/arrow_right.png", r"Assets/Images/arrow_left.png", r"Assets/Images/arrow_up.png",
               r"Assets/Images/arrow_down.png"]
AGENT_IMAGE = [r"Assets/Images/player_facing_to_right.png", r"Assets/Images/player_facing_to_left.png",
               r"Assets/Images/player_facing_to_up.png", r"Assets/Images/player_facing_to_down.png"]
# --- End Image

# Entity
PIT = 'P'
BREEZE = 'B'
WUMPUS = 'W'
STENCH = 'S'
GOLD = 'G'
AGENT = 'A'
EMPTY = '-'
# --- end Entity

# LINK
ROOT_INPUT = r"Assets/Input/"
# -------

# --- Default point --------
POINT = {
    "PICK_GOLD": 100,
    "SHOOT": -100,
    "DYING": -10000,
    "CLIMB": 10,
    "MOVE": -10
}
# -------------------------
