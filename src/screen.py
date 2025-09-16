import pygame
from src.settings import SCREEN_SIZE, WINDOW_TITLE, FRAMERATE

class Screen:
    """Wrapper around the pygame display and frame timing."""

    def __init__(self) -> None:
        """Create the main window and configure frame timing."""

        self.display = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(WINDOW_TITLE)

        self.clock = pygame.time.Clock()
        self.framerate = FRAMERATE
        # Delta time (seconds) elapsed since last frame. Updated in begin_frame().
        self.dt: float = 0.0

    def begin_frame(self):
        """Start a new frame: cap FPS and clear the screen before drawing.

        Also updates the delta time (seconds) since the previous frame, which
        is used to make movement and animations framerate-independent.
        """
        self.clock.tick(self.framerate)
        # Convert milliseconds to seconds for dt
        self.dt = self.clock.get_time() / 1000.0
        self.display.fill((0, 0, 0))

    def end_frame(self):
        """Finish the frame: present the backbuffer to the screen."""
        pygame.display.update()

    def get_dt(self) -> float:
        """Return the last computed delta time in seconds.

        Returns:
            float: Elapsed time in seconds since the previous frame.
        """
        return self.dt

    def get_size(self):
        """Return the current display width and height."""
        return self.display.get_size()

    def get_display(self):
        """Return the underlying pygame Surface used for rendering."""
        return self.display
