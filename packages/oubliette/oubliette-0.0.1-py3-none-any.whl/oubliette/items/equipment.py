from .inventory import RestrictedInventory, Inventory
from oubliette.exceptions import IntentTargetResolutionException


class Equipment(RestrictedInventory):
    """An objects equipment.

    Notes:
    - Two handed weapons will have two body slots: weapon and shield.
      When attacking, reference only the players weapon slot.
    """
    _allowed = ("head",
                "legs",
                "torso",
                "feet",
                "body",  # whole body (cloak/cape/etc...)
                "hands",
                "weapon",
                "shield")

    def __repr__(self):
        str_dict = "\n".join([f"{k}: {v.__name__}" for k, v in self.items()])
        return str_dict

    def tick(self, global_count, session):
        for item in self.values():
            try:
                item.tick(global_count, session)
            except Exception:
                pass

    def equip(self, inventory, intent):
        old_equipment = Inventory()
        for item in inventory:
            old = self.unequip(item, intent)  # remove existing equipment
            old_equipment.update(old)
            for slot in item.body_slots:
                self[slot] = item
            item.on_equip(item, intent)
        return old_equipment

    def unequip(self, item, intent):
        """Remove an item from all related equipment slots.

        Note: This doesn't place an item back in a players inventory.

        Args:
            item (Item): The item to remove.

        Returns:
            Inventory: The unequiped item in an inventory.
        """
        old_equipment = Inventory()
        main_slot, *remaining_slots = item.body_slots
        old_item = self.pop(main_slot, None)
        if old_item:
            Inventory.update({old_item: 1})
        for remaining in remaining_slots:
            self.pop(remaining, None)
        item.on_unequip(item, intent)
        return old_equipment

    def resolve_target(self, target, context):
        for item in self.values():
            if target == item.__name__:
                return item, self
        raise IntentTargetResolutionException("Not found in equipment")
