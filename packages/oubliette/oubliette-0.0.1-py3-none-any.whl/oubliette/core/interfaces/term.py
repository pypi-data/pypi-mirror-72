import sys
from oubliette.attributes import Commandable
from oubliette.exceptions import NotCommandable, EmptyCommandException, InvalidCommand
from .prompt import ContextPrompt
from .target_stack import TargetStack
from oubliette.exceptions import IntentTargetResolutionException


class Term:
    """A Term instance proxies commands from a prompt to a target object."""

    def __init__(self, target, target_stack=TargetStack, prompt=ContextPrompt):
        """

        Args:
            target (Commandable): The target object for the terminal to pass commands to.
            target_stack (TargetStack): The mechanism that manages the which target the Term is focused on.
            prompt (Prompt): The mechanism that gets input and converts it into intents.
        """
        self.target_stack = target_stack(target)
        self.prompt = prompt

    @property
    def target(self):
        return self.target_stack.target

    def start(self, tick):
        """Start the interface.

        Responsible for tasks related to starting the interface.
        This includes:
        kicking off the cue() loop.

        Args:
            tick (function): function to increment game tick
        """
        while True:
            try:
                self.cue()
                tick()
            except IntentTargetResolutionException as e:
                self.prompt.render_text(e)
            except EmptyCommandException:
                pass
            except InvalidCommand as e:
                self.prompt.render_text(e)

    def cue(self, target=None):
        """Cue the target for input.

        self.context is set by the session.

        Args:
            target (object): object that will be prompted for Intents and asked to execute them.

        Returns:
            object: Anything a called method potentially returns
        """
        data = None
        active_target = self.target or target
        self.prompt.pre_prompt(active_target, self.context)
        intent = self.prompt.prompt(active_target, self.context)
        self.prompt.render_text("")
        if intent.action == "quit":
            sys.exit()
        data = active_target.on_command(active_target, intent)
        self.prompt.post_prompt(active_target, self.context)
        return data
