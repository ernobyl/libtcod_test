import tcod
from scripts.engine import Engine
from scripts.StartMenu import StartMenu
from scripts.player.input_handlers import EventHandler
from scripts.entity.entity import Entity
from scripts.map import game_map
from scripts.entity import stats
from scripts import equipment
from scripts import engine as dimensions
import random

from typing import TYPE_CHECKING

def main() -> None:
    # screen_width = 85
    # screen_height = 50

    map_width = 80
    map_height = 45

    room_max_size = 18
    room_min_size = 8
    max_rooms = 30

    tileset = tcod.tileset.load_tilesheet(
        "assets/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    with tcod.context.new_terminal(
        map_width, map_height, tileset=tileset, title="Magic Slam 3000", vsync=True
    ) as context:
        start_menu = StartMenu(map_width, map_height)
        choice = start_menu.show(context)

        if choice == "Exit":
            raise SystemExit()
        elif choice == "Start with Rune pouch":
            starting_gear = equipment.r_pouch
        elif choice == "Start with Mage's discus":
            starting_gear = equipment.m_disc

    root_console = tcod.console.Console(dimensions.screen_width, dimensions.screen_height, order="F")  # Root console initialization

    player = Entity(int(map_width / 2), int(map_height / 2), "@", "player", (255, 255, 255), True, stats.base_player)
    entities = [player]

    map = game_map.generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        player=player
    )

    engine = Engine(console=root_console, entities=entities, event_handler=None, game_map=map, player=player, context=None)
    event_handler = EventHandler(engine)
    engine.event_handler = event_handler
    player.engine = engine
    engine.spawn_entities(2)

    #testing equipment
    player.equip_item(starting_gear)
    player.print_stats()

    with tcod.context.new_terminal(
        dimensions.screen_width,
        dimensions.screen_height,
        tileset=tileset,
        title="MAGIC SLAM 3000",
        vsync=True,
    ) as context:
        engine.context = context
       #root_console = tcod.console.Console(screen_width, screen_height, order="F")
       # engine.console = root_console
        while True:
            engine.render(context=context)

            events = tcod.event.wait()
            
            engine.entities = [entity for entity in engine.entities if entity.alive]
            if not player.alive:
                raise SystemExit()
            engine.handle_events(events)




if __name__ == "__main__":
    main()