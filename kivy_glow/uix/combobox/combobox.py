__all__ = ('GlowComboBox', )

from typing import Self

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    ListProperty,
    NumericProperty,
    OptionProperty,
    StringProperty,
)
from kivy.uix.widget import Widget

from kivy_glow.theme import ThemeManager
from kivy_glow.uix.button import GlowButton
from kivy_glow.uix.dropdowncontainer import GlowDropDownContainer
from kivy_glow.uix.textfield import GlowTextField


class GlowComboBox(GlowTextField):
    '''Widget for selecting an item from a list

    This widget uses  :class:`~kivy_glow.uix.dropdowncontainer.GlowDropDownContainer` to display a dropdown list.

    For more information, see in the
    :class:`~kivy_glow.uix.textfield.GlowTextField` and
    :class:`~kivy_glow.uix.dropdowncontainers.GlowDropDownContainer`
    classes documentation.
    '''

    items = ListProperty()
    '''Avaliable items for select

    :attr:`items` is an :class:`~kivy.properties.ListProperty`.
    '''

    selected_item = StringProperty(defaultvalue=None)
    '''Current selected item

    :attr:`active` is an :class:`~kivy.properties.StringProperty`
    '''

    direction = OptionProperty(defaultvalue='down', options=('down', 'up'))
    '''Expansion direction

    :attr:`direction` is an :class:`~kivy.properties.OptionProperty`
    and default to `down`.
    '''

    use_separator = BooleanProperty(defaultvalue=True)
    '''Whether to add a separator between elements

    :attr:`use_separator` is an :class:`~kivy.properties.BooleanProperty`.
    and default to `True`.
    '''

    icon = StringProperty(defaultvalue='unfold-more-horizontal')
    '''Combobox icon

    :attr:`icon` is an :class:`~kivy.properties.StringProperty`
    and default to `unfold-more-horizontal`.
    '''

    selected_item_icon = StringProperty(defaultvalue='check')
    '''Icon for selected item

    :attr:`selected_item_icon` is an :class:`~kivy.properties.StringProperty`
    and default to `check`.
    '''

    item_text_color = ColorProperty(defaultvalue=None, allownone=True)
    '''The color in (r, g, b, a) or string format of the item text

    :attr:`item_text_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    selected_item_icon_color = ColorProperty(defaultvalue=None, allownone=True)
    '''The color in (r, g, b, a) or string format of the selected item icon

    :attr:`selected_item_icon_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    selected_item_text_color = ColorProperty(defaultvalue=None, allownone=True)
    '''The color in (r, g, b, a) or string format of the selected item text

    :attr:`selected_item_text_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    max_height = NumericProperty(defaultvalue=None, allownone=True)
    '''Maximum expansion height

    :attr:`max_height` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `None`.
    '''

    opening_transition = StringProperty(defaultvalue='out_cubic')
    '''Transition for opening animation

    :attr:`opening_transition` is an :class:`~kivy.properties.StringProperty`
    and defaults to `out_cubic`.
    '''

    opening_time = NumericProperty(defaultvalue=.2)
    '''Diration for opening animation

    :attr:`opening_time` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `.2`.
    '''

    closing_transition = StringProperty(defaultvalue='out_sine')
    '''Transition for closing animation

    :attr:`closing_transition` is an :class:`~kivy.properties.StringProperty`
    and defaults to `out_sine`.
    '''

    closing_time = NumericProperty(defaultvalue=.2)
    '''Duration for closing animation

    :attr:`closing_time` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `.2`.
    '''

    button_icon_color = ColorProperty(defaultvalue=None, allownonw=True)
    '''Button icon color

    :attr:`button_icon_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    button_border_color = ColorProperty(defaultvalue=None, allownonw=True)
    '''Button border color

    :attr:`button_border_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    dropdown_bg_color = ColorProperty(defaultvalue=None, allownonw=True)
    '''Dropdown bg color

    :attr:`dropdown_bg_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    _item_text_color = ColorProperty(defaultvalue=(0, 0, 0, 0))
    _selected_item_icon_color = ColorProperty(defaultvalue=(0, 0, 0, 0))
    _selected_item_text_color = ColorProperty(defaultvalue=(0, 0, 0, 0))

    def __init__(self, *args, **kwargs) -> None:
        self.bind(item_text_color=self.setter('_item_text_color'))
        self.bind(selected_item_icon_color=self.setter('_selected_item_icon_color'))
        self.bind(selected_item_text_color=self.setter('_selected_item_text_color'))
        self.dropdown_container = None

        super().__init__(*args, **kwargs)

        self.readonly = True
        self.text_align = 'right'

        self.register_event_type('on_pre_open')

        Clock.schedule_once(self.initialize_combobox, -1)

    def on_parent(self, instance: Self, parent: Widget) -> None:
        if self.dropdown_container is not None:
            if parent is None:
                self.unbind(width=self.dropdown_container.setter('min_width'))
            else:
                self.bind(width=self.dropdown_container.setter('min_width'))

        return super().on_parent(instance, parent)

    def on_enter(self) -> None:
        '''Fired at the Checkbox hover enter event.'''
        pass

    def on_leave(self) -> None:
        '''Fired at the Checkbox hover leave event.'''
        pass

    def on_items(self, combobox: Self, items: list) -> None:
        '''Fired when the :attr:`items` value changes.'''
        if self.selected_item not in items:
            self.selected_item = items[0]

    def on_selected_item(self, combobox: Self, selected_item: str) -> None:
        '''Fired when the :attr:`selected_item` value changes.'''
        self.text = self.selected_item

    def _open(self, *args) -> None:
        '''Open Combobox.'''
        if self.dropdown_container._state == 'closed' and not self.dropdown_container._anim_playing:
            self.dispatch('on_pre_open')
            self.dropdown_container.items = [
                GlowButton(text_color=self._item_text_color,
                           adaptive_height=True,
                           mode='text',
                           text=item,

                           on_release=lambda _, item=item: self._select_item(item))
                if item != self.selected_item else
                GlowButton(text_color=self._selected_item_text_color,
                           icon_color=self._selected_item_icon_color,
                           icon=self.selected_item_icon,
                           adaptive_height=True,
                           icon_size=dp(16),
                           mode='text',
                           text=item,

                           on_release=lambda _, item=item: self._select_item(item))
                for item in self.items
            ]
            self.dropdown_container.open(self)

    def _select_item(self, item: str) -> None:
        '''Fired at the Combobox item on_release event.'''
        self.selected_item = item
        self.dropdown_container.dismiss()

    def initialize_combobox(self, *args) -> None:
        '''Initializing the Combobox.'''
        self.button_open = GlowButton(
            border_color=self.button_border_color,
            icon_color=self.button_icon_color,
            adaptive_size=True,
            icon_size=dp(16),
            mode='outline',
            icon=self.icon,

            on_release=self._open,
        )
        self.dropdown_container = GlowDropDownContainer(
            opening_transition=self.opening_transition,
            closing_transition=self.closing_transition,
            use_separator=self.use_separator,
            bg_color=self.dropdown_bg_color,
            opening_time=self.opening_time,
            closing_time=self.closing_time,
            max_height=self.max_height,
            direction=self.direction,
            min_width=self.width,
        )

        self.bind(button_icon_color=self.button_open.setter('icon_color'),
                  button_border_color=self.button_open.setter('border_color'))

        self.bind(width=self.dropdown_container.setter('min_width'),
                  dropdown_bg_color=self.dropdown_container.setter('bg_color'),
                  use_separator=self.dropdown_container.setter('use_separator'))

        self.right_content = self.button_open
        self.ids.textfield.disabled = True

    def set_default_colors(self, *args) -> None:
        '''Set defaults colors.'''
        super().set_default_colors()

        if self.item_text_color is None:
            self._item_text_color = self.theme_cls.text_color

        if self.selected_item_icon_color is None:
            self._selected_item_icon_color = self.theme_cls.primary_color

        if self.selected_item_text_color is None:
            self._selected_item_text_color = self.theme_cls.primary_color

    def on_pre_open(self) -> None:
        '''Fires before the ComboVox is opened.'''
        pass

    def on_theme_style(self, theme_manager: ThemeManager, theme_style: str) -> None:
        super().on_theme_style(theme_manager, theme_style)

        if self.item_text_color is None:
            self._item_text_color = self.theme_cls.text_color
