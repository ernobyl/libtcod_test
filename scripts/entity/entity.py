from __future__ import annotations
from typing import Tuple, Optional, TYPE_CHECKING
import math
import random
from scripts.entity.stats import Stats
from scripts.equipment import Equipment
from scripts import equipment
import tcod

if TYPE_CHECKING:
    from scripts.engine import Engine

class Entity:
    """
    Base object to represent player, enemies, items, etc.
    """
    def __init__(self,
                x: int,
                y: int,
                char: str,
                name: str,
                color: Tuple[int, int, int],
                pc: bool,
                stats: Stats,
                equipment: Optional[Equipment] = None,
                alive: bool = True,
                engine: Optional[Engine] = None):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.pc = pc
        self.stats = stats
        self.equipment = equipment
        self.alive = alive
        self.engine = engine

    def move(self, dx: int, dy: int) -> None:
        # Move the entity by given amount
        self.x += dx
        self.y += dy

    def equip_item(self, equipped: Equipment):
        self.equipment = equipped
        self.stats.basepow += equipped.basepow
        self.stats.addpow += equipped.addpow
        self.stats.slots += equipped.slots
        self.stats.max_charges += equipped.max_charges
        self.stats.effect_duration += equipped.effect_duration
        self.stats.max_distance += equipped.max_distance
        self.stats.aoe += equipped.aoe


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
            if player.x == next_x and player.y == next_y:  # Attack player instead of moving
                self.hostile_attack()
            elif self.engine.game_map.tiles["walkable"][next_x, next_y]:  # Move normally
                self.move(dx, dy)
            else:
                self.find_alternative_move()  # Find another way

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
            
    def hostile_attack(self):
        player = self.engine.player
        damage = int(self.stats.basepow + (self.stats.addpow / 100 * self.stats.basepow))
        player.take_damage(damage)

    def take_damage(self, amount: int):
        self.stats.hp -= amount
        print(f"{self.name} takes {amount} damage!")
        if self.stats.hp <= 0:
            self.die()

    def die(self):
        print(f"{self.name} has died!")
        self.alive = False

    def print_stats(self):
        print(", ".join(f"{key}: {value}" for key, value in vars(self.stats).items() if isinstance(value, int)))

    def ranged_attack(self, target_x: int, target_y: int):
        """Perform a ranged attack at a specific tile."""
        max_distance = self.stats.max_distance

        if self.distance_to_tile(target_x, target_y) > max_distance:
            print("Target is out of range!")
            return
        
        if not self.has_line_of_sight(target_x, target_y):
            print("No clear line of sight!")
            return
        
        print(f"{self.name} fires at ({target_x}, {target_y})!")

        # Apply damage to entities in the target area
        self.apply_aoe_damage(target_x, target_y)

    def apply_aoe_damage(self, target_x: int, target_y: int):
        """Applies damage to all enemies within the AOE radius."""
        aoe_radius = self.stats.aoe

        for entity in self.engine.entities:
            if not entity.pc and entity.alive:  # Only damage enemies
                if self.distance_to_tile(entity.x, entity.y, target_x, target_y) <= aoe_radius:
                    damage = int(self.stats.basepow + (self.stats.addpow / 100 * self.stats.basepow))
                    entity.take_damage(damage)
                    print(f"{entity.name} takes {damage} damage!")

    def distance_to_tile(self, tile_x: int, tile_y: int, origin_x=None, origin_y=None) -> float:
        """Calculate distance from a tile (or entity) to another tile."""
        if origin_x is None: origin_x = self.x
        if origin_y is None: origin_y = self.y
        dx = tile_x - origin_x
        dy = tile_y - origin_y
        return math.sqrt(dx ** 2 + dy ** 2)

    def has_line_of_sight(self, target_x: int, target_y: int) -> bool:
        """Check if there's an unobstructed line of sight (LOS) to a tile."""
        line = list(tcod.los.bresenham((self.x, self.y), (target_x, target_y)))

        # Ensure all tiles between player and target are walkable
        for x, y in line[1:-1]:  # Exclude the first (self) and last (target) positions
            if not self.engine.game_map.tiles["walkable"][x, y]:
                return False  # LOS is blocked

        return True  # LOS is clear