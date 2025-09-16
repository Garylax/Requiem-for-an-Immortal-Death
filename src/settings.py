"""Centralized game settings and paths.

This module centralizes constants used across the project to avoid magic
numbers and duplicated literals. It also exposes project-relative asset paths
via pathlib for robust cross-platform file handling.
"""


from pathlib import Path

# Project root (folder that contains assets/, config/, src/)
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent

# Window and timing
SCREEN_SIZE: tuple[int, int] = (1280, 720)
WINDOW_TITLE: str = "Requiem for an Immortal Death"
FRAMERATE: int = 60

# World and camera
CAMERA_ZOOM: float = 3.0
START_MAP: str = "map0"

# Player related
PLAYER_WALK_SPEED: float = 140.0  # pixels per second
PLAYER_SPRINT_SPEED: float = 220.0  # pixels per second
PLAYER_SPRITE_SIZE: tuple[int, int] = (24, 32)

# Asset directories
ASSETS_DIR: Path = PROJECT_ROOT / "assets"
SPRITES_DIR: Path = ASSETS_DIR / "sprites"
MAPS_DIR: Path = ASSETS_DIR / "maps"
TILES_DIR: Path = ASSETS_DIR / "tiles"
