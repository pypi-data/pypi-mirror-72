from .base import Trader
from oubliette.attributes import Forgable, Observable, Talkable
from oubliette.items import weapons, minerals
from oubliette.exceptions import IntentTargetResolutionException


class Blacksmith(Trader, Observable, Talkable):

    def __init__(self, menu=None, dialog="Hi. How can I help you?", *args, **kwargs):
        super().__init__(menu=menu, dialog=dialog, *args, **kwargs)

    def resolve_target(self, target, context):
        """Custom intent target resolver for a basic blacksmith.

        Args:
            target (str): The intent target to resolve to an object.

        Returns:
            object: The Item that was found.

        Raises:
            IntentTargetResolutionException
        """
        can_forge = [weapons, minerals]
        for collection in can_forge:
            try:
                item = getattr(collection, target)
                return item, self
            except AttributeError:
                pass
        raise IntentTargetResolutionException(f"Blacksmith can't find {target}")

    @staticmethod
    def on_look(this, intent):
        intent.context.interface.prompt.render_text("A Blacksmith")

    def forge(self, intent):
        item = intent.target
        inventory = intent.meta.source.inventory  # Buyers inventory
        if not issubclass(item, Forgable):
            raise Exception(f"{item.__name__} is not Forgable")
        goods = self.debit_by_ingredients(item, inventory)
        inventory.update(goods)

    @staticmethod
    def on_talk(this, intent):
        this.shop(intent)
        # if this.dialog:
        #     intent.context.interface.prompt.render_text(this.dialog)
        #     if this.menu:
        #         this.menu.on_context(this.menu, intent)
        # if this.menu.selected.startswith("forge "):
        #     weapon = " ".join(this.menu.selected.split()[1:])
        #     joiner = "an" if weapon.lower().startswith(("a", "e", "i", "o", "u")) else "a"
        #     intent.context.interface.prompt.render_text(f"I can make you {joiner} {weapon}")


