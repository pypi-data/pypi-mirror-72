from uuid import uuid4
from oubliette.attributes import Navigable, Activatable, Observable, Takeable
from oubliette.exceptions import IntentTargetResolutionException
from oubliette.items.inventory import Inventory
from oubliette.core.events import Events
from oubliette.core.intents import Intent


class Area(Navigable, Observable, Takeable):
    """An object with junctions to other areas.

    Think of areas as graph nodes
    """

    def __init__(self, name, junctions=None, inventory=None, hidden_inventory=None,  # noqa
                 characters=None, objects=None, events=Events(),  # noqa
                 enter_text="You enter the {}", exit_text="You exit the {}"):  # noqa
        self.name = name
        self.id_ = uuid4()
        self.junctions = junctions or {}
        self.inventory = inventory or Inventory({})
        self.hidden_inventory = hidden_inventory or Inventory({})
        self.characters = characters or {}
        self.objects = objects or {}
        self.visit_count = 0
        self.events = events
        self.need_tick_keys = [self.objects]
        self.need_tick_values = [self.characters,
                                 self.junctions]
        self.enter_text = enter_text
        self.exit_text = exit_text

    def tick(self, global_count, session):
        self.events.tick(global_count, session)
        self.inventory.tick(global_count, session)
        self.hidden_inventory.tick(global_count, session)
        for collection in self.need_tick_keys:
            for obj in collection.keys():
                try:
                    obj.tick(global_count, session)
                except Exception as e:
                    session.render_text(f"tick error {obj}: {e}")
        for collection in self.need_tick_values:
            for obj in collection.values():
                try:
                    obj.tick(global_count, session)
                except Exception as e:
                    session.render_text(f"tick error {obj}: {e}")

    def resolve_target(self, target, context):
        intent = Intent('', context=context, build_targets=False)
        for item in self.inventory.keys():
            if target == str(item):
                return item, self
        for name, character in self.characters.items():
            if target == name:
                return character, self
        for name, obj in self.objects.items():
            if target == name:
                return obj, self
        for direction, junction in self.junctions.items():
            desc = junction.render_description(junction, intent)
            if target in [direction.__name__, desc]:
                return junction, self
        raise IntentTargetResolutionException("Not found in area")

    @staticmethod
    def render_description(this, intent):
        """Get a custom discription for this object.

        Args:
            this (Area): object that needs to be described.
            intent (Intent): Intent for pulling extra data.

        Returns:
            str: The description.
        """
        return this.name

    @staticmethod
    def get_descriptive_directions(this, intent):
        """Get the available junction directions and where they lead.

        Args:
            this (Area): The area to search for directions.
            intent (Intent): Intent to pull extra data from.

        Returns:
            list: Strings describing directions.
        """
        dirs = []
        for direction, junction in this.junctions.items():
            dirs.append(f"{direction}: {junction.render_description(junction, intent)}")
        return dirs

    @staticmethod
    def on_look(this, intent):
        """Describe the area.

        Args:
            this (Area): The area to describe.
            intent (Intent): The intent carrying extra data.
        """
        intent.context.render_text("")
        dirs = this.get_descriptive_directions(this, intent)
        intent.context.render_text("Directions:")
        for d in dirs:
            intent.context.render_text(f"  {d}")
        if this.inventory:
            intent.context.render_text("Items:")
            for i in map(str, this.inventory.keys()):
                intent.context.render_text(f"  {i}")
        if this.characters:
            intent.context.render_text("Characters:")
            for c in map(str, this.characters.keys()):
                intent.context.render_text(f"  {c}")
        if this.objects:
            intent.context.render_text(f"Objects:")
            for o in map(str, this.objects.keys()):
                intent.context.render_text("  {o}")

    def add_junction(self, junction, direction):
        """Make this aware of being part of a junction.

        Args:
            junction (Junction): The junction this area is joining.
            direction (Direction): The direction the junction will attach to in this area.
        """
        self.remove_junction(direction, notify=False)
        self.junctions[direction] = junction

    def remove_junction(self, direction, notify=True):
        """Remove this area from a junction.

        Args:
            direction (Direction): Direction corresponding to which junction to remove.
            notify (bool): Should the junction be notified of the removal?
        """
        junction_obj = self.junctions.pop(direction, None)
        if junction_obj is not None and notify:
            junction_obj.unlink(dont_notify=[self])

    @staticmethod
    def _setup(this, intent):
        """Basic actions on entering an area.

        populate local objects and set the area.
        """
        intent.context.local_objects.update(this.objects)
        intent.context.area = this
        this.visit_count += 1

    @staticmethod
    def _teardown(this, intent):
        """Basic actions on exiting an area.

        Empty local objects and unset the area.
        """
        intent.context.local_objects = {}
        intent.context.area = Area(-1)

    @staticmethod
    def render_enter_text(this, intent):
        if this.enter_text:
            intent.context.render_text(this.enter_text.format(this.name))

    @staticmethod
    def render_exit_text(this, intent):
        if this.exit_text:
            intent.context.render_text(this.exit_text.format(this.name))

    @staticmethod
    def on_enter(this, intent):
        """Customize entering an exit.

        Call this._setup(this, intent) to enable basic area enter functionality.
        """
        this._setup(this, intent)
        this.render_enter_text(this, intent)
        this.on_look(this, intent)

    @staticmethod
    def on_exit(this, intent):
        """Customize exiting an exit.

        default behavior is to call on_enter on the intent target, usually a junction.

        """
        intent.target.on_enter(intent.target, intent)
