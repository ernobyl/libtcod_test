from __future__ import annotations
from typing import Tuple, Optional, TYPE_CHECKING
import math

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
        if self.pc == False:
            # Get player and enemy positions
            dx = player.x - self.x
            dy = player.y - self.y

            # Normalize direction
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance > 0:  # Avoid division by zero
                dx = round(dx / distance)
                dy = round(dy / distance)
            self.move(dx, dy)
