__all__ = ('GlowDoubleSlider', )

import os
from typing import Self

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import (
    Window,
    WindowBase,
)
from kivy.input.motionevent import MotionEvent
from kivy.lang import Builder
from kivy.properties import (
    AliasProperty,
    BooleanProperty,
    BoundedNumericProperty,
    ColorProperty,
    NumericProperty,
    OptionProperty,
    ReferenceListProperty,
    StringProperty,
    VariableListProperty,
)

from kivy_glow import kivy_glow_uix_dir
from kivy_glow.theme import ThemeManager
from kivy_glow.uix.behaviors import HoverBehavior
from kivy_glow.uix.icon import GlowIcon
from kivy_glow.uix.widget import GlowWidget

with open(
    os.path.join(kivy_glow_uix_dir, 'slider', 'doubleslider.kv'), encoding='utf-8',
) as kv_file:
    Builder.load_string(kv_file.read())


class Thumb(GlowIcon):

    def _on_window_motion(self, window: WindowBase, etype: str, motionevent: MotionEvent) -> bool:
        '''Fired at the Window motion event.'''
        motionevent.scale_for_screen(window.width, window.height)
        if 'hover' == motionevent.type_id:
            if not self.disabled and self.get_root_window():
                pos = self.to_widget(*motionevent.pos)
                if self.collide_point(*pos):

                    if self not in Window.children[0].walk():
                        return False

                    if not self._is_visible():
                        return False

                    if not self.hover:
                        self.hover = True
                        if HoverBehavior.hovered_widget is not None:
                            HoverBehavior.hovered_widget.hover = False
                            HoverBehavior.hovered_widget.dispatch('on_leave')

                        HoverBehavior.hovered_widget = self
                        self.dispatch('on_enter')

                elif self.hover:
                    HoverBehavior.hovered_widget = None
                    self.hover = False
                    self.dispatch('on_leave')

        return False

    def on_enter(self) -> None:
        Window.set_system_cursor('hand')

    def on_leave(self) -> None:
        Window.set_system_cursor('arrow')


class GlowDoubleSlider(GlowWidget):
    '''Class for creating a Double slider widget.

    Check module documentation for more details.
    '''

    padding = NumericProperty('16sp')
    '''Padding of the slider. The padding is used for graphical representation
    and interaction. It prevents the cursor from going out of the bounds of the
    slider bounding box.

    By default, padding is 16sp. The range of the slider is reduced from
    padding \\*2 on the screen. It allows drawing the default thumb of 32sp
    size without having the thumb go out of the widget.

    :attr:`padding` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `sp(16)`.
    '''

    min_value = NumericProperty(0.)
    '''Current minimum value used for the slider.

    :attr:`min_value` is an :class:`~kivy.properties.NumericProperty` and defaults
    to `0.`
    '''

    max_value = NumericProperty(100.)
    '''Current minimum value used for the slider.

    :attr:`min_value` is an :class:`~kivy.properties.NumericProperty` and defaults
    to `100.`
    '''

    min = NumericProperty(0.)
    '''Minimum value allowed for :attr:`min_value` and :attr:`max_value`.

    :attr:`min` is an :class:`~kivy.properties.NumericProperty` and defaults to
    `0.`
    '''

    max = NumericProperty(100.)
    '''Maximum value allowed for :attr:`min_value` and :attr:`max_value`.

    :attr:`max` is an :class:`~kivy.properties.NumericProperty` and defaults to
    `100.`
    '''

    range = ReferenceListProperty(min, max)
    '''Range of the double slider in the format (minimum value, maximum value)

    :attr:`range` is an :class:`~kivy.properties.ReferenceListProperty` of
    (:attr:`min`, :attr:`max`) properties.
    '''

    step = BoundedNumericProperty(0, min=0)
    '''Step size of the slider.

    :attr:`step` is an :class:`~kivy.properties.NumericProperty` and defaults
    to `0`.
    '''

    orientation = OptionProperty('horizontal', options=(
        'vertical', 'horizontal'))
    '''
    Orientation of the slider.

    :attr:`orientation` is an :class:`~kivy.properties.OptionProperty` and
    defaults to `'horizontal'`.
    '''

    thumb_size = NumericProperty('16sp')
    ''' Thumb size

    :attr:`thumb_size` is an :class:`~kivy.properties.NumericProperty` and
    defaults to `sp(16)`.
    '''

    value_track = BooleanProperty(True)
    '''Decides if slider should draw the line indicating the
    space between :attr:`min_value` and :attr:`max_value` properties values.

    :attr:`value_track` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `True`.
    '''

    line_width = NumericProperty('4dp')
    '''Slider line width

    :attr:`line_width` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `dp(4)`.
    '''

    active = BooleanProperty(False)
    '''

    :attr:`active` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    '''

    thumb_active_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the thumb when it active

    :attr:`thumb_active_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    thumb_inactive_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the thumb when it inactive

    :attr:`thumb_inactive_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    track_active_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format that indicated range between
    :attr:`min_value` - :attr:`max_value` properties values.

    :attr:`track_active_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    track_inactive_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format that indicated range between
     :attr:`min` - :attr:`min_value` and :attr:`max_value` - :attr:`max` properties values.

    :attr:`track_inactive_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    hint = BooleanProperty(True)
    '''If active, then show a tooltip showing the current value

    :attr:`hint` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `True`.
    '''

    hint_bg_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the hint background color

    :attr:`hint_bg_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    hint_text_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the hint text color

    :attr:`hint_text_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    hint_border_radius = VariableListProperty(['4dp'], length=4)
    '''Hint border radius

    :attr:`hint_border_radius` is an :class:`~kivy.properties.VariableListProperty`
    and defaults to `(dp(4), dp(4), dp(4), dp(4))`.
    '''

    use_center = BooleanProperty(True)
    '''Whether to move two sliders at the same time.

    :attr:`use_center` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `True`.
    '''

    _thumb_color = ColorProperty((0, 0, 0, 0))
    _thumb_active_color = ColorProperty((0, 0, 0, 0))
    _thumb_inactive_color = ColorProperty((0, 0, 0, 0))
    _track_active_color = ColorProperty((0, 0, 0, 0))
    _track_inactive_color = ColorProperty((0, 0, 0, 0))
    _hint_bg_color = ColorProperty((0, 0, 0, 0))
    _hint_text_color = ColorProperty((0, 0, 0, 0))

    _min_hint_text = StringProperty(' ')
    _max_hint_text = StringProperty(' ')
    _current_thumb = StringProperty('')
    _min_active = BooleanProperty(False)
    _max_active = BooleanProperty(False)

    _last_center_pos = None

    def __init__(self, *args, **kwargs) -> None:
        self.bind(thumb_active_color=self.setter('_thumb_active_color'))
        self.bind(thumb_inactive_color=self.setter('_thumb_inactive_color'))
        self.bind(track_active_color=self.setter('_track_active_color'))
        self.bind(track_inactive_color=self.setter('_track_inactive_color'))
        self.bind(hint_bg_color=self.setter('_hint_bg_color'))
        self.bind(hint_text_color=self.setter('_hint_text_color'))

        super().__init__(*args, **kwargs)

        Clock.schedule_once(self.set_default_colors, -1)

    def on_min(self, *largs) -> None:
        self.min_value = min(self.max, max(self.min, self.min_value))

    def on_max(self, *largs) -> None:
        self.max_value = min(self.max, max(self.min, self.max_value))

    def get_norm_min_value(self) -> float:
        vmin = self.min
        d = self.max - vmin
        if d == 0:
            return 0
        return (self.min_value - vmin) / float(d)

    def set_norm_min_value(self, value: float | int) -> None:
        vmin = self.min
        vmax = self.max
        step = self.step
        val = min(value * (vmax - vmin) + vmin, vmax)
        if step == 0:
            self.min_value = val
        else:
            self.min_value = min(round((val - vmin) / step) * step + vmin,
                                 vmax)

    def get_norm_max_value(self) -> float:
        vmin = self.min
        d = self.max - vmin
        if d == 0:
            return 0
        return (self.max_value - vmin) / float(d)

    def set_norm_max_value(self, value: float | int) -> None:
        vmin = self.min
        vmax = self.max
        step = self.step
        val = min(value * (vmax - vmin) + vmin, vmax)
        if step == 0:
            self.max_value = val
        else:
            self.max_value = min(round((val - vmin) / step) * step + vmin,
                                 vmax)

    min_value_normalized = AliasProperty(get_norm_min_value, set_norm_min_value,
                                         bind=('min_value', 'min', 'max'),
                                         cache=True)
    max_value_normalized = AliasProperty(get_norm_max_value, set_norm_max_value,
                                         bind=('max_value', 'min', 'max'),
                                         cache=True)

    def get_min_value_pos(self) -> float:
        padding = self.padding
        x = self.x
        y = self.y
        nval = self.min_value_normalized
        if self.orientation == 'horizontal':
            return (x + padding + nval * (self.width - 2 * padding - self.thumb_size), y)
        return (x, y + padding + nval * (self.height - 2 * padding - self.thumb_size))

    def set_min_value_pos(self, pos: tuple[float | int, float | int]) -> None:
        padding = self.padding
        x = min(self.right - padding - self.thumb_size, max(pos[0], self.x + padding))
        y = min(self.top - padding - self.thumb_size, max(pos[1], self.y + padding))
        if self.orientation == 'horizontal':
            if self.width == 0:
                self.min_value_normalized = 0
            else:
                new_min_value_normalized = (x - self.x - padding) / float(self.width - 2 * padding - self.thumb_size)
                if new_min_value_normalized <= self.max_value_normalized:
                    self.min_value_normalized = new_min_value_normalized
                else:
                    self.min_value_normalized = self.max_value_normalized
        elif self.height == 0:
            self.min_value_normalized = 0
        else:
            new_min_value_normalized = (y - self.y - padding) / float(self.height - 2 * padding - self.thumb_size)
            if new_min_value_normalized <= self.max_value_normalized:
                self.min_value_normalized = new_min_value_normalized
            else:
                self.min_value_normalized = self.max_value_normalized

    def get_max_value_pos(self) -> float:
        padding = self.padding
        x = self.x
        y = self.y
        nval = self.max_value_normalized
        if self.orientation == 'horizontal':
            return (x + padding + self.thumb_size + nval * (self.width - 2 * padding - self.thumb_size), y)
        return (x, y + padding + self.thumb_size + nval * (self.height - 2 * padding - self.thumb_size))

    def set_max_value_pos(self, pos: tuple[float | int, float | int]) -> None:
        padding = self.padding
        x = min(self.right - padding, max(pos[0], self.x + padding + self.thumb_size))
        y = min(self.top - padding, max(pos[1], self.y + padding + self.thumb_size))

        if self.orientation == 'horizontal':
            if self.width == 0:
                self.max_value_normalized = 0
            else:
                new_max_value_normalized = (x - self.x - padding - self.thumb_size) / float(self.width - 2 * padding - self.thumb_size)
                if new_max_value_normalized >= self.min_value_normalized:
                    self.max_value_normalized = new_max_value_normalized
                else:
                    self.max_value_normalized = self.min_value_normalized
        elif self.height == 0:
            self.max_value_normalized = 0
        else:
            new_max_value_normalized = (y - self.y - padding - self.thumb_size) / float(self.height - 2 * padding - self.thumb_size)
            if new_max_value_normalized >= self.min_value_normalized:
                self.max_value_normalized = new_max_value_normalized
            else:
                self.max_value_normalized = self.min_value_normalized

    min_value_pos = AliasProperty(get_min_value_pos, set_min_value_pos,
                                  bind=('pos', 'size', 'min', 'max', 'padding',
                                        'min_value_normalized', 'orientation'),
                                  cache=True)

    max_value_pos = AliasProperty(get_max_value_pos, set_max_value_pos,
                                  bind=('pos', 'size', 'min', 'max', 'padding',
                                        'max_value_normalized', 'orientation'),
                                  cache=True)

    def on_touch_down(self, touch: MotionEvent) -> bool:
        if self.disabled or not self.collide_point(*touch.pos):
            return False

        if self.use_center:
            if self.ids.glow_doubleslider_min_thumb.collide_point(*touch.pos):
                self._current_thumb = 'min_value'
                touch.grab(self)
            elif self.ids.glow_doubleslider_max_thumb.collide_point(*touch.pos):
                self._current_thumb = 'max_value'
                touch.grab(self)
            else:
                touch.grab(self)
                if self.orientation == 'horizontal':
                    if self.min_value_pos[0] < touch.pos[0] < self.max_value_pos[0]:
                        self._current_thumb = 'center'
                        self._last_center_pos = touch.pos
                if self.orientation == 'vertical':
                    if self.min_value_pos[1] < touch.pos[1] < self.max_value_pos[1]:
                        self._current_thumb = 'center'
                        self._last_center_pos = touch.pos
        elif self.ids.glow_doubleslider_min_thumb.collide_point(*touch.pos):
            self._current_thumb = 'min_value'
            touch.grab(self)
        elif self.ids.glow_doubleslider_max_thumb.collide_point(*touch.pos):
            self._current_thumb = 'max_value'
            touch.grab(self)

        self.active = True

        return True

    def on_touch_move(self, touch: MotionEvent) -> bool:
        if touch.grab_current == self:
            if self._current_thumb == 'min_value':
                self.min_value_pos = touch.pos
            elif self._current_thumb == 'max_value':
                self.max_value_pos = touch.pos
            elif self._current_thumb == 'center' and self._last_center_pos is not None:
                difference = touch.pos[0] - self._last_center_pos[0], touch.pos[1] - self._last_center_pos[1]
                min_value_pos = self.min_value_pos
                max_value_pos = self.max_value_pos

                self.min_value_pos = min_value_pos[0] + difference[0], min_value_pos[1] + difference[1]
                self.max_value_pos = max_value_pos[0] + difference[0], max_value_pos[1] + difference[1]

                if self.min_value_pos != min_value_pos or self.max_value_pos != max_value_pos:
                    self._last_center_pos = touch.pos

            return True

        return False

    def on_touch_up(self, touch: MotionEvent) -> bool:
        if touch.grab_current == self:
            if self._current_thumb == 'min_value':
                self.min_value_pos = touch.pos
            elif self._current_thumb == 'max_value':
                self.max_value_pos = touch.pos
            elif self._current_thumb == 'center' and self._last_center_pos is not None:
                difference = touch.pos[0] - self._last_center_pos[0], touch.pos[1] - self._last_center_pos[1]
                min_value_pos = self.min_value_pos
                max_value_pos = self.max_value_pos

                self.min_value_pos = min_value_pos[0] + difference[0], min_value_pos[1] + difference[1]
                self.max_value_pos = max_value_pos[0] + difference[0], max_value_pos[1] + difference[1]

                if self.min_value_pos != min_value_pos or self.max_value_pos != max_value_pos:
                    self._last_center_pos = touch.pos

            self._current_thumb = ''
            self._last_center_pos = None
            self.active = False

            return True

        return False

    def on_hint(self, instance: Self, value: bool) -> None:
        if not value:
            self.remove_widget(self._left_hint_box)
            self.remove_widget(self._right_hint_box)

    def on_active(self, instance: Self, value: bool) -> None:
        pass
        if self.active:
            if self._current_thumb in {'min_value', 'center'}:
                self._min_active = True
                animation = Animation(
                    width=self.thumb_size * 1.2,
                    height=self.thumb_size * 1.2,
                    duration=0.1, t='out_quad')
                animation.start(self.ids.glow_doubleslider_min_thumb)
            if self._current_thumb in {'max_value', 'center'}:
                self._max_active = True
                animation = Animation(
                    width=self.thumb_size * 1.2,
                    height=self.thumb_size * 1.2,
                    duration=0.1, t='out_quad')
                animation.start(self.ids.glow_doubleslider_max_thumb)
            self._thumb_color = self._thumb_active_color
        else:
            self._min_active = False
            self._max_active = False
            animation = Animation(
                width=self.thumb_size,
                height=self.thumb_size,
                duration=0.1, t='out_quad')
            animation.start(self.ids.glow_doubleslider_min_thumb)
            animation = Animation(
                width=self.thumb_size,
                height=self.thumb_size,
                duration=0.1, t='out_quad')
            animation.start(self.ids.glow_doubleslider_max_thumb)
            self._thumb_color = self._thumb_inactive_color

    def set_default_colors(self, *args) -> None:

        if self.bg_color is None:
            self._bg_color = self.theme_cls.background_dark_color

        if self.thumb_active_color is None:
            self._thumb_active_color = self.theme_cls.primary_color

        if self.thumb_inactive_color is None:
            self._thumb_inactive_color = self.theme_cls.primary_color

        if self.track_active_color is None:
            self._track_active_color = self.theme_cls.primary_color

        if self.track_inactive_color is None:
            self._track_inactive_color = self.theme_cls.background_dark_color

        if self.hint_text_color is None:
            self._hint_text_color = self.theme_cls.primary_color

        if self.hint_bg_color is None:
            self._hint_bg_color = self.theme_cls.background_dark_color

        self._thumb_color = self._thumb_inactive_color

    def on_theme_style(self, theme_manager: ThemeManager, theme_style: str) -> None:
        super().on_theme_style(theme_manager, theme_style)

        if self.track_inactive_color is None:
            self._thumb_color = self.theme_cls.background_dark_color
            if self.theme_cls.theme_style_switch_animation:
                Animation(
                    _track_inactive_color=self.theme_cls.background_dark_color,
                    d=self.theme_cls.theme_style_switch_animation_duration,
                    t='linear',
                ).start(self)
            else:
                self._track_inactive_color = self.theme_cls.background_dark_color

        if self.hint_bg_color is None:
            if self.theme_cls.theme_style_switch_animation:
                Animation(
                    _hint_bg_color=self.theme_cls.background_dark_color,
                    d=self.theme_cls.theme_style_switch_animation_duration,
                    t='linear',
                ).start(self)
            else:
                self._hint_bg_color = self.theme_cls.background_dark_color

        if self.bg_color is None:
            if self.theme_cls.theme_style_switch_animation:
                Animation(
                    _bg_color=self.theme_cls.background_dark_color,
                    d=self.theme_cls.theme_style_switch_animation_duration,
                    t='linear',
                ).start(self)
            else:
                self._bg_color = self.theme_cls.background_dark_color

    def on_min_value(self, instance: Self, value: float | int) -> None:
        self._min_hint_text = str(round(self.min_value, 2))

    def on_max_value(self, instance: Self, value: float | int) -> None:
        self._max_hint_text = str(round(self.max_value, 2))
