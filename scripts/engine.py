from typing import Set, Iterable, Any, TYPE_CHECKING, Optional

from tcod.context import Context
from tcod.console import Console
import tcod

from scripts.entity.entity import Entity
from scripts.map.game_map import GameMap
from scripts.player.input_handlers import EventHandler
from scripts.entity import stats
import random

screen_width = 85
screen_height = 50

class Engine:
    def __init__(self, console: Console, entities: list[Entity], event_handler: EventHandler,
                 game_map: GameMap, player: Entity, context: Optional[tcod.context.Context] = None
                 ):
        self.console = console
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.context = context  # Store the context here
        self.stats_panel = StatsPanel(30, 16)

    def spawn_entities(self, num_enemies: int):
        """Spawn a set number of enemies randomly on the map."""
        for _ in range(num_enemies):
            enemy_stats = stats.enemy.copy()  # Ensure unique stats per enemy
            npc = Entity(
                random.randint(0, self.game_map.width - 1),
                random.randint(0, self.game_map.height - 1),
                "E", "enemy", (0, 255, 0), False, enemy_stats
            )
            npc.engine = self  # Link entity to engine
            self.entities.append(npc)  # Add enemy to game

    level = 1
    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)
            for entity in self.entities.copy():
                entity.hostile()

        if not any(entity for entity in self.entities if not entity.pc and entity.alive):
            self.level += 1
            print(f"You sure SLAMMED them! Moving on to level {self.level}.")
            self.levelup()
            
    def render(self, context: tcod.context.Context) -> None:

        self.game_map.render(self.console)

        for entity in self.entities:
            self.console.print(entity.x, entity.y, entity.char, fg=entity.color)
        
        if self.stats_panel and self.stats_panel.visible:
            self.stats_panel.render(self)

        if context is not None:  # Ensure context exists before presenting
            context.present(self.console)

        self.console.clear()

    entity_count = 2
    def levelup(self):
        self.player.stats.max_hp += 5
        self.player.stats.hp += int(self.player.stats.max_hp / 100 * 50)
        self.player.equipment.charges += int(self.player.equipment.max_charges / 100 * 75)
        self.player.update_equipped()
        self.stats_panel.toggle()
        while self.stats_panel.visible:
            self.render(self.context)  # Keep rendering the screen
            events = tcod.event.wait()  # Wait for player input
            for event in events:
                action = self.event_handler.dispatch(event)  # Process input

                if action:
                    action.perform(self, self.player)
        self.entity_count += 1
        self.spawn_entities(self.entity_count)


class StatsPanel:
    """A panel for displaying and modifying stats."""
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.panel = tcod.console.Console(width, height, order="F")
        self.visible = False  # Panel starts hidden
        self.selected_index = 0  # Track which menu item is selected
        self.menu_items = ["max_hp", "hp", "basepow", "addpow", "slots",
                           "max_charges", "charges", "effect_duration", "max_distance",
                           "aoe"]

    def toggle(self):
        """Show or hide the panel."""
        self.visible = not self.visible
        print(f"Stats panel is now {'visible' if self.visible else 'hidden'}.")

    def render(self, engine: Engine):
        """Render the stats panel with selection cursor."""
        if not self.visible:
            return

        self.panel.clear()
        self.panel.draw_frame(0, 0, self.width, self.height, title="Stats Allocation", fg=(255, 255, 255), bg=(0, 0, 0))

        list_length = 0
        # Example stat display with selection cursor
        for index, item in enumerate(self.menu_items):
            cursor = ">" if index == self.selected_index else " "  # Add cursor to selected item
            if item == "hp" or item == "basepow":
                self.panel.print(3, 2 + index, f"{cursor} {item}: {getattr(engine.player.stats, item.lower())}", fg=(255, 155, 155))
            elif item == "charges":
                self.panel.print(3, 2 + index, f"{cursor} {item}: {getattr(engine.player.equipment, item.lower())}", fg=(255, 155, 155))
            elif item == "addpow":
                self.panel.print(2, 2 + index, f"{cursor} {item}: {getattr(engine.player.stats, item.lower())} %", fg=(255, 255, 255))
            else:
                self.panel.print(2, 2 + index, f"{cursor} {item}: {getattr(engine.player.stats, item.lower())}", fg=(255, 255, 255))
            list_length = index
        total_atk = engine.player.stats.basepow + engine.player.stats.addpow / 100 * engine.player.stats.basepow
        total_atk = int(total_atk)
        list_length += 2
        self.panel.print(2, 2 + list_length, f"Total attack power: {total_atk}", fg=(155, 255, 155))

        # copy panel's content directly to engine console
        engine.console.rgb[10:10+self.width, 5:5+self.height] = self.panel.rgb[:]


