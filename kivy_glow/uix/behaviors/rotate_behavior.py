__all__ = ('RotateBehavior', )

from kivy.lang import Builder
from kivy.properties import (
    NumericProperty,
    ListProperty,
)


Builder.load_string(
    '''
<RotateBehavior>
    canvas.before:
        PushMatrix
        Rotate:
            angle: self.rotate_angle
            axis: tuple(self.rotate_axis)
            origin: self.origin if self.origin else self.center
    canvas.after:
        PopMatrix
'''
)


class RotateBehavior:
    '''
    Rotate behavior class.
    '''

    rotate_angle = NumericProperty(0)
    '''Property for getting/setting the angle of the rotation.

    :attr:`rotate_angle` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `0`.
    '''

    rotate_axis = ListProperty((0, 0, 1))
    '''Property for getting/setting the axis of the rotation.

    :attr:`rotate_axis` is an :class:`~kivy.properties.ListProperty`
    and defaults to `(0, 0, 1)`.
    '''

    origin = ListProperty(None, allownone=True)
    '''Property for getting/setting the origin of the rotation.

    :attr:`origin` is an :class:`~kivy.properties.ListProperty`
    and defaults to `None`.
    '''
