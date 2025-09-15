import pygame

# Utility helpers for image manipulation and other tools.
class Tools:
    """Helper utilities used across the game.
    """
    @staticmethod
    def split_image(spritesheet, x, y, width, height):
        """Return a sub-surface cut from a sprite sheet.

        Args:
            spritesheet: Source surface containing the sprites.
            x: Top-left x coordinate of the region to extract.
            y: Top-left y coordinate of the region to extract.
            width: Width of the region.
            height: Height of the region.

        Returns:
            A new surface representing the cut region.
        """
        return spritesheet.subsurface(pygame.Rect(x, y, width, height))


class KeyDebouncer:
    """
    A utility class to handle keyboard debouncing.
    Prevents multiple rapid triggers when a key is held down.
    """
    
    def __init__(self):
        """Initialize the key debouncer with an empty state."""
        self._key_states = {}
    
    def is_key_pressed(self, key):
        """
        Check if a key is pressed with debouncing.
        
        Args:
            key: The pygame key constant to check (e.g., pygame.K_UP)
            
        Returns:
            True if the key was just pressed (not held down)
        """
        keys = pygame.key.get_pressed()
        
        if keys[key]:
            if key not in self._key_states or not self._key_states[key]:
                self._key_states[key] = True
                return True
        else:
            self._key_states[key] = False
            
        return False
    
    def on_key_event(self, event, key, callback):
        """
        Handle a key event with debouncing.
        
        Args:
            event: The pygame event to check
            key: The pygame key constant to check (e.g., pygame.K_UP)
            callback: Function to call when the key is pressed (not held)
        """
        if event.type == pygame.KEYDOWN and event.key == key:
            if not self._key_states.get(key, False):
                self._key_states[key] = True
                callback()
        elif event.type == pygame.KEYUP and event.key == key:
            self._key_states[key] = False
