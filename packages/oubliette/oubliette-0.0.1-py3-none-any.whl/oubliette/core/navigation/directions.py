from oubliette.utils import StrNameMetaclass


class Direction(metaclass=StrNameMetaclass):
    """Base class for directions to move"""
    pass


class North(Direction):
    pass


class South(Direction):
    pass


class East(Direction):
    pass


class West(Direction):
    pass


class NorthEast(Direction):
    pass


class NorthWest(Direction):
    pass


class SouthEast(Direction):
    pass


class SouthWest(Direction):
    pass


class Up(Direction):
    pass


class Down(Direction):
    pass

alises = {
    "n": "North",
    "north": "North",
    "s": "South",
    "south": "South",
    "e": "East",
    "east": "East",
    "w": "West",
    "west": "West",
    "ne": "NorthEast",
    "NE": "NorthEast",
    "northeast": "NorthEast",
    "Northeast": "NorthEast",
    "nw": "NorthWest",
    "NW": "NorthWest",
    "northwest": "NorthWest",
    "Northwest": "NorthWest",
    "se": "SouthEast",
    "SE": "SouthEast",
    "southeast": "SouthEast",
    "Southeast": "SouthEast",
    "sw": "SouthWest",
    "SW": "SouthWest",
    "southwest": "SouthWest",
    "SouthWest": "SouthWest",
    "u": "Up",
    "up": "Up",
    "d": "Down",
    "down": "Down"
}
