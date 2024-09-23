__all__ = ('ThemeBehavior', )

from kivy.event import EventDispatcher
from kivy.core.window import Window
from kivy.utils import platform
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.app import App
from kivy.properties import (
    NumericProperty,
    ObjectProperty,
    OptionProperty,
)


class ThemeBehavior(EventDispatcher):

    theme_cls = ObjectProperty()
    '''Instance of :class:`kivy_glow.theme.ThemeManager` class.

    :attr:`theme_cls` is an :class:`~kivy.properties.ObjectProperty`.
    '''
    widget_style = OptionProperty(None, options=('desctop', 'mobile'), allownone=True)
    '''Allows to set one of the two style properties for the widget:
    `'desctop'`, `'mobile'`.

    Some widgets have slightly modified appearance and/or additional controls for mobile devices.
    :attr:`widget_style` is an :class:`~kivy.properties.OptionProperty`.
    Installed by default from kivy.utils.platform
    '''
    device = 'unonknow'

    row = NumericProperty(0)
    col = NumericProperty(0)
    rowspan = NumericProperty(1)
    colspan = NumericProperty(1)
    '''
    Support for GlowTableLayout
    '''

    def __init__(self, *args, **kwargs) -> None:
        self.theme_cls = App.get_running_app().theme_cls
        self.set_device()

        Clock.schedule_once(self.set_default_widget_style, -1)
        super().__init__(**kwargs)

    def set_default_widget_style(self, *args) -> None:
        '''Set default widget style. Based on kivy.utils.platform.'''
        if self.widget_style is None:
            if platform in ('android', 'ios'):
                self.widget_style = 'mobile'
            else:
                self.widget_style = 'desctop'

    def set_device(self, *args):
        if platform != "android" and platform != "ios":
            self.device = "desktop"
        elif Window.width >= dp(600) and Window.height >= dp(600):
            self.device = "tablet"
        else:
            self.device = "mobile"
