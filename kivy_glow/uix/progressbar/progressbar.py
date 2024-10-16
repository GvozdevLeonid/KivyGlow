__all__ = ('GlowProgressBar', )

from kivy.uix.progressbar import ProgressBar
from kivy_glow.theme import ThemeManager
from kivy_glow import kivy_glow_uix_dir
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.clock import Clock
import os
from kivy_glow.uix.behaviors import (
    DeclarativeBehavior,
    AdaptiveBehavior,
    StyleBehavior,
    ThemeBehavior,
)
from kivy.properties import (
    NumericProperty,
    OptionProperty,
    ColorProperty,
    AliasProperty,
)


with open(
    os.path.join(kivy_glow_uix_dir, 'progressbar', 'progressbar.kv'), encoding='utf-8'
) as kv_file:
    Builder.load_string(kv_file.read())


class GlowProgressBar(DeclarativeBehavior,
                      AdaptiveBehavior,
                      StyleBehavior,
                      ThemeBehavior,
                      ProgressBar,
                      ):

    min = NumericProperty(0.)
    '''Minimum value allowed for :attr:`value`.

    :attr:`min` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `0`.
    '''

    padding = NumericProperty('16dp')
    '''Padding for progress bar. One size all borders.

    :attr:`padding` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `dp(16)`.
    '''

    active_color = ColorProperty(None, allownone=True)
    '''Padding for progress bar. One size all borders.

    :attr:`padding` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `dp(16)`.
    '''

    inactive_color = ColorProperty(None, allownone=True)
    '''Padding for progress bar. One size all borders.

    :attr:`padding` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `dp(16)`.
    '''

    line_width = NumericProperty('4dp')
    '''Padding for progress bar. One size all borders.

    :attr:`padding` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `dp(16)`.
    '''

    mode = OptionProperty('line', options=('line', 'circle'))
    '''Padding for progress bar. One size all borders.

    :attr:`padding` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `dp(16)`.
    '''

    _active_color = ColorProperty((0, 0, 0, 0))
    _inactive_color = ColorProperty((0, 0, 0, 0))

    def __init__(self, *args, **kwargs):
        self.bind(active_color=self.setter('_active_color'))
        self.bind(inactive_color=self.setter('_inactive_color'))

        super().__init__(*args, **kwargs)

        Clock.schedule_once(self.set_default_colors, -1)

    def set_default_colors(self, *args):

        if self.active_color is None:
            self._active_color = self.theme_cls.primary_color

        if self.inactive_color is None:
            self._inactive_color = self.theme_cls.background_dark_color

    def on_theme_style(self, theme_manager: ThemeManager, theme_style: str) -> None:
        super().on_theme_style(theme_manager, theme_style)

        if self.inactive_color is None:
            if self.theme_cls.theme_style_switch_animation:
                Animation(
                    _inactive_color=self.theme_cls.background_dark_color,
                    d=self.theme_cls.theme_style_switch_animation_duration,
                    t='linear',
                ).start(self)
            else:
                self._inactive_color = self.theme_cls.background_dark_color

    def _set_value(self, value):
        value = max(self.min, min(self.max, value))
        if value != self._value:
            self._value = value
            return True

    def get_norm_value(self):
        d = self.max - self.min
        if d == 0:
            return 0
        return (self.value - self.min) / float(d)

    def set_norm_value(self, value):
        self.value = value * (self.max - self.min) + self.min

    value_normalized = AliasProperty(get_norm_value, set_norm_value,
                                     bind=('value', 'max'), cache=True)

    def _get_value_pos(self):
        nval = self.value_normalized
        padding = self.padding
        x = self.x

        return x + padding + nval * (self.width - 2 * padding)

    value_pos = AliasProperty(_get_value_pos, None, bind=('value_normalized', 'mode', 'min', 'max'))

    def _get_value_angle(self):
        nval = self.value_normalized
        return nval * 360

    value_angle = AliasProperty(_get_value_angle, None, bind=('value_normalized', 'mode', 'min', 'max'))
