__all__ = ('GlowDropDown', 'GlowSelectableDropDown')

from kivy_glow.uix.dropdowncontainer import GlowDropDownContainer
from kivy_glow.uix.button import GlowButton
from kivy.clock import Clock
from kivy.metrics import dp
from typing import Self
from kivy.properties import (
    NumericProperty,
    StringProperty,
    OptionProperty,
    ColorProperty,
    ListProperty,
)


class GlowDropDown(GlowButton):
    '''Widget for creating a drop-down list.

    :Events:
        :attr:`on_selected_item`
            Called when one of the items is selected

    It doesn't save the selected value

    This widget uses  :class:`~kivy_glow.uix.dropdowncontainer.GlowDropDownContainer` to display a dropdown list.

    For more information, see in the
    :class:`~kivy_glow.uix.button.GlowButton` and
    :class:`~kivy_glow.uix.dropdowncontainer.GlowDropDownContainer`
    classes documentation.
    '''

    items = ListProperty()
    '''Avaliable items for select

    :attr:`items` is an :class:`~kivy.properties.ListProperty`.
    '''

    direction = OptionProperty('down', options=('down', 'up'))
    '''Expansion direction

    :attr:`direction` is an :class:`~kivy.properties.OptionProperty`
    and default to `down`.
    '''

    max_height = NumericProperty(None, allownone=True)
    '''Maximum expansion height

    :attr:`max_height` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `None`.
    '''

    opening_transition = StringProperty('out_cubic')
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

    item_text_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the item text

    :attr:`item_text_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    _item_text_color = ColorProperty((0, 0, 0, 0))

    def __init__(self, *args, **kwargs) -> None:
        self.bind(item_text_color=self.setter('_item_text_color'))
        self.dropdown_container = None

        super().__init__(*args, **kwargs)

        self.register_event_type('on_selected_item')

        Clock.schedule_once(self.set_default_colors, -1)
        Clock.schedule_once(self.initialize_dropdown, -1)

    def on_parent(self, instance: Self, parent) -> None:
        if self.dropdown_container is not None:
            if parent is None:
                self.unbind(width=self.dropdown_container.setter('min_width'))
            else:
                self.bind(width=self.dropdown_container.setter('min_width'))

        return super().on_parent(instance, parent)

    def on_release(self) -> None:
        '''Fired at the DropDown on_release event.'''
        self._open()

    def on_selected_item(self, selected_item: str) -> None:
        '''Fired at the DropDown on_selected_item event.'''
        pass

    def _open(self, *args) -> None:
        '''Open DropDown.'''
        self.dropdown_container.items = [
            GlowButton(adaptive_height=True,
                       mode='text',
                       text=item,
                       text_color=self._item_text_color,
                       on_release=lambda _, item=item: self._select_item(item))
            for item in self.items
        ]
        self.dropdown_container.open(self)

    def _select_item(self, item: str) -> None:
        '''Fired at the DropDown item on_release event.'''
        self.dispatch('on_selected_item', item)
        self.dropdown_container.dismiss()

    def initialize_dropdown(self, *args) -> None:
        '''Initializing the DropDown.'''
        self.dropdown_container = GlowDropDownContainer(
            opening_transition=self.opening_transition,
            closing_transition=self.closing_transition,
            opening_time=self.opening_time,
            closing_time=self.closing_time,
            max_height=self.max_height,
            direction=self.direction,
            min_width=self.width,
        )
        self.bind(width=self.dropdown_container.setter('min_width'))

    def set_default_colors(self, *args) -> None:
        '''Set defaults colors.'''
        super().set_default_colors()

        if self.item_text_color is None:
            self.item_text_color = self.theme_cls.text_color


class GlowSelectableDropDown(GlowButton):
    '''Widget for creating a drop-down list.

    It doesn't save the selected value

    This widget uses  :class:`~kivy_glow.uix.dropdowncontainer.GlowDropDownContainer` to display a dropdown list.

    For more information, see in the
    :class:`~kivy_glow.uix.button.GlowButton` and
    :class:`~kivy_glow.uix.dropdowncontainer.GlowDropDownContainer`
    classes documentation.
    '''

    items = ListProperty()
    '''Avaliable items for select

    :attr:`items` is an :class:`~kivy.properties.ListProperty`.
    '''

    selected_item = StringProperty()
    '''Current selected item

    :attr:`active` is an :class:`~kivy.properties.StringProperty`
    '''

    direction = OptionProperty('down', options=('down', 'up'))
    '''Expansion direction

    :attr:`direction` is an :class:`~kivy.properties.OptionProperty`
    and default to `down`.
    '''

    max_height = NumericProperty(None, allownone=True)
    '''Maximum expansion height

    :attr:`max_height` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `None`.
    '''

    opening_transition = StringProperty('out_cubic')
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

    selected_item_icon = StringProperty('check')
    '''Icon for selected item

    :attr:`selected_item_icon` is an :class:`~kivy.properties.StringProperty`
    and default to `check`.
    '''

    item_text_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the item text

    :attr:`item_text_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    selected_item_text_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the selected item text

    :attr:`selected_item_text_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    selected_item_icon_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the selected item icon

    :attr:`selected_item_icon_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    _item_text_color = ColorProperty((0, 0, 0, 0))
    _selected_item_icon_color = ColorProperty((0, 0, 0, 0))
    _selected_item_text_color = ColorProperty((0, 0, 0, 0))

    def __init__(self, *args, **kwargs) -> None:
        self.bind(item_text_color=self.setter('_item_text_color'))
        self.bind(selected_item_icon_color=self.setter('_selected_item_icon_color'))
        self.bind(selected_item_text_color=self.setter('_selected_item_text_color'))
        self.dropdown_container = None

        super().__init__(*args, **kwargs)

        Clock.schedule_once(self.set_default_colors, -1)
        Clock.schedule_once(self.initialize_selectable_dropdown, -1)

    def on_parent(self, instance: Self, parent) -> None:
        if self.dropdown_container is not None:
            if parent is None:
                self.unbind(width=self.dropdown_container.setter('min_width'))
            else:
                self.bind(width=self.dropdown_container.setter('min_width'))

        return super().on_parent(instance, parent)

    def on_release(self) -> None:
        '''Fired at the DropDown on_release event.'''
        self._open()

    def on_items(self, combobox: Self, items: list) -> None:
        '''Fired when the :attr:`items` value changes.'''
        self.selected_item = items[0]

    def _open(self, *args) -> None:
        '''Open DropDown.'''
        self.dropdown_container.items = [
            GlowButton(adaptive_height=True,
                       mode='text',
                       text=item,
                       text_color=self._item_text_color,
                       icon_color=self._selected_item_icon_color,
                       on_release=lambda _, item=item: self._select_item(item))
            if item != self.selected_item else
            GlowButton(adaptive_height=True,
                       mode='text',
                       text=item,
                       text_color=self._selected_item_text_color,
                       icon_color=self._selected_item_icon_color,
                       icon=self.selected_item_icon,
                       icon_size=dp(16),
                       on_release=lambda _, item=item: self._select_item(item))
            for item in self.items
        ]
        self.dropdown_container.open(self)

    def _select_item(self, item: str) -> None:
        '''Fired at the DropDown item on_release event.'''
        self.selected_item = item
        self.dropdown_container.dismiss()

    def initialize_selectable_dropdown(self, *args) -> None:
        '''Initializing the DropDown.'''
        self.dropdown_container = GlowDropDownContainer(
            opening_transition=self.opening_transition,
            closing_transition=self.closing_transition,
            opening_time=self.opening_time,
            closing_time=self.closing_time,
            max_height=self.max_height,
            direction=self.direction,
            min_width=self.width,
        )
        self.bind(width=self.dropdown_container.setter('min_width'))

    def set_default_colors(self, *args) -> None:
        '''Set defaults colors.'''
        super().set_default_colors()

        if self.item_text_color is None:
            self.item_text_color = self.theme_cls.text_color

        if self.selected_item_icon_color is None:
            self.selected_item_icon_color = self.theme_cls.primary_color

        if self.selected_item_text_color is None:
            self.selected_item_text_color = self.theme_cls.primary_color
