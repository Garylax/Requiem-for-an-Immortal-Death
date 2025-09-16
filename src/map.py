import pygame
from pytmx import load_pygame
import pyscroll
from pathlib import Path

from src.screen import Screen
from src.settings import MAPS_DIR, START_MAP, CAMERA_ZOOM

class Map:
    """Loads Tiled TMX maps and renders them with pyscroll.

    Manages the scrolling group that contains the player and other sprites.
    """
    def __init__(self, screen :Screen) -> None:
        """Initialize the map system with a target screen.

        Args:
            screen (Screen): The screen wrapper used for size and rendering.
        """
        self.screen = screen
        self.tmx_data = None
        self.map_layer = None
        self.group = None

        self.switch_map(START_MAP)
        self.player = None

    def switch_map(self, map :str):
        """Load a TMX map and set up the scrolling renderer.

        Args:
            map (str): Map basename without extension (e.g. "map0").
        """
        tmx_path = MAPS_DIR / f'{map}.tmx'
        self.tmx_data = load_pygame(str(tmx_path))
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=7)
        self.map_layer.zoom = CAMERA_ZOOM

    def add_player(self, player):
        """Add the player sprite to the scrolling group.

        Args:
            player (pygame.sprite.Sprite): The player entity to render.
        """
        self.group.add(player)
        self.player = player

    def update(self, dt: float):
        """Update sprites and camera.

        Args:
            dt (float): Delta time in seconds since the last frame, used for
                framerate-independent sprite updates.
        """
        # Propagate dt to sprites; pygame sprites can accept parameters in update()
        self.group.update(dt)
        self.group.center(self.player.rect.center)

    def render(self, screen: Screen) -> None:
        """Render the current map and sprites to the screen display."""
        self.group.draw(self.screen.get_display())
