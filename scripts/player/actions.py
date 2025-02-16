from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

import tcod
import tcod.event
from tcod import libtcodpy


if TYPE_CHECKING:
    from scripts.engine import Engine
    from scripts.entity.entity import Entity

class Action:
     def perform(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError()

class EscapeAction(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()

class MovementAction(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Destination is blocked by a tile.

        entity.move(self.dx, self.dy)

class AttackAction(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        pass

class StatsAction(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        engine.stats_panel.toggle()

class StatsAllocationAction(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        stats_panel = engine.stats_panel
        player_stats = engine.player.stats
        equipped_stats = engine.player.equipment

        # Get the currently selected stat name
        selected_stat = stats_panel.menu_items[stats_panel.selected_index].lower()  # Convert to lowercase to match attributes

        # Use max_hp as the allocation pool
        if player_stats.max_hp > 0:  # Ensure there's at least 1 point to allocate
            if hasattr(equipped_stats, selected_stat) and (selected_stat != "hp" and selected_stat != "basepow" and selected_stat != "charges"):  # Ensure the stat exists
                setattr(equipped_stats, selected_stat, getattr(equipped_stats, selected_stat) + 1)
                player_stats.max_hp -= 1  # Reduce allocation pool
                engine.player.equip_item(engine.player.equipment)
                engine.player.print_stats()

                print(f"Allocated 1 point to {selected_stat}. New {selected_stat}: {getattr(player_stats, selected_stat)}")
                print(f"Remaining Pool: {player_stats.max_hp}")
            else:
                print(f"Error: {selected_stat} is not a valid stat.")
        else:
            print("No points left to allocate!")
        


class StatsDeallocationAction(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        stats_panel = engine.stats_panel
        player_stats = engine.player.stats
        equipped_stats = engine.player.equipment

        # Get the currently selected stat name
        selected_stat = stats_panel.menu_items[stats_panel.selected_index].lower()

        if hasattr(equipped_stats, selected_stat):  # Ensure the stat exists
            stat_value = getattr(equipped_stats, selected_stat)  # Get current value
            
            if stat_value > 0:  # Check if value is greater than 0
                setattr(equipped_stats, selected_stat, stat_value - 1)  # Reduce stat
                player_stats.max_hp += 1  # Increase allocation pool

                engine.player.equip_item(engine.player.equipment)  # Reapply equipment stats
                engine.player.print_stats()  # Print new stats for debugging

                print(f"Deallocated 1 point from {selected_stat}. New {selected_stat}: {stat_value - 1}")
                print(f"Remaining Pool: {player_stats.max_hp}")
            else:
                print(f"{selected_stat} cannot be lower than 0")  # Prevent negative stats
        else:
            print(f"Error: {selected_stat} is not a valid stat.")



class TargetingAction(Action):
    def __init__(self, max_distance: int):
        self.max_distance = max_distance  # Max range of attack/effect

    def perform(self, engine: Engine, entity: Entity) -> Optional[Tuple[int, int]]:
        """Allows the player to move a targeting cursor and select a tile."""
        cursor_x, cursor_y = entity.x, entity.y  # Start at entity position

        while True:
            self.render_targeting(engine, cursor_x, cursor_y)

            events = tcod.event.wait()
            for event in events:
                action = engine.event_handler.dispatch(event)
                if isinstance(event, tcod.event.KeyDown):
                    key = event.sym  # Get key input

                if action is None:
                    continue

                # Cancel targeting if Escape is pressed
                if isinstance(action, EscapeAction):
                    return None
                # Confirm selection when Space is pressed
                if isinstance(action, AttackAction):
                    return engine.player.ranged_attack(cursor_x, cursor_y)  # Call attack
                prev_x = cursor_x
                prev_y = cursor_y
                # Move cursor
                if key == tcod.event.KeySym.KP_8:
                    cursor_y -= 1
                elif key == tcod.event.KeySym.KP_2:
                    cursor_y += 1
                elif key == tcod.event.KeySym.KP_4:
                    cursor_x -= 1
                elif key == tcod.event.KeySym.KP_6:
                    cursor_x += 1
                
                # Ensure cursor stays within valid range
                if entity.distance_to_tile(cursor_x, cursor_y) > self.max_distance:
                    cursor_x, cursor_y = prev_x, prev_y  # prevent going out of range

            # Update the screen with the cursor
            engine.context.present(engine.console)


    def render_targeting(self, engine: Engine, cursor_x: int, cursor_y: int):
        """Render a targeting overlay smoothly without flickering."""

        # Create an offscreen console for full rendering
        buffer_console = tcod.console.Console(engine.console.width, engine.console.height, order="F")

        # Render the normal game screen onto the buffer (not directly to engine.console)
        engine.game_map.render(buffer_console)

        for entity in engine.entities:
            buffer_console.print(entity.x, entity.y, entity.char, fg=entity.color)

        # Create an overlay for targeting
        overlay = tcod.console.Console(engine.console.width, engine.console.height, order="F")

        # Apply semi-transparent highlight to valid tiles
        for x in range(engine.game_map.width):
            for y in range(engine.game_map.height):
                if engine.player.distance_to_tile(x, y) <= self.max_distance:
                    overlay.bg[x, y] = (100, 100, 100)  # Gray highlight

        for x in range(engine.game_map.width):
            for y in range(engine.game_map.height):
                if engine.player.distance_to_tile(x, y, cursor_x, cursor_y) <= engine.player.stats.aoe:
                    overlay.bg[x, y] = (180, 100, 50) # orange aoe indicator
        # Draw the targeting cursor in red
        overlay.bg[cursor_x, cursor_y] = (255, 0, 0)  # Red cursor

        # Blit the overlay onto the buffer with transparency
        overlay.blit(buffer_console, bg_alpha=0.5)  # Smoothly blend the highlight

        # Copy the final buffer to `engine.console` and present
        buffer_console.blit(engine.console)
        engine.context.present(engine.console)

