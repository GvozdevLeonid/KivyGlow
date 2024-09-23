__all__ = ('AdaptiveBehavior', )

from kivy.uix.floatlayout import FloatLayout
from kivy.event import EventDispatcher
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.metrics import dp
from typing import Self
from kivy.core.window import (
    WindowBase,
    Window,
)
from kivy.properties import (
    BooleanProperty,
    DictProperty,
)


class AdaptiveBehavior(EventDispatcher):
    '''
    Adaptive behavior class.

    For more information, see in the :class:`~kivy_glow.uix.behaviors.AdaptiveBehavior`

    :Events:
        :attr:`on_breakpoint`
            Called when window width is changed to specified breakpoint.
            It trigger at a breakpoint that is less than or equal to the current width.

            This can be useful for creating a responsive application.
            For example, you can change the number of columns in a grid or change fonts and sizes of static widgets and much more!

            For default breakpoints:
            xs: 0 - 480
            sm: 481 - 768
            md: 769 - 976
            lg: 977 - 1440
            xl: 1441 - ∞
    '''

    breakpoints = DictProperty(
        {
            'xs': 480,
            'sm': 768,
            'md': 976,
            'lg': 1440,
            'xl': float('inf')

        }
    )
    '''Possible breakpoints for adaptive behavior

    :attr:`breakpoints` is an :class:`~kivy.properties.DictProperty`
    and defaults to `{ 'xs': 480, 'sm': 768, 'md': 976, 'lg': 1440, 'xl': ∞}`.
    '''

    adaptive_width = BooleanProperty(False)
    '''If `True`, the following properties will be applied to the widget:

        .. code-block:: kv
        size_hint_x: None
        width: self.minimum_width

    :attr:`adaptive_width` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    '''

    adaptive_height = BooleanProperty(False)
    '''If `True`, the following properties will be applied to the widget:

        .. code-block:: kv
        size_hint_y: None
        height: self.minimum_height

    :attr:`adaptive_height` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    '''

    adaptive_size = BooleanProperty(False)
    '''If `True`, the following properties will be applied to the widget:

        .. code-block:: kv
        size_hint: None, None
        size: self.minimum_size

    :attr:`adaptive_size` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    '''

    hidden = BooleanProperty(False)
    '''If `True`, the following properties will be applied to the widget:

        .. code-block:: kv
        size_hint: None, None
        size: 0, 0
        opacity: 0

    :attr:`hidden` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.

    This function will save the previous state and return it when hidden is restored
    '''

    def __init__(self, *args, **kwargs) -> None:
        self.register_event_type('on_breakpoint')
        self.breakpoint = 'unknown'

        self._size_hint = self.size_hint_x, self.size_hint_y
        self._size = self.width, self.height

        self._adaptive_width = self.adaptive_width
        self._adaptive_height = self.adaptive_height
        self._adaptive_size = self.adaptive_size

        super().__init__(**kwargs)

        self._update_breakpoint_trigger = Clock.create_trigger(self._update_breakpoint)
        self._update_breakpoint_trigger()

    def on_parent(self, instance: Self, parent) -> None:
        if parent is None:
            Window.unbind(on_resize=self._on_window_resize)
        else:
            Window.bind(on_resize=self._on_window_resize)

        if hasattr(super(), 'on_parent'):
            return super().on_parent(instance, parent)

    def _on_window_resize(self, window: WindowBase, width: int, height: int) -> None:
        '''Fired at the Window resize event.'''
        self._update_breakpoint_trigger()

    def _update_breakpoint(self, *args):
        breakpoints_keys = sorted(self.breakpoints.keys(), key=lambda x: self.breakpoints[x])
        breakpoints_values = sorted(self.breakpoints.values())

        for key, value in zip(breakpoints_keys, breakpoints_values):
            if Window.width <= dp(value):
                if self.breakpoint != key:
                    self.breakpoint = key
                    self.dispatch('on_breakpoint', key)
                break

    def _update_width_by_min_width(self, *args) -> None:
        self.width = max(self.minimum_width, dp(1))

    def _update_height_by_min_height(self, *args) -> None:
        self.height = max(self.minimum_height, dp(1))

    def _update_width_by_texture_size(self, *args) -> None:
        self.width = max(self.texture_size[0], dp(1))

    def _update_height_by_texture_size(self, *args) -> None:
        self.height = max(self.texture_size[1], dp(1))

    def on_breakpoint(self, breakpoint: str) -> None:
        '''Fired when the :attr:`breakpoint` value changes.'''
        pass

    def on_adaptive_height(self, instance: Self, adaptive_height: bool) -> None:
        '''Fired when the :attr:`adaptive_height` value changes.'''
        if adaptive_height:
            self.size_hint_y = None
            if issubclass(self.__class__, Label):
                self.bind(texture_size=self._update_height_by_texture_size)
                self._update_height_by_texture_size()
            else:
                if not issubclass(self.__class__, FloatLayout):
                    self.bind(minimum_height=self._update_height_by_min_height)
                    if not self.children:
                        self.height = 0
                    else:
                        self._update_height_by_min_height()
        else:
            self.size_hint_y = 1
            if issubclass(self.__class__, Label):
                self.unbind(texture_size=self._update_height_by_texture_size)
            else:
                if not issubclass(self.__class__, FloatLayout):
                    self.unbind(minimum_height=self._update_height_by_min_height)

    def on_adaptive_width(self, instance: Self, adaptive_width: bool) -> None:
        '''Fired when the :attr:`adaptive_width` value changes.'''
        if adaptive_width:
            self.size_hint_x = None
            if issubclass(self.__class__, Label):
                self.bind(texture_size=self._update_width_by_texture_size)
                self._update_width_by_texture_size()
            else:
                if not issubclass(self.__class__, FloatLayout):
                    self.bind(minimum_width=self._update_width_by_min_width)
                    if not self.children:
                        self.width = 0
                    else:
                        self._update_width_by_min_width()
        else:
            self.size_hint_x = 1
            if issubclass(self.__class__, Label):
                self.unbind(texture_size=self._update_width_by_texture_size)
            else:
                if not issubclass(self.__class__, FloatLayout):
                    self.unbind(minimum_width=self._update_width_by_min_width)

    def on_adaptive_size(self, instance: Self, adaptive_size: bool) -> None:
        '''Fired when the :attr:`adaptive_size` value changes.'''
        if adaptive_size:
            self.size_hint = (None, None)
            if issubclass(self.__class__, Label):
                self.bind(texture_size=self._update_width_by_texture_size)
                self.bind(texture_size=self._update_height_by_texture_size)
                self._update_width_by_texture_size()
                self._update_height_by_texture_size()
            else:
                if not isinstance(self.__class__, FloatLayout):
                    self.bind(minimum_width=self._update_width_by_min_width)
                    self.bind(minimum_height=self._update_height_by_min_height)
                    if not self.children:
                        self.size = (0, 0)
                    else:
                        self._update_width_by_min_width()
                        self._update_height_by_min_height()
        else:
            self.size_hint = (1, 1)
            if issubclass(self.__class__, Label):
                self.unbind(texture_size=self._update_width_by_texture_size)
                self.unbind(texture_size=self._update_height_by_texture_size)
            else:
                if not isinstance(self.__class__, FloatLayout):
                    self.unbind(minimum_width=self._update_width_by_min_width)
                    self.unbind(minimum_height=self._update_height_by_min_height)

    def on_hidden(self, instance: Self, hidden: bool) -> None:
        '''Fired when the :attr:`hidden` value changes.'''
        # for child in self.children:
        #     child.hidden = hidden

        if hidden:
            self._adaptive_width = self.adaptive_width
            self._adaptive_height = self.adaptive_height
            self._adaptive_size = self.adaptive_size

            self._size_hint = self.size_hint_x, self.size_hint_y
            self._size = self.width, self.height

            self.adaptive_height = False
            self.adaptive_width = False
            self.adaptive_size = False

            self.size_hint = None, None
            self.size = dp(1), dp(1)

            self.opacity = 0
        else:
            self.size_hint = self._size_hint
            self.size = self._size

            self.adaptive_width = self._adaptive_width
            self.adaptive_height = self._adaptive_height
            self.adaptive_size = self._adaptive_size

            self.opacity = 1
