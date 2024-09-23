__all__ = ('GlowTextField', )

from kivy_glow.uix.boxlayout import GlowBoxLayout
from kivy_glow.uix.behaviors import HoverBehavior
from kivy.input.motionevent import MotionEvent
from kivy.uix.textinput import TextInput
from kivy_glow import kivy_glow_uix_dir
from kivy.animation import Animation
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.metrics import sp
from typing import Self
import os
from kivy.core.window import (
    WindowBase,
    Window,
)
from kivy.properties import (
    NumericProperty,
    ObjectProperty,
    OptionProperty,
    StringProperty,
    ColorProperty,
    BooleanProperty
)

with open(
    os.path.join(kivy_glow_uix_dir, 'textfield', 'textfield.kv'), encoding='utf-8'
) as kv_file:
    Builder.load_string(kv_file.read())


class GlowTextField(HoverBehavior,
                    GlowBoxLayout):
    font_size = NumericProperty('16sp')

    cursor_color = ColorProperty(None, allownone=True)
    selection_color = ColorProperty(None, allownone=True)

    focus_border_color = ColorProperty(None, allownone=True)
    error_color = ColorProperty(None, allownone=True)

    placeholder_color = ColorProperty(None, allownone=True)

    text_color = ColorProperty(None, allownone=True)
    focus_text_color = ColorProperty(None, allownone=True)
    disabled_text_color = ColorProperty(None, allownone=True)

    label_color = ColorProperty(None, allownone=True)
    focus_label_color = ColorProperty(None, allownone=True)

    help_text_color = ColorProperty(None, allownone=True)
    focus_help_text_color = ColorProperty(None, allownone=True)

    focus = BooleanProperty(False)
    password = BooleanProperty(False)
    error = BooleanProperty(False)
    readonly = BooleanProperty(False)
    required = BooleanProperty(False)
    multiline = BooleanProperty(False)

    mode = OptionProperty('overlap', options=('overlap', 'inside', 'outside'))
    border_style = OptionProperty('full', options=('full', 'underline'))

    use_handles = BooleanProperty(None, allownone=True)
    use_bubble = BooleanProperty(None, allownone=True)

    label = StringProperty('')
    label_position = OptionProperty('left', options=('left', 'right', 'center'))

    help_text = StringProperty('')
    help_text_position = OptionProperty('left', options=('left', 'right', 'center'))
    help_text_mode = OptionProperty(
        'persistent', options=['persistent', 'on_focus', 'on_error']
    )

    text = StringProperty('')
    text_align = OptionProperty('left', options=('left', 'right', 'center'))

    placeholder = StringProperty('')

    _cursor_color = ColorProperty((0, 0, 0, 0))
    _selection_color = ColorProperty((0, 0, 0, 0))
    _placeholder_color = ColorProperty((0, 0, 0, 0))
    _text_color = ColorProperty((0, 0, 0, 0))
    _label_color = ColorProperty((0, 0, 0, 0))
    _help_text_color = ColorProperty((0, 0, 0, 0))
    _disabled_text_color = ColorProperty((0, 0, 0, 0))

    mask = StringProperty('')
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
    '''  # noqa W605

    left_content = ObjectProperty(None, allownone=True)
    right_content = ObjectProperty(None, allownone=True)

    def __init__(self, *args, **kwargs):
        self._textfield = None

        self._mask = []
        self._mask_is_applied = False

        self._label = Label(text=' ', valign='center', halign='center', font_size=sp(12), font_name='Montserrat')
        self._help_text = Label(text=' ', valign='center', halign='center', font_size=sp(12), font_name='Montserrat')

        self.bind(label_color=self.setter('_label_color'))
        self.bind(help_text_color=self.setter('_help_text_color'))
        self.bind(text_color=self.setter('_text_color'))
        self.bind(selection_color=self.setter('_selection_color'))
        self.bind(placeholder_color=self.setter('_placeholder_color'))
        self.bind(cursor_color=self.setter('_cursor_color'))
        self.bind(disabled_text_color=self.setter('_disabled_text_color'))

        super().__init__(*args, **kwargs)

        Clock.schedule_once(self.set_default_colors, -1)
        Clock.schedule_once(self.initialize_textfield, -1)

    def on_parent(self, instance: Self, parent) -> None:
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

                else:
                    if self.hover:
                        HoverBehavior.hovered_widget = None
                        self.hover = False
                        self.dispatch('on_leave')

        return False

    def on_enter(self):
        Window.set_system_cursor('ibeam')

    def on_leave(self):
        Window.set_system_cursor('arrow')

    def initialize_textfield(self, *args):
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

    def on_left_content(self, _, __):
        if self.left_content is not None:
            self.left_content.pos_hint = {'center_y': 0.5}
            self.left_content.hidden = self.hidden
            Clock.schedule_once(lambda _: self.add_widget(self.left_content, index=2), -1)

    def on_right_content(self, _, __):
        if self.right_content is not None:
            self.right_content.pos_hint = {'center_y': 0.5}
            self.right_content.hidden = self.hidden
            Clock.schedule_once(lambda _: self.add_widget(self.right_content, index=0), -1)

    def set_default_colors(self, *args):
        self.background_color = 0, 0, 0, 0

        if self.bg_color is None:
            self.bg_color = self.theme_cls.background_color

        if self.border_color is None:
            self.border_color = self.theme_cls.background_dark_color

        if self.focus_border_color is None:
            self.focus_border_color = self.theme_cls.primary_color

        if self.text_color is None:
            self.text_color = self.theme_cls.text_color

        if self.focus_text_color is None:
            self.focus_text_color = self.theme_cls.text_color

        if self.disabled_text_color is None:
            self.disabled_text_color = self.theme_cls.disabled_color

        if self.label_color is None:
            self.label_color = self.theme_cls.secondary_text_color

        if self.focus_label_color is None:
            self.focus_label_color = self.theme_cls.primary_color

        if self.help_text_color is None:
            self.help_text_color = self.theme_cls.secondary_text_color

        if self.focus_help_text_color is None:
            self.focus_help_text_color = self.theme_cls.secondary_text_color

        if self.cursor_color is None:
            self.cursor_color = self.theme_cls.primary_light_color

        if self.placeholder_color is None:
            self.placeholder_color = self.theme_cls.secondary_text_color

        if self.selection_color is None:
            self.selection_color = self.theme_cls.primary_light_color[:3] + [.5]

        if self.error_color is None:
            self.error_color = self.theme_cls.error_color

    def on_focus(self, _, __):
        if not self.error:
            if self.focus:
                animation = (
                    Animation(_border_color=self.focus_border_color, d=.2)
                    & Animation(_text_color=self.focus_text_color, d=.2)
                    & Animation(_label_color=self.focus_label_color, d=.2)
                    & Animation(_help_text_color=self.focus_help_text_color, d=.2))
                animation.start(self)
            else:
                animation = (
                    Animation(_border_color=self.border_color, d=.2)
                    & Animation(_text_color=self.text_color, d=.2)
                    & Animation(_label_color=self.label_color, d=.2)
                    & Animation(_help_text_color=self.help_text_color, d=.2))
                animation.start(self)

    def on_error(self, _, __):
        if self.error:
            animation = (
                Animation(_border_color=self.error_color, d=.2)
                & Animation(_text_color=self.error_color, d=.2)
                & Animation(_label_color=self.error_color, d=.2)
                & Animation(_help_text_color=self.error_color, d=.2))
            animation.start(self)
        else:
            self.on_focus(self, self.focus)

    def on_label(self, _, __):
        self._label.text = ' ' + self.label + ' '

    def on_help_text(self, _, __):
        self._help_text.text = self.help_text

    def on_placeholder(self, _, __):
        self.ids.textfield.hint_text = self.placeholder

    def _apply_mask(self, text, fill: bool = True):

        def get_text_character(text, text_position):
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

    def _get_masked_character(self, mask, char):
        if mask[0] == '\\':
            return mask[1]
        else:
            if mask in ('L', 'l') and char.isalpha():
                return char
            elif mask in ('W', 'w') and (char.isalpha() or char.isdigit()):
                return char
            elif mask in ('X', 'x') and char != ' ':
                return char
            elif mask in ('9', '0') and char.isdigit():
                return char
            elif mask in ('D', 'd') and char.isdigit() and char != '0':
                return char
            elif mask == '#' and char in ('+', '-'):
                return char
            elif mask in ('H', 'h') and (char.isdigit() or char in ('A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e', 'F', 'f')):
                return char
            elif mask in ('B', 'b') and char in ('0', '1'):
                return char
            elif mask in ('l', 'w', 'x', '0', 'd', '#', 'h', 'b'):
                return 'next'
            elif mask in ('L', 'W', 'X', '9', 'D', 'H', 'B'):
                return 'empty'
            else:
                return mask

        return ''

    def on_mask(self, _, __):
        mask = list(self.mask)
        self._mask = []
        while len(mask):
            char = mask.pop(0)
            if char == '\\':
                self._mask.append('\\' + mask.pop(0))
            else:
                self._mask.append(char)

        self.on_text(self, self.text)

    def on_text(self, _, text):
        if len(self._mask) and not self._mask_is_applied:
            self.text = self._apply_mask(text)
            self._mask_is_applied = False

        if self.required:
            if len(self.mask):
                self.error = self.text != self._apply_mask(self.text, False)
                self._mask_is_applied = False
            else:
                self.error = len(self.text) == 0

    def insert_text(self, substring, from_undo=False):
        return TextInput.insert_text(self.ids.textfield, substring, from_undo=from_undo)
