from .base import Item
from oubliette.attributes import Forgable

class Ore(Item, Forgable):
    """Base ore class"""
    pass

class IronOre(Ore):
    material = "iron"

class Ingot(Item, Forgable):
    pass

class IronIngot(Ingot):
    name = "IronIngot"
    ingredients = {IronOre: 1}
