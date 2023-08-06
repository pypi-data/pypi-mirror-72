from . import properties


class Material:
    name = ""


class Null(Material):
    opacity = properties.Transparent


class Wood(Material):
    name = "wood"
    opacity = properties.Opaque
