__all__ = ('GlowSlider', )

from kivy_glow.uix.icon import GlowIcon
from kivy_glow import kivy_glow_uix_dir
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.slider import Slider
from kivy.lang import Builder
from kivy.clock import Clock
import os
from kivy.properties import (
    VariableListProperty,
    BooleanProperty,
    NumericProperty,
    StringProperty,
    ColorProperty,
)
from kivy_glow.uix.behaviors import (
    DeclarativeBehavior,
    AdaptiveBehavior,
    StyleBehavior,
    ThemeBehavior,
)


with open(
    os.path.join(kivy_glow_uix_dir, 'slider', 'slider.kv'), encoding='utf-8'
) as kv_file:
    Builder.load_string(kv_file.read())


class Thumb(GlowIcon):

    def on_enter(self):
        Window.set_system_cursor('hand')

    def on_leave(self):
        Window.set_system_cursor('arrow')


class GlowSlider(DeclarativeBehavior,
                 AdaptiveBehavior,
                 ThemeBehavior,
                 StyleBehavior,
                 Slider):

    thumb_size = NumericProperty('16dp')
    value_track = BooleanProperty(True)
    line_width = NumericProperty('4dp')

    active = BooleanProperty(False)

    thumb_active_color = ColorProperty(None, allownone=True)
    thumb_inactive_color = ColorProperty(None, allownone=True)

    track_active_color = ColorProperty(None, allownone=True)
    track_inactive_color = ColorProperty(None, allownone=True)

    hint = BooleanProperty(True)
    hint_bg_color = ColorProperty(None, allownone=True)
    hint_text_color = ColorProperty(None, allownone=True)
    hint_border_radius = VariableListProperty(['4dp', ], length=4)

    _thumb_color = ColorProperty((0, 0, 0, 0))
    _track_active_color = ColorProperty((1, 0, 0, 0))
    _track_inactive_color = ColorProperty((0, 0, 0, 0))
    _hint_bg_color = ColorProperty((0, 0, 0, 0))
    _hint_text_color = ColorProperty((0, 0, 0, 0))

    _hint_text = StringProperty(' ')

    def __init__(self, *args, **kwargs):
        self.bind(track_active_color=self.setter('_track_active_color'))
        self.bind(track_inactive_color=self.setter('_track_inactive_color'))
        self.bind(hint_bg_color=self.setter('_hint_bg_color'))
        self.bind(hint_text_color=self.setter('_hint_text_color'))

        super().__init__(*args, **kwargs)

        Clock.schedule_once(self.set_default_colors, -1)

    def on_active(self, _, __):
        if self.active:
            animation = Animation(
                width=self.thumb_size * 1.2,
                height=self.thumb_size * 1.2,
                duration=0.1, t='out_quad')
            animation.start(self.ids.glow_slider_thumb)
            self._thumb_color = self.thumb_active_color
        else:
            animation = Animation(
                width=(self.thumb_size),
                height=(self.thumb_size),
                duration=0.1, t='out_quad')
            animation.start(self.ids.glow_slider_thumb)
            self._thumb_color = self.thumb_inactive_color

    def on_touch_down(self, touch):
        if super().on_touch_down(touch):
            self.active = True

    def on_touch_up(self, touch):
        if super().on_touch_up(touch):
            self.active = False

    def set_default_colors(self, *args):
        if self.thumb_active_color is None:
            self.thumb_active_color = self.theme_cls.primary_color

        if self.thumb_inactive_color is None:
            self.thumb_inactive_color = self.theme_cls.primary_color

        if self.track_active_color is None:
            self.track_active_color = self.theme_cls.primary_color

        if self.track_inactive_color is None:
            self.track_inactive_color = self.theme_cls.background_dark_color

        if self.hint_text_color is None:
            self.hint_text_color = self.theme_cls.primary_color

        if self.hint_bg_color is None:
            self.hint_bg_color = self.theme_cls.background_dark_color

        self._thumb_color = self.thumb_inactive_color

        if self.bg_color is None:
            self.bg_color = self.theme_cls.background_dark_color

    def on_value(self, _, __):
        self._hint_text = str(round(self.value, 2))
