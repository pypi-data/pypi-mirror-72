from oubliette.exceptions import (IntentException, IntentTargetResolutionException,
                                  IntentValidationException)

from oubliette import alises


class UnsetTarget:
    """Used to help an target decide if it needs to execute it's mro"""
    pass


class Target:
    """Represent an object and provide tools to discover them"""

    def __init__(self, target, default_obj, context, *args, target_mro=None, **kwargs):
        """
        The mro (method resolution order) is a list that specifies the order to execute target look-up methods.
        The default is to:
        1. search using the default_obj objects custom resolver
        2. check if the target is an attribute on the default_obj
        3. search using the current interface targets custom resolver
        4. check if the target is an attribute on the current interface target
        5. check area
        6. check global objects

        The order of these can be changed on Target creation by providing a custom mro list.

        Remember that everything in python is an object, so can be stored and passed around.
        You'll notice that mro_funcs has functions as values. Storing them this way allows us to
        get a handle to the functions by dictionary look up, or swap out what function is attached
        to a key. The function object is returned when its key is accessed from the dictionary,
        so they can be called easily like this:
        ```
        def func():
            print("hi")

        d = {"key": func}
        d["key"]()
        hi
        ```
        Notice when the function is stored, the name is used without calling it with ().

        Args:
            target (str): name of the object to look up.
            default_obj (obj): The default object to begin searching for the target in.
            context (Context): The game context in which this action was invoked.
            target_mro (list): Custom method resolution order for resolving the target object.
        """
        self.mro = target_mro or ["custom",
                                  "default_obj",
                                  "context_target_resolver",
                                  "context_target",
                                  "area",
                                  "global"]
        self.mro_funcs = {"custom": self._resolve_object_from_default_obj_resolver,
                          "default_obj": self._resolve_object_from_default_obj,
                          "context_target_resolver": self._resolve_object_from_context_targets_resolver,
                          "context_target": self._resolve_object_from_context_target,
                          "area": self._resolve_object_from_area,
                          "global": self._resolve_object_from_global_objects}
        self._cached_target = UnsetTarget
        self._owner = None
        self._target = target or ""
        self.context = context
        self.default_obj = default_obj

    def __repr__(self):
        return repr(self.target)

    def resolve_target(self):
        """Execute the object method resolution order (mro).

        Target objects need to be located and loaded.
        This method executes all the object locator methods in the order specified by self.mro.

        Returns:
            object: The resolved object

        Raises:
            IntentTargetResolutionException
        """
        if not self._target:
            return self.default_obj
        self._target = alises.lookup(self._target, self._target)
        for scope in self.mro:
            try:
                obj, self._owner = self.mro_funcs[scope](self.context)
                return obj
            except IntentTargetResolutionException:
                pass
        raise IntentTargetResolutionException(f"Couldn't locate {self._target}")

    @property
    def target(self):
        """The target object.

        Technique: Memoization

        This method uses a technique called memoization to avoid repeated, expensive, calculation.
        If the property _memoized_target is set to UnsetTarget, we run resolve_target to get the
        target, store it in _memoized_target, and return it.
        Subsequent access of `target` will have the _memoized_target already and will simply return it.

        Returns:
            object: The targeted object.
        """
        if self._cached_target is UnsetTarget:
            self._cached_target = self.resolve_target()
        return self._cached_target

    @target.setter
    def target(self, val):
        self._cached_target = val

    @property
    def owner(self):
        """Where was the target found?"""
        if not self._owner:
            self.resolve_target()
        return self._owner

    def _resolve_object_from_default_obj_resolver(self, context):
        """Use default_obj objects custom resolve function.

        Returns:
            object: The resolved object

        Raises:
            IntentTargetResolutionException
        """
        try:
            return self.default_obj.resolve_target(self._target, context)
        except AttributeError:
            raise IntentTargetResolutionException(f"Targets default object:{self.default_obj} has no target resolver, or generated error")

    def _resolve_object_from_default_obj(self, context):
        """Look for target in attributes of the targets default_obj.

        Returns:
            object: The resolved object

        Raises:
            IntentTargetResolutionException
        """
        try:
            target = getattr(self.default_obj, self._target)
            return target, self.default_obj
        except AttributeError:
            raise IntentTargetResolutionException(f"Targets default object:{self.default_obj} has no attribute {self._target}")

    def _resolve_object_from_context_targets_resolver(self, context):
        """Convert an target name into a class or instance from an attribute using the current interface targets resolver.

        Uses current interface targets object resolver function to locate the target object.

        Returns:
            object: The resolved object

        Raises:
            IntentTargetResolutionException
        """
        try:
            return self.context.interface.target.resolve_target(self._target, context)
        except AttributeError:
            raise IntentTargetResolutionException(f"Couldn't locate {self._target}")

    def _resolve_object_from_context_target(self, context):
        """Convert an target name into a class or instance from an attribute from the current interface target.

        Searches the current interface target for an attribute called {self._target} and returns it.

        Returns:
            object: The resolved object

        Raises:
            IntentTargetResolutionException
        """
        try:
            target = getattr(self.context.interface.target, self._target)
            return target, self.context.interface.target
        except AttributeError:
            raise IntentTargetResolutionException(f"Couldn't locate {self._target}")

    def _resolve_object_from_area(self, context):
        """Search the area for junctions.

        Returns:
            object: The resolved object

        Raises:
            IntentTargetResolutionException
        """
        return self.context.area.resolve_target(self._target, context)

    def _resolve_object_from_global_objects(self, context):
        """Convert an intent target into an actual class or instance.

        Searches objects global to the default_obj of the target to find one with the provided target name.

        Returns:
            object: The resolved object

        Raises:
            IntentTargetResolutionException
        """
        try:
            target = self.context.global_objects[self._target]
            return target, self.context.global_objects
        except KeyError:
            raise IntentTargetResolutionException(f"Couldn't locate {self._target} in global context objects")

    @classmethod
    def build_targets(cls, target_names, source, context, target_mro=None):
        targets = []
        full_name = ""
        for name in target_names:
            if full_name:
                name = " ".join([name, full_name])
            try:
                target = Target(name, source, context, target_mro=target_mro)
                target.target
                targets.insert(0, target)
                full_name = ""
            except IntentTargetResolutionException:
                full_name = name
        if full_name:  # Unfinished target lookup
            raise IntentTargetResolutionException(f"{full_name} not found")
        if not targets:
            raise IntentTargetResolutionException("No targets in command")
        return targets


class Intent():
    """An Intent to be executed.

    An Intent is a pairing of an Action and a target along with game context,
    to be performed by a Commandable entity.
    Intents provide helper functions to identify the object specified as the target.
    """

    def __init__(self, action, *args,
                 source=None, targets=None, context=None,
                 target_mro=None, meta=None, build_targets=True,
                 **kwargs):
        """
        Args:
            action (str): The action to execute.
            source (Commandable): The object that issued the Intent
            targets (list): names of the reaction objects to receive the Intent.
            context (Context): The game context in which this action was invoked.
            target_mro (list): Custom method resolution order for resolving the target object.
            meta (Intent): Another intent involved this one in some capacity.
        """
        self.action = action
        self.source = source
        self.context = context
        if build_targets:
            self.targets = Target.build_targets(targets or [""], source,
                                                context, target_mro=target_mro)
        else:
            targets = targets or [""]
            if not isinstance(targets, list):
                targets = [targets]
            self.targets = targets
        self.meta = meta
        # for target_name in targets:
        #     if isinstance(target_name, Target):
        #         continue
        #     self.targets.append(Target(target_name, source, context, target_mro=target_mro))

    @classmethod
    def from_command(cls, command, source, context, **kwargs):
        """Convert a plain text line into an intent.

        Args:
            command (str): The command to be processed.
            source (object): The object that issued the command.
            context (Context): The game context the command was issued in.

        Returns:
            Intent: The command as an intent.
        """
        action, *intent_targets = command.split()
        if not intent_targets:
            intent_targets = []
        intent_targets.reverse()
        return cls(action, source=source, targets=intent_targets, context=context, **kwargs)

    @property
    def target(self):
        return self.get_target().target

    @property
    def args(self):
        return self.targets[2:]

    def get_target(self, index=0, default=None):
        try:
            return self.targets[index]
        except IndexError:
            return default
