from oubliette.utils import StrNameMetaclass
from oubliette.attributes import Activatable, Observable
from oubliette.materials import materials
from oubliette.items.misc import Lock
from oubliette.core.events import Events


class Portal(Activatable, Observable, metaclass=StrNameMetaclass):
    """doors and stuff. maybe literal portals."""

    name = None
    material = None
    lock = Lock(locked=False)

    def __init__(self, key=None, events=Events(), lock_events=Events()):
        self.visit_count = 0
        self.events = events
        if key:
            self.lock = Lock(key, events=lock_events)

    def tick(self, global_count, session):
        self.events.tick(global_count, session)
        self.lock.tick(global_count, session)

    @staticmethod
    def render_description(this, intent):
        desc = [this.lock.render_description(this.lock, intent),
                this.material.name,
                this.name]
        return ' '.join(x for x in desc if x)

    @staticmethod
    def render_activate(this, intent):
        pass

    @staticmethod
    def render_deactivate(this, intent):
        pass

    @staticmethod
    def on_activate(this, intent):
        if this.lock.locked:
            this.lock.unlock(this.lock, intent)
        else:
            this.render_activate(this, intent)
            this.visit_count += 1

    @staticmethod
    def on_deactivate(this, intent):
        this.render_deactivate(this, intent)

    @staticmethod
    def on_look(this, intent):
        intent.context.interface.prompt.render_text(f"A {this.render_description(this, intent)}")


class Door(Portal):
    """Wooden Door"""

    name = "door"
    material = materials.Wood

    @staticmethod
    def render_activate(this, intent):
        intent.context.interface.prompt.render_text(f"You open the {this.render_description(this, intent)}")

    @staticmethod
    def render_deactivate(this, intent):
        intent.context.interface.prompt.render_text(f"You walk through the {this.render_description(this, intent)}")


class BrokenDoor(Door):

    name = "broken door"
    material = materials.Null


class ExteriorDoor(Door):

    material = materials.Null


class Hatch(Portal):

    name = "hatch"
    material = materials.Wood

    @staticmethod
    def render_activate(this, intent):
        intent.context.interface.prompt.render_text(f"You haul open the {this.render_description(this, intent)}")

    @staticmethod
    def render_deactivate(this, intent):
        intent.context.interface.prompt.render_text(f"You climb through the {this.render_description(this, intent)}")


class NullHatch(Hatch):
    material = materials.Null

class Road(Portal):

    name = "road"
    material = materials.Null

    @staticmethod
    def render_deactivate(this, intent):
        intent.context.interface.prompt.render_text(f"You cross the {this.render_description(this, intent)}")
        pass


class Grass(Portal):

    name = "grass"
    material = materials.Null

    @staticmethod
    def render_deactivate(this, intent):
        intent.context.interface.prompt.render_text(f"You cross the {this.render_description(this, intent)}")
        pass


class Floor(Portal):

    name = "floor"
    material = materials.Null

    @staticmethod
    def render_deactivate(this, intent):
        intent.context.interface.prompt.render_text(f"You cross the {this.render_description(this, intent)}")
        pass
