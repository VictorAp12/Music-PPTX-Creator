"""
This module contains the variables used in the application.
"""

from pathlib import Path

ROOT_DIR = Path(__file__).parent
ASSETS_DIR = ROOT_DIR / "assets"
WINDOW_ICON_PATH = ASSETS_DIR / "Music_PPTX_Creator_icon.png"

# Colors
PRIMARY_COLOR = "#1e81b0"
DARKER_PRIMARY_COLOR = "#16658a"
DARKEST_PRIMARY_COLOR = "115270"

# Sizing
BIG_FONT_SIZE = 40
MEDIUM_FONT_SIZE = 24
SMALL_FONT_SIZE = 14
TEXT_MARGIN = 15
MINIMUM_WIDTH = 600
