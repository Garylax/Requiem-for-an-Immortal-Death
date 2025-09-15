"""
Inventory management system for the game.

This module provides an Inventory class that handles item management for game entities.
It allows adding, removing, and tracking items with their quantities, as well as
providing functionality to display the inventory in the game interface.

The inventory system is designed to be flexible and extensible, allowing for easy
integration with various game mechanics and interfaces.
"""
import pygame

class Inventory:
    """
    A class representing a game inventory system.
    
    The Inventory class manages a collection of items where each item is associated
    with a quantity. It provides methods to add, remove, and query items, as well as
    a method to render the inventory on screen.
    
    Attributes:
        items (dict): A dictionary where keys are item names and values are quantities.
    """
    def __init__(self):
        self.items = {}

    def add_item(self, item, quantity):
        if item in self.items:
            self.items[item] += quantity
        else:
            self.items[item] = quantity

    def remove_item(self, item, quantity):
        if item in self.items:
            if self.items[item] > quantity:
                self.items[item] -= quantity
            elif self.items[item] == quantity:
                del self.items[item]

    def get_inventory(self):
        return self.items

    def draw_inventory(self, screen):
        pass