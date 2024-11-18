__all__ = ('GlowSlider', )

import os
from typing import Self

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.input.motionevent import MotionEvent
from kivy.lang import Builder
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    NumericProperty,
    StringProperty,
    VariableListProperty,
)
from kivy.uix.slider import Slider

from kivy_glow import kivy_glow_uix_dir
from kivy_glow.theme import ThemeManager
from kivy_glow.uix.behaviors import (
    AdaptiveBehavior,
    DeclarativeBehavior,
    StyleBehavior,
    ThemeBehavior,
)
from kivy_glow.uix.icon import GlowIcon

with open(
    os.path.join(kivy_glow_uix_dir, 'slider', 'slider.kv'), encoding='utf-8',
) as kv_file:
    Builder.load_string(kv_file.read())


class Thumb(GlowIcon):

    def on_enter(self) -> None:
        Window.set_system_cursor('hand')

    def on_leave(self) -> None:
        Window.set_system_cursor('arrow')


class GlowSlider(DeclarativeBehavior,
                 AdaptiveBehavior,
                 ThemeBehavior,
                 StyleBehavior,
                 Slider):

    thumb_size = NumericProperty('16sp')
    ''' Thumb size

    :attr:`thumb_size` is an :class:`~kivy.properties.NumericProperty` and
    defaults to `sp(16)`.
    '''

    value_track = BooleanProperty(True)
    '''Decides if slider should draw the line indicating the
    space between :attr:`min_value` and :attr:`max_value` properties values.

    :attr:`value_track` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `True`.
    '''

    line_width = NumericProperty('4dp')
    '''Slider line width

    :attr:`line_width` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `dp(4)`.
    '''

    active = BooleanProperty(False)
    '''

    :attr:`active` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    '''

    thumb_active_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the thumb when it active

    :attr:`thumb_active_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    thumb_inactive_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the thumb when it inactive

    :attr:`thumb_inactive_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    track_active_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format that indicated range between
    :attr:`min_value` - :attr:`max_value` properties values.

    :attr:`track_active_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    track_inactive_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format that indicated range between
     :attr:`min` - :attr:`min_value` and :attr:`max_value` - :attr:`max` properties values.

    :attr:`track_inactive_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    hint = BooleanProperty(True)
    '''If active, then show a tooltip showing the current value

    :attr:`hint` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `True`.
    '''

    hint_bg_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the hint background color

    :attr:`hint_bg_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    hint_text_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the hint text color

    :attr:`hint_text_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    hint_border_radius = VariableListProperty(['4dp'], length=4)
    '''Hint border radius

    :attr:`hint_border_radius` is an :class:`~kivy.properties.VariableListProperty`
    and defaults to `(dp(4), dp(4), dp(4), dp(4))`.
    '''

    _thumb_color = ColorProperty((0, 0, 0, 0))
    _thumb_active_color = ColorProperty((0, 0, 0, 0))
    _thumb_inactive_color = ColorProperty((0, 0, 0, 0))
    _track_active_color = ColorProperty((0, 0, 0, 0))
    _track_inactive_color = ColorProperty((0, 0, 0, 0))
    _hint_bg_color = ColorProperty((0, 0, 0, 0))
    _hint_text_color = ColorProperty((0, 0, 0, 0))

    _hint_text = StringProperty(' ')

    def __init__(self, *args, **kwargs) -> None:
        self.bind(thumb_active_color=self.setter('_thumb_active_color'))
        self.bind(thumb_inactive_color=self.setter('_thumb_inactive_color'))
        self.bind(track_active_color=self.setter('_track_active_color'))
        self.bind(track_inactive_color=self.setter('_track_inactive_color'))
        self.bind(hint_bg_color=self.setter('_hint_bg_color'))
        self.bind(hint_text_color=self.setter('_hint_text_color'))

        super().__init__(*args, **kwargs)

        Clock.schedule_once(self.set_default_colors, -1)

    def on_active(self, instance: Self, value: bool) -> None:
        if self.active:
            animation = Animation(
                width=self.thumb_size * 1.2,
                height=self.thumb_size * 1.2,
                duration=0.1, t='out_quad')
            animation.start(self.ids.glow_slider_thumb)
            self._thumb_color = self._thumb_active_color
        else:
            animation = Animation(
                width=(self.thumb_size),
                height=(self.thumb_size),
                duration=0.1, t='out_quad')
            animation.start(self.ids.glow_slider_thumb)
            self._thumb_color = self._thumb_inactive_color

    def on_touch_down(self, touch: MotionEvent) -> bool:
        if super().on_touch_down(touch):
            self.active = True
            return True

        return False

    def on_touch_up(self, touch: MotionEvent) -> bool:
        if super().on_touch_up(touch):
            self.active = False
            return True

        return False

    def set_default_colors(self, *args) -> None:

        if self.bg_color is None:
            self._bg_color = self.theme_cls.background_dark_color

        if self.thumb_active_color is None:
            self._thumb_active_color = self.theme_cls.primary_color

        if self.thumb_inactive_color is None:
            self._thumb_inactive_color = self.theme_cls.primary_color

        if self.track_active_color is None:
            self._track_active_color = self.theme_cls.primary_color

        if self.track_inactive_color is None:
            self._track_inactive_color = self.theme_cls.background_dark_color

        if self.hint_text_color is None:
            self._hint_text_color = self.theme_cls.primary_color

        if self.hint_bg_color is None:
            self._hint_bg_color = self.theme_cls.background_dark_color

        self._thumb_color = self._thumb_inactive_color

    def on_theme_style(self, theme_manager: ThemeManager, theme_style: str) -> None:
        super().on_theme_style(theme_manager, theme_style)

        if self.track_inactive_color is None:
            self._thumb_color = self.theme_cls.background_dark_color
            if self.theme_cls.theme_style_switch_animation:
                Animation(
                    _track_inactive_color=self.theme_cls.background_dark_color,
                    d=self.theme_cls.theme_style_switch_animation_duration,
                    t='linear',
                ).start(self)
            else:
                self._track_inactive_color = self.theme_cls.background_dark_color

        if self.hint_bg_color is None:
            if self.theme_cls.theme_style_switch_animation:
                Animation(
                    _hint_bg_color=self.theme_cls.background_dark_color,
                    d=self.theme_cls.theme_style_switch_animation_duration,
                    t='linear',
                ).start(self)
            else:
                self._hint_bg_color = self.theme_cls.background_dark_color

        if self.bg_color is None:
            if self.theme_cls.theme_style_switch_animation:
                Animation(
                    _bg_color=self.theme_cls.background_dark_color,
                    d=self.theme_cls.theme_style_switch_animation_duration,
                    t='linear',
                ).start(self)
            else:
                self._bg_color = self.theme_cls.background_dark_color

    def on_value(self, instance: Self, value: float | int) -> None:
        self._hint_text = str(round(self.value, 2))
