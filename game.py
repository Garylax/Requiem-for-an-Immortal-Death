import pygame
from screen import Screen
from map import Map
from entity import Entity
from keylisterner import KeyListener

"""Python Game Module.

Contains the main game controller class.
"""

class Game:
    """Main game controller.

    Sets up screen, map and player, runs the main loop, and handles input.
    """

    def __init__(self):
        """Initialize core systems and game objects."""
        self.running = True
        self.screen = Screen()
        self.keylisterner = KeyListener()
        self.map = Map(self.screen)
        self.entity = Entity(self.keylisterner)
        self.map.add_player(self.entity)
        

    def run(self):
        """Main game loop.

        Polls input, updates world, and refreshes the display each frame.
        """
        while self.running:
            self.handle_input()
            self.map.update()
            self.screen.update()
        # Clean up pygame after the loop exits
        pygame.quit()

    def handle_input(self):
        """Process window and keyboard events, updating the key listener."""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.keylisterner.add_key(event.key)
                elif event.type == pygame.KEYUP:
                    self.keylisterner.remove_key(event.key)