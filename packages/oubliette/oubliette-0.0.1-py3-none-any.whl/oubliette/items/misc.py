from .base import Item
import oubliette
from oubliette.attributes import Usable, Contextable, Navigator, Commandable
from oubliette.exceptions import PortalDenial
from uuid import uuid4


class Code(Item, Usable):

    name = "code"
    code = None

    def __init__(self, name=None, code=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name or Key.name
        self.code = code or self.code_gen()

    @staticmethod
    def code_gen():
        return str(uuid4())

    @staticmethod
    def on_use(this, intent):
        """Use this code on an object"""
        locked_obj = intent.get_target(1).target
        if not locked_obj:
            intent.context.render_text("Use on what?")
            return
        locked_obj.on_activate(locked_obj, intent)

    # def use(self, intent):
    #     intent.target.on_activate(intent.target, intent)
    #     self.back(intent)


class Key(Code):

    name = "key"

    # def go(self, intent):
    #     junction = intent.context.area.junctions[intent.target]
    #     junction.on_activate(junction, intent)
    #     self.back(intent)


class Lock(Item):

    name = "lock"
    code = None
    locked = True

    def __init__(self, code=None, locked=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if code:
            self.code = code.code
        self.locked = locked

    @staticmethod
    def render_description(this, intent):
        return "locked" if this.locked else ""

    @staticmethod
    def unlock(this, intent):
        if this.locked:
            try:
                if intent.target.code == this.code:
                    this.locked = False
                    intent.context.render_text("The lock clicks open")
                else:
                    raise PortalDenial(this.render_description(this, intent))
            except AttributeError:
                raise PortalDenial(this.render_description(this, intent))


class Currency:
    """Currency base."""
    pass


class Shekel(Currency):
    pass


class Dollarydoo(Currency):
    pass


class OublietteFunBuck(Currency):
    pass


game_currency = Dollarydoo
