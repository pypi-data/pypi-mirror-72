from oubliette.core.events import Events


class Session:
    """Holds the state of the local game for a player."""

    def __init__(self, player, interface, area, events=Events()):
        """

        local_objects is the collection of objects local to the player in the game (maybe in a room).
        global_objects is the collection of objects the player has access to everywhere that aren't on their person.

        Args:
            player (Player): The player this session is responsible for.
            interface (Interface): The interface the player will use for the session.
            area (Area): The initial area for the session
        """
        self.player = player
        self.interface = interface
        self.area = area
        self.junction = None
        self.global_objects = {}
        self.ticks = 0
        self.events = events

    def start(self):
        """Start the session.

        Responsible for bootstrapping the session.
        This includes:
        starting the players interface
        """
        self.interface.context = self
        self.interface.start(tick=self.tick)

    def render_text(self, string):
        """Ask the screen to print text.

        Args:
            string (str): The text to print.
        """
        self.interface.prompt.render_text(string)

    def tick(self):
        """propagate game ticks throughout the session"""
        self.ticks += 1
        need_ticks = [self.player,
                      self.area,
                      self.junction]
        for obj in need_ticks:
            if obj is None:
                continue
            try:
                obj.tick(self.ticks, self)
            except Exception as e:
                self.render_text(f"tick failed for {obj}: {e}")

        for collection in [self.global_objects]:
            for name, obj in collection.items():
                try:
                    obj.tick(self.ticks, self)
                except Exception as e:
                    self.render_text(f"tick failed for {name}: {e}")
        self.events.tick(self.ticks, self)
