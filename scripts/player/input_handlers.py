from typing import Optional

import tcod.event

from scripts.player.actions import Action, EscapeAction, MovementAction

class EventHandler(tcod.event.EventDispatch[Action]):
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

        elif key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction()
        
        return action