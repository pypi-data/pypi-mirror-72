from abc import ABC, abstractmethod

class BaseTargetStack(ABC):
    """LIFO stack of target.

    A target stack allows for nesting of command targets.
    FOr instance, if a user wants to look at an item in their inventory,
    they can select the inventory as their new target, show an item or two,
    then pop that target off the stack and return to their previous command
    target (likely their player).
    """

    @property
    @abstractmethod
    def target(self):
        """Shortcut to get the active target.

        Returns:
            Commandable: a commandable target
        """
        pass

    @abstractmethod
    def push(self, target):
        """Set focus on a new target.

        Args:
            Target (Commandable): A Commandable object

        Returns:
            COmmandable: The pushed target
        """
        pass

    @abstractmethod
    def pop(self):
        """Navigate one target back up the stack.

        Returns:
            Commandable: the popped target.
        """
        pass


class TargetStack:
    """LIFO stack of target.

    A target stack allows for nesting of command targets.
    FOr instance, if a user wants to look at an item in their inventory,
    they can select the inventory as their new target, show an item or two,
    then pop that target off the stack and return to their previous command
    target (likely their player).
    """

    def __init__(self, target):
        self._target_stack = [target]

    @property
    def target(self):
        """Shortcut to get the active target"""
        return self._target_stack[-1]

    def push(self, target):
        """Set focus on a new target"""
        self._target_stack.append(target)
        return target

    def pop(self):
        """Navigate one target back up the stack."""
        return self._target_stack.pop()
