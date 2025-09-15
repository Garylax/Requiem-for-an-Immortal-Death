import pygame

class Screen:
    """Wrapper around the pygame display and frame timing."""

    def __init__(self) -> None:
        """Create the main window and configure frame timing."""

        self.display = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption('Requiem for an Immortal Death')

        self.clock = pygame.time.Clock()
        self.framerate = 60

    def update(self):
        """Flip buffers, cap FPS, and clear the screen for next frame."""
        pygame.display.update()
        self.clock.tick(self.framerate)
        self.display.fill((0, 0, 0))

    def get_size(self):
        """Return the current display width and height."""
        return self.display.get_size()

    def get_display(self):
        """Return the underlying pygame Surface used for rendering."""
        return self.display