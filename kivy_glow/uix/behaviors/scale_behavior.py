__all__ = ('ScaleBehavior', )

from kivy.lang import Builder
from kivy.properties import (
    NumericProperty,
    ListProperty,
)


Builder.load_string(
    '''
<ScaleBehavior>
    canvas.before:
        PushMatrix
        Scale:
            x: self.scale_x
            y: self.scale_y
            z: self.scale_z
            origin: self.origin if self.origin else self.center
    canvas.after:
        PopMatrix
'''
)


class ScaleBehavior:
    '''
    Scale behavior class.
    '''

    scale_x = NumericProperty(1)
    '''Property for getting/setting the X-axis scale.

    :attr:`scale_x` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `1`.
    '''
    scale_y = NumericProperty(1)
    '''Property for getting/setting the Y-axis scale.

    :attr:`scale_y` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `1`.
    '''
    scale_z = NumericProperty(1)
    '''Property for getting/setting the Z-axis scale.

    :attr:`scale_z` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `1`.
    '''

    origin = ListProperty(None, allownone=True)
    '''Property for getting/setting the origin of the scaling.

    :attr:`origin` is an :class:`~kivy.properties.ListProperty`
    and defaults to `None`.
    '''
