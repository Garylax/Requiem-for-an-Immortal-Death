class KeyListener:
    """Tracks pressed keys between pygame events.

    Provides a simple state store to query if a key is currently pressed.
    """
    def __init__(self):
        """Create an empty key list."""
        self.keys = []

    def add_key(self, key):
        """Mark a key as pressed.

        Args:
            key (int): pygame key code from a KEYDOWN event.
        """
        if key not in self.keys:
            self.keys.append(key)

    def remove_key(self, key):
        """Mark a key as released.

        Args:
            key (int): pygame key code from a KEYUP event.
        """
        if key in self.keys:
            self.keys.remove(key)

    def key_pressed(self, key):
        """Return True if the key is currently pressed.

        Args:
            key (int): pygame key code to check.

        Returns:
            bool: Whether the key is pressed.
        """
        return key in self.keys

    def clear(self):
        """Clear all tracked keys (none are pressed)."""
        self.keys.clear()
