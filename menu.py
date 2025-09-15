"""
Main game menu management module.

This module provides an interactive menu interface that can be controlled
using the keyboard arrow keys. The menu allows access to different game features.
"""

import pygame
import sys
from tools import KeyDebouncer

class Menu:
    """
    Class managing the main game menu.
    
    The menu displays multiple options that the user can select
    using the arrow keys. The selected option is visually highlighted.
    
    Attributes:
        screen: Pygame display surface
        width, height: Screen dimensions
        menu_items: List of menu options
        selected_item: Index of the currently selected option
        font: Font used for the menu
        colors: Dictionary of used colors
    """
    
    def __init__(self, screen):
        """
        Initialize the menu with default options.
        
        Args:
            screen: Pygame display surface
        """
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.menu_items = ["Inventory", "Quests", "Map", "Settings", "Save", "Quit"]
        self.selected_item = 0
        self.font = pygame.font.Font(None, 24)  # Taille de police réduite
        self.menu_width = 200  # Largeur fixe pour le menu
        self.menu_height = len(self.menu_items) * 30 + 20  # Hauteur basée sur le nombre d'éléments
        self.visible = False
        
        # Couleurs
        self.colors = {
            'selected': (255, 255, 255),  # Blanc pour l'élément sélectionné
            'unselected': (150, 150, 150),  # Gris pour les autres éléments
            'background': (40, 40, 40, 200),  # Fond semi-transparent
            'border': (100, 100, 100)
        }
        
        # Créer une surface pour le menu avec transparence
        self.menu_surface = pygame.Surface((self.menu_width, self.menu_height), pygame.SRCALPHA)
        self.menu_rect = pygame.Rect(self.width - self.menu_width - 10, 10, 
                                    self.menu_width, self.menu_height)
    
    def handle_events(self, game_state=None):
        """
        Handle keyboard events for menu navigation.
        
        Args:
            game_state: Game state to update when pausing
            
        Returns:
            str or None: The selected option or None if no selection
        """
        # Get all events to process
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_item = (self.selected_item - 1) % len(self.menu_items)
                    # Return None to prevent menu from closing
                    return None
                elif event.key == pygame.K_DOWN:
                    self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                    # Return None to prevent menu from closing
                    return None
                elif event.key == pygame.K_RETURN:
                    # Return the selected item when Enter is pressed
                    return self.menu_items[self.selected_item]
                elif event.key == pygame.K_ESCAPE:
                    self.toggle(game_state)
                    return None
        
        return None
    
    def toggle(self, game_state=None):
        """
        Toggle menu visibility.
        
        Args:
            game_state: Reference to game state for pausing
        """
        self.visible = not self.visible
        if game_state is not None:
            game_state['paused'] = self.visible
    
    def draw(self):
        """
        Draw the menu on screen.
        
        The menu is displayed as a semi-transparent rectangle in the top-right corner.
        The selected option is displayed in white, others in gray.
        """
        if not self.visible:
            return
            
        # Clear the menu surface with transparency
        self.menu_surface.fill((0, 0, 0, 0))
        
        # Draw menu background
        pygame.draw.rect(self.menu_surface, self.colors['background'], 
                        (0, 0, self.menu_width, self.menu_height), 
                        border_radius=5)
        pygame.draw.rect(self.menu_surface, self.colors['border'], 
                        (0, 0, self.menu_width, self.menu_height), 
                        1, border_radius=5)  # Border
        
        # Draw menu items
        for i, item in enumerate(self.menu_items):
            color = self.colors['selected'] if i == self.selected_item else self.colors['unselected']
            text = self.font.render(item, True, color)
            text_rect = text.get_rect(
                x=10,
                y=10 + i * 30,  # 30px de hauteur par élément
                width=self.menu_width - 20,
                height=25
            )
            self.menu_surface.blit(text, text_rect)
            
            # Draw highlight for selected item
            if i == self.selected_item:
                highlight = pygame.Surface((self.menu_width - 4, 25), pygame.SRCALPHA)
                highlight.fill((255, 255, 255, 25))  # Légère surbrillance
                self.menu_surface.blit(highlight, (2, 10 + i * 30))
        
        # Draw the menu onto the screen
        self.screen.blit(self.menu_surface, (self.menu_rect.x, self.menu_rect.y))


def main():
    """Menu demonstration function."""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game Menu")
    
    # Simulated game state for demonstration
    game_state = {
        'paused': False,
        'player_pos': [400, 300],
        'player_speed': 5
    }
    
    menu = Menu(screen)
    
    clock = pygame.time.Clock()
    
    running = True
    while running:
        # Handle events with game state passing
        selected_option = menu.handle_events(game_state)
        
        if selected_option:
            print(f"Selected option: {selected_option}")
            if selected_option == "Save":
                print("Game saved!")
            elif selected_option == "Quit":
                running = False
        
        # Demonstration background
        screen.fill((30, 30, 50))
        
        # Game simulation in the background
        screen.fill((30, 30, 50))  # Clear the screen
        
        # Display status message
        font = pygame.font.Font(None, 36)
        if menu.visible:
            text = font.render("GAME PAUSED - Press ESC to resume", True, (255, 255, 255))
        else:
            text = font.render("Press ESC to open the menu", True, (255, 255, 255))
            
            # Game simulation (only when not paused)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                game_state['player_pos'][0] -= game_state['player_speed']
            if keys[pygame.K_RIGHT]:
                game_state['player_pos'][0] += game_state['player_speed']
            if keys[pygame.K_UP]:
                game_state['player_pos'][1] -= game_state['player_speed']
            if keys[pygame.K_DOWN]:
                game_state['player_pos'][1] += game_state['player_speed']
                
            # Draw a simple player (a square)
            pygame.draw.rect(screen, (0, 255, 0), (*game_state['player_pos'], 30, 30))
        
        text_rect = text.get_rect(center=(400, 50))
        screen.blit(text, text_rect)
        
        menu.draw()
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
