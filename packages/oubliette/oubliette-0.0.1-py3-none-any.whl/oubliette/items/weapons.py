from .base import Item
from oubliette.attributes import Forgable, Observable, Equipable
from .minerals import IronOre, IronIngot


class Weapon(Item, Observable, Equipable):
    """Base weapon class"""

    name = None
    material = None
    attack_type = None
    body_slots = ("weapon",)

    @staticmethod
    def on_look(this, intent):
        if this.material.lower().startswith(("a", "e", "i", "o", "u")):
            prefix = "An"
        else:
            prefix = "A"
        intent.context.interface.prompt.render_text(f"{prefix} {this.material} {this.name}")


class TwoHandedWeapon(Weapon):
    """A weapon that requires both hands."""
    body_slots = ("weapon", "shield")

class ForgableWeapon(Forgable, Weapon):
    pass

class Sword(ForgableWeapon):

    name = "sword"
    attack_type = "swing"

class IronSword(Sword):

    ingredients = {IronIngot: 3}
    material = "iron"
    value = 20

class Dagger(ForgableWeapon):

    name = "dagger"
    attack_type = "stab"

class IronDagger(Dagger):

    ingredients = {IronIngot: 1}  # executive decision - daggers should only be one ingot, don't forget short swords
    recycled_ingredient = {IronIngot: 0}  # not enough metal to shape back into
    material = "iron"
    value = 5
