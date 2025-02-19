import tcod
import tcod.event

class StartMenu:
    """Handles the game start menu."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.console = tcod.console.Console(width, height, order="F")
        self.selected_index = 0  # Track selected menu option
        self.menu_items = ["Start with Rune pouch", "Start with Mage's discus", "Exit"]

    def render(self, context: tcod.context.Context):
        """Render the start menu."""
        self.console.clear()
        self.console.draw_frame(10, 5, 40, 10, title="Magic Slam 3000", fg=(255, 255, 255))

        for index, item in enumerate(self.menu_items):
            color = (255, 255, 255) if index == self.selected_index else (150, 150, 150)
            self.console.print(20, 7 + index, f"{item}", fg=color)

        context.present(self.console)

    def handle_input(self, key: tcod.event.KeySym) -> str:
        """Handle keypresses for menu navigation."""
        if key == tcod.event.KeySym.UP or key == tcod.event.KeySym.KP_8:
            self.selected_index = (self.selected_index - 1) % len(self.menu_items)
        elif key == tcod.event.KeySym.DOWN or key == tcod.event.KeySym.KP_2:
            self.selected_index = (self.selected_index + 1) % len(self.menu_items)
        elif key == tcod.event.KeySym.RETURN:
            return self.menu_items[self.selected_index]  # Return selected option
        return ""

    def show(self, context: tcod.context.Context) -> str:
        """Runs the start menu and returns the player's selection."""
        while True:
            self.render(context)

            for event in tcod.event.wait():
                if event.type == "QUIT":
                    raise SystemExit()

                if event.type == "KEYDOWN":
                    choice = self.handle_input(event.sym)

                    if choice:
                        return choice  # Return "Start Game" or "Exit"
