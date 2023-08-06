from abc import ABC, abstractmethod
from oubliette.core.intents import Intent
from oubliette.exceptions import EmptyCommandException


class BasePrompt(ABC):
    """Prompts define how users interact with the game and generate actions

    ps1 defines the look of the prompt.
    """

    ps1 = ""
    aliases = {"exit": "quit"}

    @staticmethod
    @abstractmethod
    def sanitize(command):
        """Clean the input.

        Could be security/UI/etc... related.

        Args:
            command (str): Input from the target.

        Returns:
            str: The sanitazed input.
        """
        pass

    @staticmethod
    @abstractmethod
    def parse(command, source, context):
        """Convert the input command into an intent.

        Args:
            command (str): The command to be processed.
            source (object): The object that issued the command.
            context (Context): The game context the command was issued in.

        Returns:
            Intent: The command as an intent.
        """
        pass

    @classmethod
    @abstractmethod
    def render_prompt(cls, *args, **kwargs):
        """Generate the prompt text that requests input.

        Returns:
            str: The prompt text.
        """
        pass

    @classmethod
    @abstractmethod
    def prompt(cls, target, context):
        """Get command from target, convert to intent, and have said target execute it.

        Args:
            target (Commandable): The target to prompt.
            context (Context): The current game context.
        """
        pass


class Prompt(BasePrompt):
    """Simple prompt"""

    ps1 = "--> "
    aliases = {"exit": "quit"}
    go_aliases = {"north": "go north",
                  "n": "go north",
                  "south": "go south",
                  "s": "go south",
                  "east": "go east",
                  "e": "go east",
                  "west": "go west",
                  "w": "go west",
                  "northeast": "go northeast",
                  "ne": "go northeast",
                  "northwest": "go northwest",
                  "nw": "go northwest",
                  "southwest": "go southwest",
                  "sw": "go southwest",
                  "southeast": "go southeast",
                  "se": "go southeast",
                  "up": "go up",
                  "u": "go up",
                  "down": "go down",
                  "d": "go down"}

    stop_words = ["a", "about", "above", "after", "again", "against", "all",
                  "am", "an", "and", "any", "are", "as", "at", "be",
                  "because", "been", "before", "being", "below", "between",
                  "both", "but", "by", "can", "did", "do", "does", "doing",
                  "down", "during", "each", "few", "for", "from", "further",
                  "had", "has", "have", "having", "he", "her", "here", "hers",
                  "herself", "him", "himself", "his", "how", "if", "in", "into",
                  "is", "it", "its", "itself", "just", "me", "more", "most",
                  "my", "myself", "not", "now", "of", "off", "on",
                  "once", "only", "or", "other", "our", "ours", "ourselves", "out",
                  "over", "own", "same", "she", "should", "so", "some", "such",
                  "t", "than", "that", "the", "their", "theirs", "them", "themselves",
                  "then", "there", "these", "they", "this", "those", "through", "to",
                  "too", "under", "until", "up", "very", "was", "we", "were",
                  "what", "when", "where", "which", "while", "who", "whom", "why",
                  "will", "with", "you", "your", "yours", "yourself", "yourselves"]

    @classmethod
    def resolve_aliases(cls, command):
        """Search any available alias and translate"""
        aliases = [cls.aliases,
                   cls.go_aliases]
        for alias_group in aliases:
            if command in alias_group:
                return alias_group[command]
        return command

    @classmethod
    def sanitize(cls, command):
        """Clean the input.

        Could be security/UI/etc... related.

        Args:
            command (str): Input from the target.

        Returns:
            str: The sanitazed input.
        """
        command = command.strip().split()
        for word in cls.stop_words:
            command = list(filter(lambda x: x != word, command))
        return ' '.join(command)

    @staticmethod
    def parse(command, source, context):
        """Convert a plain text line into an intent.

        Args:
            command (str): The command to be processed.
            source (object): The object that issued the command.
            context (Context): The game context the command was issued in.

        Returns:
            Intent: The command as an intent.
        """
        return Intent.from_command(command, source, context)

    @classmethod
    def render_prompt(cls, *args, **kwargs):
        """Present a prompt to the user

        Returns:
            str: The users request string
        """
        return input(cls.ps1)

    @classmethod
    def prompt(cls, target, context):
        """Get command from target, convert to intent.

        Args:
            target (Commandable): The target to prompt.
            context (Context): The current game context.

        Returns:
            Intent: The intent created from the users input
        """
        ps1 = cls.render_prompt(target=target, context=context)
        command = cls.sanitize(input(ps1))
        command = cls.resolve_aliases(command)
        if not command:
            raise EmptyCommandException()
        return cls.parse(command, target, context)

    @classmethod
    def pre_prompt(cls, target, context):
        """Run immediately before prompting.

        Args:
            target (Commandable): The target to prompt.
            context (Context): The current game context.
        """
        print("")  # Print a blank line

    @classmethod
    def post_prompt(cls, target, context):
        """Run immediately after prompting.

        Args:
            target (Commandable): The target to prompt.
            context (Context): The current game context.
        """
        print("")  # Print a blank line

    @classmethod
    def render_text(cls, text):
        """Ask the prompt to display something.

        Args:
            text str: message to display.
        """
        print(f" {text}")


class ContextPrompt(Prompt):
    """Include the current targets name in the prompt."""

    @classmethod
    def pre_prompt(cls, target, context):
        print("")
        print("----------------------------------------------------------------")

    @classmethod
    def render_prompt(cls, *args, **kwargs):
        focus = ""
        target = kwargs.get("target")
        if target:
            try:
                focus = getattr(target, "name")
            except AttributeError:
                try:
                    focus = kwargs.get("target").__class__.__name__
                except Exception:
                    focus = ""
        try:
            area = kwargs['context'].area.name
        except Exception:
            area = ""
        context_list = [focus, area]
        context = " | ".join([part for part in context_list if part])
        return f"{context}{cls.ps1}"
