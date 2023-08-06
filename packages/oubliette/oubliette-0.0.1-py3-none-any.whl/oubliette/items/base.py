from oubliette.attributes import Observable, Observer, Commandable, Takeable
from oubliette.exceptions import ExchangerException, CantAffordException
from oubliette.utils import StrNameMetaclass
from .inventory import Inventory
from oubliette.core.events import Events

from inspect import isclass


class Item(Observable, Takeable, metaclass=StrNameMetaclass):
    """Item base class

    Pattern: Interface, Factory

    Used to repersent the basics of all items.
    Provides utility methods for creation, and various types of cost checking.
    """

    ingredients = {}
    value = 0
    name = ""

    def __init__(self, name="", events=Events()):
        self.name = name
        self.events = events
        self.ticks = 0

    def __repr__(self):
        return self.name or self.__class__.__name__

    def tick(self=None, global_count=None, session=None):
        if not isinstance(self, Item):
            return
        if not all([global_count, session]):
            raise ValueError("global_count and session must be provided")
        self.ticks += 1
        self.events.tick(global_count, session)

    @classmethod
    def tick(cls, global_count, session):
        pass

    @classmethod
    def can_create(cls, inventory):
        """Are there enough of the required ingredients to make this item?

        If there are not enough of the required ingredients for this item in the
        inventory supplied, raise an Exception.
        If there are, return an inventory of the required materials.

        Args:
            inventory (Inventory): A players item collection.

        Returns:
            Inventory: An Inventory of the required ingredients.
        """
        # TODO should this move to the exchanger?
        cost = Inventory(cls.ingredients)
        balance = cost.copy()
        balance.subtract(inventory)
        if any(filter(lambda x: x > 0, balance.values())):  # not enough in inventory
            missing_msg = "\n    ".join([f"{k}: {v*-1}" for k, v in balance.items() if v < 0])
            raise CantAffordException(f"Missing ingredients:{missing_msg}")
        return cost

    @classmethod
    def create(cls, inventory, force=False):
        """Create an item and subtract the cost from an inventory.

        Args:
            inventory (Inventory): An inventory
            force (bool): Ignore cost, create item without subtraction.

        Returns:
            Inventory: The created item in a new inventory bucket.
        """
        cost = cls.can_create(inventory)
        inventory.subtract(cost)
        return Inventory({cls: 1})

    @classmethod
    def can_buy(cls, inventory, currency, count):
        """Does the provided inventory have enough currency to afford this item?

        Args:
            inventory (Inventory): A players item collection.

        Returns:
            Inventory: An Inventory of the required ingredients.
        """
        cost = cls.value*count
        if inventory.get(currency, -1) < cost:
            raise CantAffordException(f"Not enough {currency}")
        return Inventory({currency: cost})

    @classmethod
    def buy(cls, inventory, currency, count=1, force=False):
        if force is True:
            cost = cls.can_buy(inventory, currency, count)
            inventory.subtract(cost)
        return Inventory({cls: count})
