"""Game entry point.

Initializes pygame and starts the main game loop.
"""
import pygame
from src.game import Game

pygame.init()

if __name__ == "__main__":
    # Create and run the game
    game = Game()
    game.run()