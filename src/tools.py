import pygame

# Utility helpers for image manipulation and other tools.
class Tools:
    """Helper utilities used across the game.
    """
    @staticmethod
    def split_image(spritesheet, x, y, width, height):
        """Return a sub-surface cut from a sprite sheet.

        Args:
            spritesheet (pygame.Surface): Source surface containing the sprites.
            x (int): Top-left x coordinate of the region to extract.
            y (int): Top-left y coordinate of the region to extract.
            width (int): Width of the region.
            height (int): Height of the region.

        Returns:
            pygame.Surface: A new surface representing the cut region.
        """
        # Create a rectangle region and grab a sub-surface from the spritesheet
        return spritesheet.subsurface(pygame.Rect(x, y, width, height))
