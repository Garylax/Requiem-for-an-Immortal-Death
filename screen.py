import pygame

class Screen:
    """Wrapper around the pygame display and frame timing."""

    def __init__(self) -> None:
        """Create the main window and configure frame timing."""

        self.display = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Requiem for an Immortal Death')

        self.clock = pygame.time.Clock()
        self.framerate = 60

    def update(self):
        """Update the display and cap the frame rate."""
        pygame.display.update()
        self.clock.tick(self.framerate)

    def get_size(self):
        """Return the current display width and height."""
        return self.display.get_size()

    def get_display(self):
        """Return the underlying pygame Surface used for rendering."""
        return self.display