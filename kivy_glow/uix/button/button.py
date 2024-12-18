__all__ = ('GlowButton', )

import os
from typing import Self

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.input.motionevent import MotionEvent
from kivy.lang import Builder
from kivy.properties import (
    ColorProperty,
    NumericProperty,
    OptionProperty,
    ReferenceListProperty,
    StringProperty,
)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget

from kivy_glow import kivy_glow_uix_dir
from kivy_glow.theme import ThemeManager
from kivy_glow.uix.anchorlayout import GlowAnchorLayout
from kivy_glow.uix.behaviors import HoverBehavior
from kivy_glow.uix.icon import GlowIcon

with open(
    os.path.join(kivy_glow_uix_dir, 'button', 'button.kv'), encoding='utf-8',
) as kv_file:
    Builder.load_string(kv_file.read())


class GlowButton(HoverBehavior,
                 ButtonBehavior,
                 GlowAnchorLayout):
    '''Button widget

    For more information, see in the
    :class:`~kivy_glow.uix.behaviors.HoverBehavior` and
    :class:`~kivy.uix.behaviors.ButtonBehavior` and
    :class:`~kivy_glow.uix.anchorlayout.GlowAnchorLayout`
    classes documentation.
    '''

    text = StringProperty(defaultvalue=None, allownone=True)
    '''Button text

    If text is `None` then label will be removed from the button

    :attr:`text` is an :class:`~kivy.properties.StringProperty`
    and defaults to `None`.
    '''

    icon = StringProperty(defaultvalue='blank')
    '''Button icon

    :attr:`icon` is an :class:`~kivy.properties.StringProperty`
    and defaults to `blank`.
    '''

    text_color = ColorProperty(defaultvalue=None, allownone=True)
    '''The color in (r, g, b, a) or string format of the text

    :attr:`text_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    icon_color = ColorProperty(defaultvalue=None, allownone=True)
    '''The color in (r, g, b, a) or string format of the icon

    :attr:`icon_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    font_style = StringProperty(defaultvalue='BodyL')
    '''Font style (font, size, bold and/or italic, letter spacing, line height). Check out the available styles.

    :attr:`font_style` is an :class:`~kivy.properties.StringProperty`
    and defaults to `BodyL`.
    '''

    mode = OptionProperty(defaultvalue='filled', options=('filled', 'outline', 'soft', 'soft-outline', 'text'))
    '''Various button display options

    :attr:`mode` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `filled`.
    '''

    icon_size = NumericProperty(defaultvalue='24dp')
    '''Icon size

    :attr:`icon_size` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `24dp`.
    '''

    icon_position = OptionProperty(defaultvalue='left', options=('left', 'right', 'top', 'bottom'))
    '''Icon position.
    The icon in a button can be located on the left, right, above and below the text

    :attr:`icon_position` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `left`.
    '''

    spacing = NumericProperty(defaultvalue='5dp')
    '''Spacing between text and icon

    :attr:`spacing` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `5dp`.
    '''

    minimum_width = NumericProperty(defaultvalue=0)
    '''Minimum button width

    :attr:`minimum_width` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `0`.
    '''

    minimum_height = NumericProperty(defaultvalue=0)
    '''Minimum button height

    :attr:`minimum_height` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `0`.
    '''

    minimum_size = ReferenceListProperty(minimum_width, minimum_height)
    '''Minimum button size

    :attr:`minimum_size` is an :class:`~kivy.properties.ReferenceListProperty`
    '''

    _text_color = ColorProperty(defaultvalue=(0, 0, 0, 0))
    _icon_color = ColorProperty(defaultvalue=(0, 0, 0, 0))

    def __init__(self, *args, **kwargs) -> None:
        self.bind(text_color=self.setter('_text_color'))
        self.bind(icon_color=self.setter('_icon_color'))
        self.glow_icon = None

        super().__init__(*args, **kwargs)

        fbind = self.fbind
        update = self._update_minimum_size

        fbind('parent', update)
        fbind('spacing', update)
        fbind('padding', update)
        fbind('children', update)
        fbind('size', update)

        Clock.schedule_once(self.set_default_colors, -1)
        Clock.schedule_once(lambda _: self.children[0].fbind('size', update), -1)

    def on_parent(self, instance: Self, parent: Widget) -> None:
        if self.glow_icon is not None:
            if parent is None:
                self.unbind(icon_size=self.glow_icon.setter('font_size'),
                            icon=self.glow_icon.setter('icon'),
                            _icon_color=self.glow_icon.setter('color'))
            else:
                self.bind(icon_size=self.glow_icon.setter('font_size'),
                          icon=self.glow_icon.setter('icon'),
                          _icon_color=self.glow_icon.setter('color'))

        return super().on_parent(instance, parent)

    def on_enter(self) -> None:
        '''Fired at the Button hover enter event.'''
        Window.set_system_cursor('hand')

    def on_leave(self) -> None:
        '''Fired at the Button hover leave event.'''
        Window.set_system_cursor('arrow')

    def on_icon(self, instance: Self, icon: str) -> None:
        Clock.schedule_once(self._set_icon, -1)

    def on_mode(self, instance: Self, mode: str) -> None:
        '''Fired when the :attr:`mode` value changes.'''
        self.set_default_colors()

    def on_disabled(self, instance: Self, disabled: bool) -> None:
        '''Fired when the :attr:`disabled` value changes.'''
        Clock.schedule_once(self.set_disabled_colors, -1)

    def on_touch_down(self, touch: MotionEvent) -> bool:
        '''Fired at the Button on_touch_down event.'''
        if touch.is_mouse_scrolling:
            return False

        if self.collide_point(*touch.pos):
            if not self.disabled:
                if self.mode == 'filled':
                    self._animation = Animation(
                        _border_color=self.theme_cls.darken_or_lighten_color(self._border_color),
                        d=.01,
                    )
                elif self.mode == 'outline':
                    self._animation = Animation(
                        _border_color=self.theme_cls.darken_or_lighten_color(self._border_color),
                        d=.01,
                    )
                elif self.mode == 'soft':
                    self._animation = Animation(
                        _border_color=self._border_color[:3] + [1],
                        d=.01,
                    )
                elif self.mode == 'soft-outline':
                    self._animation = Animation(
                        _border_color=self._border_color[:3] + [0],
                        d=.01,
                    )
                elif self.mode == 'text':
                    self._animation = Animation(
                        _text_color=self.theme_cls.darken_or_lighten_color(self._text_color),
                        _icon_color=self.theme_cls.darken_or_lighten_color(self._icon_color),
                        d=.01,
                    )

                self._animation.start(self)
            else:
                self.set_disabled_colors()

        return super().on_touch_down(touch)

    def on_touch_up(self, touch: MotionEvent) -> bool:
        '''Fired at the Button on_touch_up event.'''
        def update_colors() -> None:
            if not self.disabled:
                if self.mode == 'filled':
                    self._border_color = self.border_color if self.border_color else self.theme_cls.primary_color
                elif self.mode == 'outline':
                    self._border_color = self.border_color if self.border_color else self.theme_cls.primary_color
                elif self.mode == 'soft':
                    self._border_color = self.border_color[:3] + [0] if self.border_color else self.theme_cls.primary_color[:3] + [0]
                elif self.mode == 'soft-outline':
                    self._border_color = self.border_color[:3] + [1] if self.border_color else self.theme_cls.primary_color
                elif self.mode == 'text':
                    self._text_color = self.text_color if self.text_color else self.theme_cls.primary_color
                    self._icon_color = self.icon_color if self.icon_color else self.theme_cls.primary_color
            else:
                self.set_disabled_colors()

        Clock.schedule_once(lambda _: update_colors(), 0.1)

        return super().on_touch_up(touch)

    def set_default_colors(self, *args) -> None:
        '''Set defaults colors. Based on mode.'''

        if self.mode == 'filled':
            if self.bg_color is None:
                self._bg_color = self.theme_cls.primary_color
            if self.border_color is None:
                self._border_color = self.theme_cls.primary_color
            if self.text_color is None:
                self._text_color = self.theme_cls.opposite_text_color
            if self.icon_color is None:
                self._icon_color = self.theme_cls.opposite_text_color

        elif self.mode == 'outline':
            if self.bg_color is not None:
                self._bg_color = (0, 0, 0, 0)
            if self.border_color is None:
                self._border_color = self.theme_cls.primary_color
            if self.text_color is None:
                self._text_color = self.theme_cls.text_color
            if self.icon_color is None:
                self._icon_color = self.theme_cls.text_color

        elif self.mode == 'soft':
            if self.bg_color is None:
                self._bg_color = self.theme_cls.primary_color[:3] + [.3]
            else:
                self.bg_color = self.bg_color[:3] + [.3]

            if self.border_color is None:
                self._border_color = self.theme_cls.primary_color[:3] + [0]
            else:
                self._border_color = self.border_color[:3] + [0]

            if self.text_color is None:
                self._text_color = self.theme_cls.primary_color
            if self.icon_color is None:
                self._icon_color = self.theme_cls.primary_color

        elif self.mode == 'soft-outline':
            if self.bg_color is None:
                self._bg_color = self.theme_cls.primary_color[:3] + [.3]
            else:
                self.bg_color = self.bg_color[:3] + [.3]

            if self.border_color is None:
                self._border_color = self.theme_cls.primary_color

            if self.text_color is None:
                self._text_color = self.theme_cls.primary_color
            if self.icon_color is None:
                self._icon_color = self.theme_cls.primary_color

        elif self.mode == 'text':
            if self.bg_color is not None:
                self._bg_color = (0, 0, 0, 0)

            if self.border_color is not None:
                self._border_color = (0, 0, 0, 0)

            if self.text_color is None:
                self._text_color = self.theme_cls.primary_color
            if self.icon_color is None:
                self._icon_color = self.theme_cls.primary_color

    def set_disabled_colors(self, *args) -> None:
        '''Set disabled colors. Based on mode.'''
        if self.disabled:
            if self.mode == 'filled':
                self._border_color = self.theme_cls.disabled_color[:3] + [0]
                self._bg_color = self.theme_cls.disabled_color[:3] + [.5]
            elif self.mode == 'outline':
                self._border_color = self.theme_cls.disabled_color
            elif self.mode == 'soft':
                self._bg_color = self.theme_cls.disabled_color[:3] + [.3]
            elif self.mode == 'soft-outline':
                self._bg_color = self.theme_cls.disabled_color[:3] + [.3]
                self._border_color = self.theme_cls.disabled_color
        elif self.mode == 'filled':
            self._bg_color = self.bg_color if self.bg_color else self.theme_cls.primary_color
            self._border_color = self.border_color if self.border_color else self.theme_cls.primary_color
        elif self.mode == 'outline':
            self._border_color = self.border_color if self.border_color else self.theme_cls.primary_color
        elif self.mode == 'soft':
            self._bg_color = self.bg_color if self.bg_color else self.theme_cls.primary_color[:3] + [.3]
        elif self.mode == 'soft-outline':
            self._bg_color = self.bg_color if self.bg_color else self.theme_cls.primary_color[:3] + [.3]
            self._border_color = self.border_color if self.border_color else self.theme_cls.primary_color

    def on_theme_style(self, theme_manager: ThemeManager, theme_style: str) -> None:
        '''Fired when the app :attr:`theme_style` value changes.'''
        super().on_theme_style(theme_manager, theme_style)

        if self.disabled:
            self.set_disabled_colors()

        if self.mode == 'filled':
            if self.text_color is None:
                if self.theme_cls.theme_style_switch_animation:
                    Animation(
                        _text_color=self.theme_cls.opposite_text_color,
                        d=self.theme_cls.theme_style_switch_animation_duration,
                        t='linear',
                    ).start(self)
                else:
                    self._text_color = self.theme_cls.opposite_text_color

            if self.icon_color is None:
                if self.theme_cls.theme_style_switch_animation:
                    Animation(
                        _icon_color=self.theme_cls.opposite_text_color,
                        d=self.theme_cls.theme_style_switch_animation_duration,
                        t='linear',
                    ).start(self)
                else:
                    self._icon_color = self.theme_cls.opposite_text_color

        elif self.mode == 'outline':
            if self.text_color is None:
                if self.theme_cls.theme_style_switch_animation:
                    Animation(
                        _text_color=self.theme_cls.text_color,
                        d=self.theme_cls.theme_style_switch_animation_duration,
                        t='linear',
                    ).start(self)
                else:
                    self._text_color = self.theme_cls.text_color

            if self.icon_color is None:
                if self.theme_cls.theme_style_switch_animation:
                    Animation(
                        _icon_color=self.theme_cls.text_color,
                        d=self.theme_cls.theme_style_switch_animation_duration,
                        t='linear',
                    ).start(self)
                else:
                    self._icon_color = self.theme_cls.text_color

    def _set_icon(self, *args) -> None:
        '''Add icon to the Button'''
        if self.glow_icon is not None:
            self.unbind(icon=self.glow_icon.setter('icon'),
                        _icon_color=self.glow_icon.setter('color'),
                        icon_size=self.glow_icon.setter('font_size'))
            self.ids.glow_button_container.remove_widget(self.glow_icon)

        if self.icon != 'blank':
            self.glow_icon = GlowIcon(
                pos_hint={'center_y': 0.5, 'center_x': .5},
                icon_size=self.icon_size,
                color=self._icon_color,
                icon=self.icon,
            )
            self.bind(icon=self.glow_icon.setter('icon'),
                      _icon_color=self.glow_icon.setter('color'),
                      icon_size=self.glow_icon.setter('font_size'))

            if self.icon_position in {'left', 'top'}:
                self.ids.glow_button_container.add_widget(self.glow_icon, index=1)
            elif self.icon_position in {'right', 'bottom'}:
                self.ids.glow_button_container.add_widget(self.glow_icon)

            if self.icon_position in {'top', 'bottom'}:
                self.ids.glow_button_container.orientation = 'vertical'

            if self.text is None:
                if 'glow_button_text' in self.ids:
                    self.ids.glow_button_container.remove_widget(self.ids.glow_button_text)
                    self.ids.pop('glow_button_text')

    def _update_minimum_size(self, *args) -> None:
        '''Calculate miminum Buttom size'''
        left, top, right, bottom = self.padding
        try:
            self.minimum_size = (left + right + self.ids.glow_button_container.width,
                                 top + bottom + self.ids.glow_button_container.height)
        except Exception:
            self.minimum_size = 0, 0

    def do_layout(self, *args) -> None:
        '''Modified default function'''
        super().do_layout(*args)
        self._update_minimum_size()
