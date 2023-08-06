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



class Actor(object):
    """Generic class for an actor that moves in an animation."""

    def __init__(
            self,
            x: float,
            y: float,
            size: float,
            animation: 'topdown._animator.Animation',
            visible: bool = True,
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
        """
        self._x = x
        self._y = y
        self._size = size
        self._visible = visible
        self._animation = animation

        tick_count = self._animation.tick_count
        self._position_history = {0: {'x': x, 'y': y, 'tick': 0}}
        self._position_history[tick_count] = {
            'x': x, 'y': y, 'tick': tick_count
        }
        self._visibility_history = {0: {'visible': False, 'tick': 0}}
        self._visibility_history[tick_count] = {
            'visible': True, 'tick': tick_count
        }

    def move_to(
            self,
            x: float,
            y: float,
            allow_overwrite: bool = False
    ):
        """
        Move to the specified x, y coordinates.

        :param x:
            The x position to go to.
        :param y:
            The y position to go to.
        :param allow_overwrite:
            Allow the existing move for the tick to be overwritten.
        """
        tick = self._animation.tick_count
        if not allow_overwrite and tick in self._position_history:
            raise RuntimeError('Move already occurred this frame.')
        self._position_history[tick - 1] = {
            'x': self._x, 'y': self._y, 'tick': tick - 1
        }
        self._position_history[tick] = {'x': x, 'y': y, 'tick': tick}
        self._x = x
        self._y = y

    def show(self, allow_overwrite: bool = False):
        """
        Show the actor on the animation.

        :param allow_overwrite:
            Allow the existing visibility for the tick to be overwritten.
        """
        self._set_visibility(True, allow_overwrite)

    def hide(self, allow_overwrite: bool = False):
        """
        Hide the actor on the animation.

        :param allow_overwrite:
            Allow the existing visibility for the tick to be overwritten.
        """
        self._set_visibility(False, allow_overwrite)


    def _set_visibility(self, is_visible: bool, allow_overwrite: bool):
        """
        Set the visibility of the actor.

        :param is_visible:
            Whether the actor should be visible.
        :param allow_overwrite:
            Allow the existing visibility for the tick to be overwritten.
        """
        tick = self._animation.tick_count
        if not allow_overwrite and tick in self._visibility_history:
            raise RuntimeError('Visibility already set this frame.')
        self._visibility_history[tick - 1] = {
            'visible': self._visible, 'tick': tick - 1
        }
        self._visibility_history[tick] = {'visible': is_visible, 'tick': tick}
        self._visible = is_visible


class Circle(Actor):
    """A circular actor to be animated."""

    def __init__(
            self,
            x: float,
            y: float,
            size: float,
            animation: 'topdown._animator.Animation',
            visible: bool = True,
    ):
        """
        Initialize the state of the circle.

        :param x:
            The starting x position of the circle.
        :param y:
            The starting y position of the circle.
        :param size:
            The initial size of the circle.
        :param visible:
            Whether the token should start out as visible.
        """
        super().__init__(x, y, size, animation, visible)


    def element(self) -> ElementTree.Element:
        """The visual svg element as an XML element object."""
        start_pos = self._position_history[0]
        return ElementTree.Element(
            'circle',
            attrib={
                'r': str(self._size / 2),
                'cx': str(start_pos['x']),
                'cy': str(start_pos['y']),
            }
        )

    def render_xml(self) -> ElementTree.Element:
        """Render the animation as an xml tree."""
        max_tick = self._animation.tick_count
        max_time = self._animation.tick_length * max_tick
        base_element = self.element()
        base_attrs = {
            'dur': f'{max_time}s',
            'repeatCount': 'indefinite',
        }

        vis_frames = [
            {
                'tick': f['tick'],
                'radius': str(self._size / 2) if f['visible'] else '0'
            }
            for f in self._visibility_history.values()
        ]
        to_animate = [
            ('r', 'radius', vis_frames),
            ('cx', 'x', self._position_history.values()),
            ('cy', 'y', self._position_history.values()),
        ]
        for svg_attr, key, frames in to_animate:
            attributes = _get_keyframe_strings(frames, key, max_tick)
            attributes['attributeName'] = svg_attr
            attributes.update(base_attrs)
            ElementTree.SubElement(base_element, 'animate', attrib=attributes)
        return base_element
