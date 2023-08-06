from uuid import uuid4
from oubliette.attributes import Navigable, Activatable, Observable
from oubliette import materials
from oubliette.exceptions import PortalDenial
from oubliette.core.events import Events


class Junction(Navigable, Observable, Activatable):
    """Used to connect two locations"""

    def __init__(self, area_1, direction_1, area_2, direction_2, portal, events=Events()):
        self.id_ = uuid4()
        self.area_1 = area_1
        self.area_2 = area_2
        self.portal = portal
        self.events = events
        self.link(area_1, direction_1, area_2, direction_2)

    def __repr__(self):
        return f"{self.area_1.name} <--> {self.area_2.name}"

    def link(self, area_1, direction_1, area_2, direction_2):
        """Join two areas with this junction.

        Inform both areas they have been joined by this junction.

        Args:
            area_1 (Area): Node at first end of edge.
            direction_1 (Direction): Title of the direction this junction represents for area_1
            area_2 (Area): Node at other end of edge.
            direction_2 (Direction): Title of the direction this junction represents for area_2
        """
        area_1 = area_1 or self.area_1
        area_2 = area_2 or self.area_2
        area_1.add_junction(self, direction_1)
        area_2.add_junction(self, direction_2)

    def unlink(self, dont_notify=None):
        """Detach this junction from one or both nodes.

        Args:
            dont_notify: list of nodes that don't need notification of this change (like the issuer).
        """
        dont_notify = dont_notify or []
        if self.area_1 not in dont_notify:
            self.area_1.remove_junctions([self])
        if self.area_2 not in dont_notify:
            self.area_2.remove_junctions([self])

    @staticmethod
    def render_description(this, intent):
        """Get a custom description of this junction.

        This depends on the portal this junction represents.
        An Opaque portal will only allow a user to see the portal, whereas a transparent portal will
        allow a user to see the rendered description of the node on the other side od this juction.

        Args:
            this (Junction): the juction being described.
            intent (Intent): Intent object with exrta info.

        Returns:
            str: The description.
        """
        if this.portal.material.opacity is materials.properties.Transparent:
            other = this.get_other(intent.context.area)
            return other.render_description(other, intent)
        else:
            return this.portal.render_description(this.portal, intent)

    @staticmethod
    def on_look(this, intent):
        intent.context.interface.prompt.render_text(this.render_description(this, intent))

    @staticmethod
    def render_enter(this, intent):
        pass

    @staticmethod
    def on_activate(this, intent):
        this.portal.on_activate(this.portal, intent)

    @staticmethod
    def on_enter(this, intent):
        """What happens when you enter a junction.

        Try to activate the portal. this might trigger a lock or a trap.
        If successful, fire this junctions on_exit.
        """
        prev_junction = intent.context.junction
        try:
            intent.context.junction = this
            this.portal.on_activate(this.portal, intent)
        except PortalDenial as denial:
            # intent.context.interface.prompt.render_text(denial)
            intent.context.junction = prev_junction
            raise denial
        else:
            this.render_enter(this, intent)
            intent.context.area.render_exit_text(intent.context.area, intent)
            this.on_exit(this, intent)

    @staticmethod
    def on_exit(this, intent):
        prev_area = intent.context.area
        prev_area._teardown(prev_area, intent)
        new_area = this.get_other(prev_area)
        new_area.on_enter(new_area, intent)
        intent.context.junction = None

    def get_other(self, area):
        """Get the area opposite the one provided.

        Args:
            area (Area): The area to get the get the opposite of.

        Returns:
            Area: The area at the other end of the junction from the area given.
        """
        if area == self.area_1:
            return self.area_2
        return self.area_1

    def tick(self, global_count, session):
        self.events.tick(global_count, session)
        self.portal.tick(global_count, session)


class DoorJunction(Junction):

    @staticmethod
    def render_enter(this, intent):
        intent.context.interface.prompt.render_text(f"You reach for the {this.portal.material.name} {this.portal.name}")
