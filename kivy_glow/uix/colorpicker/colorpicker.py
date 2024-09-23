__all__ = ('GlowColorPicker', )

from kivy_glow.uix.boxlayout import GlowBoxLayout
from kivy.input.motionevent import MotionEvent
from kivy_glow.uix.button import GlowButton
from kivy.uix.modalview import ModalView
from kivy_glow import kivy_glow_uix_dir
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.metrics import dp
import os
from kivy_glow.uix.behaviors import (
    DeclarativeBehavior,
    AdaptiveBehavior,
    StyleBehavior,
    ThemeBehavior,
)
from kivy.core.window import (
    WindowBase,
    Window,
)
from kivy_glow.colors import (
    available_palette,
    available_hue,
    colors,
)
from kivy.properties import (
    NumericProperty,
    OptionProperty,
    StringProperty,
    ColorProperty,
)

with open(
    os.path.join(kivy_glow_uix_dir, 'colorpicker', 'colorpicker.kv'), encoding='utf-8'
) as kv_file:
    Builder.load_string(kv_file.read())


class GlowColorPicker(DeclarativeBehavior,
                      AdaptiveBehavior,
                      StyleBehavior,
                      ThemeBehavior,
                      ModalView):

    '''Colorpicker widget.

    For more information, see in the
    :class:`~kivy_glow.uix.behaviors.DeclarativeBehavior` and
    :class:`~kivy_glow.uix.behaviors.AdaptiveBehavior` and
    :class:`~kivy_glow.uix.behaviors.StyleBehavior` and
    :class:`~kivy_glow.uix.behaviors.ThemeBehavior` and
    :class:`~kivy.uix.modalview.ModalView`
    classes documentation.
    '''

    default_color = ColorProperty((1, 0, 0, 1))
    '''Initial selected color

    :attr:`default_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `(1, 0, 0, 1)`.
    '''

    icon = StringProperty('blank')
    '''Colorpicker icon

    :attr:`icon` is an :class:`~kivy.properties.StringProperty`
    and defaults to `blank`.
    '''

    icon_size = NumericProperty('64dp')
    '''Colorpicker icon size

    :attr:`icon_size` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `24dp`.
    '''

    icon_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the icon

    :attr:`icon_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    icon_position = OptionProperty('center', options=('left', 'center', 'right'))
    '''Icon position.
    The icon in a colorpicker can be located on the left, center right, above the title

    :attr:`icon_position` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `center`.
    '''

    title = StringProperty(None, allownone=True)
    '''Title colorpicker text

    :attr:`title` is an :class:`~kivy.properties.StringProperty`
    and defaults to `None`.
    '''

    title_halign = OptionProperty('center', options=('left', 'center', 'right'))
    '''Title horizontal aligh.

    :attr:`title_haligh` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `center`.
    '''

    _selected_color = ColorProperty((1, 0, 0, 1))

    margin = NumericProperty('48dp')
    """Colorpicker maegin from device width.

    :attr:`margin` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `48dp`.
    """

    opening_transition = StringProperty('in_sine')
    '''Transition for opening animation

    :attr:`opening_transition` is an :class:`~kivy.properties.StringProperty`
    and defaults to `out_cubic`.
    '''

    opening_time = NumericProperty(.2)
    '''Diration for opening animation

    :attr:`opening_time` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `.2`.
    '''

    closing_transition = StringProperty('out_sine')
    '''Transition for closing animation

    :attr:`closing_transition` is an :class:`~kivy.properties.StringProperty`
    and defaults to `out_sine`.
    '''

    closing_time = NumericProperty(.2)
    '''Duration for closing animation

    :attr:`closing_time` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `.2`.
    '''

    _size_hint_y = 0
    _icon_color = ColorProperty((0, 0, 0, 0))
    _gradient_color = ColorProperty((1, 0, 0, 1))

    def __init__(self, *args, **kwargs):
        self.bind(icon_color=self.setter('_icon_color'))
        self.bind(default_color=self.setter('_selected_color'))

        super().__init__(*args, **kwargs)
        self.background = ''
        self.background_color = 0, 0, 0, 0

        self.register_event_type('on_selected_color')

        if self.size_hint[0] == 1 and self.size_hint[1] == 1 and (self.device == "desktop" or self.device == "tablet"):
            self.size_hint = (None, None)
            self.width = min(dp(560), Window.width - self.margin)
        elif self.size_hint[0] == 1 and self.size_hint[1] == 1 and self.device == "mobile":
            self.size_hint = (None, None)
            self.width = min(dp(280), Window.width - self.margin)
        else:
            self._size_hint_y = self.size_hint_y

        Clock.schedule_once(self.set_default_colors, -1)
        Clock.schedule_once(self.initialize_colorpicker, -1)
        self._update_selected_color()

    def open(self, *args, **kwargs):
        '''Display the colorpicker in the Window.'''

        if self._is_open:
            return

        self.ids.glow_colorpicker_content.opacity = 0
        if self.size_hint_y is None:
            self.height = 0
        else:
            self.size_hint_y = 0

        Window.bind(on_resize=self._align_center, on_keyboard=self._handle_keyboard)
        Window.add_widget(self)

        self._window = Window
        self._is_open = True

        self.dispatch('on_pre_open')

        self.center = Window.center
        self.fbind('center', self._align_center)
        self.fbind('size', self._align_center)

        Clock.schedule_once(self._open)

    def _open(self, *args):
        '''Open with calculatet colorpicker height.'''
        if self.size_hint_y is None:
            animation_height = Animation(
                height=self.ids.glow_colorpicker_content.minimum_height,
                t=self.opening_transition,
                d=self.opening_time,
            )
        else:
            animation_height = Animation(
                size_hint_y=self._size_hint_y,
                t=self.opening_transition,
                d=self.opening_time,
            )

        animation_opacity = Animation(
            _anim_alpha=1.,
            t=self.opening_transition,
            d=self.opening_time,
        )

        animation = animation_height & animation_opacity
        animation.bind(on_complete=lambda _, __: self._continue_open())
        animation.start(self)

    def _continue_open(self):
        '''Final step for openning '''
        self.ids.glow_colorpicker_content.opacity = 1
        self.dispatch('on_open')

    def dismiss(self, *args, **kwargs):
        '''Close the colorpicker if it is open.'''
        if not self._is_open:
            return

        self.ids.glow_colorpicker_content.opacity = 0

        self.dispatch('on_pre_dismiss')
        if self.dispatch('on_dismiss') is True:
            if kwargs.get('force', False) is not True:
                return

        if self.size_hint_y is None:
            animation_height = Animation(
                height=0,
                t=self.closing_transition,
                d=self.closing_time,
            )
        else:
            animation_height = Animation(
                size_hint_y=0,
                t=self.closing_transition,
                d=self.closing_time,
            )

        animation_opacity = Animation(
            _anim_alpha=0.,
            t=self.closing_transition,
            d=self.closing_time,
        )

        animation = animation_height & animation_opacity
        animation.bind(on_complete=lambda _, __: self._dismiss())
        animation.start(self)

    def _dismiss(self):
        '''Final step for closing '''
        self.ids.glow_colorpicker_content.opacity = 1
        self._real_remove_widget()

    def _on_window_resize(self, window: WindowBase, width: int, height: int) -> None:
        '''Fired at the Window resize event.'''

        self.width = min(dp(560) if self.device != "mobile" else dp(280), window.width - self.margin)

    def initialize_colorpicker(self, *args):
        '''Initializing the colorpicker.'''
        self._set_palette(available_palette[0])

        if self.icon == 'blank':
            self.ids.glow_colorpicker_content.remove_widget(self.ids.glow_colorpicker_icon)

        if self.title is None:
            self.ids.glow_colorpicker_content.remove_widget(self.ids.glow_colorpicker_title)

    def set_default_colors(self, *args):
        '''Set defaults colors.'''
        if self.bg_color is None:
            self.bg_color = self.theme_cls.background_color

        if self.icon_color is None:
            self.icon_color = self.theme_cls.primary_color

    def on__selected_color(self, *args):
        self._update_selected_color()

    def _update_selected_color(self):
        if 'glow_colorpicker_selected_color' in self.ids:
            self.ids.glow_colorpicker_selected_color.text = self.get_formatted_color(self._selected_color)

    def _set_palette(self, palette):
        self.ids.palette_scroll_view.clear_widgets()
        self.ids.palette_scroll_view.add_widget(
            GlowBoxLayout(
                *[GlowButton(text=hue, bg_color=colors[palette][hue], border_color=colors[palette][hue], adaptive_height=True, on_release=lambda button: setattr(self, '_selected_color', button.bg_color)) for hue in available_hue],
                orientation='vertical',
                adaptive_height=True,
                spacing='10dp',
            )
        )

    def get_formatted_color(self, color):
        if 'glow_colorpicker_selected_color_format' in self.ids:
            if self.ids.glow_colorpicker_selected_color_format.selected_item == 'hex':
                formated_selected_color = f'#{int(color[0] * 255):02x}{int(color[1] * 255):02x}{int(color[2] * 255):02x}{int(color[3] * 255):02x}'
            elif self.ids.glow_colorpicker_selected_color_format.selected_item == 'rgb':
                formated_selected_color = f'{round(color[0], 2)}, {round(color[1], 2)}, {round(color[2], 2)}'
            elif self.ids.glow_colorpicker_selected_color_format.selected_item == 'rgba':
                formated_selected_color = f'{round(color[0], 2)}, {round(color[1], 2)}, {round(color[2], 2)}, {round(color[3], 2)}'

            return formated_selected_color

        return ''

    def get_color_from_gradient(self, value, max_value):
        colors = [(1, 0, 0, 1), (1, 1, 0, 1), (0, 1, 0, 1), (0, 1, 1, 1), (0, 0, 1, 1), (1, 0, 1, 1), (1, 0, 0, 1)]
        n = len(colors) - 1
        interval = (value / max_value) * n
        index = int(interval)
        t = interval - index

        color1 = colors[index]
        color2 = colors[min(index + 1, len(colors) - 1)]

        interpolated_color = [color1[i] * (1 - t) + color2[i] * t for i in range(4)]

        return interpolated_color

    def on_select_color_from_gradient(self, instance: Widget, touch: MotionEvent):
        if instance.collide_point(*touch.pos):
            gradient = instance.export_as_image()
            tx = int(touch.x - instance.x)
            ty = gradient.height - int(touch.y - instance.y)
            if 0 <= tx < gradient.width and 0 <= ty < gradient.height:
                index = (ty * gradient.width + tx) * 4
                pixel_color = gradient.texture.pixels[index:index + 4]
                self._selected_color = [round(int(p) / 255, 2) for p in pixel_color]

    def on_selected_color(self, color):
        pass
