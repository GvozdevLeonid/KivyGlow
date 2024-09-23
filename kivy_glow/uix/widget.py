__all__ = ('GlowWidget', )

from kivy.uix.widget import Widget
from kivy_glow.uix.behaviors import (
    DeclarativeBehavior,
    AdaptiveBehavior,
    StyleBehavior,
    ThemeBehavior,
)
from kivy.properties import (
    ReferenceListProperty,
    NumericProperty,
)


class GlowWidget(DeclarativeBehavior,
                 AdaptiveBehavior,
                 ThemeBehavior,
                 StyleBehavior,
                 Widget,
                 ):

    minimum_width = NumericProperty(0)
    '''Automatically computed minimum width needed to contain all children.

    :attr:`minimum_width` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 0. It is read only.
    '''

    minimum_height = NumericProperty(0)
    '''Automatically computed minimum height needed to contain all children.

    :attr:`minimum_height` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 0. It is read only.
    '''

    minimum_size = ReferenceListProperty(minimum_width, minimum_height)
    '''Automatically computed minimum size needed to contain all children.

    :attr:`minimum_size` is a
    :class:`~kivy.properties.ReferenceListProperty` of
    (:attr:`minimum_width`, :attr:`minimum_height`) properties. It is read
    only.
    '''
