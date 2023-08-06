from abc import ABC, abstractmethod
from uuid import uuid4
from types import MethodType
from oubliette.exceptions import EventDiscardException


class Events:

    def __init__(self, events=None):
        """Take a list of events and manage them.

        events (list): a list of event objects.
        """
        events = events or {}
        self.events = {e.id: e for e in events}

    def tick(self, global_count, session):
        if self.events:
            for event_id, event in list(self.events.items()):
                try:
                    event.tick(global_count, session)
                except EventDiscardException:
                    self.events.pop(event_id, None)


class Event():
    """An event is regestered with session and takes an action when a condition is met."""

    def __init__(self, target=None):
        """Run the check on each tick to see if we should execute the callback. """
        self.id = str(uuid4())
        self.ticks = 0
        self.target = target
        self.fire_count = 0
        self.supress = 0

    def tick(self, global_count, session):
        """Run an update on each game tick

        Args:
            global_count (int): Total game ticks
            session (Session): The current game session

        Raises:
            EventDiscardException
        """
        self.ticks += 1
        if self.check(global_count, session):
            if self.supress:
                self.supress -= 1
            else:
                self.callback(global_count, session)
                self.fire_count += 1

    def set(self):
        """Use this to register methods to this class.

        This method is used to register new check and callback methods for instances
        of this event.
        Just name the functions you're registering as check or callback and make sure
        they have the right signature (self, gc, sess)
        the arg names don't matter, just make sure they have the right amount.
        the event will be able to access th events self to get ticks and the target.

        e = Event()

        @e.set()
        def new(self, gc, s):
            if gc > 10:
                session.render_text("you've made 10 moves")

        e.new(11, session)
        """
        def decorator(func):
            meth = MethodType(func, self)
            setattr(self, func.__name__, meth)
            return func
        return decorator

    def check(self, global_count, session):
        """Should we activate this event?

        To discard this event, raise EventDiscardException.

        Args:
            global_count (int): Total game ticks
            session (Session): The current game session

        Returns:
            bool: Activate the event?

        Raises:
            EventDiscardException
        """
        return True

    def callback(self, global_count, session):
        """Perform a callback action when this event is activated.

        To discard this event, raise EventDiscardException.

        Args:
            global_count (int): Total game ticks
            session (Session): The current game session

        Raises:
            EventDiscardException
        """
        raise EventDiscardException()

    def add_supress(self, count=1):
        """Supress event checking for `count` more rounds.

        Args:
            count (int): How may rounds to supress event fire checks.
        """
        self.supress += count

    def remove_supress(self, count=1):
        """Remove ticks that supress event checks.

        Args:
            count (int): Number of ticks to remove from the event supression count.
        """
        self.supress -= count
        if self.supresss < 0:
            self.supress = 0

    def clear_supress(self):
        """Remove all event supression."""
        self.supress = 0
