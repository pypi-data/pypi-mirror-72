from itertools import chain
from collections import Counter
from oubliette import attributes
from oubliette.exceptions import IntentTargetResolutionException


class Inventory(Counter, attributes.Observable, attributes.Observer, attributes.Commandable, attributes.Contextable,
                attributes.Usable):
    """An inventory is used to hold items and perform operations on quantities.

    Patttern: Command

    Use the built-in `subtract` and `update` methods of the Counter for management.
    """

    def __repr__(self):
        string = ", ".join(f"{str(key)}: {val}" for key, val in self.items())
        return f"{{{string}}}"

    def resolve_target(self, target, context):
        """Custom intent target resolver that allows intents to look at inventory items.

        Args:
            target (string): The intent target to try to get from the inventory.

        Returns:
            Item: The inventory item that was found.

        Raises:
            IntentTargetResolutionException
        """
        for item in self.keys():
            if target == str(item):
                return item, self
        raise IntentTargetResolutionException("Item not in inventory")

    @staticmethod
    def on_use(this, intent):
        """Executed when used.

        If no target was provided, we're looking at the inventory itself, otherwise
        call our on_context method to set this as the interface target.
        """
        if intent.target is this:
            if intent.source is this:
                intent.context.interface.prompt.render_text(this)
            else:
                this.on_context(this, intent)
        else:
            intent.context.render_text(this)

    def tick(self, global_count, session):
        for item in self.keys():
            item.tick(global_count, session)

    @staticmethod
    def on_look(this, intent):
        intent.context.render_text(this)

    def __getitem__(self, key):
        """Deal with zero balances"""
        if self.__class__.__name__ == "Inventory":
            count = super().__getitem__(key)
            if count <= 0:
                del self[key]
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if self.__class__.__name__ == "Inventory":
            new_count = self[key]
            if new_count <= 0:
                del self[key]


class RestrictedInventory(Inventory):
    """
    http://code.activestate.com/recipes/578042-restricted-dictionary/

    Stores the properties of an object. It's a dictionary that's
    restricted to a tuple of allowed keys. Any attempt to set an invalid
    key raises an error.

    >>> p = RestrictedDict(('x','y'))
    >>> print p
    RestrictedDict(('x', 'y'), {})
    >>> p['x'] = 1
    >>> p['y'] = 'item'
    >>> print p
    RestrictedDict(('x', 'y'), {'y': 'item', 'x': 1})
    >>> p.update({'x': 2, 'y': 5})
    >>> print p
    RestrictedDict(('x', 'y'), {'y': 5, 'x': 2})
    >>> p['x']
    2
    >>> p['z'] = 0
    Traceback (most recent call last):
    ...
    KeyError: 'z is not allowed as key'
    >>> q = RestrictedDict(('x', 'y'), x=2, y=5)
    >>> p==q
    True
    >>> q = RestrictedDict(('x', 'y', 'z'), x=2, y=5)
    >>> p==q
    False
    >>> len(q)
    2
    >>> q.keys()
    ['y', 'x']
    >>> q._allowed_keys
    ('x', 'y', 'z')
    >>> p._allowed_keys = ('x', 'y', 'z')
    >>> p['z'] = 3
    >>> print p
    RestrictedDict(('x', 'y', 'z'), {'y': 5, 'x': 2, 'z': 3})

    """
    _allowed = None

    def __init__(self, *args, allowed_keys=None, seq=(), **kwargs):
        """
        Initializes the class instance. The allowed_keys tuple is
        required, and it cannot be changed later.
        If seq and/or kwargs are provided, the values are added (just
        like a normal dictionary).
        """
        allowed = self._allowed or allowed_keys
        if not allowed:
            raise ValueError("No restricted key set provided")
        self._allowed_keys = tuple(allowed)
        # normalize arguments to a (key, value) iterable
        if hasattr(seq, 'keys'):
            get = seq.__getitem__
            seq = ((k, get(k)) for k in seq.keys())
        if kwargs:
            seq = chain(seq, kwargs.items())
        # scan the items keeping track of the keys' order
        for key, val in seq:
            self.__setitem__(key, val)

    def __setitem__(self, key, value):
        """Checks if the key is allowed before setting the value"""
        if key in self._allowed_keys:
            super().__setitem__(key, value)
        else:
            raise KeyError("%s is not allowed as key" % key)

    def update(self, e=None, **kwargs):
        """
        Equivalent to dict.update(), but it was needed to call
        RestrictedDict.__setitem__() instead of dict.__setitem__
        """
        try:
            for k in e:
                self.__setitem__(k, e[k])
        except AttributeError:
            for (k, v) in e:
                self.__setitem__(k, v)
        for k in kwargs:
            self.__setitem__(k, kwargs[k])

    def __eq__(self, other):
        """
        Two RestrictedDicts are equal when their dictionaries and allowed keys
        are all equal.
        """
        if other is None:
            return False
        try:
            allowedcmp = (self._allowed_keys == other._allowed_keys)
            if allowedcmp:
                dictcmp = super().__eq__(other)
            else:
                return False
        except AttributeError:  # Other is not a RestrictedDict
            return False
        return bool(dictcmp)

    def __ne__(self, other):
        """x.__ne__(y) <==> not x.__eq__(y)"""
        return not self.__eq__(other)

    def __repr__(self):
        """Representation of the RestrictedDict"""
        return 'RestrictedDict(%s, %s)' % (self._allowed_keys.__repr__(),
                                           super().__repr__())
