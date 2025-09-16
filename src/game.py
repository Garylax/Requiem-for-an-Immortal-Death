import pygame
from src.screen import Screen
from src.input_manager import InputManager
from src.states.play_state import PlayState

"""Python Game Module (src version).

Contains the main game controller class using a state machine.
"""

class Game:
    """Main game controller.

    Sets up screen and input, manages the active state (e.g., Play, Menu),
    runs the main loop, and routes input/events.
    """

    def __init__(self):
        """Initialize core systems and game objects."""
        self.running = True
        self.screen = Screen()
        # Action-based input manager (rebindable)
        self.input = InputManager()
        # State machine: start in PlayState
        self.current_state = PlayState(self.screen, self.input)

    def run(self):
        """Main game loop.

        Polls input, updates world, and refreshes the display each frame.
        """
        while self.running:
            self.handle_input()  # routes to input manager and current state
            # Start frame: clear screen and cap FPS
            self.screen.begin_frame()
            # Reset edge states for input at the start of frame
            self.input.begin_frame()
            # Delta time (seconds) since last frame, for framerate-independent updates
            dt = self.screen.get_dt()
            # Update current state
            self.current_state.update(dt)
            # Allow state transition requests
            next_state = self.current_state.next_state()
            if next_state is not None:
                self.current_state.on_exit()
                self.current_state = next_state
                self.current_state.on_enter()
            # End of frame: finalize input edge states if needed
            self.input.end_frame()
            # Render current state and present the frame
            self.current_state.render(self.screen)
            self.screen.end_frame()
        # Clean up pygame after the loop exits
        pygame.quit()

    def handle_input(self):
        """Process window and keyboard events and route them appropriately."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                # Route key events to InputManager for action state updates
                self.input.handle_event(event)
            # Always give the state a chance to consume the event
            self.current_state.handle_event(event)
