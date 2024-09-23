__all__ = ('GlowPanel', )

from kivy_glow.uix.boxlayout import GlowBoxLayout
from kivy_glow.uix.button import GlowButton
from kivy_glow.uix.widget import GlowWidget
from kivy_glow import kivy_glow_uix_dir
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.clock import Clock
from typing import Self
import os
from kivy.properties import (
    NumericProperty,
    ObjectProperty,
    OptionProperty,
    ColorProperty,
    ListProperty,
)

with open(
    os.path.join(kivy_glow_uix_dir, 'panel', 'panel.kv'), encoding='utf-8'
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

    def __init__(self, *args, **kwargs):
        self.bind(active_color=self.setter('_active_color'))
        self.bind(text_color=self.setter('_text_color'))
        self.bind(icon_color=self.setter('_icon_color'))

        super().__init__(*args, **kwargs)
        self.register_event_type('on_active_tab')

        Clock.schedule_once(self.set_default_colors, -1)

    def on_parent(self, instance: Self, parent) -> None:
        if self._active_tab is not None:
            if parent is None:
                self._active_tab.unbind(pos=self._set_active_pos)
                self._active_tab.unbind(size=self._set_active_size)
            else:
                self._active_tab.bind(pos=self._set_active_pos)
                self._active_tab.bind(size=self._set_active_size)

        return super().on_parent(instance, parent)

    def on_tabs(self, panel_instance: Self, tabs: list[dict]) -> None:
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
                        size_hint_x=None,
                        size_hint_y=.5,
                        pos_hint={'center_y': .5},
                        width='2dp',
                        bg_color=self.theme_cls.divider_color
                    )
                )
            if tab.get('active', False):
                self._active_tab = tab_button

        if self._active_tab is None:
            self._active_tab = self.children[-1]

    def on_tab_width(self, panel_instance: Self, tab_width: int) -> None:
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

    def on__text_color(self, panel_instance: Self, text_color) -> None:
        '''Fired when the :attr:`text_color` value changes.'''
        for child in self.children[:]:
            if isinstance(child, GlowButton):
                if child == self._active_tab and self.mode == 'text':
                    child.text_color = self.active_color
                else:
                    child.text_color = text_color

    def on__icon_color(self, panel_instance: Self, icon_color) -> None:
        '''Fired when the :attr:`icon_color` value changes.'''
        for child in self.children[:]:
            if isinstance(child, GlowButton):
                if child == self._active_tab and self.mode == 'text':
                    child.icon_color = self.active_color
                else:
                    child.icon_color = icon_color

    def _set_active_pos(self, button_instance: GlowButton, pos: tuple) -> None:
        self._active_pos = pos

    def _set_active_size(self, button_instance: GlowButton, size: tuple) -> None:
        self._active_size = size

    def _select_tab(self, tab):
        self._active_tab.unbind(pos=self._set_active_pos)
        self._active_tab.unbind(size=self._set_active_size)
        if self.mode == 'text':
            self._active_tab.text_color = self._text_color
            self._active_tab.icon_color = self._icon_color

        self._active_tab = tab

    def on_active_tab(self, active_tab: GlowButton):
        pass

    def on__active_tab(self, _, __):
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
        if self.active_color is None:
            self.active_color = self.theme_cls.primary_color
        if self.bg_color is None and self.mode == 'badge':
            self.bg_color = self.theme_cls.primary_dark_color
        if self.text_color is None:
            self.text_color = self.theme_cls.text_color
        if self.icon_color is None:
            self.icon_color = self.theme_cls.text_color

    def set_active_tab(self, idx: int) -> None:
        for child in self.children[::-1]:
            if isinstance(child, GlowButton):
                if idx == 0:
                    self._select_tab(child)
                    break
                else:
                    idx -= 1
