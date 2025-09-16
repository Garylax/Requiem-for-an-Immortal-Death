"""Input Manager for rebindable actions (src version).

This module provides an `InputManager` that maps abstract actions (e.g.,
"move_left", "sprint") to one or more concrete Pygame keys. It supports:
- Loading/saving JSON config from `config/controls.json`
- Querying action states: held, pressed (edge), released (edge)
- Handling pygame KEYDOWN/KEYUP events
- Rebinding actions at runtime with persistence

The config format uses Pygame key constant names (e.g., "K_LEFT", "K_q").
Internally we convert them to integer key codes for performance.
"""
from dataclasses import dataclass
from pathlib import Path
import json
import logging
import pygame
from typing import Dict, List, Set


logger = logging.getLogger(__name__)


DEFAULT_CONFIG = {
    "version": 1,
    "profiles": {
        "default": {
            "move_left": ["K_LEFT", "K_q"],
            "move_right": ["K_RIGHT", "K_d"],
            "move_up": ["K_UP", "K_z"],
            "move_down": ["K_DOWN", "K_s"],
            "sprint": ["K_LSHIFT"],
            "pause": ["K_ESCAPE"],
        }
    },
    "active_profile": "default",
}


def _project_root() -> Path:
    """Return the project root directory (one level above src)."""
    return Path(__file__).resolve().parent.parent


def _config_path() -> Path:
    return _project_root() / "config" / "controls.json"


def _key_name_to_code(name: str) -> int | None:
    """Convert a Pygame key name like "K_LEFT" to its integer key code."""
    if not name.startswith("K_"):
        return None
    code = getattr(pygame, name, None)
    return code if isinstance(code, int) else None


def _key_code_to_name(code: int) -> str:
    """Convert a Pygame key code (int) back to its name string, if possible."""
    for attr in dir(pygame):
        if attr.startswith("K_") and getattr(pygame, attr) == code:
            return attr
    return f"K_{code}"


@dataclass
class Profile:
    name: str
    action_to_keys: Dict[str, Set[int]]  # action -> set of key codes


class InputManager:
    """Rebindable input manager with action-based queries."""

    def __init__(self) -> None:
        self.profile: Profile = self._load_or_create_default()
        # Edge and hold states
        self._actions_held: Set[str] = set()
        self._actions_pressed: Set[str] = set()
        self._actions_released: Set[str] = set()
        # Reverse map: key -> actions
        self._key_to_actions: Dict[int, Set[str]] = self._build_reverse_map(self.profile)

    # ---------- Frame lifecycle ----------
    def begin_frame(self) -> None:
        self._actions_pressed.clear()
        self._actions_released.clear()

    def end_frame(self) -> None:
        pass

    # ---------- Event routing ----------
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            self._on_key_down(event.key)
        elif event.type == pygame.KEYUP:
            self._on_key_up(event.key)

    def _on_key_down(self, key: int) -> None:
        actions = self._key_to_actions.get(key)
        if not actions:
            return
        for action in actions:
            if action not in self._actions_held:
                self._actions_held.add(action)
                self._actions_pressed.add(action)

    def _on_key_up(self, key: int) -> None:
        actions = self._key_to_actions.get(key)
        if not actions:
            return
        for action in actions:
            if action in self._actions_held:
                self._actions_held.remove(action)
                self._actions_released.add(action)

    # ---------- Queries ----------
    def is_action_active(self, action: str) -> bool:
        return action in self._actions_held

    def was_action_pressed(self, action: str) -> bool:
        return action in self._actions_pressed

    def was_action_released(self, action: str) -> bool:
        return action in self._actions_released

    # ---------- Rebinding & persistence ----------
    def rebind(self, action: str, key_names: List[str]) -> None:
        key_codes: Set[int] = set()
        for name in key_names:
            code = _key_name_to_code(name)
            if code is None:
                logger.warning("Unknown key name in rebind: %s", name)
                continue
            key_codes.add(code)
        self.profile.action_to_keys[action] = key_codes
        self._key_to_actions = self._build_reverse_map(self.profile)

    def save(self) -> None:
        cfg_path = _config_path()
        cfg_path.parent.mkdir(parents=True, exist_ok=True)
        named: Dict[str, List[str]] = {}
        for action, codes in self.profile.action_to_keys.items():
            named[action] = sorted(_key_code_to_name(c) for c in codes)
        data = {
            "version": 1,
            "profiles": {self.profile.name: named},
            "active_profile": self.profile.name,
        }
        cfg_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    # ---------- Loading helpers ----------
    def _load_or_create_default(self) -> Profile:
        path = _config_path()
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(DEFAULT_CONFIG, indent=2), encoding="utf-8")
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            logger.error("Failed to read controls.json, using defaults: %s", exc)
            data = DEFAULT_CONFIG
        profile_name = data.get("active_profile", "default")
        profiles = data.get("profiles", {})
        profile_data = profiles.get(profile_name, profiles.get("default", {}))
        action_to_keys: Dict[str, Set[int]] = {}
        for action, names in profile_data.items():
            codes: Set[int] = set()
            for name in names:
                code = _key_name_to_code(name)
                if code is None:
                    logger.warning("Unknown key name in config: %s", name)
                    continue
                codes.add(code)
            action_to_keys[action] = codes
        return Profile(name=profile_name, action_to_keys=action_to_keys)

    @staticmethod
    def _build_reverse_map(profile: Profile) -> Dict[int, Set[str]]:
        reverse: Dict[int, Set[str]] = {}
        for action, codes in profile.action_to_keys.items():
            for code in codes:
                reverse.setdefault(code, set()).add(action)
        return reverse
