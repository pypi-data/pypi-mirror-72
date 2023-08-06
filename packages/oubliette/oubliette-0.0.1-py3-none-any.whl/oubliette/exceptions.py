class CommandException(Exception):
    """Base for command related exceptions."""
    pass


class NotCommandable(CommandException):
    """Raised when a non-commandable object is the terminal target or issued a command."""
    pass


class InvalidCommand(CommandException):
    """An invalied command was attempted."""
    pass


class EmptyCommandException(CommandException):
    """Issued an empty command"""
    pass


class IntentException(Exception):
    """Base exception for Intents."""
    pass


class IntentValidationException(IntentException):
    """Invalid Intent"""
    pass


class IntentTargetResolutionException(IntentException):
    """Could not resolve the target object for an action."""
    pass


class ActionException(Exception):
    """Base exception for Actions"""
    pass


class PortalDenial(Exception):
    """Portal passage denied."""
    pass


class ExchangerException(Exception):
    """Issue using an exchanger."""
    pass


class CantAffordException(ExchangerException):
    """Cant afford an exchanger transaction"""
    pass


class MenuException(Exception):
    pass


class MenuExitedException(MenuException):
    """Player quit the menu without completeing selection."""
    pass


class EventDiscardException(Exception):
    """Signal to discard an event"""
    pass
