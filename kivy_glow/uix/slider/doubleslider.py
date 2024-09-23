__all__ = ('GlowDoubleSlider', )

from kivy_glow.uix.behaviors import HoverBehavior
from kivy.input.motionevent import MotionEvent
from kivy_glow.uix.widget import GlowWidget
from kivy_glow.uix.icon import GlowIcon
from kivy_glow import kivy_glow_uix_dir
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.clock import Clock
import os
from kivy.core.window import (
    WindowBase,
    Window,
)
from kivy.properties import (
    BoundedNumericProperty,
    ReferenceListProperty,
    VariableListProperty,
    NumericProperty,
    BooleanProperty,
    OptionProperty,
    StringProperty,
    ColorProperty,
    AliasProperty,
)


with open(
    os.path.join(kivy_glow_uix_dir, 'slider', 'doubleslider.kv'), encoding='utf-8'
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

                else:
                    if self.hover:
                        HoverBehavior.hovered_widget = None
                        self.hover = False
                        self.dispatch('on_leave')

        return False

    def on_enter(self):
        Window.set_system_cursor('hand')

    def on_leave(self):
        Window.set_system_cursor('arrow')


class GlowDoubleSlider(GlowWidget):
    '''Class for creating a Double slider widget.

    Check module documentation for more details.
    '''

    padding = NumericProperty('16sp')

    min_value = NumericProperty(0.)
    max_value = NumericProperty(100.)

    min = NumericProperty(0.)
    max = NumericProperty(100.)
    range = ReferenceListProperty(min, max)

    step = BoundedNumericProperty(0, min=0)

    orientation = OptionProperty('horizontal', options=(
        'vertical', 'horizontal'))

    thumb_size = NumericProperty('16dp')
    value_track = BooleanProperty(True)
    line_width = NumericProperty('4dp')

    active = BooleanProperty(False)

    thumb_active_color = ColorProperty(None, allownone=True)
    thumb_inactive_color = ColorProperty(None, allownone=True)

    track_active_color = ColorProperty(None, allownone=True)
    track_inactive_color = ColorProperty(None, allownone=True)

    hint = BooleanProperty(True)
    hint_bg_color = ColorProperty(None, allownone=True)
    hint_text_color = ColorProperty(None, allownone=True)
    hint_border_radius = VariableListProperty(['4dp', ], length=4)

    _thumb_color = ColorProperty((0, 0, 0, 0))
    _track_active_color = ColorProperty((1, 0, 0, 0))
    _track_inactive_color = ColorProperty((0, 0, 0, 0))
    _hint_bg_color = ColorProperty((0, 0, 0, 0))
    _hint_text_color = ColorProperty((0, 0, 0, 0))

    _min_hint_text = StringProperty(' ')
    _max_hint_text = StringProperty(' ')
    _current_thumb = StringProperty('')
    _min_active = BooleanProperty(False)
    _max_active = BooleanProperty(False)

    use_center = BooleanProperty(True)
    '''Whether to move two sliders at the same time.
    default is True.
    '''
    _last_center_pos = None

    def __init__(self, *args, **kwargs):
        self.bind(track_active_color=self.setter('_track_active_color'))
        self.bind(track_inactive_color=self.setter('_track_inactive_color'))
        self.bind(hint_bg_color=self.setter('_hint_bg_color'))
        self.bind(hint_text_color=self.setter('_hint_text_color'))

        super().__init__(*args, **kwargs)

        Clock.schedule_once(self.set_default_colors, -1)

    def on_min(self, *largs):
        self.min_value = min(self.max, max(self.min, self.min_value))

    def on_max(self, *largs):
        self.max_value = min(self.max, max(self.min, self.max_value))

    def get_norm_min_value(self):
        vmin = self.min
        d = self.max - vmin
        if d == 0:
            return 0
        return (self.min_value - vmin) / float(d)

    def set_norm_min_value(self, value):
        vmin = self.min
        vmax = self.max
        step = self.step
        val = min(value * (vmax - vmin) + vmin, vmax)
        if step == 0:
            self.min_value = val
        else:
            self.min_value = min(round((val - vmin) / step) * step + vmin,
                                 vmax)

    def get_norm_max_value(self):
        vmin = self.min
        d = self.max - vmin
        if d == 0:
            return 0
        return (self.max_value - vmin) / float(d)

    def set_norm_max_value(self, value):
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

    def get_min_value_pos(self):
        padding = self.padding
        x = self.x
        y = self.y
        nval = self.min_value_normalized
        if self.orientation == 'horizontal':
            return (x + padding + nval * (self.width - 2 * padding - self.thumb_size), y)
        else:
            return (x, y + padding + nval * (self.height - 2 * padding - self.thumb_size))

    def set_min_value_pos(self, pos):
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
        else:
            if self.height == 0:
                self.min_value_normalized = 0
            else:
                new_min_value_normalized = (y - self.y - padding) / float(self.height - 2 * padding - self.thumb_size)
                if new_min_value_normalized <= self.max_value_normalized:
                    self.min_value_normalized = new_min_value_normalized
                else:
                    self.min_value_normalized = self.max_value_normalized

    def get_max_value_pos(self):
        padding = self.padding
        x = self.x
        y = self.y
        nval = self.max_value_normalized
        if self.orientation == 'horizontal':
            return (x + padding + self.thumb_size + nval * (self.width - 2 * padding - self.thumb_size), y)
        else:
            return (x, y + padding + self.thumb_size + nval * (self.height - 2 * padding - self.thumb_size))

    def set_max_value_pos(self, pos):
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
        else:
            if self.height == 0:
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

    def on_touch_down(self, touch):
        if self.disabled or not self.collide_point(*touch.pos):
            return

        elif self.use_center:
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
        else:
            if self.ids.glow_doubleslider_min_thumb.collide_point(*touch.pos):
                self._current_thumb = 'min_value'
                touch.grab(self)
            elif self.ids.glow_doubleslider_max_thumb.collide_point(*touch.pos):
                self._current_thumb = 'max_value'
                touch.grab(self)

        self.active = True

        return True

    def on_touch_move(self, touch):
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

    def on_touch_up(self, touch):
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

    def on_hint(self, _, value) -> None:
        if not value:
            self.remove_widget(self._left_hint_box)
            self.remove_widget(self._right_hint_box)

    def on_active(self, _, __):
        pass
        if self.active:
            if self._current_thumb in ('min_value', 'center'):
                self._min_active = True
                animation = Animation(
                    width=self.thumb_size * 1.2,
                    height=self.thumb_size * 1.2,
                    duration=0.1, t='out_quad')
                animation.start(self.ids.glow_doubleslider_min_thumb)
            if self._current_thumb in ('max_value', 'center'):
                self._max_active = True
                animation = Animation(
                    width=self.thumb_size * 1.2,
                    height=self.thumb_size * 1.2,
                    duration=0.1, t='out_quad')
                animation.start(self.ids.glow_doubleslider_max_thumb)
            self._thumb_color = self.thumb_active_color
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
            self._thumb_color = self.thumb_inactive_color

    def set_default_colors(self, *args):
        if self.thumb_active_color is None:
            self.thumb_active_color = self.theme_cls.primary_color

        if self.thumb_inactive_color is None:
            self.thumb_inactive_color = self.theme_cls.primary_color

        if self.track_active_color is None:
            self.track_active_color = self.theme_cls.primary_color

        if self.track_inactive_color is None:
            self.track_inactive_color = self.theme_cls.background_dark_color

        if self.hint_text_color is None:
            self.hint_text_color = self.theme_cls.primary_color

        if self.hint_bg_color is None:
            self.hint_bg_color = self.theme_cls.background_dark_color

        if self.bg_color is None:
            self.bg_color = self.theme_cls.background_dark_color

        self._thumb_color = self.thumb_inactive_color

    def on_min_value(self, _, __):
        self._min_hint_text = str(round(self.min_value, 2))

    def on_max_value(self, _, __):
        self._max_hint_text = str(round(self.max_value, 2))
