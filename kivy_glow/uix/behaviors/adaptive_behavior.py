__all__ = ('AdaptiveBehavior', )

from typing import Self

from kivy.clock import Clock
from kivy.core.window import (
    Window,
    WindowBase,
)
from kivy.event import EventDispatcher
from kivy.metrics import dp
from kivy.properties import (
    BooleanProperty,
    DictProperty,
)
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget


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
        defaultvalue={
            'xs': 480,
            'sm': 768,
            'md': 976,
            'lg': 1440,
            'xl': float('inf'),
        },
    )
    '''Possible breakpoints for adaptive behavior

    :attr:`breakpoints` is an :class:`~kivy.properties.DictProperty`
    and defaults to `{ 'xs': 480, 'sm': 768, 'md': 976, 'lg': 1440, 'xl': ∞}`.
    '''

    adaptive_width = BooleanProperty(defaultvalue=False)
    '''If `True`, the following properties will be applied to the widget:

        .. code-block:: kv
        size_hint_x: None
        width: self.minimum_width

    :attr:`adaptive_width` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    '''

    adaptive_height = BooleanProperty(defaultvalue=False)
    '''If `True`, the following properties will be applied to the widget:

        .. code-block:: kv
        size_hint_y: None
        height: self.minimum_height

    :attr:`adaptive_height` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    '''

    adaptive_size = BooleanProperty(defaultvalue=False)
    '''If `True`, the following properties will be applied to the widget:

        .. code-block:: kv
        size_hint: (None, None)
        size: self.minimum_size

    :attr:`adaptive_size` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    '''

    hidden = BooleanProperty(defaultvalue=False)
    '''If `True`, the following properties will be applied to the widget:

        .. code-block:: kv
        size_hint: (None, None)
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

        self._update_breakpoint_trigger = Clock.create_trigger(self._update_breakpoint, -1)
        self._hidden_trigger = Clock.create_trigger(self._on_hidden, -1)

        self._update_width_by_min_width_trigger = Clock.create_trigger(lambda _: setattr(self, 'width', max(self.minimum_width, dp(2))), -1)
        self._update_height_by_min_height_trigger = Clock.create_trigger(lambda _: setattr(self, 'height', max(self.minimum_height, dp(2))), -1)

        self._update_width_by_texture_size_trigger = Clock.create_trigger(lambda _: setattr(self, 'width', max(self.texture_size[0], dp(2))), -1)
        self._update_height_by_texture_size_trigger = Clock.create_trigger(lambda _: setattr(self, 'height', max(self.texture_size[1], dp(2))), -1)

        super().__init__(*args, **kwargs)

        self._update_breakpoint_trigger()

    def on_parent(self, instance: Self, parent: Widget) -> None:
        if parent is None:
            Window.unbind(on_resize=self._on_window_resize)
        else:
            Window.bind(on_resize=self._on_window_resize)

        if hasattr(super(), 'on_parent'):
            return super().on_parent(instance, parent)

        return None

    def _on_window_resize(self, window: WindowBase, width: int, height: int) -> None:
        '''Fired at the Window resize event.'''
        self._update_breakpoint_trigger()

    def _update_breakpoint(self, *args) -> None:
        breakpoints_keys = sorted(self.breakpoints.keys(), key=lambda x: self.breakpoints[x])
        breakpoints_values = sorted(self.breakpoints.values())

        for key, value in zip(breakpoints_keys, breakpoints_values):
            if Window.width <= dp(value):
                if self.breakpoint != key:
                    self.breakpoint = key
                    self.dispatch('on_breakpoint', key)
                break

    def _update_width_by_min_width(self, *args) -> None:
        self._update_width_by_min_width_trigger()

    def _update_height_by_min_height(self, *args) -> None:
        self._update_height_by_min_height_trigger()

    def _update_width_by_texture_size(self, *args) -> None:
        self._update_width_by_texture_size_trigger()

    def _update_height_by_texture_size(self, *args) -> None:
        self._update_height_by_texture_size_trigger()

    def on_breakpoint(self, breakpoint: str) -> None:
        '''Fired when the :attr:`breakpoint` value changes.'''
        pass

    def on_adaptive_height(self, instance: Self, adaptive_height: bool) -> None:
        '''Fired when the :attr:`adaptive_height` value changes.'''
        if self.hidden:
            return

        if adaptive_height:
            self.size_hint_y = None
            if issubclass(self.__class__, Label):
                self.bind(texture_size=self._update_height_by_texture_size)
                self._update_height_by_texture_size()
            elif not issubclass(self.__class__, FloatLayout):
                self.bind(minimum_height=self._update_height_by_min_height)
                self._update_height_by_min_height()
        else:
            self.size_hint_y = 1
            if issubclass(self.__class__, Label):
                self.unbind(texture_size=self._update_height_by_texture_size)
            elif not issubclass(self.__class__, FloatLayout):
                self.unbind(minimum_height=self._update_height_by_min_height)

    def on_adaptive_width(self, instance: Self, adaptive_width: bool) -> None:
        '''Fired when the :attr:`adaptive_width` value changes.'''
        if self.hidden:
            return

        if adaptive_width:

            self.size_hint_x = None
            if issubclass(self.__class__, Label):
                self.bind(texture_size=self._update_width_by_texture_size)
                self._update_width_by_texture_size()
            elif not issubclass(self.__class__, FloatLayout):
                self.bind(minimum_width=self._update_width_by_min_width)
                self._update_width_by_min_width()
        else:

            self.size_hint_x = 1
            if issubclass(self.__class__, Label):
                self.unbind(texture_size=self._update_width_by_texture_size)
            elif not issubclass(self.__class__, FloatLayout):
                self.unbind(minimum_width=self._update_width_by_min_width)

    def on_adaptive_size(self, instance: Self, adaptive_size: bool) -> None:
        '''Fired when the :attr:`adaptive_size` value changes.'''
        if self.hidden:
            return

        if adaptive_size:

            self.size_hint = (None, None)
            if issubclass(self.__class__, Label):
                self.bind(texture_size=self._update_width_by_texture_size)
                self.bind(texture_size=self._update_height_by_texture_size)
                self._update_width_by_texture_size()
                self._update_height_by_texture_size()
            elif not isinstance(self.__class__, FloatLayout):
                self.bind(minimum_width=self._update_width_by_min_width)
                self.bind(minimum_height=self._update_height_by_min_height)
                self._update_width_by_min_width()
                self._update_height_by_min_height()
        else:

            self.size_hint = (1, 1)
            if issubclass(self.__class__, Label):
                self.unbind(texture_size=self._update_width_by_texture_size)
                self.unbind(texture_size=self._update_height_by_texture_size)
            elif not isinstance(self.__class__, FloatLayout):
                self.unbind(minimum_width=self._update_width_by_min_width)
                self.unbind(minimum_height=self._update_height_by_min_height)

    def on_hidden(self, instance: Self, hidden: bool) -> None:
        '''Fired when the :attr:`hidden` value changes.'''
        self._hidden_trigger()

    def _on_hidden(self, *args) -> None:
        if self.hidden:

            self._size_hint = (self.size_hint_x, self.size_hint_y)
            self._size = (self.width, self.height)

            try:
                if issubclass(self.__class__, Label):
                    self.unbind(texture_size=self._update_width_by_texture_size)
                    self.unbind(texture_size=self._update_height_by_texture_size)
                elif not isinstance(self.__class__, FloatLayout):
                    self.unbind(minimum_width=self._update_width_by_min_width)
                    self.unbind(minimum_height=self._update_height_by_min_height)
            except Exception:
                pass

            self.size_hint = (None, None)
            self.size = (dp(2), dp(2))
            self.opacity = 0
        else:
            self.size_hint = self._size_hint
            self.size = self._size

            if self.adaptive_width:
                self.on_adaptive_width(self, self.adaptive_width)

            if self.adaptive_height:
                self.on_adaptive_height(self, self.adaptive_height)

            if self.adaptive_size:
                self.on_adaptive_size(self, self.adaptive_size)

            self.opacity = 1
