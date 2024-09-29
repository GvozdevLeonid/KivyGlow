__all__ = ('GlowNumberField', )

from kivy_glow.uix.boxlayout import GlowBoxLayout
from kivy_glow.uix.textfield import GlowTextField
from kivy_glow.uix.button import GlowButton
from kivy.clock import Clock
from kivy.metrics import dp
from typing import Self
import re
from kivy.properties import (
    NumericProperty,
    OptionProperty,
    StringProperty,
    AliasProperty,
    ColorProperty,
)


class GlowNumberField(GlowTextField):
    '''Widget for entering numbers (int and float)

    For more information, see in the :class:`~kivy_glow.uix.textfield.GlowTextField` class documentation.
    '''

    minimum = NumericProperty(1)
    '''Minimum possible number

    :attr:`minimum` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `1`.
    '''
    maximum = NumericProperty(100)
    '''Maximum possible number

    :attr:`maximum` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `100`.
    '''

    number_type = OptionProperty('int', options=('int', 'float'))
    '''If you select a float number, you can change the  :attr:`decimals`

    :attr:`number_type` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `int`.
    '''

    icon_up = StringProperty('chevron-up')
    '''Icon for button up

    :attr:`icon_up` is an :class:`~kivy.properties.StringProperty`
    and defaults to `chevron-up`.
    '''

    icon_down = StringProperty('chevron-down')
    '''Icon for button down

    :attr:`icon_down` is an :class:`~kivy.properties.StringProperty`
    and defaults to `chevron-down`.
    '''

    decimals = NumericProperty(2)
    '''Number of symbols after comma

    :attr:`decimals` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `2`.
    '''

    single_step = NumericProperty(1)
    '''Step to change number when clicking buttons

    :attr:`single_step` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `1`.
    '''

    button_icon_color = ColorProperty(None, allownonw=True)
    '''Button icon color

    :attr:`button_icon_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    button_border_color = ColorProperty(None, allownonw=True)
    '''Button border color

    :attr:`button_border_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    _value = NumericProperty(1)

    def __init__(self, *args, **kwargs) -> None:
        self._format_string = '{}'
        super().__init__(*args, **kwargs)

        Clock.schedule_once(self.initialize_numberfield, -1)
        self._set_value(self._value)

    def _get_value(self):
        '''Getter for value'''

        if self.text != self._format_string.format(self._value):
            return None

        return self._value

    def _set_value(self, value):
        '''Setter for value'''
        if self.minimum <= value <= self.maximum:
            if self.number_type == 'float':
                self._value = float(value)
            elif self.number_type == 'int':
                self._value = int(value)

            self.text = self._format_string.format(self._value)

        if hasattr(self, 'button_down'):
            if self._value == self.minimum:
                self.button_down.disabled = True
            elif self._value > self.minimum and self.button_down.disabled:
                self.button_down.disabled = False

        if hasattr(self, 'button_up'):
            if self._value == self.maximum:
                self.button_up.disabled = True
            elif self._value < self.maximum and self.button_up.disabled:
                self.button_up.disabled = False

    value = AliasProperty(_get_value, _set_value, bind=('text', '_value'))
    '''Current value

    :attr:`value` is an :class:`~kivy.properties.AliasProperty`
    and defaults to :attr:`minimum`.
    '''

    def on_minimum(self, numberfield_instance: Self, minimum: int | float) -> None:
        '''Fired when the :attr:`minimum` value changes.'''
        if self._value < minimum:
            self._set_value(minimum)

    def on_maximum(self, numberfield_instance: Self, maximum: int | float) -> None:
        '''Fired when the :attr:`maximum` value changes.'''
        if self._value > maximum:
            self._set_value(maximum)

    def on_decimals(self, numberfield_instance: Self, decimals: int) -> None:
        '''Fired when the :attr:`decimals` value changes.'''
        if self.number_type == 'int':
            self._format_string = '{}'

        elif self.number_type == 'float':
            self._format_string = f'{{:.{decimals}f}}'

        self._set_value(self._value)

    def on_number_type(self, numberfield_instance: Self, number_type: str) -> None:
        '''Fired when the :attr:`number_type` value changes.'''
        if number_type == 'int':
            self._format_string = '{}'

        elif number_type == 'float':
            self._format_string = f'{{:.{self.decimals}f}}'

        self._set_value(self._value)

    def on_text(self, numberfield_instance: Self, text: str) -> None:
        '''Fired when the :attr:`text` value changes.'''
        self.error = False
        error = True
        number = None
        if text != '':
            try:
                if self.number_type == 'int' and text not in ('', '-'):
                    number = int(text)

                elif self.number_type == 'float' and text.split('.')[0] not in ('', '-') and text.split('.')[1] not in (''):
                    number = float(text)

                if self.minimum <= number <= self.maximum:
                    self._set_value(number)
                    error = False

            except Exception:
                pass

        if error:
            self.error = True

    def on_focus(self, numberfield_instance: Self, focus: bool) -> None:
        '''Fired when the :attr:`focus` value changes.'''
        super().on_focus(self, focus)
        if not focus and ((self.text == '' and self.required) or self.error):
            self._set_value(self._value)

    def _up(self, button_instance: GlowButton) -> None:
        '''Increase current number.'''
        if self._value + self.single_step <= self.maximum:
            self._set_value(self._value + self.single_step)
            self._textfield.cursor = (0, 0)

    def _down(self, button_instance: GlowButton) -> None:
        '''Decrease current number.'''
        if self._value - self.single_step >= self.minimum:
            self._set_value(self._value - self.single_step)
            self._textfield.cursor = (0, 0)

    def insert_text(self, substring: str, from_undo: bool = False) -> None:
        pat = re.compile('[^0-9.-]')
        substring = re.sub(pat, '', substring)

        if '-' in substring:
            if self.text != '':
                cursor_pos = self._textfield.cursor_index()
                if cursor_pos != 0 or '-' in self.text:
                    substring = substring.replace('-', '')
                if self.text[cursor_pos:cursor_pos + 1] == '-':
                    self._textfield.cursor = (cursor_pos + 1, 0)

        if '.' in substring and '.' in self.text:
            cursor_pos = self._textfield.cursor_index()
            if self.text[cursor_pos:cursor_pos + 1] == '.':
                self._textfield.cursor = (cursor_pos + 1, 0)
            substring = substring.replace('.', '', 1)

        super().insert_text(substring, from_undo=from_undo)

    def initialize_numberfield(self, *args) -> None:
        '''Initializing the NumberField.'''
        if self.number_type == 'int':
            self._format_string = '{}'
        elif self.number_type == 'float':
            self._format_string = f'{{:.{self.decimals}f}}'

        if self.widget_style == 'mobile':
            self.text_align = 'center'
            self.button_up = GlowButton(adaptive_size=True, icon=self.icon_up, icon_color=self.button_icon_color, border_color=self.button_border_color, icon_size=dp(16), mode='outline', on_release=self._up, disabled=True if self._value == self.maximum else False, hidden=self.hidden)
            self.button_down = GlowButton(adaptive_size=True, icon=self.icon_down, icon_color=self.button_icon_color, border_color=self.button_border_color, icon_size=dp(16), mode='outline', on_release=self._down, disabled=True if self._value == self.minimum else False, hidden=self.hidden)

            self.left_content = self.button_down
            self.right_content = self.button_up

        else:
            self.text_align = 'right'
            self.button_up = GlowButton(adaptive_height=True,
                                        size_hint_x=None,
                                        width=dp(20),
                                        icon=self.icon_up,
                                        icon_color=self.button_icon_color,
                                        border_color=self.button_border_color,
                                        mode='outline',
                                        padding=[0, ],
                                        icon_size=dp(12),
                                        border_radius=['5dp', '5dp', 0, 0],
                                        border_width=[2, 2, 2, 1],
                                        on_release=self._up,
                                        disabled=True if self._value == self.maximum else False,
                                        hidden=self.hidden)

            self.button_down = GlowButton(adaptive_height=True,
                                          size_hint_x=None,
                                          width=dp(20),
                                          icon=self.icon_down,
                                          icon_color=self.button_icon_color,
                                          border_color=self.button_border_color,
                                          mode='outline',
                                          padding=[0, ],
                                          icon_size=dp(12),
                                          border_radius=[0, 0, '5dp', '5dp'],
                                          border_width=[2, 1, 2, 2],
                                          on_release=self._down,
                                          disabled=True if self._value == self.minimum else False,
                                          hidden=self.hidden)

            self.right_content = GlowBoxLayout(
                self.button_up,
                self.button_down,
                adaptive_size=True,
                orientation='vertical',
                padding=[0, ],
                spacing=0,
            )

        self.bind(button_icon_color=self.button_up.setter('icon_color'))
        self.bind(button_icon_color=self.button_down.setter('icon_color'))
        self.bind(button_border_color=self.button_up.setter('border_color'))
        self.bind(button_border_color=self.button_down.setter('border_color'))
