__all__ = ('GlowDialog', )

from kivy_glow.uix.label import GlowLabel
from kivy.uix.modalview import ModalView
from kivy_glow import kivy_glow_uix_dir
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.metrics import dp
from typing import Self
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
from kivy.properties import (
    NumericProperty,
    BooleanProperty,
    OptionProperty,
    StringProperty,
    ObjectProperty,
    ColorProperty,
    ListProperty,
)

with open(
    os.path.join(kivy_glow_uix_dir, 'dialog', 'dialog.kv'), encoding='utf-8'
) as kv_file:
    Builder.load_string(kv_file.read())


class GlowDialog(DeclarativeBehavior,
                 AdaptiveBehavior,
                 StyleBehavior,
                 ThemeBehavior,
                 ModalView):

    '''Dialog widget.

    For more information, see in the
    :class:`~kivy_glow.uix.behaviors.DeclarativeBehavior` and
    :class:`~kivy_glow.uix.behaviors.AdaptiveBehavior` and
    :class:`~kivy_glow.uix.behaviors.StyleBehavior` and
    :class:`~kivy_glow.uix.behaviors.ThemeBehavior` and
    :class:`~kivy.uix.modalview.ModalView`
    classes documentation.
    '''

    icon = StringProperty('blank')
    '''Dialog icon

    :attr:`icon` is an :class:`~kivy.properties.StringProperty`
    and defaults to `blank`.
    '''

    icon_size = NumericProperty('64dp')
    '''Dialog icon size

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
    The icon in a dialog can be located on the left, center right, above the title

    :attr:`icon_position` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `center`.
    '''

    title = StringProperty(None, allownone=True)
    '''Title dialog text

    :attr:`title` is an :class:`~kivy.properties.StringProperty`
    and defaults to `None`.
    '''

    title_halign = OptionProperty('center', options=('left', 'center', 'right'))
    '''Title horizontal aligh.

    :attr:`title_haligh` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `center`.
    '''

    text = StringProperty(None, allownone=True)
    '''Body dialog text

    :attr:`text` is an :class:`~kivy.properties.StringProperty`
    and defaults to `None`.
    '''

    text_halign = OptionProperty('center', options=('left', 'center', 'right'))
    '''Text horizontal aligh.

    :attr:`text_halign` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `center`.
    '''

    use_separator = BooleanProperty(False)
    '''Show separators after title and before buttons

    :attr:`use_separator` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    '''

    content = ObjectProperty(None, allownone=True)
    '''Body dialog content

    :attr:`content` is an :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`.
    '''

    buttons = ListProperty(None, allownone=True)
    '''Dialog buttons

    :attr:`content` is an :class:`~kivy.properties.ListProperty`
    and defaults to `None`.
    '''

    margin = NumericProperty('48dp')
    """Dialog maegin from device width.

    :attr:`margin` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `48dp`.
    """

    content_height = NumericProperty('300dp')
    """Content scroll height

    :attr:`content_height` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `300dp`.
    """

    adaptive_height_content = BooleanProperty(True)
    """Adjust the height according to the content

    :attr:`adaptive_height_content` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `True`.
    """

    stretch_content_height = BooleanProperty(False)
    """Adjust the height according to the Dialog free space

    :attr:`stretch_content_height` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    mode = OptionProperty(None, options=('warning', 'error', 'success'), allownone=True)
    '''Dialog mode.
        .. code-block:: kv
        warning:
        icon: 'alert-circle'
        icon_color: self.theme_cls.warning_color

        error:
        icon: 'close-circle'
        icon_color: 'self.theme_cls.error_color

        success:
        icon: 'check-circle'
        icon_color: self.theme_cls.success_color

    :attr:`mode` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `None`.
    '''

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

    def __init__(self, *args, **kwargs):
        self.bind(icon_color=self.setter('_icon_color'))

        super().__init__(*args, **kwargs)
        self.background = ''
        self.background_color = 0, 0, 0, 0

        if self.size_hint[0] == 1 and self.size_hint[1] == 1 and (self.device == "desktop" or self.device == "tablet"):
            self.size_hint = (None, None)
            self.width = min(dp(560), Window.width - self.margin)
        elif self.size_hint[0] == 1 and self.size_hint[1] == 1 and self.device == "mobile":
            self.size_hint = (None, None)
            self.width = min(dp(280), Window.width - self.margin)
        else:
            self._size_hint_y = self.size_hint_y

        Clock.schedule_once(self.set_default_colors, -1)
        Clock.schedule_once(self.initialize_dialog, -1)

    def on_parent(self, instance: Self, parent) -> None:
        if parent is None:
            Window.unbind(on_resize=self._on_window_resize)

            if self.adaptive_height_content and self.content is not None:
                self.content.unbind(height=self.ids.glow_dialog_content_container.setter('height'))
        else:
            if self.adaptive_height_content and self.content is not None:
                self.content.bind(height=self.ids.glow_dialog_content_container.setter('height'))
            Window.bind(on_resize=self._on_window_resize)

        return super().on_parent(instance, parent)

    def open(self, *args, **kwargs):
        '''Display the dialog in the Window.'''

        if self._is_open:
            return

        self.ids.glow_dialog_content.opacity = 0
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
        '''Open with calculatet dialog height.'''
        if self.size_hint_y is None:
            animation_height = Animation(
                height=self.ids.glow_dialog_content.minimum_height,
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
        self.ids.glow_dialog_content.opacity = 1
        self.dispatch('on_open')

    def dismiss(self, *args, **kwargs):
        '''Close the dialog if it is open.'''
        if not self._is_open:
            return

        self.ids.glow_dialog_content.opacity = 0

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
        self.ids.glow_dialog_content.opacity = 1
        self._real_remove_widget()

    def _on_window_resize(self, window: WindowBase, width: int, height: int) -> None:
        '''Fired at the Window resize event.'''

        self.width = min(dp(560) if self.device != "mobile" else dp(280), window.width - self.margin)

    def initialize_dialog(self, *args):
        '''Initializing the Dialog.'''
        if self.text is not None:
            self.content = GlowLabel(
                text=self.text,
                theme_color='Secondary',
                halign=self.text_halign,
                adaptive_height=True,
            )
            self.ids.glow_dialog_content_container.add_widget(self.content)

        elif self.content is not None:
            self.ids.glow_dialog_content_container.add_widget(self.content)
            self._add_content_ids()

        if self.buttons is not None:
            for button in self.buttons:
                self.ids.glow_dialog_buttons_container.add_widget(button)

        if self.icon == 'blank':
            self.ids.glow_dialog_content.remove_widget(self.ids.glow_dialog_icon)

        if self.title is None:
            self.ids.glow_dialog_content.remove_widget(self.ids.glow_dialog_title)
            self.ids.glow_dialog_content.remove_widget(self.ids.glow_dialog_top_separator)

        if self.adaptive_height_content and self.content is not None:
            self.content.bind(height=self.ids.glow_dialog_content_container.setter('height'))
        elif not self.adaptive_height_content and self.content is not None:
            self.ids.glow_dialog_content_container.height = self.content_height
        else:
            self.ids.glow_dialog_content_container.height = 0

    def set_default_colors(self, *args):
        '''Set defaults colors.'''
        if self.bg_color is None:
            self.bg_color = self.theme_cls.background_color

        if self.mode == 'warning':
            if self.icon == 'blank':
                self.icon = 'alert-circle'
            if self.icon_color is None:
                self.icon_color = self.theme_cls.warning_color

        elif self.mode == 'error':
            if self.icon == 'blank':
                self.icon = 'close-circle'
            if self.icon_color is None:
                self.icon_color = self.theme_cls.error_color

        elif self.mode == 'success':
            if self.icon == 'blank':
                self.icon = 'check-circle'
            if self.icon_color is None:
                self.icon_color = self.theme_cls.success_color

        if self.icon_color is None:
            self.icon_color = self.theme_cls.primary_color

    def _add_content_ids(self):
        '''Add content ids to dialog.'''
        if hasattr(self.content, 'id'):
            self.ids[self.content.id] = self.content

        for child_id, sub_child in self.content.ids.items():
            if child_id not in self.ids.keys():
                self.ids[child_id] = sub_child
