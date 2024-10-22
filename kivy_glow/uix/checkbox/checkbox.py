__all__ = ('GlowCheckbox', )

from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.input.motionevent import MotionEvent
from kivy_glow.uix.widget import GlowWidget
from kivy_glow.theme import ThemeManager
from kivy_glow import kivy_glow_uix_dir
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock
from typing import Self
import os
from kivy_glow.uix.behaviors import (
    HoverBehavior,
    ScaleBehavior,
)
from kivy.properties import (
    BooleanProperty,
    OptionProperty,
    StringProperty,
    ColorProperty,
)

with open(
    os.path.join(kivy_glow_uix_dir, 'checkbox', 'checkbox.kv'), encoding='utf-8'
) as kv_file:
    Builder.load_string(kv_file.read())


class GlowCheckbox(ToggleButtonBehavior,
                   HoverBehavior,
                   ScaleBehavior,
                   GlowWidget,
                   ):

    '''Checkbox widget. If checkbox in group, If the widget is in a group, it will be a radio button

    For more information, see in the
    :class:`~kivy.uix.behaviors.ToggleButtonBehavior` and
    :class:`~kivy_glow.uix.behaviors.HoverBehavior` and
    :class:`~kivy_glow.uix.behaviors.ScaleBehavior` and
    :class:`~kivy_glow.uix.widget.GlowWidget`
    classes documentation.
    '''

    active = BooleanProperty(False)
    '''Checkbox state

    :attr:`active` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    '''

    checkbox_icon_inactive = StringProperty('checkbox-blank-outline')
    '''inactive checkbox icon

    :attr:`checkbox_icon_inactive` is an :class:`~kivy.properties.StringProperty`
    and defaults to `checkbox-blank-outline`.
    '''
    checkbox_icon_active = StringProperty('checkbox-marked-outline')
    '''active checkbox icon

    :attr:`checkbox_icon_active` is an :class:`~kivy.properties.StringProperty`
    and defaults to `checkbox-marked-outline`.
    '''

    radio_icon_inactive = StringProperty('radiobox-blank')
    '''inactive radio icon

    :attr:`radio_icon_inactive` is an :class:`~kivy.properties.StringProperty`
    and defaults to `radiobox-blank`.
    '''

    radio_icon_active = StringProperty('radiobox-marked')
    '''inactive radio icon

    :attr:`inactive` is an :class:`~kivy.properties.StringProperty`
    and defaults to `radiobox-marked`.
    '''

    active_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the active checkbox

    :attr:`active_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    inactive_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the inactive checkbox

    :attr:`inactive_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    animation = OptionProperty('decrease', options=('decrease', 'increase'))
    '''Animation option (decrease', increase)

    :attr:`animation` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `decrease`.
    '''
    _active_color = ColorProperty((0, 0, 0, 0), allow_none=True)
    _inactive_color = ColorProperty((0, 0, 0, 0), allow_none=True)
    _color = ColorProperty((0, 0, 0, 0))
    _icon = StringProperty('blank')

    def __init__(self, *args, **kwargs) -> None:
        self.bind(active_color=self.setter('_active_color'))
        self.bind(inactive_color=self.setter('_inactive_color'))
        self._animation = (
            Animation(
                scale_x=.8,
                scale_y=.8,
                duration=0.1, t='out_quad')
            + Animation(
                scale_x=1,
                scale_y=1,
                duration=0.1, t='out_quad')
        )

        super().__init__(*args, **kwargs)
        Clock.schedule_once(self.set_default_colors, -1)
        Clock.schedule_once(lambda _: self.on_state(self, self.state), -1)

    def on_enter(self) -> None:
        '''Fired at the Checkbox hover enter event.'''
        Window.set_system_cursor('hand')

    def on_leave(self) -> None:
        '''Fired at the Checkbox hover leave event.'''
        Window.set_system_cursor('arrow')

    def on_active(self, checkbox_instance: Self, active: bool) -> None:
        '''Fired when the :attr:`active` value changes.'''
        if active:
            self.state = 'down'
        else:
            self.state = 'normal'

    def on_state(self, checkbox_instance: Self, state: str) -> None:
        '''Fired when the :attr:`state` value changes.'''

        if state == 'down':
            if not self.disabled:
                animation = Animation(_color=self._active_color, d=.2)
                animation.start(self)
            else:
                self._color = self._active_color

            self._animation.cancel(self)
            self._animation.start(self)
            self._icon = self.radio_icon_active if self.group else self.checkbox_icon_active

            if self.group:
                self._release_group(self)

            self.active = True
        else:
            if not self.disabled:
                animation = Animation(_color=self._inactive_color, d=.2)
                animation.start(self)
            else:
                self._color = self._inactive_color
            self._animation.cancel(self)

            if not self.group:
                self._animation.start(self)

            self._icon = self.radio_icon_inactive if self.group else self.checkbox_icon_inactive

            self.active = False

    def on_animation(self, checkbox_instance: Self, animation: str) -> None:
        if animation == 'decrease':
            self._animation = (
                Animation(
                    scale_x=.8,
                    scale_y=.8,
                    duration=0.1, t='out_quad')
                + Animation(
                    scale_x=1,
                    scale_y=1,
                    duration=0.1, t='out_quad')
            )

        elif animation == 'increase':
            self._animation = (
                Animation(
                    scale_x=1.2,
                    scale_y=1.2,
                    duration=0.1, t='out_quad')
                + Animation(
                    scale_x=1,
                    scale_y=1,
                    duration=0.1, t='out_quad')
            )

    def on_touch_up(self, touch: MotionEvent) -> bool:
        '''Fired at the Checkbox on_touch_up event.'''
        if self.collide_point(*touch.pos):
            super().on_touch_up(touch)

        return False

    def _do_press(self) -> None:
        '''Modified default function'''
        pass

    def _do_release(self, *args) -> None:
        '''Modified default function'''
        if (
            not self.allow_no_selection
            and self.group and self.state == 'down'
        ):
            return

        self._release_group(self)
        self.state = 'normal' if self.state == 'down' else 'down'

    def set_default_colors(self, *args) -> None:
        '''Set defaults colors.'''

        if self.active_color is None:
            self._active_color = self.theme_cls.primary_color
        if self.inactive_color is None:
            self._inactive_color = self.theme_cls.divider_color

        if self.state == 'normal' and self._color != self._inactive_color:
            self._color = self._inactive_color
        elif self.state == 'down' and self._color != self._active_color:
            self._color = self._active_color

    def on_theme_style(self, theme_manager: ThemeManager, theme_style: str) -> None:
        super().on_theme_style(theme_manager, theme_style)

        if self.inactive_color is None:
            self._inactive_color = self.theme_cls.divider_color

            if self.state == 'normal':
                if self.theme_cls.theme_style_switch_animation:
                    Animation(
                        _color=self._inactive_color,
                        d=self.theme_cls.theme_style_switch_animation_duration,
                        t='linear',
                    ).start(self)
                else:
                    self._color = self._inactive_color
