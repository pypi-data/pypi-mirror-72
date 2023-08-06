from oubliette.items.inventory import Inventory
from oubliette.items.misc import game_currency
from oubliette.core.intents import Intent
from oubliette.attributes import Commandable, Talkable, Observable
from oubliette.exceptions import ExchangerException, CantAffordException, MenuExitedException
from oubliette.core.events import Events


class NPC(Talkable, Observable):
    """Base calss for anything you might consider a non-player character."""

    def __init__(self, menu=None, dialog=None, inventory=None, events=Events()):
        self.menu = menu
        self.dialog = dialog or f"The {self.__class__.__name__} says nothing."
        self.inventory = inventory or Inventory()
        self.events = events
        self.talk_count = 0

    def tick(self, global_count, session):
        self.inventory.tick(global_count, session)
        self.events.tick(global_count, session)

    @staticmethod
    def on_talk(this, intent):
        this.talk_count += 1
        intent.context.render_text(this.dialog)


class Exchanger:
    """Exchanger base. Inherit to create NPCs like traders or smiths or objects like cooking ovens"

    Pattern: Interface, AbstractFactory

    This is a base class. It's purpose is to be inherited to provide utility to subclasses.
    You can add methods here that will automatically be available to subclasses.

    price buff can affect the Exchangers advantage in an exchange or produce higher quality items.
    A higher quality exchanger may have a higher price buff.
    """

    price_buff = 0
    currency = game_currency

    @staticmethod
    def debit_by_ingredients(item, inventory):
        """Create an Item via materials.

        Args:
            item (Item): The Item class you want to create.
            inventory (Inventory): an inventory of items.

        Returns:
            Inventory: The created item in an Inventory bucket.
        """
        return item.create(inventory)

    @classmethod
    def debit_by_currency(cls, item, inventory, currency=None, count=1):
        """Produce an item in exchange for currency.

        Args:
            item (Item): The Item class you want to create.
            inventory (Inventory): an inventory of items.
            currency (Object): Currency class for this transaction
            count (int): How many are being purchased?

        Returns:
            Inventory: The created item in an Inventory bucket.
        """
        currency = currency or cls.currency
        return item.buy(inventory, currency, count)


class Trader(NPC, Exchanger, Commandable):
    """Traders can interact with others to buy, sell, and perform special
    services.

    Traders are driven by a menu. Create a menu in a way that will result in
    a series of selections that, when combined in order, will look like the
    terminal command you want the trader to execute.

    example menu:

   |-forge
   |    |-IronLongsword
   |    |-IronDagger
   |    |-BronzeDagger
   |-buy
       |-IronOre

   To navigate the menu to buy an IronLongsword you would make the selections:
   forge
   IronLongsword
   those selections are joined together into a string, and processed into an intent
   as if the Trader had written it. This means it will search the Trader for the
   action at the start of the command and then perform target resolution on rest
   of the string to pull in the objects. If your menu has speical items in it you
   can add a custom resolve_target method.
   So, any first tier menu item should have a matching method name on the Trader.
   """

    def shop(self, intent):
        """Invoke the traders trade selection"""
        if self.dialog:
            intent.context.interface.prompt.render_text(self.dialog)
        if self.menu:
            while True:
                try:
                    selected = self.menu.on_context(self.menu, intent)
                    self.process_menu_selection(selected, intent)
                except CantAffordException as e:
                    # Couldn't afford
                    intent.context.interface.prompt.render_text(f"Get fucked, nerd. {e}")
                except MenuExitedException:
                    # Exited menu
                    break
            intent.context.interface.prompt.render_text("Thanks!")

    def process_menu_selection(self, selected, buyer_intent):
        """Ask the Trader to perform an action based on the buyers menu selection.

        We basically use the menu to form a command string that the Trader then
        executes as if we were controlling them.
        We attach the buyers intent as meta to the generated intent so the Trader
        has access to the original intent for info like who the buyer is.

        Args:
            selected (str): menu selection string.
            buyer_intent (Intent): The initial intent from the buyer that started the dialog.

        Returns:
            object: The result of the traders command execution.
        """
        trader_intent = Intent.from_command(selected, self, buyer_intent.context,
                                            meta=buyer_intent)
        result = self.on_command(self, trader_intent)
        return result

    def buy(self, item, inventory, currency=None, count=1):
        """Sell an item to a customer.

        Named from the customers perspective.
        """
        # XXX this needs to have the same signature as a reacion method
        raise NotImplementedError("Fix the signature")
        currency = currency or self.currency
        goods = self.debit_by_currency(item, inventory, currency, count=count)
        inventory.update(goods)
