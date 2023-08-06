from oubliette import utils
from oubliette.attributes import Commandable, Observer, Observable, Equiper, Navigator, Taker, User, Help, Talker
from oubliette.exceptions import IntentTargetResolutionException
from .base import NPC
from oubliette.items.base import Item
from oubliette.items.inventory import Inventory
from oubliette.items.equipment import Equipment
from oubliette.items.minerals import IronOre
from oubliette.items.weapons import IronSword
from oubliette.core.events import Events


class Player(Commandable, Observer, Observable, Equiper, Navigator, Taker, User, Help, Talker):

    def __init__(self, name, inventory=None, equipment=None, events=Events()):
        self.name = name
        self.inventory = inventory or Inventory()
        self.equipment = equipment or Equipment()
        self.events = events

    def tick(self, global_count, session):
        try:
            for item in self.inventory.keys():
                item.tick(global_count, session)
        except:
            pass
        try:
            for item in self.equipment.values():
                item.tick(global_count, session)
        except:
            pass
        try:
            self.events.tick(global_count, session)
        except:
            pass

    @staticmethod
    def on_look(this, intent):
        if intent.target is this:  # PLayer has issued an empty look command
            intent.context.area.on_look(intent.context.area, intent)
            intent.context.render_text(f"{this.name}:")
            intent.context.render_text(" -inventory")
            intent.context.render_text(" -equipment")

    def resolve_target(self, target, context):
        """Custom intent target resolver for a player.

        Try looking in the players inventory and equipment for intent targets.

        Args:
            target (str): The intent target to resolve to an object.

        Returns:
            object: The inventory item that was found.

        Raises:
            IntentTargetResolutionException
        """
        try:
            target, _ = self.inventory.resolve_target(target, context)
            return target, self
        except IntentTargetResolutionException:
            pass
        target, _ = self.equipment.resolve_target(target, context)
        return target, self
