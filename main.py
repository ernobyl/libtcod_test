import tcod
from scripts.engine import Engine
from scripts.player.input_handlers import EventHandler
from scripts.entity.entity import Entity
from scripts.map.game_map import GameMap

def main() -> None:
    screen_width = 85
    screen_height = 50

    map_width = 80
    map_height = 45

    tileset = tcod.tileset.load_tilesheet(
        "assets/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()

    player = Entity(int(map_width / 2), int(map_height / 2), "@", (255, 255, 255), True)
    npc = Entity(int(0), int(0), "E", (0, 255, 0), False)
    entities = {npc, player}

    game_map = GameMap(map_width, map_height)

    engine = Engine(entities=entities, event_handler=event_handler, game_map=game_map, player=player)
    player.engine = engine
    npc.engine = engine

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="MAGIC SLAM 3000",
        vsync=True,
    ) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        while True:
            engine.render(console=root_console, context=context)

            events = tcod.event.wait()
            
            engine.handle_events(events)




if __name__ == "__main__":
    main()