import pygame
from tools import Tools
from keylisterner import KeyListener

class Entity(pygame.sprite.Sprite):
    """Movable player entity rendered in the map.

    Handles input-driven movement and switches sprite based on facing direction.
    """

    def __init__(self, keylistener: KeyListener):
        """Initialize the player entity.

        Args:
            keylistener (KeyListener): Shared keyboard state used to read input.
        """
        super().__init__()
        self.keylistener = keylistener
        self.spritesheet = pygame.image.load('./assets/sprites/player.png')

        self.sprite_dimentions = [24, 32]
        # Slice spritesheet into directional frames (single column, 4 rows)
        # Order in spritesheet (top to bottom) appears: down, up, left, right
        w, h = self.sprite_dimentions
        self.images = {
            'down': Tools.split_image(self.spritesheet, 0, 0 * h, w, h),
            'up': Tools.split_image(self.spritesheet, 0, 1 * h, w, h),
            'left': Tools.split_image(self.spritesheet, 0, 2 * h, w, h),
            'right': Tools.split_image(self.spritesheet, 0, 3 * h, w, h),
        }
        self.direction = 'down'
        self.image = self.images[self.direction]

        self.position = [0, 0]
        self.rect = pygame.Rect(0, 0, self.sprite_dimentions[0], self.sprite_dimentions[1])
        self.walkspeed = 2
        self.sprint = 3

    def update(self):
        """Update entity logic every frame.

        Moves the entity and syncs its rectangle to the world position.
        """
        self.move()
        self.rect.topleft = (self.position[0], self.position[1])

    def move(self):
        """Compute movement and update position and facing sprite.
        """
        dx, dy = self.check_move()
        # Optional: normalize for diagonal movement could be added here
        # Update direction and sprite if moving
        if dx != 0 or dy != 0:
            # Prefer horizontal facing when both are pressed; tweak as desired
            if dx < 0:
                self.direction = 'right'
            elif dx > 0:
                self.direction = 'left'
            elif dy < 0:
                self.direction = 'up'
            elif dy > 0:
                self.direction = 'down'
            self.image = self.images[self.direction]
        # Apply walk or sprint speed
        if self.keylistener.key_pressed(pygame.K_LSHIFT):
            self.position[0] += dx * self.sprint
            self.position[1] += dy * self.sprint
        else:
            self.position[0] += dx * self.walkspeed
            self.position[1] += dy * self.walkspeed

    def check_move(self):
        """Return desired movement vector based on current input.

        The last pressed directional key has priority over others. This also
        disables diagonal movement because only one direction is chosen at a time.

        Returns:
            tuple[int, int]: Horizontal (dx) and vertical (dy) direction, each in {-1, 0, 1}.
        """
        # Map supported keys to direction vectors
        dir_map = {
            pygame.K_RIGHT: (1, 0),
            pygame.K_d:     (1, 0),
            pygame.K_LEFT:  (-1, 0),
            pygame.K_q:     (-1, 0),
            pygame.K_DOWN:  (0, 1),
            pygame.K_s:     (0, 1),
            pygame.K_UP:    (0, -1),
            pygame.K_z:     (0, -1),
        }
        # Traverse pressed keys in insertion order and pick the last directional one
        last_dir = None
        for key in self.keylistener.keys:
            if key in dir_map:
                last_dir = key
        if last_dir is None:
            return 0, 0
        return dir_map[last_dir]