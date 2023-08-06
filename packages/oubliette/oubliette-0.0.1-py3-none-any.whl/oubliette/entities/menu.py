from oubliette.attributes import Contextable, Commandable
from oubliette.exceptions import IntentTargetResolutionException, MenuExitedException
from oubliette.utils import StrNameMetaclass


class MenuExited:
    pass


class MenuOptionSelected:
    pass


class MenuBack:
    __metaclass__ = StrNameMetaclass
    name = "back"


class MenuSelection:

    def __init__(self, selected="back", status=MenuExited, sub=None):
        self.selected = selected
        self.status = status
        self.sub = sub

    def merge_sub_selection(self):
        if self.status is MenuExited:
            raise MenuExitedException("User quit the menu")
        merged = self.selected
        if self.sub:
            merged = " ".join([merged, self.sub.merge_sub_selection()])
        return merged


class Menu(Contextable, Commandable):

    def __init__(self, name, options, default="back", back_out="back", add_menu_back=True):
        self.name = name
        self.options = options
        self.default = default
        self.back_out = back_out
        if add_menu_back:
            self.options["back"] = "Go back"

    def __repr__(self):
        return self.name

    def resolve_target(self, target, context):
        if target not in self.options:
            raise IntentTargetResolutionException("Not a menu option")
        return target, self

    def display(self, intent):
        for option, description in self.options.items():
            intent.context.interface.prompt.render_text(f"{option}: {description}")

    @staticmethod
    def on_command(this, intent):
        """Select an option from this menu.

        Checking if the description of the chosen object is another menu allows recursion into submenus.
        """
        selected = intent.action
        sub = None
        description = this.options.get(selected, None)
        if selected == this.back_out:
            status = MenuExited
        elif isinstance(description, Menu):
            sub = description.prompt(description, intent)
            status = MenuOptionSelected
        else:
            status = MenuOptionSelected
        return MenuSelection(selected, status, sub=sub)

    @staticmethod
    def prompt(this, intent):
        """Get a response from the user and store it.

        Clear any previously selected responses.
        display menu options.
        set this object as the prompt focus.
        manually cue for user input. When this object gets a command, it stores the action in this.selected.
        pop this off the target stack.
        The object that spawned this menu can then view its `selected` attribute to see what was chosen.

        Args:
            this (object): class or instance to be the context.
            intent (Intent): Intent to pull extra info from.
        """
        intent.context.interface.target_stack.push(this)
        while True:
            selected_option = MenuSelection()
            try:
                this.display(intent)
                selected_option = intent.context.interface.cue()
            except Exception as e:
                intent.context.interface.prompt.render_text(f"not a good choice {e}")
            else:
                if (selected_option.status is not MenuExited and
                        selected_option.sub and selected_option.sub.status is MenuExited):
                    # If the submenu request was to go back, loop this menu.
                    continue
                break
        this.back(intent)
        return selected_option

    @staticmethod
    def on_context(this, intent):
        selection = this.prompt(this, intent)
        return selection.merge_sub_selection()

    def back(self, intent):
        """Release this item from the prompt focus

        Args:
            intent (Intent): Intent to pull extra info from.
        """
        intent.context.interface.target_stack.pop()
        return MenuExited
