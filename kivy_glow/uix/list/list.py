__all__ = ('GlowList', 'GlowSelectableListItem', 'GlowListItem')

from kivy_glow.uix.recycleboxlayout import GlowRecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy_glow.effects.stiffscroll import StiffScrollEffect
from kivy_glow.uix.recycleview import GlowRecycleView
from kivy_glow.uix.boxlayout import GlowBoxLayout
from kivy_glow.uix.behaviors import HoverBehavior
from kivy.input.motionevent import MotionEvent
from kivy.uix.behaviors import ButtonBehavior
from kivy_glow import kivy_glow_uix_dir
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.metrics import dp
from typing import Self
import os
from kivy.properties import (
    NumericProperty,
    BooleanProperty,
    StringProperty,
    ObjectProperty,
    ColorProperty,
    ListProperty,
)

with open(
    os.path.join(kivy_glow_uix_dir, 'list', 'list.kv'), encoding='utf-8'
) as kv_file:
    Builder.load_string(kv_file.read())


class SelectableRecycleBoxLayout(LayoutSelectionBehavior, GlowRecycleBoxLayout):
    pass


class GlowSelectableListItem(GlowBoxLayout,
                             HoverBehavior,
                             ButtonBehavior,
                             RecycleDataViewBehavior):

    '''Your list item should inherit from GlowSelectableListItem or GlowListItem depending on whether you need checkboxes for selection.

    The list item doesn't contain any additional data, so you have to design your list item to be what you want.

    By default, the minimum height of each element is 56dp. But list elements can automatically adjust their height to the content, i.e. the height can be greater than or equal to 56dp.

    An example of creating a list item with an icon, main text and subdext:
        .. code-block:: kv
        list_item = """
        <ListItem@GlowSelectableListItem>:
            icon: 'blank'
            main_text: ''
            second_text: ''
            GlowIcon:
                icon: root.icon
            GlowBoxLayout:
                orientation: 'vertical'
                adaptive_height: True
                GlowLabel:
                    adaptive_height: True
                    text: root.main_text
                    font_style: 'BodyL'
                GlowLabel:
                    adaptive_height: True
                    text: root.second_text
                    font_style: 'LabelM'
        """
        Builder.load_string(list_item)
        list_variant_1 = GlowList(
            list_data=[('android', 'item_main_text', 'item_second_text') for i in range(10)],
            item_properties=['icon', 'main_text', 'second_text'],
            viewclass='ListItem',
        )

        list_variant_2 = GlowList(
            list_data=[{'icon': 'android', 'main_text':'item_main_text', 'second_text': 'item_second_text'} for i in range(10)],
            viewclass='ListItem',
        )

    For more information, see in the
    :class:`~kivy_glow.uix.boxlayout.GlowBoxLayout` and
    :class:`~kivy_glow.uix.behaviors.HoverBehavior` and
    :class:`~kivy.uix.behaviors.ButtonBehavior` and
    :class:`~kivy.uix.recycleview.views.RecycleDataViewBehavior`
    classes documentation.
    '''

    selected = BooleanProperty(False)
    '''If item is selected.

    You cannot change this value, the checkbox will still be enabled.

    :attr:`selected` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    '''

    _index = NumericProperty(None, allownone=True)
    _clicked = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size_hint_y = None
        Clock.schedule_once(self.initialize_selectablelistitem, -1)

    def refresh_view_attrs(self, recycleview_instance: GlowRecycleView, index: int, data: dict) -> None:
        '''Catch and handle the view changes.'''

        setattr(self, 'idx', data['idx'])
        self.opacity = 0

        super().refresh_view_attrs(recycleview_instance, index, data)

        self.bg_color = self.item_bg_color
        self._index = index
        self.do_layout()

        Clock.schedule_once(self._set_visible)

    def on_enter(self) -> None:
        '''Fired at the SelectableListItem hover enter event.'''
        self.bg_color = self.hover_item_bg_color

    def on_leave(self) -> None:
        '''Fired at the SelectableListItem hover leave event.'''
        self.bg_color = self.item_bg_color

    def on_touch_down(self, touch: MotionEvent) -> bool:
        '''Fired at the SelectableListItem on_touch_down event.'''
        if not self.collide_point(touch.x, touch.y):
            return False

        if self.ids.item_checkbox.collide_point(*touch.pos) and not self.ids.item_checkbox.disabled:
            self._clicked = True
            self.ids.item_checkbox.on_touch_down(touch)
            self.parent.select_with_touch(self._index, touch)
            self.list.dispatch('on_item_selected', self)
            return True

        self.list.dispatch('on_item_press', self)
        return True

    def apply_selection(self, recycleview_instance: GlowRecycleView, index: int, is_selected: bool) -> None:
        '''Internal item selection processing function.'''
        self.selected = is_selected
        if not self._clicked and 'item_checkbox' in self.ids:
            self.ids.item_checkbox.active = self.selected
        else:
            self.list._selected_items[self.idx] = is_selected

        self._clicked = False

    def _set_visible(self, *args) -> None:
        '''Restore item visibility after updating data.'''
        self.height = max(dp(56), self.minimum_height)
        self.opacity = 1

    def initialize_selectablelistitem(self, *args) -> None:
        '''Initializing the GlowSelectableListItem.'''
        checkbox = self.ids.item_checkbox
        self.remove_widget(checkbox)
        self.add_widget(checkbox, len(self.children))


class GlowListItem(GlowBoxLayout,
                   HoverBehavior,
                   ButtonBehavior,
                   RecycleDataViewBehavior):

    '''Inheritance class to create your own list item without selectability.

    Simple example with text:
        .. code-block:: kv
        list_item = """
        <ListItem@GlowListItem>:
            text: ''
            GlowLabel:
                adaptive_height: True
                text: root.text
        """
        Builder.load_string(list_item)
        list_variant_1 = GlowList(
            list_data=['item_text' for i in range(10)],
            viewclass='ListItem',
        )

        list_variant_2 = GlowList(
            list_data=[{'text': 'item_text'} for i in range(10)],
            viewclass='ListItem',
        )

        list_variant_1 = GlowList(
            list_data=['item_text' for i in range(10)],
            item_properties=['text'],
            viewclass='ListItem',
        )

    For more information, see in the
    :class:`~kivy_glow.uix.boxlayout.GlowBoxLayout` and
    :class:`~kivy_glow.uix.behaviors.HoverBehavior` and
    :class:`~kivy.uix.behaviors.ButtonBehavior` and
    :class:`~kivy.uix.recycleview.views.RecycleDataViewBehavior`
    classes documentation.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size_hint_y = None

    def refresh_view_attrs(self, recycleview_instance: GlowRecycleView, index: int, data: dict) -> None:
        ''' Catch and handle the view changes.'''

        setattr(self, 'idx', data['idx'])
        self.opacity = 0

        super().refresh_view_attrs(recycleview_instance, index, data)
        self.bg_color = self.item_bg_color
        self.do_layout()

        Clock.schedule_once(self._set_visible)

    def on_enter(self) -> None:
        '''Fired at the SelectableListItem hover enter event.'''
        self.bg_color = self.hover_item_bg_color

    def on_leave(self) -> None:
        '''Fired at the SelectableListItem hover leave event.'''
        self.bg_color = self.item_bg_color

    def on_touch_down(self, touch: MotionEvent) -> bool:
        '''Fired at the ListItem on_touch_down event.'''
        if not self.collide_point(touch.x, touch.y):
            return False

        self.list.dispatch('on_item_press', self)
        return True

    def _set_visible(self, *args) -> None:
        '''Restore item visibility after updating data.'''
        self.height = max(dp(56), self.minimum_height)
        self.opacity = 1


class GlowList(GlowBoxLayout):

    '''
    Convenient and customizable list widget.
    '''

    list_data = ListProperty()
    '''List display data.

    There are three options for filling out this list:
    1. Indicate the details of each item in the list or container. For this option, you also need to indicate which properties each value should be associated with
    2. Specify the data of each item in the form of a dictionary, where the key is property and the value is value
    3. If an item has only one text widget, then the default property is text

    :attr:`list_data` is an :class:`~kivy.properties.list_data`
    '''

    item_properties = ListProperty(None, allownone=True)
    '''Properties list item. They will be applied in the same order as the values in the :attr:`list_data`

    Example:
        .. code-block:: kv
        GlowList(
            item_data=[('item_text', 'android') for i in range(10)],
            item_properties=['text', 'icon'],
        )
        # equal
        GlowList(
            item_data=[{'text': 'item_text', 'icon': 'android'} for i in range(10)],
        )

    :attr:`item_properties` is an :class:`~kivy.properties.ListProperty`
    and defaults to `None`.
    '''

    viewclass = StringProperty('GlowSelectableListItem')
    '''List item view class

    :attr:`viewclass` is an :class:`~kivy.properties.StringProperty`
    and defaults to `GlowSelectableListItem`.
    '''

    effect_cls = ObjectProperty(StiffScrollEffect)
    '''Effect applied to sroll

    :attr:`effect_cls` is an :class:`~kivy.properties.ObjectProperty`
    and defaults to `StiffScrollEffect`.
    '''

    odd_item_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the odd item

    :attr:`odd_item_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    even_item_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the even item

    :attr:`even_item_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    hover_item_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the hover item

    :attr:`hover_item_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    _odd_item_color = ColorProperty((0, 0, 0, 1))
    _even_item_color = ColorProperty((0, 0, 0, 1))
    _hover_item_color = ColorProperty((0, 0, 0, 1))

    _formatted_list_data = ListProperty()
    _selected_items = {}

    def __init__(self, *args, **kwargs) -> None:
        self.bind(odd_item_color=self.setter('_odd_item_color'))
        self.bind(even_item_color=self.setter('_even_item_color'))
        self.bind(hover_item_color=self.setter('_hover_item_color'))

        self.bind(_odd_item_color=lambda _, __: self.__update_colors())
        self.bind(_even_item_color=lambda _, __: self.__update_colors())
        self.bind(_hover_item_color=lambda _, __: self.__update_colors())

        super().__init__(*args, **kwargs)

        self.register_event_type('on_item_press')
        self.register_event_type('on_item_selected')

        Clock.schedule_once(self.set_default_colors, -1)
        self.orientation = 'vertical'

    @property
    def selected_items(self) -> list[int]:
        '''Returns the indexes of the selected items. Numbering of items as in :attr:`list_data`'''
        return [idx for idx, selected in self._selected_items.items() if selected]

    @property
    def selected_items_data(self) -> list[str | tuple | list | dict]:
        '''Returns selected items data.'''
        return [self.list_data[idx] for idx in self.selected_items]

    def on_list_data(self, list_instance: Self, list_data: list[str | tuple | list | dict]) -> None:
        '''Fired when the :attr:`list_data` value changes.'''
        self.__update_list_data()

    def on_item_properties(self, list_instance: Self, item_properties: list[str]) -> None:
        '''Fired when the :attr:`item_properties` value changes.'''
        self.__update_list_data()

    def on_item_press(self, item_instance: GlowSelectableListItem | GlowListItem) -> None:
        '''Fired at the item on_touch_down event.'''
        pass

    def on_item_selected(self, item_instance: GlowSelectableListItem | GlowListItem) -> None:
        '''Fired at the item selected event.'''
        pass

    def update_list_data(self) -> None:
        '''Updating display data.'''
        self.__update_list_data(False)

    def update_list_item_data(self, item_idx: int, item_data) -> None:
        '''Updating display data for item.'''
        formated_item_data = {}
        if isinstance(item_data, dict):
            formated_item_data = item_data
        else:
            formated_item_data['text'] = item_data

        formated_item_data['idx'] = item_idx
        if item_idx % 2 == 0:
            formated_item_data['item_bg_color'] = self._even_item_color
        else:
            formated_item_data['item_bg_color'] = self._odd_item_color

        formated_item_data['hover_item_bg_color'] = self._hover_item_color
        formated_item_data['list'] = self

        self._formatted_list_data[item_idx] = formated_item_data

    def select_all(self, is_selected: bool) -> None:
        '''Unselect or select checkboxes on the entire list.'''
        items = len(self._formatted_list_data)

        for idx in range(items):
            if is_selected:
                self.ids.glow_list_layout.select_node(idx)
            else:
                self.ids.glow_list_layout.deselect_node(idx)

            if idx in self._selected_items.keys():
                self._selected_items[idx] = is_selected

    def select_one(self, item_idx: int, is_selected: bool) -> None:
        '''Unselect or select checkbox on the list item.'''
        if is_selected:
            self.ids.glow_list_layout.select_node(item_idx)
        else:
            self.ids.glow_list_layout.deselect_node(item_idx)

        self._selected_items[item_idx] = is_selected

    def select_items(self, list_items_ids: list[int], is_selected: bool) -> None:
        '''Unselect or select checkbox on the list items.'''
        for item_idx in list_items_ids:
            self.select_one(item_idx, is_selected)

    def __update_list_data(self, update_selected_items: bool = True) -> None:
        '''Inner funciton for updating display data.'''
        if update_selected_items:
            self.select_all(False)
            self._selected_items = {i: False for i in range(len(self.list_data))}
        formatted_list_data = []

        for item_idx, item_data in enumerate(self.list_data):
            formated_item_data = {}
            if isinstance(item_data, dict):
                formated_item_data = item_data.copy()
            else:
                if self.item_properties is not None:
                    for item_property, value in (zip(self.item_properties, item_data)):
                        formated_item_data[item_property] = value
                else:
                    formated_item_data['text'] = item_data

            formated_item_data['idx'] = item_idx
            if item_idx % 2 == 0:
                formated_item_data['item_bg_color'] = self._even_item_color
            else:
                formated_item_data['item_bg_color'] = self._odd_item_color

            formated_item_data['hover_item_bg_color'] = self._hover_item_color
            formated_item_data['list'] = self
            formatted_list_data.append(formated_item_data)

        self._formatted_list_data = formatted_list_data

    def __update_colors(self, *args) -> None:
        '''Inner function for updating item colors.'''
        for item_idx, item_data in enumerate(self._formatted_list_data):
            if item_idx % 2 == 0:
                item_data['item_bg_color'] = self._even_item_color
            else:
                item_data['item_bg_color'] = self._odd_item_color

            item_data['hover_item_bg_color'] = self._hover_item_color

    def set_default_colors(self, *args) -> None:
        '''Set defaults colors.'''
        if self.bg_color is None:
            self.bg_color = self.theme_cls.background_darkest_color

        if self.odd_item_color is None:
            self.odd_item_color = self.theme_cls.background_darkest_color

        if self.even_item_color is None:
            self.even_item_color = self.theme_cls.background_darkest_color

        if self.hover_item_color is None:
            self.hover_item_color = self.theme_cls.background_dark_color

        self.__update_list_data()
