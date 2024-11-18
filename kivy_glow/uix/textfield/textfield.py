__all__ = ('GlowTextField', )

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
from kivy.metrics import sp
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    NumericProperty,
    ObjectProperty,
    OptionProperty,
    StringProperty,
)
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from kivy_glow import kivy_glow_uix_dir
from kivy_glow.theme import ThemeManager
from kivy_glow.uix.behaviors import HoverBehavior
from kivy_glow.uix.boxlayout import GlowBoxLayout

with open(
    os.path.join(kivy_glow_uix_dir, 'textfield', 'textfield.kv'), encoding='utf-8',
) as kv_file:
    Builder.load_string(kv_file.read())


class GlowTextField(HoverBehavior,
                    GlowBoxLayout):

    font_size = NumericProperty(defaultvalue='16sp')

    cursor_color = ColorProperty(defaultvalue=None, allownone=True)
    selection_color = ColorProperty(defaultvalue=None, allownone=True)

    focus_border_color = ColorProperty(defaultvalue=None, allownone=True)
    error_color = ColorProperty(defaultvalue=None, allownone=True)

    placeholder_color = ColorProperty(defaultvalue=None, allownone=True)

    text_color = ColorProperty(defaultvalue=None, allownone=True)
    focus_text_color = ColorProperty(defaultvalue=None, allownone=True)
    disabled_text_color = ColorProperty(defaultvalue=None, allownone=True)

    label_color = ColorProperty(defaultvalue=None, allownone=True)
    focus_label_color = ColorProperty(defaultvalue=None, allownone=True)

    help_text_color = ColorProperty(defaultvalue=None, allownone=True)
    focus_help_text_color = ColorProperty(defaultvalue=None, allownone=True)

    focus = BooleanProperty(defaultvalue=False)
    password = BooleanProperty(defaultvalue=False)
    error = BooleanProperty(defaultvalue=False)
    readonly = BooleanProperty(defaultvalue=False)
    required = BooleanProperty(defaultvalue=False)
    multiline = BooleanProperty(defaultvalue=False)

    mode = OptionProperty(defaultvalue='overlap', options=('overlap', 'inside', 'outside'))
    border_style = OptionProperty(defaultvalue='full', options=('full', 'underline'))

    use_handles = BooleanProperty(defaultvalue=None, allownone=True)
    use_bubble = BooleanProperty(defaultvalue=None, allownone=True)

    label = StringProperty(defaultvalue='')
    label_position = OptionProperty(defaultvalue='left', options=('left', 'right', 'center'))

    help_text = StringProperty(defaultvalue='')
    help_text_position = OptionProperty(defaultvalue='left', options=('left', 'right', 'center'))
    help_text_mode = OptionProperty(
        defaultvalue='persistent', options=['persistent', 'on_focus', 'on_error'],
    )

    text = StringProperty(defaultvalue='')
    text_align = OptionProperty(defaultvalue='left', options=('left', 'right', 'center'))

    placeholder = StringProperty(defaultvalue='')

    _cursor_color = ColorProperty(defaultvalue=(0, 0, 0, 0))
    _selection_color = ColorProperty(defaultvalue=(0, 0, 0, 0))
    _focus_border_color = ColorProperty(defaultvalue=(0, 0, 0, 0))
    _error_color = ColorProperty(defaultvalue=(0, 0, 0, 0))
    _placeholder_color = ColorProperty(defaultvalue=(0, 0, 0, 0))
    _text_color = ColorProperty(defaultvalue=(0, 0, 0, 0))
    _focus_text_color = ColorProperty(defaultvalue=(0, 0, 0, 0))
    _disabled_text_color = ColorProperty(defaultvalue=(0, 0, 0, 0))
    _label_color = ColorProperty(defaultvalue=(0, 0, 0, 0))
    _focus_label_color = ColorProperty(defaultvalue=(0, 0, 0, 0))
    _help_text_color = ColorProperty(defaultvalue=(0, 0, 0, 0))
    _focus_help_text_color = ColorProperty(defaultvalue=(0, 0, 0, 0))

    mask = StringProperty(defaultvalue='')
    '''
    "L" - Character of the Letter category required, such as A-Z, a-z.
    "l" - Character of the Letter category permitted but not required.

    "W" - Character of the Letter or Number category required, such as A-Z, a-z, 0-9.
    "w" - Character of the Letter or Number category permitted but not required.

    "X" - Any non-blank character required.
    "x" - Any non-blank character permitted but not required.

    "9" - Character of the Number category required, such as 0-9.
    "0" - Character of the Number category permitted but not required.

    "D" - Character of the Number category and larger than zero required, such as 1-9.
    "d" - Character of the Number category and larger than zero permitted but not required, such as 1-9.

    "#" - plus/minus sign permitted but not required.

    "H" - Hexadecimal character required. A-F, a-f, 0-9.
    "h" - Hexadecimal character permitted but not required.

    "B" - Binary character required. 0-1.
    "b" - Binary character permitted but not required.

    \\ - Use \\ to escape the special characters listed above to use them as separators.
    '''

    left_content = ObjectProperty(defaultvalue=None, allownone=True)
    right_content = ObjectProperty(defaultvalue=None, allownone=True)

    def __init__(self, *args, **kwargs) -> None:
        self._textfield = None

        self._mask = []
        self._mask_is_applied = False

        self._label = Label(text=' ', valign='center', halign='center', font_size=sp(12), font_name='Montserrat')
        self._help_text = Label(text=' ', valign='center', halign='center', font_size=sp(12), font_name='Montserrat')

        self.bind(cursor_color=self.setter('_cursor_color'))
        self.bind(selection_color=self.setter('_selection_color'))
        self.bind(focus_border_color=self.setter('_focus_border_color'))
        self.bind(error_color=self.setter('_error_color'))
        self.bind(placeholder_color=self.setter('_placeholder_color'))
        self.bind(text_color=self.setter('_text_color'))
        self.bind(focus_text_color=self.setter('_focus_text_color'))
        self.bind(disabled_text_color=self.setter('_disabled_text_color'))
        self.bind(label_color=self.setter('_label_color'))
        self.bind(focus_label_color=self.setter('_focus_label_color'))
        self.bind(help_text_color=self.setter('_help_text_color'))
        self.bind(focus_help_text_color=self.setter('_focus_help_text_color'))

        super().__init__(*args, **kwargs)

        Clock.schedule_once(self.set_default_colors, -1)
        Clock.schedule_once(self.initialize_textfield, -1)

    def on_parent(self, instance: Self, parent: Widget) -> None:
        if self._textfield is not None:
            if parent is None:
                self._textfield.unbind(focus=self.setter('focus'),
                                       text=self.setter('text'))
            else:
                self._textfield.bind(focus=self.setter('focus'),
                                     text=self.setter('text'))

        return super().on_parent(instance, parent)

    def _on_window_motion(self, window: WindowBase, etype: str, motionevent: MotionEvent) -> bool:
        '''Fired at the Window motion event.'''
        motionevent.scale_for_screen(window.width, window.height)
        if 'hover' == motionevent.type_id:
            if not self.disabled and self.get_root_window():
                pos = self.to_widget(*motionevent.pos)
                if self.ids.textfield.collide_point(*pos):

                    if self not in Window.children[0].walk():
                        return False

                    if not self._is_visible():
                        return False

                    if not self.hover:
                        if HoverBehavior.hovered_widget is not None:
                            HoverBehavior.hovered_widget.hover = False
                            HoverBehavior.hovered_widget.dispatch('on_leave')

                        HoverBehavior.hovered_widget = self
                        self.hover = True
                        self.dispatch('on_enter')

                elif self.hover:
                    HoverBehavior.hovered_widget = None
                    self.hover = False
                    self.dispatch('on_leave')

        return False

    def on_enter(self) -> None:
        Window.set_system_cursor('ibeam')

    def on_leave(self) -> None:
        Window.set_system_cursor('arrow')

    def initialize_textfield(self, *args) -> None:
        self._textfield = self.ids.textfield

        self._textfield.bind(focus=self.setter('focus'),
                             text=self.setter('text'))
        self._textfield.insert_text = self.insert_text

        for child in self.children[::-1]:
            if hasattr(child, 'content_position'):
                if child.content_position == 'right':
                    self.remove_widget(child)
                    self.right_content = child
                elif child.content_position == 'left':
                    self.remove_widget(child)
                    self.left_content = child

        if self.required:
            self.on_text(self, self.text)

    def on_left_content(self, instance: Self, value: Widget) -> None:
        if self.left_content is not None:
            self.left_content.pos_hint = {'center_y': 0.5}
            self.left_content.hidden = self.hidden
            Clock.schedule_once(lambda _: self.add_widget(self.left_content, index=2), -1)
            self.bind(hidden=self.left_content.setter('hidden'))

    def on_right_content(self, instance: Self, value: Widget) -> None:
        if self.right_content is not None:
            self.right_content.pos_hint = {'center_y': 0.5}
            self.right_content.hidden = self.hidden
            Clock.schedule_once(lambda _: self.add_widget(self.right_content, index=0), -1)
            self.bind(hidden=self.right_content.setter('hidden'))

    def set_default_colors(self, *args) -> None:
        self.background_color = 0, 0, 0, 0

        if self.bg_color is None:
            self._bg_color = self.theme_cls.background_color

        if self.border_color is None:
            self._border_color = self.theme_cls.background_dark_color

        if self.focus_border_color is None:
            self._focus_border_color = self.theme_cls.primary_color

        if self.text_color is None:
            self._text_color = self.theme_cls.text_color

        if self.focus_text_color is None:
            self._focus_text_color = self.theme_cls.text_color

        if self.disabled_text_color is None:
            self._disabled_text_color = self.theme_cls.disabled_color

        if self.label_color is None:
            self._label_color = self.theme_cls.secondary_text_color

        if self.focus_label_color is None:
            self._focus_label_color = self.theme_cls.primary_color

        if self.help_text_color is None:
            self._help_text_color = self.theme_cls.secondary_text_color

        if self.focus_help_text_color is None:
            self._focus_help_text_color = self.theme_cls.secondary_text_color

        if self.cursor_color is None:
            self._cursor_color = self.theme_cls.primary_light_color

        if self.placeholder_color is None:
            self._placeholder_color = self.theme_cls.secondary_text_color

        if self.selection_color is None:
            self._selection_color = self.theme_cls.primary_light_color[:3] + [.5]

        if self.error_color is None:
            self._error_color = self.theme_cls.error_color

    def on_theme_style(self, theme_manager: ThemeManager, theme_style: str) -> None:
        '''Fired when the app :attr:`theme_style` value changes.'''
        super().on_theme_style(theme_manager, theme_style)

        if self.bg_color is None:
            if self.theme_cls.theme_style_switch_animation:
                Animation(
                    _bg_color=self.theme_cls.background_color,
                    d=self.theme_cls.theme_style_switch_animation_duration,
                    t='linear',
                ).start(self)
            else:
                self._bg_color = self.theme_cls.background_color

        if self.border_color is None:
            if self.theme_cls.theme_style_switch_animation:
                Animation(
                    _border_color=self.theme_cls.background_dark_color,
                    d=self.theme_cls.theme_style_switch_animation_duration,
                    t='linear',
                ).start(self)
            else:
                self._border_color = self.theme_cls.background_dark_color

        if self.text_color is None:
            if self.theme_cls.theme_style_switch_animation:
                Animation(
                    _text_color=self.theme_cls.text_color,
                    d=self.theme_cls.theme_style_switch_animation_duration,
                    t='linear',
                ).start(self)
            else:
                self._text_color = self.theme_cls.text_color

        if self.disabled_text_color is None:
            if self.theme_cls.theme_style_switch_animation:
                Animation(
                    _disabled_text_color=self.theme_cls.disabled_color,
                    d=self.theme_cls.theme_style_switch_animation_duration,
                    t='linear',
                ).start(self)
            else:
                self._disabled_text_color = self.theme_cls.disabled_color

        if self.label_color is None:
            if self.theme_cls.theme_style_switch_animation:
                Animation(
                    _label_color=self.theme_cls.secondary_text_color,
                    d=self.theme_cls.theme_style_switch_animation_duration,
                    t='linear',
                ).start(self)
            else:
                self._label_color = self.theme_cls.secondary_text_color

        if self.help_text_color is None:
            if self.theme_cls.theme_style_switch_animation:
                Animation(
                    _help_text_color=self.theme_cls.secondary_text_color,
                    d=self.theme_cls.theme_style_switch_animation_duration,
                    t='linear',
                ).start(self)
            else:
                self._help_text_color = self.theme_cls.secondary_text_color

        if self.placeholder_color is None:
            if self.theme_cls.theme_style_switch_animation:
                Animation(
                    _placeholder_color=self.theme_cls.secondary_text_color,
                    d=self.theme_cls.theme_style_switch_animation_duration,
                    t='linear',
                ).start(self)
            else:
                self._placeholder_color = self.theme_cls.secondary_text_color

        if self.focus_text_color is None:
            self._focus_text_color = self.theme_cls.text_color

        if self.focus_help_text_color is None:
            self._focus_help_text_color = self.theme_cls.secondary_text_color

        if self.error_color is None:
            self._error_color = self.theme_cls.error_color

    def on_focus(self, instance: Self, value: bool) -> None:
        if not self.error:
            if self.focus:
                animation = (
                    Animation(_border_color=self._focus_border_color, d=.2)
                    & Animation(_text_color=self._focus_text_color, d=.2)
                    & Animation(_label_color=self._focus_label_color, d=.2)
                    & Animation(_help_text_color=self._focus_help_text_color, d=.2))
                animation.start(self)
            else:
                animation = (
                    Animation(_border_color=self.border_color if self.border_color else self.theme_cls.background_dark_color, d=.2)
                    & Animation(_text_color=self.text_color if self.text_color else self.theme_cls.text_color, d=.2)
                    & Animation(_label_color=self.label_color if self.label_color else self.theme_cls.secondary_text_color, d=.2)
                    & Animation(_help_text_color=self.help_text_color if self.help_text_color else self.theme_cls.secondary_text_color, d=.2))
                animation.start(self)

    def on_error(self, instance: Self, value: bool) -> None:
        if self.error:
            animation = (
                Animation(_border_color=self._error_color, d=.2)
                & Animation(_text_color=self._error_color, d=.2)
                & Animation(_label_color=self._error_color, d=.2)
                & Animation(_help_text_color=self._error_color, d=.2))
            animation.start(self)
        else:
            self.on_focus(self, self.focus)

    def on_label(self, instance: Self, value: str) -> None:
        self._label.text = ' ' + self.label + ' '

    def on_help_text(self, instance: Self, value: str) -> None:
        self._help_text.text = self.help_text

    def on_placeholder(self, instance: Self, value: str) -> None:
        self.ids.textfield.hint_text = self.placeholder

    def _apply_mask(self, text: str, fill: bool = True) -> None:

        def get_text_character(text: str, text_position: int) -> str:
            character = ''
            if text_position < len(text):
                character = text[text_position]
            return character

        masked_text = ''
        text_position = 0
        mask_position = 0
        text_character = get_text_character(text, text_position)

        while mask_position < len(self._mask):
            char = self._get_masked_character(self._mask[mask_position], text_character)
            if char != 'next':
                if char == 'empty':
                    if fill:
                        masked_text += ' '
                else:
                    masked_text += char
                text_position += 1
                text_character = get_text_character(text, text_position)
            mask_position += 1

        self._mask_is_applied = True

        return masked_text

    def _get_masked_character(self, mask: str, char: str) -> str:
        if mask[0] == '\\':
            return mask[1]

        if mask in {'L', 'l'} and char.isalpha():
            return char
        if mask in {'W', 'w'} and (char.isalpha() or char.isdigit()):
            return char
        if mask in {'X', 'x'} and char != ' ':
            return char
        if mask in {'9', '0'} and char.isdigit():
            return char
        if mask in {'D', 'd'} and char.isdigit() and char != '0':
            return char
        if mask == '#' and char in {'+', '-'}:
            return char
        if mask in {'H', 'h'} and (char.isdigit() or char in {'A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e', 'F', 'f'}):
            return char
        if mask in {'B', 'b'} and char in {'0', '1'}:
            return char
        if mask in {'l', 'w', 'x', '0', 'd', '#', 'h', 'b'}:
            return 'next'
        if mask in {'L', 'W', 'X', '9', 'D', 'H', 'B'}:
            return 'empty'

        return mask

    def on_mask(self, instance: Self, value: str) -> None:
        mask = list(self.mask)
        self._mask = []
        while len(mask):
            char = mask.pop(0)
            if char == '\\':
                self._mask.append('\\' + mask.pop(0))
            else:
                self._mask.append(char)

        self.on_text(self, self.text)

    def on_text(self, instance: Self, text: str) -> None:
        if len(self._mask) and not self._mask_is_applied:
            self.text = self._apply_mask(text)
            self._mask_is_applied = False

        if self.required:
            if len(self.mask):
                self.error = self.text != self._apply_mask(self.text, fill=False)
                self._mask_is_applied = False
            else:
                self.error = len(self.text) == 0

    def insert_text(self, substring: str, from_undo: bool = False) -> None:
        return TextInput.insert_text(self.ids.textfield, substring, from_undo=from_undo)
