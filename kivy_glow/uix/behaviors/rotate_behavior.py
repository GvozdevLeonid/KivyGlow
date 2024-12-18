__all__ = ('RotateBehavior', )

from kivy.lang import Builder
from kivy.properties import (
    ListProperty,
    NumericProperty,
)

Builder.load_string(
    '''
<RotateBehavior>
    canvas.before:
        PushMatrix
        Rotate:
            origin: self.origin if self.origin else self.center
            axis: tuple(self.rotate_axis)
            angle: self.rotate_angle
    canvas.after:
        PopMatrix
''',
)


class RotateBehavior:
    '''
    Rotate behavior class.
    '''

    rotate_angle = NumericProperty(defaultvalue=0)
    '''Property for getting/setting the angle of the rotation.

    :attr:`rotate_angle` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `0`.
    '''

    rotate_axis = ListProperty(defaultvalue=[0, 0, 1])
    '''Property for getting/setting the axis of the rotation.

    :attr:`rotate_axis` is an :class:`~kivy.properties.ListProperty`
    and defaults to `(0, 0, 1)`.
    '''

    origin = ListProperty(defaultvalue=None, allownone=True)
    '''Property for getting/setting the origin of the rotation.

    :attr:`origin` is an :class:`~kivy.properties.ListProperty`
    and defaults to `None`.
    '''
