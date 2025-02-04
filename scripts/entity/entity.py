from __future__ import annotations
from typing import Tuple, Optional, TYPE_CHECKING
import math
import random

if TYPE_CHECKING:
    from scripts.engine import Engine

class Entity:
    """
    Base object to represent player, enemies, items, etc.
    """
    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int], pc: bool, engine: Optional[Engine] = None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.pc = pc
        self.engine = engine

    def move(self, dx: int, dy: int) -> None:
        # Move the entity by given amount
        self.x += dx
        self.y += dy

    def hostile(self) -> None:
        player = self.engine.player
        if not self.pc:
            # Get player and enemy positions
            dx = player.x - self.x
            dy = player.y - self.y

            # Normalize direction
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance > 0:  # Avoid division by zero
                dx = round(dx / distance)
                dy = round(dy / distance)

            next_x = self.x + dx
            next_y = self.y + dy
            if self.engine.game_map.tiles["walkable"][next_x, next_y]:
                self.move(dx, dy)
            else:
                self.find_alternative_move()

    def find_alternative_move(self):
        """Finds an alternative move if the direct path is blocked."""
        possible_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # Shuffle to add some randomness (avoids predictable movement)
        random.shuffle(possible_moves)

        for dx, dy in possible_moves:
            next_x, next_y = self.x + dx, self.y + dy

            if (
                0 <= next_x < self.engine.game_map.width  # Check map bounds
                and 0 <= next_y < self.engine.game_map.height
                and self.engine.game_map.tiles["walkable"][next_x, next_y]
            ):
                self.move(dx, dy)  # Move to the first valid alternative
                return