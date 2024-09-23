__all__ = ('GlowProgressBar', )

from kivy.uix.progressbar import ProgressBar
from kivy_glow import kivy_glow_uix_dir
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

    padding = NumericProperty('16sp')
    active_color = ColorProperty(None, allownone=True)
    inactive_color = ColorProperty(None, allownone=True)
    line_width = NumericProperty('4dp')

    _active_color = ColorProperty((0, 0, 0, 0))
    _inactive_color = ColorProperty((0, 0, 0, 0))

    mode = OptionProperty('line', options=('line', 'circle'))

    def __init__(self, *args, **kwargs):
        self.bind(active_color=self.setter('_active_color'))
        self.bind(inactive_color=self.setter('_inactive_color'))

        super().__init__(*args, **kwargs)

        Clock.schedule_once(self.set_default_colors, -1)

    def set_default_colors(self, *args):
        if self.active_color is None:
            self.active_color = self.theme_cls.primary_color
        if self.inactive_color is None:
            self.inactive_color = self.theme_cls.background_dark_color

    def _get_value_pos(self):
        nval = self.value_normalized
        padding = self.padding
        x = self.x

        return x + padding + nval * (self.width - 2 * padding)

    value_pos = AliasProperty(_get_value_pos, None, bind=('value_normalized', 'mode'))

    def _get_value_angle(self):
        nval = self.value_normalized
        return nval * 360

    value_angle = AliasProperty(_get_value_angle, None, bind=('value_normalized', 'mode'))
