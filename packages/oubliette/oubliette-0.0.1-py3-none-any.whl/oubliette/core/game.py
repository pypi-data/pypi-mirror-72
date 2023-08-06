class Game:
    """The main game object to be run.

    Right now it's only job is to track and manage sessions.
    """

    def __init__(self):
        self.sessions = []

    def add_session(self, session):
        """Push a session to the games session list.

        Args:
            session (Session): The session to add to the game.
        """
        self.sessions.append(session)

    def start(self):
        """Start the game.

        This method is responsible for setting up global game related systems.
        This includes starting sessions.
        """
        for session in self.sessions:
            session.start()
