__all__ = ('GlowTable', )

import os
import uuid
from typing import Self

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.effects.scroll import ScrollEffect
from kivy.input.motionevent import MotionEvent
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    OptionProperty,
    StringProperty,
)
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.widget import Widget

import kivy_glow.uix.table.cells as table_cells
from kivy_glow import kivy_glow_uix_dir
from kivy_glow.theme import ThemeManager
from kivy_glow.uix.behaviors import HoverBehavior
from kivy_glow.uix.boxlayout import GlowBoxLayout
from kivy_glow.uix.button import GlowButton
from kivy_glow.uix.checkbox import GlowCheckbox
from kivy_glow.uix.paginator import GlowPaginator
from kivy_glow.uix.recycleboxlayout import GlowRecycleBoxLayout
from kivy_glow.uix.recycleview import GlowRecycleView

with open(
    os.path.join(kivy_glow_uix_dir, 'table', 'table.kv'), encoding='utf-8',
) as kv_file:
    Builder.load_string(kv_file.read())


def get_cell_property_connection(cell_idx: int, cell_property: str, cell_property_type: int, offset: int) -> str:
    if cell_property_type == 'str':
        return ' ' * offset + f'{cell_property}: str(root.col_{cell_idx}_{cell_property}) if root.col_{cell_idx}_{cell_property} is not None else ""\n'
    if cell_property_type == 'int':
        return ' ' * offset + f'{cell_property}: int(root.col_{cell_idx}_{cell_property}) if root.col_{cell_idx}_{cell_property} is not None else 0\n'
    if cell_property_type == 'float':
        return ' ' * offset + f'{cell_property}: float(root.col_{cell_idx}_{cell_property})if root.col_{cell_idx}_{cell_property} is not None else 0.0\n'
    if cell_property_type == 'bool':
        return ' ' * offset + f'{cell_property}: root.col_{cell_idx}_{cell_property}\n'
    if cell_property_type == 'tuple':
        return ' ' * offset + f'{cell_property}: tuple(root.col_{cell_idx}_{cell_property}) if root.col_{cell_idx}_{cell_property} is not None else ()\n'
    if cell_property_type == 'list':
        return ' ' * offset + f'{cell_property}: list(root.col_{cell_idx}_{cell_property}) if root.col_{cell_idx}_{cell_property} is not None else []\n'
    if cell_property_type == 'color':
        return ' ' * offset + f'{cell_property}: tuple(root.col_{cell_idx}_{cell_property}) if root.col_{cell_idx}_{cell_property} is not None else (0, 0, 0, 0)\n'
    if cell_property_type == 'function':
        return ' ' * offset + f'{cell_property}:\n' \
            + ' ' * (offset + 4) + f'root.col_{cell_idx}_{cell_property}(root.table, self) if root.col_{cell_idx}_{cell_property} is not None and not root.refreshing else None\n'

    return ' ' * offset + f'{cell_property}: root.col_{cell_idx}_{cell_property}\n'


class GlowTableRow(GlowBoxLayout,
                   HoverBehavior,
                   RecycleDataViewBehavior):

    index = NumericProperty(defaultvalue=None, allownone=True)
    selected = BooleanProperty(defaultvalue=False)

    _clicked = False
    refreshing = False

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.size_hint_y = None

    def refresh_view_attrs(self, instance: GlowRecycleView, index: int, data: dict) -> None:
        ''' Catch and handle the view changes '''
        self.opacity = 0
        self.refreshing = True

        self.idx = data['idx']
        super().refresh_view_attrs(instance, index, data)

        self.bg_color = self.row_bg_color
        self.index = index

        self.do_layout()

        Clock.schedule_once(self._set_visible)

    def _set_visible(self, *args) -> None:
        self.height = max(dp(56), self.minimum_height)
        self.opacity = 1
        self.refreshing = False

    def on_touch_down(self, touch: MotionEvent) -> bool:
        if not self.collide_point(touch.x, touch.y):
            return False

        if self.table.selectable and self.ids.row_checkbox.collide_point(*touch.pos) and not self.ids.row_checkbox.disabled:
            self._clicked = True
            self.ids.row_checkbox.on_touch_down(touch)
            self.parent.select_with_touch(self.index, touch)
            self.table.dispatch('on_row_selected', self)
            return True

        if self.table.selectable:
            children = self.children[::-1][1:]
        else:
            children = self.children[::-1]

        for child in children:
            if child.on_touch_down(touch):
                return True

        self.table.dispatch('on_row_press', self)
        return True

    def apply_selection(self, instance: GlowRecycleView, index: int, is_selected: bool) -> None:
        self.selected = is_selected
        if not self._clicked and 'row_checkbox' in self.ids:
            self.ids.row_checkbox.active = self.selected
        else:
            self.table._selected_rows[self.idx] = is_selected

        self._clicked = False

    def on_enter(self) -> None:
        self.bg_color = self.hover_row_bg_color

    def on_leave(self) -> None:
        self.bg_color = self.row_bg_color


class SelectableRecycleBoxLayout(LayoutSelectionBehavior, GlowRecycleBoxLayout):
    pass


class GlowTable(GlowBoxLayout):
    use_pagination = BooleanProperty(defaultvalue=False)
    pagination_pos = OptionProperty(
        defaultvalue='right', options=['left', 'center', 'right'],
    )

    rows_per_page = NumericProperty(defaultvalue=10)

    columns_info = ListProperty()
    '''
        columns_info = [
            {'name': 'Column 1',
             'max_width': None,
             'min_width': None,
             'size_hint': None,
             'width': 100,
             'viewclass': 'GlowLabelCell',
             'properties': ['text'],
             'constant_properties': {'color': '#FFFFFF'},
             'sorting_function': None,
            },
        ]
    '''
    table_data = ListProperty()

    use_pagination = BooleanProperty(defaultvalue=False)

    sorted_on = NumericProperty(defaultvalue=None, allownone=True)
    '''
        By which column is the input data sorted
    '''
    sorted_order = OptionProperty(defaultvalue='ASC', options=['ASC', 'DSC'])

    selectable = BooleanProperty(defaultvalue=False)
    '''
        Use or not use checkboxes for rows.
    '''

    effect_cls = ObjectProperty(defaultvalue=ScrollEffect)

    header_color = ColorProperty(defaultvalue=None, allownone=True)
    odd_row_color = ColorProperty(defaultvalue=None, allownone=True)
    even_row_color = ColorProperty(defaultvalue=None, allownone=True)
    hover_row_color = ColorProperty(defaultvalue=None, allownone=True)

    _header_color = ColorProperty(defaultvalue=(0, 0, 0, 0))
    _odd_row_color = ColorProperty(defaultvalue=(0, 0, 0, 0))
    _even_row_color = ColorProperty(defaultvalue=(0, 0, 0, 0))
    _hover_row_color = ColorProperty(defaultvalue=(0, 0, 0, 0))

    _viewclass = StringProperty(defaultvalue='GlowTableRow')
    _cell_viewclasses = []
    _formatted_table_data = []
    _display_table_data = ListProperty()
    _selected_rows = {}
    _original_rows = {}

    def __init__(self, *args, **kwargs) -> None:
        self._header = None
        self.paginator = None
        self.table_checkbox = None

        self.bind(header_color=self.setter('_header_color'))
        self.bind(odd_row_color=self.setter('_odd_row_color'))
        self.bind(even_row_color=self.setter('_even_row_color'))
        self.bind(hover_row_color=self.setter('_hover_row_color'))

        self._update_colors_trigger = Clock.create_trigger(lambda _: self.__update_colors())
        self.bind(_odd_row_color=lambda _, __: self._update_colors_trigger())
        self.bind(_even_row_color=lambda _, __: self._update_colors_trigger())
        self.bind(_hover_row_color=lambda _, __: self._update_colors_trigger())

        self.bind(selectable=lambda _, __: self.__update_table_view())

        super().__init__(*args, **kwargs)

        self.register_event_type('on_row_press')
        self.register_event_type('on_row_selected')

        Clock.schedule_once(self.set_default_colors, -1)
        Clock.schedule_once(self.initialize_table, -1)

        self.orientation = 'vertical'

    @property
    def selected_rows(self) -> list[int]:
        return [idx for idx, selected in self._selected_rows.items() if selected]

    @property
    def selected_original_rows(self) -> list[int]:
        return [self._original_rows[idx] for idx in self.selected_rows]

    @property
    def selected_rows_data(self) -> list[dict]:
        return [self.table_data[idx] for idx in self.selected_original_rows]

    @property
    def selected_original_rows_data(self) -> list[dict]:
        return [self.table_data[idx] for idx in self.selected_rows]

    def set_default_colors(self, *args) -> None:

        if self.bg_color is None:
            self._bg_color = self.theme_cls.background_darkest_color

        if self.header_color is None:
            self._header_color = self.theme_cls.background_light_color

        if self.odd_row_color is None:
            self._odd_row_color = self.theme_cls.background_darkest_color

        if self.even_row_color is None:
            self._even_row_color = self.theme_cls.background_darkest_color

        if self.hover_row_color is None:
            self._hover_row_color = self.theme_cls.background_dark_color

    def on_theme_style(self, theme_manager: ThemeManager, theme_style: str) -> None:
        '''Fired when the app :attr:`theme_style` value changes.'''
        super().on_theme_style(theme_manager, theme_style)

        if self.bg_color is None:
            if self.theme_cls.theme_style_switch_animation:
                Animation(
                    _bg_color=self.theme_cls.background_darkest_color,
                    d=self.theme_cls.theme_style_switch_animation_duration,
                    t='linear',
                ).start(self)
            else:
                self._bg_color = self.theme_cls.background_darkest_color

        if self.header_color is None:
            if self.theme_cls.theme_style_switch_animation:
                Animation(
                    _header_color=self.theme_cls.background_light_color,
                    d=self.theme_cls.theme_style_switch_animation_duration,
                    t='linear',
                ).start(self)
            else:
                self._header_color = self.theme_cls.background_light_color

        if self.odd_row_color is None:
            self._odd_row_color = self.theme_cls.background_darkest_color

        if self.even_row_color is None:
            self._even_row_color = self.theme_cls.background_darkest_color

        if self.hover_row_color is None:
            self._hover_row_color = self.theme_cls.background_dark_color

        for child in self._header.children:
            if not isinstance(child, GlowCheckbox):
                if self.theme_cls.theme_style_switch_animation:
                    Animation(
                        text_color=self.theme_cls.text_color,
                        icon_color=self.theme_cls.text_color,
                        d=self.theme_cls.theme_style_switch_animation_duration,
                        t='linear',
                    ).start(child)
                else:
                    child.text_color = self.theme_cls.text_color
                    child.icon_color = self.theme_cls.text_color

    def initialize_table(self, *args) -> None:
        self.ids.glow_table_view.bind(scroll_x=self.ids.glow_table_header.setter('scroll_x'))

        if self.use_pagination:
            self.ids.glow_table_paginator_container.add_widget(self.paginator)

        self.ids.glow_table_header.add_widget(self._header)
        self._header.bind(height=self.ids.glow_table_header.setter('height'),
                          minimum_width=self._header.setter('size_hint_min_x'))
        self._header.bind(minimum_width=self.ids.glow_table_layout.setter('size_hint_min_x'))

    def on_columns_info(self, instance: Self, value: list[dict]) -> None:
        self.__update_table_view()

    def on_sorted_order(self, instance: Self, value: str) -> None:
        if self.selectable:
            columns = self._header.children[::-1][1:]
        else:
            columns = self._header.children[::-1]

        if self.sorted_order == 'ASC':
            columns[self.sorted_on].icon = 'arrow-down'
        else:
            columns[self.sorted_on].icon = 'arrow-up'

    def on_sorted_on(self, instance: Self, value: int) -> None:
        if self.selectable:
            columns = self._header.children[::-1][1:]
        else:
            columns = self._header.children[::-1]

        if self.sorted_order == 'ASC':
            columns[self.sorted_on].icon = 'arrow-down'
        else:
            columns[self.sorted_on].icon = 'arrow-up'

    def on_table_data(self, instance: Self, value: list) -> None:
        self.__update_table_data()

    def on_rows_per_page(self, instance: Self, rows_per_page: int) -> None:
        if self.paginator is not None:
            self.paginator.items_per_page = rows_per_page

    def on_use_pagination(self, instance: Self, valie: bool) -> None:
        self.paginator = GlowPaginator(
            items_per_page=self.rows_per_page,
            pos_hint={'right': 1} if self.pagination_pos == 'right' else ({'left': 0} if self.pagination_pos == 'left' else {'center_x': .5}),
            reset_page=False,
        )
        self.paginator.bind(on_page_changed=self._update_display_table_data)

    def select_all(self, is_selected: bool) -> None:
        '''
            Uncselect or select checkboxes on the entire page.
            If update_selected_rows is False then only the visual representation will be produced
              and when the page is refreshed all checkboxes will be returned back.
        '''
        if self.selectable and len(self._display_table_data):
            rows = min(self.rows_per_page, len(self._formatted_table_data)) if self.use_pagination else len(self._formatted_table_data)

            for idx in range(rows):
                if is_selected:
                    self.ids.glow_table_layout.select_node(idx)
                else:
                    self.ids.glow_table_layout.deselect_node(idx)

                offset = 0
                if self.use_pagination:
                    offset = self.paginator.page * self.rows_per_page

                self._selected_rows[idx + offset] = is_selected

    def select_one(self, row_idx: int, is_selected: bool) -> None:
        '''Unselect or select checkbox on the list item.'''
        same_page = True
        if self.use_pagination:
            same_page = self.paginator.page == (row_idx // self.rows_per_page)

        if same_page:
            if is_selected:
                self.ids.glow_table_layout.select_node(row_idx)
            else:
                self.ids.glow_table_layout.deselect_node(row_idx)

        self._selected_rows[row_idx] = is_selected

    def select_items(self, table_rows_ids: list[int], is_selected: bool) -> None:
        '''Unselect or select checkbox on the list items.'''
        for row_idx in table_rows_ids:
            self.select_one(row_idx, is_selected)

    def update_table_data(self) -> None:
        self.__update_table_data(update_selected_rows=False)

    def __on_click_column(self, instance: Self, column: int) -> None:
        sorting_function = self.columns_info[column].get('sorting_function', None)

        if sorting_function is not None:
            if self.sorted_on == column:
                if self.sorted_order == 'ASC':
                    self.sorted_order = 'DSC'
                else:
                    self.sorted_order = 'ASC'
            else:
                self.sorted_order = 'ASC'

            for child in self._header.children:
                child.icon = 'blank'

            self.sorted_on = column

            new_table_indices, new_table_data = sorting_function(self.table_data[:])

            rows = self.rows_per_page if self.use_pagination else len(self._formatted_table_data)
            for idx in range(rows):
                self.ids.glow_table_layout.deselect_node(idx)

            if self.sorted_order == 'ASC':
                instance.icon = 'arrow-down'
            else:
                instance.icon = 'arrow-up'
                new_table_data = new_table_data[::-1]
                new_table_indices = new_table_indices[::-1]

            new_selected_rows = {}
            new_original_rows = {}
            for new_idx, old_idx in enumerate(new_table_indices):
                new_selected_rows[new_idx] = self._selected_rows[old_idx]
                new_original_rows[new_idx] = self._original_rows[old_idx]

            self.table_data = new_table_data

            self._selected_rows = new_selected_rows
            self._original_rows = new_original_rows

            if self.use_pagination:
                self._update_display_table_data(self.paginator, self.paginator.page)
            else:
                for idx, selected in self._selected_rows.items():
                    if selected:
                        self.ids.glow_table_layout.select_node(idx)

    def _on_click_table_checkbox(self, instance: GlowCheckbox, active: bool) -> None:
        self.select_all(active)

    def __update_table_view(self) -> None:
        if self._header is None:
            self._header = GlowBoxLayout(
                adaptive_height=True,
                orientation='horizontal',
                bg_color=self._header_color,
                padding=['10dp'],
                spacing='5dp',
            )
            self.bind(_header_color=self._header.setter('bg_color'))
        else:
            self._header.clear_widgets()

        _cell_viewclasses = []
        viewclass = f'GlowRow-{uuid.uuid4()}'
        view_header = f'<{viewclass}@GlowTableRow>:\n'
        view_body = ''
        view_properties = ''

        if self.selectable:
            view_body += ' ' * 4 + 'checkbox_disabled: False\n'
            view_body += ' ' * 4 + 'GlowCheckbox:\n'
            view_body += ' ' * 8 + 'id: row_checkbox\n'
            view_body += ' ' * 8 + 'disabled: root.checkbox_disabled\n'
            view_body += ' ' * 8 + 'pos_hint: {"center_y": .5}\n'

            self.table_checkbox = GlowCheckbox(
                pos_hint={'center_y': .5},
            )
            self.table_checkbox.bind(active=self._on_click_table_checkbox)
            self._header.add_widget(self.table_checkbox)

        for cell_idx, cell in enumerate(self.columns_info):
            cell_viewclass_name = cell.get('viewclass', 'GlowLabelCell')
            column_name = cell.get('name', f'Column_{cell_idx}')
            cell_properties = cell.get('properties', ['value'])
            cell_constant_properties = cell.get('constant_properties', {})
            cell_size_hint = cell.get('size_hint', None)
            cell_min_width = cell.get('min_width', None)
            cell_max_width = cell.get('max_width', None)
            cell_width = cell.get('width', 100)

            self._header.add_widget(
                GlowButton(
                    icon='blank' if self.sorted_on != cell_idx else ('arrow-down' if self.sorted_order == 'ASC' else 'arrow-up'),
                    pos_hint={'center_y': .5, 'left': 0},
                    text_color=self.theme_cls.text_color,
                    icon_color=self.theme_cls.text_color,
                    size_hint_min_x=cell_min_width,
                    size_hint_max_x=cell_max_width,
                    size_hint_x=cell_size_hint,
                    adaptive_height=True,
                    font_style='TitleM',
                    width=cell_width,
                    text=column_name,
                    anchor_x='left',
                    padding=(0, ),
                    mode='text',
                    on_press=lambda button, column=cell_idx: self.__on_click_column(button, column),
                ),
            )

            cell_viewclass = getattr(table_cells, cell_viewclass_name)
            allowed_properties, property_types = zip(*cell_viewclass.allowed_properties)

            cell_id = f'col_{cell_idx}'
            if cell_viewclass.use_wrapper:
                view_body += ' ' * 4 + 'GlowBoxLayout:\n'
                view_body += ' ' * 8 + 'use_wrapper: True\n'
                view_body += ' ' * 8 + 'adaptive_height: True\n'
                view_body += ' ' * 8 + 'pos_hint: {"center_x": .5, "center_y": .5}\n'

                view_body += ' ' * 8 + f'size_hint_x: {cell_size_hint}\n'
                view_body += ' ' * 8 + f'size_hint_min_x: {cell_min_width}\n'
                view_body += ' ' * 8 + f'size_hint_max_x: {cell_max_width}\n'
                view_body += ' ' * 8 + f'width: {cell_width}\n'
                view_body += ' ' * 8 + 'GlowHSpacer\n'
                view_body += ' ' * 8 + f'{cell_viewclass_name}:\n'
                view_body += ' ' * 12 + 'use_wrapper: True\n'
                view_body += ' ' * 12 + f'id: {cell_id}\n'
                view_body += ' ' * 12 + 'pos_hint: {"center_y": .5}\n'
                offset = 12
            else:
                view_body += ' ' * 4 + f'{cell_viewclass_name}:\n'
                view_body += ' ' * 8 + f'id: {cell_id}\n'
                view_body += ' ' * 8 + 'adaptive_height: True\n'
                view_body += ' ' * 8 + 'use_wrapper: False\n'
                view_body += ' ' * 8 + 'pos_hint: {"center_x": .5, "center_y": .5}\n'

                view_body += ' ' * 8 + f'size_hint_x: {cell_size_hint}\n'
                view_body += ' ' * 8 + f'size_hint_min_x: {cell_min_width}\n'
                view_body += ' ' * 8 + f'size_hint_max_x: {cell_max_width}\n'
                view_body += ' ' * 8 + f'width: {cell_width}\n'

                offset = 8

            for cell_constant_property, cell_constant_property_value in cell_constant_properties.items():
                view_body += ' ' * 8 + f'{cell_constant_property}: {cell_constant_property_value}\n'

            formatted_cell_properties = []
            for cell_property in cell_properties:
                if cell_property in allowed_properties:
                    cell_property_type = property_types[allowed_properties.index(cell_property)]
                    view_body += get_cell_property_connection(cell_idx, cell_property, cell_property_type, offset)

                    formatted_cell_properties.append(cell_property)
                elif cell_property == 'value':
                    cell_property, cell_property_type = cell_viewclass.value_property
                    view_body += get_cell_property_connection(cell_idx, cell_property, cell_property_type, offset)

                if cell_property_type != 'function':
                    view_properties += ' ' * 4 + f'col_{cell_idx}_{cell_property}: {cell_id}.{cell_property}\n'
                else:
                    view_properties += ' ' * 4 + f'col_{cell_idx}_{cell_property}: None\n'

            self.columns_info[cell_idx]['properties'] = formatted_cell_properties
            _cell_viewclasses.append((cell_viewclass_name, cell_viewclass.value_property[0], allowed_properties))

            if cell_viewclass.use_wrapper:
                view_body += ' ' * 8 + 'GlowHSpacer\n'

        self.view = view_header + view_properties + view_body

        Builder.load_string(self.view)
        self._viewclass = f'{viewclass}'
        self._cell_viewclasses = _cell_viewclasses

    def __update_table_data(self, update_selected_rows: bool = True) -> None:
        if update_selected_rows:
            self.select_all(is_selected=False)
            self._selected_rows = dict.fromkeys(range(len(self.table_data)), False)
            self._original_rows = {i: i for i in range(len(self.table_data))}
        formatted_table_data = []

        for row_idx, row in enumerate(self.table_data):
            formatted_row_data = {}
            for cell_idx, cell_data in enumerate(row):
                if isinstance(cell_data, dict):
                    for key, value in cell_data.items():
                        if key in self._cell_viewclasses[cell_idx][2]:
                            formatted_row_data[f'col_{cell_idx}_{key}'] = value
                elif isinstance(cell_data, (list, tuple)):
                    for row_property, value in (zip(self.columns_info[cell_idx]['properties'], cell_data)):
                        formatted_row_data[f'col_{cell_idx}_{row_property}'] = value
                else:
                    formatted_row_data[f'col_{cell_idx}_{self._cell_viewclasses[cell_idx][1]}'] = cell_data

            formatted_row_data['idx'] = row_idx
            if row_idx % 2 == 0:
                formatted_row_data['row_bg_color'] = self._even_row_color
            else:
                formatted_row_data['row_bg_color'] = self._odd_row_color

            formatted_row_data['hover_row_bg_color'] = self._hover_row_color
            formatted_row_data['table'] = self
            formatted_table_data.append(formatted_row_data)

        self._formatted_table_data = formatted_table_data
        if self.use_pagination:
            self.paginator.items = self._formatted_table_data
            self._update_display_table_data(self.paginator, self.paginator.page)
        else:
            self._display_table_data = self._formatted_table_data

    def update_table_row_data(self, row_idx: int, row_data: list) -> None:
        formatted_row_data = {}
        for cell_idx, cell_data in enumerate(row_data):
            if isinstance(cell_data, dict):
                for key, value in cell_data.items():
                    if key in self._cell_viewclasses[cell_idx][2]:
                        formatted_row_data[f'col_{cell_idx}_{key}'] = value
            else:
                formatted_row_data[f'col_{cell_idx}_{self._cell_viewclasses[cell_idx][1]}'] = cell_data

        formatted_row_data['idx'] = row_idx
        if row_idx % 2 == 0:
            formatted_row_data['row_bg_color'] = self._even_row_color
        else:
            formatted_row_data['row_bg_color'] = self._odd_row_color

        formatted_row_data['hover_row_bg_color'] = self._hover_row_color
        formatted_row_data['table'] = self
        self._formatted_table_data[row_idx] = formatted_row_data

        if self.use_pagination:
            self.paginator.items = self._formatted_table_data
            self._update_display_table_data(self.paginator, self.paginator.page)
        else:
            self._display_table_data = self._formatted_table_data

    def __update_colors(self, *args) -> None:
        for row_idx, row_data in enumerate(self._formatted_table_data):
            if row_idx % 2 == 0:
                row_data['row_bg_color'] = self._even_row_color
            else:
                row_data['row_bg_color'] = self._odd_row_color

            row_data['hover_row_bg_color'] = self._hover_row_color

        self.ids.glow_table_view.refresh_from_data()

    def _update_display_table_data(self, instance: GlowPaginator, page: int) -> None:
        self._display_table_data = self.paginator.get_page_items()
        item_from, item_to = self.paginator.get_from_to()

        for i, idx in enumerate(range(item_from, item_to)):
            if self._selected_rows[idx]:
                self.ids.glow_table_layout.select_node(i)

        selected_rows = self._selected_rows.copy()
        if self.selectable:
            self.table_checkbox.active = False
        self._selected_rows = selected_rows

    def on_row_press(self, instance: GlowTableRow) -> None:
        '''Called when a table row is clicked.'''
        pass

    def on_row_selected(self, instance: GlowTableRow) -> None:
        '''Called when the row is checked.'''
        pass
