from oubliette.core.navigation.areas import Area
from oubliette.core.navigation.junctions import Junction
from oubliette.core.navigation.portals import Road, Door
from oubliette.core.navigation import directions

from oubliette.entities.npcs import Blacksmith
from oubliette.entities.menu import Menu
from oubliette import items

key_a = items.misc.Key(name="black key")

# Setup bar
bar = Area("Bar")

# Setup Armory
forge_menu = Menu("Forge an item", {"IronIngot": "forge an iron ingot.",
                                    "IronLongsword": "forge a longsword",
                                    "IronDagger": "forge a dagger",
                                    "axe": "A massive axe"})
action_menu = Menu("Blacksmith services", {"forge": forge_menu})
armory = Area("Armory", characters={"blacksmith": Blacksmith(menu=action_menu)})

general_store = Area("General Store")

home = Area("Home", inventory=items.inventory.Inventory({items.weapons.IronSword: 1,
                                                         items.weapons.IronDagger: 1,
                                                         items.minerals.IronIngot: 1,
                                                         key_a: 1}))

bar_home = Junction(bar, directions.South,
                    home, directions.North,
                    Road())
bar_general_store = Junction(bar, directions.North,
                             general_store, directions.SouthEast,
                             Road())
bar_armory = Junction(bar, directions.East,
                      armory, directions.West,
                      Door())
armory_general_store = Junction(armory, directions.North,
                                general_store, directions.SouthWest,
                                Door(key=key_a))
