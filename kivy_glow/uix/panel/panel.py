__all__ = ('GlowPanel', )

import os
from typing import Self

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import (
    ColorProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    OptionProperty,
)
from kivy.uix.widget import Widget

from kivy_glow import kivy_glow_uix_dir
from kivy_glow.theme import ThemeManager
from kivy_glow.uix.boxlayout import GlowBoxLayout
from kivy_glow.uix.button import GlowButton
from kivy_glow.uix.widget import GlowWidget

with open(
    os.path.join(kivy_glow_uix_dir, 'panel', 'panel.kv'), encoding='utf-8',
) as kv_file:
    Builder.load_string(kv_file.read())


class GlowPanel(GlowBoxLayout):
    '''Tabbed panel widget to control screen manager.

    :Events:
        :attr:`on_active_tab`
            Called on changed active tab
    '''

    active_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the active tab

    :attr:`active_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    text_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the tab text

    :attr:`text_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    icon_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the tab icon

    :attr:`icon_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    tabs = ListProperty()
    '''Data for each tab in dict.

    Allowed tab properties:
    'id', 'text', 'icon', 'icon_size', 'icon_position', 'font_style', 'spacing', 'active'

    Example:
        .. code-block:: kv
        GlowPanel(
            tabs=[{'text': 'tab_1', 'icon': 'android'}, {'icon': 'android', 'active': True}]
        )

    :attr:`tabs` is an :class:`~kivy.properties.ListProperty`
    '''

    tab_width = NumericProperty(None, allownone=True)
    '''Fixed width for each tab

    :attr:`tab_width` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `None`.
    '''

    mode = OptionProperty('badge', options=('badge', 'underline', 'text'))
    '''Various panel display options

    :attr:`tab_width` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `badge`.
    '''

    _active_color = ColorProperty((0, 0, 0, 0))
    _text_color = ColorProperty((0, 0, 0, 0))
    _icon_color = ColorProperty((0, 0, 0, 0))

    _active_tab = ObjectProperty(None, allownone=True)
    _active_pos = ListProperty(None, allownone=True)
    _active_size = ListProperty(None, allownone=True)

    def __init__(self, *args, **kwargs) -> None:
        self.bind(active_color=self.setter('_active_color'))
        self.bind(text_color=self.setter('_text_color'))
        self.bind(icon_color=self.setter('_icon_color'))

        super().__init__(*args, **kwargs)
        self.register_event_type('on_active_tab')

        Clock.schedule_once(self.set_default_colors, -1)

    def on_parent(self, instance: Self, parent: Widget) -> None:
        if self._active_tab is not None:
            if parent is None:
                self._active_tab.unbind(pos=self._set_active_pos)
                self._active_tab.unbind(size=self._set_active_size)
            else:
                self._active_tab.bind(pos=self._set_active_pos)
                self._active_tab.bind(size=self._set_active_size)

        return super().on_parent(instance, parent)

    def on_tabs(self, instance: Self, tabs: list[dict]) -> None:
        '''Fired when the :attr:`tabs` value changes.'''
        self.clear_widgets()
        for i, tab in enumerate(tabs):
            tab_button = GlowButton(
                adaptive_height=True,
                size_hint_x=None if self.tab_width else 1,
                adaptive_width=True if (self.adaptive_width or self.adaptive_size) and not self.tab_width else False,
                width=self.tab_width if self.tab_width else 0,
                mode='text',
                id=tab.get('id', f'tab_{i}'),
                text=tab.get('text', None),
                icon=tab.get('icon', 'blank'),
                icon_size=tab.get('icon_size', '24dp'),
                icon_position=tab.get('icon_position', 'left'),
                font_style=tab.get('font_style', 'BodyL'),
                spacing=tab.get('spacing', '5dp'),
                pos_hint={'center_y': .5},
                on_release=self._select_tab,
            )
            self.add_widget(tab_button)

            if (i < len(tabs) - 1) and self.mode == 'badge':
                self.add_widget(
                    GlowWidget(
                        bg_color=self.theme_cls.divider_color,
                        pos_hint={'center_y': .5},
                        size_hint_x=None,
                        size_hint_y=.5,
                        width='2dp',
                    ),
                )
            if tab.get('active', False):
                self._active_tab = tab_button

        if self._active_tab is None:
            self._active_tab = self.children[-1]

    def on_tab_width(self, instance: Self, tab_width: int) -> None:
        '''Fired when the :attr:`tab_width` value changes.'''
        if tab_width is not None:
            self.adaptive_width = True
        else:
            self.adaptive_width = False

        for child in self.children[:]:
            if isinstance(child, GlowButton):
                if tab_width is not None:
                    child.adaptive_width = False
                    child.size_hint_x = None
                    child.width = tab_width
                else:
                    child.size_hint_x = 1
                    child.adaptive_width = True if (self.adaptive_width or self.adaptive_size) else False

    def on__active_color(self, instance: Self, active_color: tuple[float, float, float, float]) -> None:
        '''Fired when the :attr:`active_color` value changes.'''
        for child in self.children[:]:
            if isinstance(child, GlowButton):
                if child == self._active_tab and self.mode == 'text':
                    child.text_color = active_color
                else:
                    child.text_color = self._text_color

    def on__text_color(self, instance: Self, text_color: tuple[float, float, float, float]) -> None:
        '''Fired when the :attr:`text_color` value changes.'''
        for child in self.children[:]:
            if isinstance(child, GlowButton):
                if child == self._active_tab and self.mode == 'text':
                    child.text_color = self._active_color
                else:
                    child.text_color = text_color

    def on__icon_color(self, instance: Self, icon_color: tuple[float, float, float, float]) -> None:
        '''Fired when the :attr:`icon_color` value changes.'''
        for child in self.children[:]:
            if isinstance(child, GlowButton):
                if child == self._active_tab and self.mode == 'text':
                    child.icon_color = self._active_color
                else:
                    child.icon_color = icon_color

    def _set_active_pos(self, instance: GlowButton, pos: tuple) -> None:
        self._active_pos = pos

    def _set_active_size(self, instance: GlowButton, size: tuple) -> None:
        self._active_size = size

    def _select_tab(self, tab_instance: GlowButton) -> None:
        self._active_tab.unbind(pos=self._set_active_pos)
        self._active_tab.unbind(size=self._set_active_size)
        if self.mode == 'text':
            self._active_tab.text_color = self._text_color
            self._active_tab.icon_color = self._icon_color

        self._active_tab = tab_instance

    def on_active_tab(self, active_tab: GlowButton) -> None:
        pass

    def on__active_tab(self, instance: Self, tab_instance: GlowButton) -> None:
        if self._active_pos is not None:
            animation = Animation(
                _active_pos=self._active_tab.pos,
                _active_size=self._active_tab.size,
                d=.2, t='in_cubic',
            )
            animation.start(self)
        else:
            self._active_pos = self._active_tab.pos
            self._active_size = self._active_tab.size

        if self.mode == 'text':
            self._active_tab.text_color = self._active_color
            self._active_tab.icon_color = self._active_color

        self._active_tab.bind(pos=self._set_active_pos)
        self._active_tab.bind(size=self._set_active_size)
        self.dispatch('on_active_tab', self._active_tab)

    def set_default_colors(self, *args) -> None:
        '''Set defaults colors.'''

        if self.bg_color is None and self.mode == 'badge':
            self._bg_color = self.theme_cls.primary_dark_color

        if self.active_color is None:
            self._active_color = self.theme_cls.primary_color

        if self.text_color is None:
            self._text_color = self.theme_cls.text_color

        if self.icon_color is None:
            self._icon_color = self.theme_cls.text_color

    def on_theme_style(self, theme_manager: ThemeManager, theme_style: str) -> None:
        super().on_theme_style(theme_manager, theme_style)

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

        if self.mode == 'badge':
            for child in self.children[1::2]:
                child.bg_color = self.theme_cls.divider_color

    def set_active_tab(self, idx: int) -> None:
        for child in self.children[::-1]:
            if isinstance(child, GlowButton):
                if idx == 0:
                    self._select_tab(child)
                    break
                idx -= 1
