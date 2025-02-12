from __future__ import annotations
from typing import Optional, TYPE_CHECKING

import tcod.event
if TYPE_CHECKING:
    from scripts.engine import Engine

from scripts.player.actions import Action, EscapeAction, MovementAction, TargetingAction, AttackAction

class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine):
        self.engine = engine  # Store reference to engine
    
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()
    
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

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

        elif key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction()
        
        return action