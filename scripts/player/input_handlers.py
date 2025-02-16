from __future__ import annotations
from typing import Optional, TYPE_CHECKING

import tcod.event
if TYPE_CHECKING:
    from scripts.engine import Engine

from scripts.player.actions import Action, EscapeAction, MovementAction, TargetingAction, AttackAction, StatsAction, StatsAllocationAction, StatsDeallocationAction

class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine):
        self.engine = engine  # Store reference to engine
    
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()
    
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        if self.engine.stats_panel.visible:
            if key == tcod.event.KeySym.KP_8:
                self.engine.stats_panel.selected_index -= 1
                if self.engine.stats_panel.selected_index < 0:
                    self.engine.stats_panel.selected_index = len(self.engine.stats_panel.menu_items) - 1  # Wrap around
            elif key == tcod.event.KeySym.KP_2:
                self.engine.stats_panel.selected_index += 1
                if self.engine.stats_panel.selected_index >= len(self.engine.stats_panel.menu_items):
                    self.engine.stats_panel.selected_index = 0  # Wrap around
            elif key == tcod.event.KeySym.KP_PLUS:
                action = StatsAllocationAction()
            elif key == tcod.event.KeySym.KP_MINUS:
                action = StatsDeallocationAction()
        else:
            if key == tcod.event.KeySym.KP_7:
                action = MovementAction(dx=-1, dy=-1)
            elif key == tcod.event.KeySym.KP_8:
                action = MovementAction(dx=0, dy=-1)
            elif key == tcod.event.KeySym.KP_9:
                action = MovementAction(dx=1, dy=-1)
            elif key == tcod.event.KeySym.KP_4:
                action = MovementAction(dx=-1, dy=0)
            elif key == tcod.event.KeySym.KP_6:
                action = MovementAction(dx=1, dy=0)
            elif key == tcod.event.KeySym.KP_1:
                action = MovementAction(dx=-1, dy=1)
            elif key == tcod.event.KeySym.KP_2:
                action = MovementAction(dx=0, dy=1)
            elif key == tcod.event.KeySym.KP_3:
                action = MovementAction(dx=1, dy=1)

            elif key == tcod.event.KeySym.f:
                action = TargetingAction(self.engine.player.stats.max_distance)
            
            elif key == tcod.event.KeySym.SPACE:
                action = AttackAction()

        if key == tcod.event.KeySym.TAB:  # Open stats panel with TAB
            action = StatsAction()

        if key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction()
        
        return action