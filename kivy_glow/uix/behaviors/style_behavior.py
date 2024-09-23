__all__ = ('StyleBehavior', )

from kivy.lang import Builder
from typing import Self
from kivy.properties import (
    VariableListProperty,
    NumericProperty,
    StringProperty,
    OptionProperty,
    ColorProperty,
    ListProperty,
)


Builder.load_string(
    '''
<StyleBehavior>
    canvas.before:
        PushMatrix
        Rotate:
            angle: self.rotate_angle
            axis: tuple(self.rotate_axis)
            origin: self.background_origin if self.background_origin else self.center
        Color:
            rgba: self._shadow_color if self.shadow == 'outside' else (0, 0, 0, 0)
        BoxShadow:
            size: self.size
            pos: self.pos
            border_radius: self._border_radius
            offset: self.shadow_offset
            blur_radius: self.shadow_blur_radius
            spread_radius: self.shadow_spread_radius
    canvas:
        Color:
            rgba: self._bg_color
        SmoothRoundedRectangle:
            group: "bg_color_instruction"
            pos: self.pos
            size: self.size
            radius: self._border_radius if self._border_radius else (0, 0, 0, 0)
            source: self.background_image
        Color:
            rgba: self._border_color if self._border_width[0] >= 1 else (0, 0, 0, 0)
        SmoothLine:  # left
            cap: 'none'
            width: self._border_width[0]
            points: [ \
                self.x + self._border_width[0], \
                self.y + self._border_radius[3] + (1 if self._border_radius[3] < 1 else 0), \
                self.x + self._border_width[0], \
                self.top - self._border_radius[0] - (1 if self._border_radius[0] < 1 else 0) \
            ]
        Color:
            rgba: self._border_color if self._border_width[1] >= 1 else (0, 0, 0, 0)
        SmoothLine:  # top
            cap: 'none'
            width: self._border_width[1]
            points: [ \
                self.x + self._border_radius[0] + (1 if self._border_radius[0] < 1 else 0), \
                self.top - self._border_width[1], \
                self.right - self._border_radius[1] - (1 if self._border_radius[1] < 1 else 0), \
                self.top - self._border_width[1] \
            ]
        Color:
            rgba: self._border_color if self._border_width[2] >= 1 else (0, 0, 0, 0)
        SmoothLine:  # right
            cap: 'none'
            width: self._border_width[2]
            points: [ \
                self.right - self._border_width[2], \
                self.y + self._border_radius[2] + (1 if self._border_radius[2] < 1 else 0), \
                self.right - self._border_width[2], \
                self.top - self._border_radius[1] - (1 if self._border_radius[1] < 1 else 0) \
            ]
        Color:
            rgba: self._border_color if self._border_width[3] >= 1 else (0, 0, 0, 0)
        SmoothLine:  # bottom
            cap: 'none'
            width: self._border_width[3]
            points: [ \
                self.x + self._border_radius[3] + (1 if self._border_radius[3] < 1 else 0), \
                self.y + self._border_width[3], \
                self.right - self._border_radius[2] - (1 if self._border_radius[2] < 1 else 0), \
                self.y + self._border_width[3] \
            ]
        Color:
            rgba: self._border_color if self._border_radius[0] and self._border_width[1] >= 1 else (0, 0, 0, 0)
        SmoothLine:  # lt
            cap: 'none'
            width: self._border_width[1]
            ellipse: [ \
                self.x + self._border_width[0], \
                self.top - 2 * self._border_radius[0] + self._border_width[1], \
                2 * self._border_radius[0] - self._border_width[0] * 2, \
                2 * self._border_radius[0] - self._border_width[1] * 2, \
                270, \
                360 \
            ]
        Color:
            rgba: self._border_color if self._border_radius[1] and self._border_width[1] >= 1 else (0, 0, 0, 0)
        SmoothLine:  # rt
            cap: 'none'
            width: self._border_width[1]
            ellipse: [ \
                self.right - 2 * self._border_radius[1] + self._border_width[1], \
                self.top - 2 * self._border_radius[1] + self._border_width[1], \
                2 * self._border_radius[1] - self._border_width[1] * 2, \
                2 * self._border_radius[1] - self._border_width[1] * 2, \
                0, \
                90 \
            ]
        Color:
            rgba: self._border_color if self._border_radius[2] and self._border_width[3] >= 1 else (0, 0, 0, 0)
        SmoothLine:  # rb
            cap: 'none'
            width: self._border_width[3]
            ellipse: [ \
                self.right - 2 * self._border_radius[2] + self._border_width[3], \
                self.y + self._border_width[3], \
                2 * self._border_radius[2] - self._border_width[3] * 2, \
                2 * self._border_radius[2] - self._border_width[3] * 2, \
                90, \
                180 \
            ]
        Color:
            rgba: self._border_color if self._border_radius[3] and self._border_width[3] >= 1 else (0, 0, 0, 0)
        SmoothLine:  # lb
            cap: 'none'
            width: self._border_width[3]
            ellipse: [ \
                self.x + self._border_width[3], \
                self.y + self._border_width[3], \
                2 * self._border_radius[3] - self._border_width[3] * 2, \
                2 * self._border_radius[3] - self._border_width[3] * 2, \
                180, \
                270 \
            ]
    canvas.after:
        Color:
            rgba: self._shadow_color if self.shadow == 'inside' else (0, 0, 0, 0)
        BoxShadow:
            size: self.size
            pos: self.pos
            inset: True
            border_radius: self._border_radius
            offset: self.shadow_offset
            blur_radius: self.shadow_blur_radius
            spread_radius: self.shadow_spread_radius
        PopMatrix
    ''',
    filename='StyleBehavior.kv'
)


class StyleBehavior:
    '''
    Style behavior class.

    For more information, see in the :class:`~kivy_glow.uix.behaviors.StyleBehavior`
    '''

    background_image = StringProperty(None, allownone=True)
    '''Widget background image

    :attr:`background_image` is an :class:`~kivy.properties.StringProperty`
    and defaults to `None`.
    '''

    bg_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the background

    :attr:`bg_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    border_radius = VariableListProperty([0], length=4)
    '''Canvas radius.

    :attr:`border_radius` is an :class:`~kivy.properties.VariableListProperty`
    and defaults to `[0, 0, 0, 0]`.
    '''

    border_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the border

    :attr:`border_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    border_width = VariableListProperty([0], length=4)
    '''Border width.

    :attr:`border_width` is an :class:`~kivy.properties.VariableListProperty`
    and defaults to `[0, 0, 0, 0]`.
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

    background_origin = ListProperty(None, allownone=True)
    '''Property for getting/setting the origin of the widget.

    :attr:`background_origin` is an :class:`~kivy.properties.ListProperty`
    and defaults to `None`.
    '''

    shadow = OptionProperty('off', options=('off', 'outside', 'inside'))
    '''Shadow option (off, outside, inside)

    :attr:`shadow` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `off`.
    '''

    shadow_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the shadow

    :attr:`shadow_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    shadow_offset = VariableListProperty([0], length=2)
    '''Specifies shadow offsets in (horizontal, vertical) format.
    Positive values for the offset indicate that the shadow should move to the right and/or top.
    The negative ones indicate that the shadow should move to the left and/or down.


    :attr:`shadow_offset` is an :class:`~kivy.properties.VariableListProperty`
    and defaults to `[0, 0]`.
    '''

    shadow_blur_radius = NumericProperty(15)
    '''Define the shadow blur radius. Controls shadow expansion and softness.

    :attr:`shadow_blur_radius` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `15`.
    '''

    shadow_spread_radius = VariableListProperty([0], length=2)
    '''Define the shrink/expansion of the shadow.

    :attr:`shadow_spread_radius` is an :class:`~kivy.properties.VariableListProperty`
    and defaults to `[0, 0]`.
    '''

    _bg_color = ColorProperty((0, 0, 0, 0))
    _border_color = ColorProperty((0, 0, 0, 0))
    _shadow_color = ColorProperty((0, 0, 0, 0))
    _border_radius = VariableListProperty([0], length=4)
    _border_width = VariableListProperty([0.0001], length=4)

    def __init__(self, *args, **kwargs) -> None:
        self.bind(border_color=self.setter('_border_color'))
        self.bind(bg_color=self.setter('_bg_color'))
        self.bind(shadow_color=self.setter('_shadow_color'))

        super().__init__(*args, **kwargs)

    def on_border_width(self, instance: Self, border_width: list) -> None:
        '''Fired when the :attr:`border_width` value changes.'''
        self._border_width = [max(0.0001, border) for border in border_width]

    def on_width(self, instancw: Self, width: float | int) -> None:
        '''Fired when the :attr:`width` value changes.'''
        self.on_border_radius(self, self.border_radius)

    def on_height(self, instance: Self, height: float | int) -> None:
        '''Fired when the :attr:`height` value changes.'''
        self.on_border_radius(self, self.border_radius)

    def on_border_radius(self, instance: Self, border_radius: list) -> None:
        '''Fired when the :attr:`border_radius` value changes.'''
        min_size = min(self.width, self.height) / 2
        self._border_radius = [radius if radius <= min_size else min_size for radius in border_radius]
