import tcod
from scripts.engine import Engine
from scripts.player.input_handlers import EventHandler
from scripts.entity.entity import Entity
from scripts.map.game_map import GameMap
from scripts.entity import stats
from scripts import equipment
from scripts import engine as dimensions

def main() -> None:
    # screen_width = 85
    # screen_height = 50

    map_width = 80
    map_height = 45

    tileset = tcod.tileset.load_tilesheet(
        "assets/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    root_console = tcod.console.Console(dimensions.screen_width, dimensions.screen_height, order="F")  # Root console initialization

    player = Entity(int(map_width / 2), int(map_height / 2), "@", "player", (255, 255, 255), True, stats.base_player)
    npc = Entity(int(0), int(0), "E", "enemy", (0, 255, 0), False, stats.enemy)
    entities = {npc, player}

    game_map = GameMap(map_width, map_height)

    engine = Engine(console=root_console, entities=entities, event_handler=None, game_map=game_map, player=player, context=None)
    event_handler = EventHandler(engine)
    engine.event_handler = event_handler
    player.engine = engine
    npc.engine = engine

    #testing equipment
    runepouch = equipment.r_pouch
    player.equip_item(runepouch)
    player.print_stats()
    runepouch.aoe += 3
    player.equip_item(runepouch) # will maybe need to do an upgrade_equipment method later on
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