"""Gameplay (Play) state (src version).

This state encapsulates the main gameplay: world update and rendering.
It owns the Map and the Player Entity and uses the action-based InputManager
(already integrated by the Entity) to move the player.
"""


import pygame

from src.screen import Screen
from src.input_manager import InputManager
from src.map import Map
from src.entity import Entity
from .base_state import BaseState


class PlayState(BaseState):
    """Active gameplay state."""

    def __init__(self, screen: Screen, input_manager: InputManager) -> None:
        super().__init__()
        self.screen = screen
        self.input = input_manager
        # World objects
        self.map = Map(self.screen)
        self.player = Entity(self.input)
        self.map.add_player(self.player)

    def handle_event(self, event: pygame.event.Event) -> None:
        # Example: detect pause action edge here later if needed
        # if event.type == pygame.KEYDOWN and self.input.was_action_pressed("pause"):
        #     self._next_state = PauseState(...)
        pass

    def update(self, dt: float) -> None:
        # Update world with dt. Map update moves sprites and centers camera.
        self.map.update(dt)

    def render(self, screen: Screen) -> None:
        # Draw world
        self.map.render(screen)
