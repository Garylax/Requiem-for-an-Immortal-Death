import pygame
from src.tools import Tools
from src.input_manager import InputManager
import math
from pathlib import Path
from src.settings import (
    PLAYER_WALK_SPEED,
    PLAYER_SPRINT_SPEED,
    PLAYER_SPRITE_SIZE,
    SPRITES_DIR,
)

class Entity(pygame.sprite.Sprite):
    """Movable player entity rendered in the map.

    Handles input-driven movement and switches sprite based on facing direction.
    """

    def __init__(self, input_manager: InputManager):
        """Initialize the player entity.

        Args:
            input_manager (InputManager): Action-based input manager.
        """
        super().__init__()
        self.input = input_manager
        # Load player spritesheet from centralized SPRITES_DIR
        self.spritesheet = pygame.image.load(str(SPRITES_DIR / 'player.png')).convert_alpha()

        self.sprite_dimentions = [PLAYER_SPRITE_SIZE[0], PLAYER_SPRITE_SIZE[1]]
        # Slice spritesheet into directional frames (single column, 4 rows)
        # Order in spritesheet (top to bottom) appears: down, up, left, right
        w, h = self.sprite_dimentions
        self.images = {
            'down': Tools.split_image(self.spritesheet, 0, 0 * h, w, h),
            'up': Tools.split_image(self.spritesheet, 0, 1 * h, w, h),
            'right': Tools.split_image(self.spritesheet, 0, 2 * h, w, h),
            'left': Tools.split_image(self.spritesheet, 0, 3 * h, w, h),
        }
        self.direction = 'down'
        self.image = self.images[self.direction]

        # World position in pixels (floats to allow subpixel movement)
        self.position: list[float] = [0.0, 0.0]
        self.rect = pygame.Rect(0, 0, self.sprite_dimentions[0], self.sprite_dimentions[1])
        # Movement speeds in pixels per second from settings
        self.walkspeed: float = PLAYER_WALK_SPEED
        self.sprint: float = PLAYER_SPRINT_SPEED

    def update(self, dt: float = 0.0):
        """Update entity logic every frame.

        Args:
            dt (float): Delta time in seconds since the previous frame. Used to
                make movement framerate-independent.

        Moves the entity and syncs its rectangle to the world position.
        """
        self.move(dt)
        # Ensure rect gets integer pixel coordinates
        self.rect.topleft = (int(self.position[0]), int(self.position[1]))

    def move(self, dt: float):
        """Compute movement and update position and facing sprite.

        Args:
            dt (float): Delta time in seconds used to scale movement.
        """
        dx, dy = self.check_move()
        # Normalize diagonal movement to keep constant speed
        if dx != 0 or dy != 0:
            length = math.hypot(dx, dy)
            if length != 0:
                dx /= length
                dy /= length
        # Update direction and sprite if moving
        if dx != 0 or dy != 0:
            # Face based on dominant axis (horizontal vs vertical)
            if abs(dx) >= abs(dy):
                self.direction = 'right' if dx > 0 else 'left'
            else:
                self.direction = 'down' if dy > 0 else 'up'
            self.image = self.images[self.direction]
        # Apply walk or sprint speed (px/s scaled by dt)
        # Sprint action
        speed = self.sprint if self.input.is_action_active('sprint') else self.walkspeed
        self.position[0] += dx * speed * dt
        self.position[1] += dy * speed * dt

    def check_move(self):
        """Return desired movement vector based on current input.

        Supports simultaneous key presses to allow diagonal movement. Uses
        action states from the InputManager instead of raw keys.

        Returns:
            tuple[float, float]: Raw direction vector before speed scaling.
        """
        # Horizontal via actions
        right = self.input.is_action_active('move_right')
        left = self.input.is_action_active('move_left')
        dx = (1 if right else 0) + (-1 if left else 0)

        # Vertical via actions
        down = self.input.is_action_active('move_down')
        up = self.input.is_action_active('move_up')
        dy = (1 if down else 0) + (-1 if up else 0)

        return dx, dy
