from typing import Set, Iterable, Any, TYPE_CHECKING, Optional

from tcod.context import Context
from tcod.console import Console
import tcod

from scripts.entity.entity import Entity
from scripts.map.game_map import GameMap
from scripts.player.input_handlers import EventHandler

screen_width = 85
screen_height = 50

class Engine:
    def __init__(self, console: Console, entities: Set[Entity], event_handler: EventHandler,
                 game_map: GameMap, player: Entity, context: Optional[tcod.context.Context] = None):
        self.console = console
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.context = context  # Store the context here

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)
            for entity in self.entities:
                entity.hostile()
            
    def render(self, context: tcod.context.Context) -> None:
        self.game_map.render(self.console)

        for entity in self.entities:
            self.console.print(entity.x, entity.y, entity.char, fg=entity.color)

        if context is not None:  # Ensure context exists before presenting
            context.present(self.console)

        self.console.clear()