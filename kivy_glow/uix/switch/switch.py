__all__ = ('GlowSwitch', )

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
    OptionProperty,
    StringProperty,
)
from kivy.uix.behaviors import ToggleButtonBehavior

from kivy_glow import kivy_glow_uix_dir
from kivy_glow.theme import ThemeManager
from kivy_glow.uix.behaviors import HoverBehavior
from kivy_glow.uix.widget import GlowWidget

with open(
    os.path.join(kivy_glow_uix_dir, 'switch', 'switch.kv'), encoding='utf-8',
) as kv_file:
    Builder.load_string(kv_file.read())


class GlowSwitch(ToggleButtonBehavior,
                 HoverBehavior,
                 GlowWidget,
                 ):

    active = BooleanProperty(defaultvalue=False)
    '''Switch state

    :attr:`active` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    '''

    icon_active = StringProperty(defaultvalue='check-bold')
    '''active switch icon

    :attr:`icon_active` is an :class:`~kivy.properties.StringProperty`
    and defaults to `check-bold`.
    '''

    icon_inactive = StringProperty(defaultvalue='close-thick')
    '''inactive switch icon

    :attr:`icon_inactive` is an :class:`~kivy.properties.StringProperty`
    and defaults to `close-thick`.
    '''

    active_color = ColorProperty(defaultvalue=None, allownone=True)
    '''The color in (r, g, b, a) or string format of the active switch

    :attr:`active_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    inactive_color = ColorProperty(defaultvalue=None, allownone=True)
    '''The color in (r, g, b, a) or string format of the inactive switch

    :attr:`inactive_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    thumb_color = ColorProperty(defaultvalue=None, allownone=True)
    '''The color in (r, g, b, a) or string format of the switch thumb

    :attr:`thumb_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    thumb_size = NumericProperty(defaultvalue='24dp')
    ''' Thumb size

    :attr:`thumb_size` is an :class:`~kivy.properties.NumericProperty` and
    defaults to `dp(24)`.
    '''

    mode = OptionProperty(defaultvalue='normal-icon', options=('normal', 'short', 'normal-icon', 'short-icon'))
    '''Various switch display options

    :attr:`mode` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `normal-icon`.
    '''

    _icon = StringProperty(defaultvalue='blank')
    _color = ColorProperty(defaultvalue=(0, 0, 0, 0))
    _active_color = ColorProperty(defaultvalue=(0, 0, 0, 0))
    _inactive_color = ColorProperty(defaultvalue=(0, 0, 0, 0))
    _thumb_color = ColorProperty(defaultvalue=(0, 0, 0, 0))

    def __init__(self, *args, **kwargs) -> None:
        self.bind(active_color=self.setter('_active_color'))
        self.bind(inactive_color=self.setter('_inactive_color'))
        self.bind(thumb_color=self.setter('_thumb_color'))

        super().__init__(*args, **kwargs)

        self.always_release = False
        Clock.schedule_once(self.set_default_colors, -1)
        Clock.schedule_once(lambda _: self.on_state(self, self.state), -1)

        update = self.update_thumb_pos
        fbind = self.fbind
        fbind('pos', update)
        fbind('size', update)

    def update_thumb_pos(self, *args) -> None:
        Animation.cancel_all(self)
        Animation.cancel_all(self.ids.glow_switch_thumb)
        if self.active:
            self.ids.glow_switch_thumb.x = self.right - self.thumb_size
        else:
            self.ids.glow_switch_thumb.x = self.x

    def set_default_colors(self, *args) -> None:

        if self.active_color is None:
            self._active_color = self.theme_cls.primary_color

        if self.inactive_color is None:
            self._inactive_color = self.theme_cls.background_dark_color

        if self.thumb_color is None:
            self._thumb_color = self.theme_cls.background_color

        if self.state == 'normal' and self._color != self._inactive_color:
            self._color = self._inactive_color
        elif self.state == 'down' and self._color != self._active_color:
            self._color = self._active_color

    def on_theme_style(self, theme_manager: ThemeManager, theme_style: str) -> None:
        super().on_theme_style(theme_manager, theme_style)

        if self.inactive_color is None:
            self._inactive_color = self.theme_cls.background_dark_color
            if self.state == 'normal':
                if self.theme_cls.theme_style_switch_animation:
                    Animation(
                        _color=self._inactive_color,
                        d=self.theme_cls.theme_style_switch_animation_duration,
                        t='linear',
                    ).start(self)
                else:
                    self._color = self._inactive_color

        if self.thumb_color is None:
            if self.theme_cls.theme_style_switch_animation:
                Animation(
                    _thumb_color=self.theme_cls.background_color,
                    d=self.theme_cls.theme_style_switch_animation_duration,
                    t='linear',
                ).start(self)
            else:
                self._thumb_color = self.theme_cls.background_color

    def on_enter(self) -> None:
        Window.set_system_cursor('hand')

    def on_leave(self) -> None:
        Window.set_system_cursor('arrow')

    def on_active(self, instance: Self, value: bool) -> None:
        if self.active:
            self.state = 'down'
        else:
            self.state = 'normal'

    def on_state(self, instance: Self, value: str) -> None:
        Clock.schedule_once(lambda _: self._on_state(), 0)

    def _on_state(self) -> None:
        if self.state == 'down':
            self._icon = self.icon_active

            thumb_animation = Animation(x=self.right - self.thumb_size, d=0.3, t='out_bounce')
            thumb_animation.start(self.ids.glow_switch_thumb)
            if not self.disabled:
                self._animation = Animation(_color=self._active_color, d=.2)
                self._animation.start(self)
            else:
                self._color = self._active_color

            self.active = True
        else:
            self._icon = self.icon_inactive

            thumb_animation = Animation(x=self.x, d=0.3, t='out_bounce')
            thumb_animation.start(self.ids.glow_switch_thumb)
            if not self.disabled:
                self._animation = Animation(_color=self._inactive_color, d=.2)
                self._animation.start(self)
            else:
                self._color = self._inactive_color

            self.active = False

    def _do_press(self) -> None:
        pass

    def _do_release(self, *args) -> None:
        if (
            not self.allow_no_selection
            and self.group and self.state == 'down'
        ):
            return

        self._release_group(self)
        self.state = 'normal' if self.state == 'down' else 'down'

    def on_touch_up(self, touch: MotionEvent) -> bool:
        return super().on_touch_up(touch)
