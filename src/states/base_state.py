"""Base class for game states (src version).

States encapsulate logic and rendering for different screens (e.g.,
menu, gameplay, pause). Each state handles events, updates with dt,
and renders to the provided Screen wrapper.
"""


import pygame
from abc import ABC, abstractmethod
from typing import Optional


class BaseState(ABC):
    """Abstract base class for a game state."""

    def __init__(self) -> None:
        self._next_state: Optional[BaseState] = None

    def next_state(self) -> Optional["BaseState"]:
        """Return a state to switch to at end of frame, if any."""
        return self._next_state

    def on_enter(self) -> None:
        """Called when the state becomes active."""
        pass

    def on_exit(self) -> None:
        """Called before the state is deactivated."""
        pass

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """Process a single pygame event (keyboard, window, etc.)."""
        raise NotImplementedError

    @abstractmethod
    def update(self, dt: float) -> None:
        """Advance the simulation by dt seconds (framerate-independent)."""
        raise NotImplementedError

    @abstractmethod
    def render(self, screen) -> None:
        """Draw the current state to the screen wrapper."""
        raise NotImplementedError
