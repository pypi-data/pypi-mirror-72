"""
This file contains attribute classes that are ment to be inherited to
provide mixin abilities.

When doing multiple inheritance, remember, methods are resolved left to right:

class Mixin1(object):
    def test(self):
        print "Mixin1"

class Mixin2(object):
    def test(self):
        print "Mixin2"

class MyClass(BaseClass, Mixin1, Mixin2):
    pass

>>> obj = MyClass()
>>> obj.test()
Mixin1
"""
from oubliette.exceptions import ActionException, InvalidCommand, PortalDenial
import oubliette.core
from . import items
from oubliette.utils import is_sub
from functools import wraps


def missing_target_filter(f):
    @wraps(f)
    def wrapper(self, intent):
        if intent.target is self:
            raise InvalidCommand("You must provide a valid target")
        else:
            return f(self, intent)
    return wrapper


class Action:
    """An Action defines a verb that an object perform like look, use, or take.

    ---
    Should I use an Action, Reaction, or both?

    Actions are typically issued by the player from the interface.
    Reactions are typically called by other objects in response to an action.

    Objects inheriting Action *can affect others* or is the source of the realated action.
    Objects inheriting Reaction *are affected by other* or is the target/goal of an action.
    ---



    Actions *MUST* define a method with that verb as its name.

    def look(self, intent)
    """

    action_name = ""
    description = ""
    doc = ""

    @classmethod
    def get_actions(cls):
        """Get all available action method names and descriptions.

        Returns:
            dict: method names and description.
        """
        actions = {}
        for super_class in cls.mro():
            if issubclass(super_class, Action) and super_class.action_name:
                actions[super_class.action_name] = {"description": super_class.description,
                                                    "usage": super_class.usage,
                                                    "doc": super_class.doc}
        return actions


class Reaction:
    """A Reaction defines a response trigger for different actions, like on_look could be triggered by look.

    ---
    Should I use an Action, Reaction, or both?

    Actions are typically issued by the interface.
    Reactions are typically called by other objects in response to an action.

    Objects inheriting Action *can affect others* or is the source of the realated action.
    Objects inheriting Reaction *are affected by other* or is the target/goal of an action.
    ---


    on_x is a static method so it doesn't implicitly receive a cls or self arg. This way we can pass
    an instance, a class object, or something totally different.

    @staticmethod
    def on_look(this, intent):
        if intent.target is this:  # Check if this object requested this reaction from itself.
           print(this.name)
        else:
           print(this)
    """
    pass


class Help(Action):
    """Can get help."""

    action_name = "help"
    description = "Get help on what you can do, or a specific command."
    usage = "help [command]"
    doc = """Show this menu."""

    def help(self, intent):
        """Get helpful information.

        Args:
            intent (Intent): Intent to pull extra info from.
        """
        actions = self.get_actions()
        if intent.get_target(0)._target in actions:
            action = intent.get_target(0)._target
            data = actions.get(action)
            if not data:
                intent.context.render_text(f"no command: {action}")
                return

            intent.context.render_text(f"| {action}")
            intent.context.render_text("|")
            intent.context.render_text(f"| {data['description']}")
            intent.context.render_text("|")
            intent.context.render_text("| Usage:")
            intent.context.render_text(f"|     {data['usage']}")
            intent.context.render_text("|")
            doc = data['doc'].split("\n")
            for line in doc:
                intent.context.render_text("|     "+line)
        else:
            padding = max([len(action) for action in actions])
            pad_char = " "
            divider = " - "
            for action, data in sorted(actions.items()):
                desc = data['description']
                intent.context.render_text(f"{action.ljust(padding, pad_char)}{divider}{desc}")
                intent.context.render_text("")


class Observer(Action):
    """Can look at other objects"""

    action_name = "look"
    description = "Make general observation of an area or object, view the contents of containers."
    usage = "look [target]"
    doc = """Look at a target. If the target is omitted, look at yourself.
You can look at targets in your local area or on your person."""

    def look(self, intent):
        """Look at another object. usually calling it's on_look method.

        Args:
            intent (Intent): Intent to pull extra info from.
        """
        try:
            intent.target.on_look(intent.target, intent)
        except AttributeError:
            intent.context.render_text("Nothing to see")


class Observable(Reaction):
    """can be looked at."""

    @staticmethod
    def on_look(this, intent):
        """Execute this objects behavior when being looked at.

        Being looked will usually print an object or it's name, but it can also be used for more interesting things.
        Looking at a Contextable object might open it's context. Looking at a cursed object might damage the player.

        Args:
            this (object): class or instance to be the context.
            intent (Intent): Intent to pull extra info from.
        """
        intent.context.interface.prompt.render_text(this)


class Commandable(Reaction):
    """This object can be targeted for Actions"""

    def __repr__(self):
        if getattr(self, "name") and self.name:
            return self.name
        else:
            return self.__class__.__name__

    @staticmethod
    def debug(intent):
        import pdb; pdb.set_trace()

    @staticmethod
    def _execute(this, intent):
        """Default command execution method.

        Keeping this hidden here so we can reference it.

        search this instance for a method matching the string in intent.action.
        pass that method the intent to process.
        ex.
        if intent.action == "look", try to find self.look. If you do, execute it and pass it the intent.

        Args:
            this (object): class or instance that will be reacting.
            intent (Intent): Intent to pull commands action name from.
        """
        try:
            callback = getattr(this, intent.action)
            return callback(intent)
        except AttributeError as e:
            intent.context.interface.prompt.render_text(f"{str(intent.source)} can't {intent.action}")

    @staticmethod
    def on_command(this, intent):
        """Execute an Action.

        Args:
            this (object): class or instance that will be reacting.
            intent (Intent): Intent to pull commands action name from.
        """
        return this._execute(this, intent)


class Contextable(Action, Reaction):
    """Can act as a prompt menu

    This class is a bit special and inherits Action and Reaction.
    back() is an action so this object can respond to direct commands from the interface when it's the interface target
    on_context() is a reaction os this object can be summoned by other objects actions
    """

    @staticmethod
    def on_context(this, intent):
        """Take required steps to be the prompt focus.

        Push this object onto the interface target stack.

        Args:
            this (object): class or instance to be the context.
            intent (Intent): Intent to pull extra info from.
        """
        intent.context.interface.target_stack.push(this)

    action_name = "back"
    description = "Return to the previous context or exit a menu."
    usage = "back"
    doc = ""

    def back(self, intent):
        """Release this item from the prompt focus

        Args:
            intent (Intent): Intent to pull extra info from.
        """
        intent.context.interface.target_stack.pop()


class Unequiper(Action):
    """can unequip"""

    action_name = "unequip"
    description = "Unequip an item"
    usage = "unequip <item>"
    doc = """Unequip a selected item. You must provide a target item to unequip."""

    def _enable_equiper(self):
        """Ensure this object has equipment"""
        if getattr(self, "equipment", None) is None:
            self.equipment = items.equipment.Equipment()

    @missing_target_filter
    def unequip(self, intent):
        """Remove an Item from equipment.

        Args:
            intent (Intent): Intent to pull extra info from.
        """
        self._enable_equiper()
        equipment = intent.target
        if not isinstance(equipment, items.inventory.Inventory):
            equipment = items.inventory.Inventory({equipment: 1})

        unequipped = self.equipment.unequip(equipment, intent)
        try:
            intent.source.inventory.update(unequipped)
        except AttributeError:
            intent.context.local_objects.update(unequipped)


class Equiper(Unequiper):
    """can equip"""

    action_name = "equip"
    description = "Equip an item. Place previously equipped items in you inventory."
    usage = "equip <item>"
    doc = """Equip a selected item. You must provide a target item.
You can equip items in you inventory or local area."""

    @missing_target_filter
    def equip(self, intent):
        """Move an item to this objects equipment collection.

        Args:
            intent (Intent): Intent to pull extra info from.
        """
        self._enable_equiper()
        equipment = intent.target
        if not isinstance(equipment, items.inventory.Inventory):
            equipment = items.inventory.Inventory({equipment: 1})

        # Equip the item and retrieve anything that was in the occupied slots
        # Put the unequipped item back in the inventory
        # If we can't, drop it in local_objects (might be an exchager with no inventory)
        unequipped = self.equipment.equip(equipment, intent)
        try:
            intent.source.inventory.update(unequipped)
        except AttributeError:
            intent.context.local_objects.update(unequipped)
        # Removed the equipped item from the inventory
        # If we can't remove the equipment from this objects inventory,
        # try to remove it from local objects
        try:
            self.inventory.subtract(equipment)
        except AttributeError:
            intent.context.local_objects.subtract(equipment)


class Equipable(Reaction):
    """Can be equipped."""

    @staticmethod
    def on_equip(this, intent):
        """Method to execute when this object is equipped.

        Args:
            this (object): class or instance being equipped.
            intent (Intent): Intent to pull extra info from.
        """
        pass

    @staticmethod
    def on_unequip(this, intent):
        """Method to execute when this object is unequipped.

        Args:
            this (object): class or instance being unequipped.
            intent (Intent): Intent to pull extra info from.
        """
        pass


class Navigable(Reaction):
    """Can be entered and exited"""

    @staticmethod
    def on_enter(this, intent):
        """Callback for when this object is entered.

        Args:
            this (object): class or instance being entered.
            intent (Intent): Intent to pull extra info from.
        """
        pass

    @staticmethod
    def on_exit(this, intent):
        """callback for when this object is exited

        Args:
            this (object): class or instance being exited.
            intent (Intent): Intent to pull extra info from.
        """
        pass


class Navigator(Action):
    """ can navigate"""

    action_name = "go"
    description = "Move in a direction."
    usage = "go <direction>"
    doc = """Move in a direction. Keep in mind you can use alises.
ex. move south:
  go South
  go south
  go s
  south
  s
Will all attempt to move you south"""

    @missing_target_filter
    def go(self, intent):
        """Access directions and move through junctions

        Args:
            intent (Intent): Intent to pull extra info from.
        """
        try:
            intent.context.area.on_exit(intent.context.area, intent)
        except PortalDenial as denial:
            direction = intent.get_target(0)._target
            for item in intent.source.inventory.keys():
                if isinstance(item, items.misc.Code):
                    key_intent = oubliette.core.intents.Intent.from_command(f"use {item} {direction}",
                                                                            intent.source, intent.context)
                    try:
                        key_intent.target.on_use(key_intent.target, key_intent)
                        intent.context.render_text(f"You use your {item}")
                        intent.context.render_text("")
                        intent.context.area.on_exit(intent.context.area, intent)
                        break
                    except PortalDenial:
                        pass
                    except AttributeError:
                        pass
            else:
                intent.context.render_text(denial)


class Activator(Action):
    """Can Activate"""

    action_name = "activate"
    description = "Attempt to activate or engage an item or object"
    usage = "Usage: activate <target>"
    doc = ""

    @missing_target_filter
    def activate(self, intent):
        """Activate an object.

        Args:
            intent (Intent): Intent to pull extra info from.
        """
        try:
            intent.target.on_activate(intent.target, intent)
        except AttributeError:
            intent.context.render_text(f"{intent.target} can't be activated")


class Activatable(Reaction):
    """Can be activated and deactivated"""

    @staticmethod
    def on_activate(this, intent):
        """Callback for when this object is activated.

        Args:
            this (object): class or instance being activated.
            intent (Intent): Intent to pull extra info from.
        """
        pass

    @staticmethod
    def on_deactivate(this, intent):
        """Callback for when this object is deactivated.

        Args:
            this (object): class or instance being deactivated.
            intent (Intent): Intent to pull extra info from.
        """
        pass


class Taker(Action):
    """Can take items."""

    action_name = "take"
    description = "Take an item or object and place it in your inventory."
    usage = "take <target>"
    doc = ""

    @missing_target_filter
    def take(self, intent):
        """Take an object and put it in your inventory.

        Args:
            intent (Intent): Intent to pull extra info from.
        """
        try:
            if is_sub(Takeable, intent.target):
                taken = intent.get_target().owner.on_take(intent.get_target().owner, intent)
                self.inventory.update(taken)  # noqa
                intent.context.render_text(f"took {intent.target}")
            else:
                raise AttributeError()
        except AttributeError:
            intent.context.render_text(f"{intent.get_target()} can't be taken")


class Takeable(Reaction):
    """Has items that can be taken."""

    @staticmethod
    def on_take(this, intent):
        """Callback for when this item is taken.

        Args:
            this (object): class or instance being taken.
            intent (Intent): Intent to pull extra info from.
        """
        requested = items.inventory.Inventory({intent.target: 1})
        this.inventory.subtract(requested)
        return requested


class User(Action):
    """Can use objects"""

    action_name = "use"
    description = """Use an item or object."""
    usage = "use <target 1> [target 2]"
    doc = """one target: use that target.
two targets: use target 1 on target 2.
ex.
    use key north (use a key on the door to the north of you)
    use hammer nail (use the hammer on the nail)"""

    @missing_target_filter
    def use(self, intent):
        """Call a targets on_use method.

        Args:
            intent (Intent): Intent to pull extra info from.
        """
        try:
            intent.target.on_use(intent.target, intent)
        except AttributeError:
            intent.context.render_text(f"{intent.target} can't be used")


class Usable(Reaction):
    """Can be used"""

    @staticmethod
    def on_use(this, intent):
        """Callback for when this object is used.

        Args:
            this (object): class or instance being deactivated.
            intent (Intent): Intent to pull extra info from.
        """
        pass


class Talker(Action):
    """Can talk to objects."""

    action_name = "talk"
    description = "Talk to something"
    usage = "talk <target>"
    doc = ""

    @missing_target_filter
    def talk(self, intent):
        """calls a targets on_talk

        Args:
            intent (Intent): Intent to pull extra info from.
        """
        try:
            intent.target.on_talk(intent.target, intent)
        except AttributeError:
            intent.context.render_text(f"{intent.target} can't talk")


class Talkable(Reaction):
    """Can respond to talk actions"""

    @staticmethod
    def on_talk(this, intent):
        """Callback for when this object is talked to.

        Args:
            this (object): class or instance being talked to.
            intent (Intent): Intent ot pull extra info from.
        """
        pass


class Forgable:
    pass
