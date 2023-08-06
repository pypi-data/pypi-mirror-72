import typing
from xml.etree import ElementTree

from topdown import _actomizer


class Animation(object):

    def __init__(
            self,
            x_max: int,
            y_max: int,
            x_min: int = 0,
            y_min: int = 0,
            tick_length: float = 1
    ):
        """
        An entity containing the motion of all actors within the animation.

        :param x_max:
            The maximum x-value on the canvas.
        :param y_max:
            The maximum y-value on the canvas.
        :param x_min:
            The minimum x-value on the canvas.
        :param y_min:
            The minimum y-value on the canvas.
        :param tick_length:
            The number of seconds each tick corresponds to.
        """
        self.x_max = x_max
        self.x_min = x_min
        self.y_max = y_max
        self.y_min = y_min
        self.tick_length = tick_length
        self.tick_count = 0

        self._actors = []

    def add(
            self,
            actor_cls: typing.Type[_actomizer.Actor],
            x: int,
            y: int,
            size: int = 10,
            visible: bool = True,
            **kwargs,
    ) -> _actomizer.Actor:
        """
        Add an actor to the given location in the animation.

        :param actor_cls:
            The class of the actor to create.
        :param x:
            The x position the actor should start at.
        :param y:
            The y position the actor should start at.
        :param size:
            The size of the actor.
        :param visible:
            Whether the actor should start out as visible.
        :param kwargs:
            Any arguments specific to the given actor_cls.
        """
        actor = actor_cls(
            x=x,
            y=y,
            size=size,
            visible=visible,
            animation=self,
            **kwargs)
        self._actors.append(actor)
        return actor

    def render_xml(self) -> ElementTree.Element:
        """Render the animation as an xml tree."""
        attributes = {
            'viewBox': f'{self.x_min} {self.y_min} {self.x_max} {self.y_max}',
            'xmlns': 'http://www.w3.org/2000/svg'
        }
        element = ElementTree.Element('svg', attrib=attributes)
        element.extend([actor.render_xml() for actor in self._actors])
        return element

    def render_to(self, filepath: str):
        xml = self.render_xml()
        with open(filepath, 'w') as f:
            f.write(ElementTree.tostring(xml).decode())

    def tick(self) -> int:
        """Tick to the next frame of the animation."""
        self.tick_count += 1
        return self.tick_count
