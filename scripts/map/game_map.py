import numpy as np  # type: ignore
from tcod.console import Console

from scripts.map import tile_types

class GameMap:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tile_types.floor, order="F")

        self.tiles[30:36, 15] = tile_types.wall
        self.tiles[30, 15:20] = tile_types.wall
    
    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height
    
    def render(self, console: Console) -> None:
        console.rgb[0:self.width, 0:self.height] = self.tiles["dark"]