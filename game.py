import pygame
from screen import Screen
from map import Map
from entity import Entity
from keylisterner import KeyListener
from menu import Menu

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
        
        # Initialize game state
        self.game_state = {
            'paused': False,
            'player': self.entity,
            'map': self.map
        }
        
        # Initialize menu with the display surface
        self.menu = Menu(self.screen.display)  # Pass the Pygame surface
        

    def run(self):
        """Main game loop.

        Polls input, updates world, and refreshes the display each frame.
        """
        clock = pygame.time.Clock()
        
        while self.running:
            # Handle input and menu
            selected_option = self.handle_input()
            
            # Process menu selection if any
            if selected_option:
                self.handle_menu_selection(selected_option)
            
            # Clear the screen
            self.screen.display.fill((0, 0, 0))
            
            # Update and draw the game world
            if not self.game_state['paused']:
                self.map.update()
            else:
                # If game is paused, we still need to draw the map
                self.map.group.draw(self.screen.display)
            
            # Draw menu if visible (on top of everything else)
            if self.menu.visible:
                self.menu.draw()
            
            # Update the display
            pygame.display.flip()
            
            # Cap the frame rate
            clock.tick(60)
            
        # Clean up pygame after the loop exits
        pygame.quit()
    
    def handle_menu_selection(self, option):
        """Handle menu selection actions."""
        if option == "Save":
            print("Game saved!")
            # Add save game logic here
        elif option == "Quit":
            self.running = False

    def handle_input(self):
        """
        Process window and keyboard events, updating the key listener.
        
        Returns:
            str or None: The selected menu option, if any
        """
        # Handle all events
        events = list(pygame.event.get())
        
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                return None
                
            # Handle ESC key to toggle menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.menu.toggle(self.game_state)
                return None
        
        # If menu is visible, let it handle navigation
        if self.menu.visible:
            for event in events:
                # Let menu handle its own events
                if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                    return self.menu.handle_events(self.game_state)
            return None
            
        # Handle game input (only when menu is not visible)
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.keylisterner.add_key(event.key)
            elif event.type == pygame.KEYUP:
                self.keylisterner.remove_key(event.key)
                
        return None