__all__ = ('ThemeBehavior', )

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.metrics import dp
from kivy.properties import (
    NumericProperty,
    ObjectProperty,
    OptionProperty,
)
from kivy.utils import platform

from kivy_glow.theme import ThemeManager


class ThemeBehavior(EventDispatcher):

    theme_cls = ObjectProperty()
    '''Instance of :class:`kivy_glow.theme.ThemeManager` class.

    :attr:`theme_cls` is an :class:`~kivy.properties.ObjectProperty`.
    '''
    widget_style = OptionProperty(defaultvalue=None, options=('desktop', 'mobile'), allownone=True)
    '''Allows to set one of the two style properties for the widget:
    `'desktop'`, `'mobile'`.

    Some widgets have slightly modified appearance and/or additional controls for mobile devices.
    :attr:`widget_style` is an :class:`~kivy.properties.OptionProperty`.
    Installed by default from kivy.utils.platform
    '''
    device = 'unonknow'

    row = NumericProperty(defaultvalue=0)
    col = NumericProperty(defaultvalue=0)
    rowspan = NumericProperty(defaultvalue=1)
    colspan = NumericProperty(defaultvalue=1)
    '''
    Support for GlowTableLayout
    '''

    def __init__(self, *args, **kwargs) -> None:
        self.theme_cls = App.get_running_app().theme_cls
        self.register_event_type('on_theme_style')

        super().__init__(*args, **kwargs)

        self.set_device()
        self.theme_cls.bind(theme_style=lambda theme_manager, theme_style: self.dispatch('on_theme_style', theme_manager, theme_style))
        Clock.schedule_once(self.set_default_widget_style, -1)

    def set_default_widget_style(self, *args) -> None:
        '''Set default widget style. Based on kivy.utils.platform.'''
        if self.widget_style is None:
            if platform in {'android', 'ios'}:
                self.widget_style = 'mobile'
            else:
                self.widget_style = 'desktop'

    def set_device(self, *args) -> None:
        '''Set device type. Based on kivy.utils.platform.'''
        if platform not in {'android', 'ios'}:
            self.device = 'desktop'
        elif Window.width >= dp(600) and Window.height >= dp(600):
            self.device = 'tablet'
        else:
            self.device = 'mobile'

    def on_theme_style(self, theme_manager: ThemeManager, theme_style: str) -> None:
        pass
