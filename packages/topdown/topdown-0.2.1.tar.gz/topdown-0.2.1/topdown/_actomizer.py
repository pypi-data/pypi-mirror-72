import typing

from xml.etree import ElementTree


def _to_svg_time(tick: int, max_tick: int) -> str:
    """Convert a tick time to an svg time."""
    places = len(str(max_tick)) + 1
    value = '{:.{places}f}'.format(tick / max_tick, places=places)
    return value.rstrip('0').rstrip('.')


def _get_keyframe_strings(
        keyframes: list, value_key: str, max_tick: int
) -> dict:
    """
    Get the keyframe times and value strings to use within an svg animation.

    :param keyframes:
        A list of dictionaries with each dictionary containing a 'tick' key
        and the value_key.
    :param value_key:
        The key in the keyframes dictionary to use for the animated value.
    :param max_tick:
        The last tick of the animation.
    :return:
        A dictionary containing `values` and `keyTimes`.
    """
    frames = list(sorted(keyframes, key=lambda x: x['tick']))
    if frames[-1]['tick'] != max_tick:
        copied = frames[-1].copy()
        copied['tick'] = max_tick
        frames.append(copied)
    deduplicated = []
    for i, frame in enumerate(frames):
        is_needed = (
            (0 == i) or (i == len(frames) - 1)
            or (frames[i - 1][value_key] != frame[value_key])
            or (frames[i + 1][value_key] != frame[value_key])
        )
        if not is_needed:
            continue
        deduplicated.append({'tick': frame['tick'], 'value': frame[value_key]})
    return {
        'values': ';'.join(str(f['value']) for f in deduplicated),
        'keyTimes': ';'.join(
            _to_svg_time(f['tick'], max_tick) for f in deduplicated
        )
    }


def _animate_attribute(
        frames: list, svg_attr: str, max_tick: int, max_time: float
) -> ElementTree.Element:
    """
    Animate the specified attribute.

    :param frames:
        The frames of svg states to transition through.
    :param svg_attr:
        The attribute being animated.
    :param max_tick:
        The final tick in the animation.
    :param max_time:
        The total time of the animation.
    :return:
        The element containing the animation for the attribute.
    """
    tranform_attrs = {'rotate', 'scale', 'translate'}
    element_attrs = {
        'dur': f'{max_time}s',
        'repeatCount': 'indefinite',
        'attributeName': svg_attr,
        **_get_keyframe_strings(frames, svg_attr, max_tick)
    }
    if svg_attr in tranform_attrs:
        element_attrs['attributeName'] = 'transform'
        element_attrs['type'] = svg_attr
        element_attrs['additive'] = 'sum'

    element_type = (
        'animateTransform'
        if svg_attr in tranform_attrs
        else 'animate'
    )
    return ElementTree.Element(element_type, attrib=element_attrs)


class Actor(object):
    """Generic class for an actor that moves in an animation."""

    def __init__(
            self,
            x: float,
            y: float,
            size: float,
            animation: 'topdown._animator.Animation',
            visible: bool = True,
            color: str = 'black',
            rotation: float = 0
    ):
        """
        Initialize the state of the actor.

        :param x:
            The starting x position of the center of the actor.
        :param y:
            The starting y position of the center of the actor.
        :param size:
            The initial size of the actor.
        :param visible:
            Whether the token should start out as visible.
        :param color:
            The color to fill the actor with.
        :param rotation:
            The number of degrees to turn the actor clockwise.
        """
        self._x = x
        self._y = y
        self._size = size
        self._color = color
        self._rotation = rotation
        self._animation = animation
        self._change_history = {}

        self._visible = False
        self._save_state(tick=0)
        self._visible = visible
        self._save_state()

    def _save_state(self, tick: int = None):
        """
        Save the current state in the change history.

        :param tick:
            The tick to associate with this state. If not given the
            current tick_count of the animation will be used.
        """
        tick_count = tick if tick is not None else self._animation.tick_count
        self._change_history[tick_count] = {
            'tick': tick_count,
            'x': self._x, 'y': self._y,
            'size': self._size,
            'visible': self._visible,
            'color': self._color,
            'rotation': self._rotation,
        }

    def move_to(
            self,
            x: float,
            y: float,
    ):
        """
        Move to the specified x, y coordinates.

        :param x:
            The x position to go to.
        :param y:
            The y position to go to.
        """
        self._x = x
        self._y = y
        self._save_state()

    def rotate_to(self, degrees: float):
        """Rotate the agent to the specified degree rotation."""
        self._rotation = degrees
        self._save_state()

    def set_color(self, color: str):
        """Set the color of the actor to the given color."""
        self._color = color
        self._save_state()

    def show(self):
        """Show the actor on the animation."""
        self._visible = True
        self._save_state()

    def hide(self):
        """Hide the actor on the animation."""
        self._visible = False
        self._save_state()

    def render_xml(self) -> ElementTree.Element:
        """Render the animation as an xml tree."""
        max_tick = self._animation.tick_count
        max_time = self._animation.tick_length * max_tick
        base_element = self._element()

        frames = [
            self._state_to_svg_attrs(state) for state in self._history.values()
        ]
        for svg_attr in frames[0].keys():
            if svg_attr == 'tick':
                continue
            animated = _animate_attribute(frames, svg_attr, max_tick, max_time)
            base_element.extend([animated])
        return base_element


    @property
    def _history(self) -> dict:
        """
        Convert the change history to a history of states, bookending every
        transition with a copy of the original state.
        """
        changes = list(sorted(
            self._change_history.values(),
            key=lambda x: x['tick']
        ))
        result = {}
        for i, change in enumerate(changes):
            tick = change['tick']
            if i != 0:
                previous = changes[i - 1].copy()
                previous['tick'] = tick - 1
                result[tick - 1] = previous
            result[tick] = change.copy()
        return result

    @classmethod
    def _state_to_svg_attrs(cls, state: dict) -> dict:
        """Convert a state to the svg representation of the state."""
        raise NotImplementedError('_state_to_svg_attrs must be implemented')

    def _element(self) -> ElementTree.Element:
        """The visual svg element as an XML element object."""
        raise NotImplementedError('_element must be implemented')


class Circle(Actor):
    """A circular actor to be animated."""

    def _element(self) -> ElementTree.Element:
        """The visual svg element as an XML element object."""
        state = self._history[0]
        return ElementTree.Element(
            'circle',
            attrib={
                'r': str(self._size / 2),
                'cx': '0',
                'cy': '0',
                'fill': state['color'],
            }
        )

    @classmethod
    def _state_to_svg_attrs(cls, state: dict) -> dict:
        """Convert a state to the svg representation of the state."""
        size = state['size'] if state['visible'] else 0
        return {
            'tick': state['tick'],
            'cx': '0',
            'cy': '0',
            'r': str(size / 2),
            'fill': state['color'],
            'translate': f'{state["x"]} {state["y"]}',
            'rotate': f'{state["rotation"]} 0 0',
        }


class Square(Actor):
    """A square actor to be animated."""

    def _element(self) -> ElementTree.Element:
        """The visual svg element as an XML element object."""
        state = self._history[0]
        x = state['x'] - state['size'] / 2
        y = state['y'] - state['size'] / 2
        return ElementTree.Element(
            'rect',
            attrib={
                'width': str(state['size']),
                'height': str(state['size']),
                'x': '0',
                'y': '0',
                'fill': state['color'],
            }
        )

    @classmethod
    def _state_to_svg_attrs(cls, state: dict) -> dict:
        """Convert a state to the svg representation of the state."""
        size = state['size'] if state['visible'] else 0

        return {
            'tick': state['tick'],
            'x': '0',
            'y': '0',
            'width': str(size),
            'height': str(size),
            'fill': state['color'],
            'translate': f'{state["x"] - size / 2} {state["y"] - size / 2}',
            'rotate': f'{state["rotation"]} 0 0',
        }


class Triangle(Actor):
    """A triangle actor to be animated."""

    def _element(self) -> ElementTree.Element:
        """The visual svg element as an XML element object."""
        state = self._history[0]
        x = state['x']
        y = state['y']
        size = state['size'] if state['visible'] else 0
        return ElementTree.Element(
            'polygon',
            attrib={
                'points': '-0.5,-0.43 0.5,-0.43 0,0.43',
                'fill': state['color'],
            }
        )

    @classmethod
    def _state_to_svg_attrs(cls, state: dict) -> dict:
        """Convert a state to the svg representation of the state."""
        size = state['size'] if state['visible'] else 0
        return {
            'tick': state['tick'],
            'fill': state['color'],
            'translate': f'{state["x"]} {state["y"]}',
            'scale': str(size),
            'rotate': f'{state["rotation"]} 0 0',
        }
