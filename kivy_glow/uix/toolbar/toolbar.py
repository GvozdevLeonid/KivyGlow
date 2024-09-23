__all__ = ('GlowToolBar', )

from kivy_glow.uix.dropdowncontainer import GlowDropDownContainer
from kivy_glow.uix.boxlayout import GlowBoxLayout
from kivy_glow.uix.button import GlowButton
from kivy.core.window import WindowBase
from kivy_glow import kivy_glow_uix_dir
from kivy.lang import Builder
from kivy.clock import Clock
from typing import Self
import os
from kivy.properties import (
    BooleanProperty,
    OptionProperty,
    StringProperty,
    ListProperty,
)

with open(
    os.path.join(kivy_glow_uix_dir, 'toolbar', 'toolbar.kv'), encoding='utf-8'
) as kv_file:
    Builder.load_string(kv_file.read())


class GlowToolBar(GlowBoxLayout):

    title = StringProperty(None, allownone=True)
    '''Title toolbar text

    :attr:`title` is an :class:`~kivy.properties.StringProperty`
    and defaults to `None`.
    '''

    title_halign = OptionProperty('left', options=('left', 'center', 'right'))
    '''Title horizontal aligh.

    :attr:`title_haligh` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `center`.
    '''

    title_font_style = StringProperty('DisplayM')
    '''Title font style (font, size, bold and/or italic, letter spacing, line height). Check out the available styles.

    :attr:`font_style` is an :class:`~kivy.properties.StringProperty`
    and defaults to `DisplayM`.
    '''

    left_buttons = ListProperty(None, allownone=True)
    '''Toolbar left buttons.

    :attr:`left_buttons` is an :class:`~kivy.properties.ListProperty`
    and defaults to `None`.
    '''

    right_buttons = ListProperty(None, allownone=True)
    '''Toolbar right buttons.

    :attr:`right_buttons` is an :class:`~kivy.properties.ListProperty`
    and defaults to `None`.
    '''

    use_overflow = BooleanProperty(False)
    '''If yoolbar is resized, buttons move to the overflow menu from right
    to left.

    :attr:`use_overflow` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    '''

    overflow_buttons = ListProperty([])
    '''Toolbar overflow buttons.

    :attr:`overflow_buttons` is an :class:`~kivy.properties.ListProperty`
    and defaults to `empty`.
    '''

    overflow_button_icon = StringProperty('dots-vertical')
    '''Toolbar overflow button icon.

    :attr:`overflow_button_icon` is an :class:`~kivy.properties.StringProperty`
    and defaults to `dots-vertical`.
    '''

    is_overflow = BooleanProperty(False)
    _width = 0

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._overflow_menu = None
        self.overflow_button = GlowButton(
            icon_color=self.theme_cls.text_color,
            icon=self.overflow_button_icon,
            adaptive_size=True,
            disabled=True,
            mode='text',
            on_release=lambda _: self.open_overflow_menu()
        )

        Clock.schedule_once(self.set_default_colors, -1)
        Clock.schedule_once(self.initialize_toolbar, -1)

    def _on_window_resize(self, window: WindowBase, width: int, height: int) -> None:
        '''Fired at the Window resize event.'''
        super()._on_window_resize(window, width, height)

        if self._overflow_menu is not None:
            self._overflow_menu.dismiss()
            return

        if self.title is not None and self.ids.glow_toolbar_title.is_shortened and self._width > width:
            self.is_overflow = True
            if self.right_buttons is not None and len(self.right_buttons) > 0:
                button = self.right_buttons.pop(-1)
                self.ids.glow_toolbar_right_buttons_container.remove_widget(button)
                self.overflow_buttons.append(button)
            elif self.left_buttons is not None and len(self.left_buttons) > 0:
                button = self.left_buttons.pop(-1)
                self.ids.glow_toolbar_left_buttons_container.remove_widget(button)
                self.overflow_buttons.append(button)
            elif len(self.overflow_buttons) == 0:
                self.is_overflow = False

        elif self.title is not None and not self.ids.glow_toolbar_title.is_shortened and self._width < width:
            if len(self.overflow_buttons) and getattr(self.overflow_buttons[-1], 'container', None) is not None:
                button = self.overflow_buttons.pop(-1)
                button_container = getattr(button, 'container')

                if button_container == 'left':
                    self.ids.glow_toolbar_left_buttons_container.add_widget(button)
                    self.left_buttons.append(button)
                elif button_container == 'right':
                    self.ids.glow_toolbar_right_buttons_container.add_widget(button, index=1)
                    self.right_buttons.append(button)

                is_overflow = False
                for button in self.overflow_buttons:
                    if getattr(button, 'container', None) is not None:
                        is_overflow = True
                        break

                self.is_overflow = is_overflow

            elif len(self.overflow_buttons) == 0:
                self.is_overflow = False

        self._width = width

    def on_is_overflow(self, toolbar_instance: Self, is_overflow: list):
        '''Fired when the :attr:`is_overflow` value changes.'''
        if is_overflow:
            self.ids.glow_toolbar_right_buttons_container.add_widget(self.overflow_button)
            self.overflow_button.disabled = False
        else:
            self.ids.glow_toolbar_right_buttons_container.remove_widget(self.overflow_button)
            self.overflow_button.disabled = True

    def set_left_buttons(self, left_buttons: list):
        to_remove = []
        for button in self.overflow_buttons:
            if getattr(button, 'container', None) == 'left':
                to_remove.append(button)
        for button in to_remove:
            self.overflow_buttons.remove(button)

        self.left_buttons = left_buttons
        self.ids.glow_toolbar_left_buttons_container.clear_widgets()
        self.initialize_toolbar()

    def set_right_buttons(self, right_buttons: list):
        to_remove = []
        for button in self.overflow_buttons:
            if getattr(button, 'container', None) == 'right':
                to_remove.append(button)
        for button in to_remove:
            self.overflow_buttons.remove(button)

        self.right_buttons = right_buttons
        self.ids.glow_toolbar_right_buttons_container.clear_widgets()
        self.initialize_toolbar()

    def initialize_toolbar(self, *args):
        '''Initializing the ToolBar.'''
        if self.left_buttons is not None:
            for button in self.left_buttons:
                setattr(button, 'container', 'left')
                button.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
                self.ids.glow_toolbar_left_buttons_container.add_widget(button)

        if self.right_buttons is not None:
            for button in self.right_buttons:
                setattr(button, 'container', 'right')
                button.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
                self.ids.glow_toolbar_right_buttons_container.add_widget(button)

        if self.title is None:
            self.remove_widget(self.ids.glow_toolbar_title)

    def set_default_colors(self, *args):
        '''Set defaults colors.'''
        if self.bg_color is None:
            self.bg_color = self.theme_cls.primary_color

    def open_overflow_menu(self):
        '''Open menu with overflow buttons'''

        if self._overflow_menu is None:
            self._overflow_menu = GlowDropDownContainer(items=self.overflow_buttons[::-1])
            self._overflow_menu.open(self.overflow_button)
            self._overflow_menu.bind(on_dismiss=self.update_overflow)
        else:
            self._overflow_menu.dismiss()

    def update_overflow(self, overflow_menu: GlowDropDownContainer):
        self._overflow_menu.unbind(on_dismiss=self.update_overflow)
        for button in self.overflow_buttons:
            button.parent = None
        self._overflow_menu = None
