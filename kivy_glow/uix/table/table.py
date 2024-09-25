__all__ = ('GlowTable', )

from kivy_glow.uix.recycleboxlayout import GlowRecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy_glow.effects.stiffscroll import StiffScrollEffect
from kivy_glow.uix.paginator import GlowPaginator
from kivy_glow.uix.boxlayout import GlowBoxLayout
from kivy_glow.uix.behaviors import HoverBehavior
import kivy_glow.uix.table.cells as table_cells
from kivy_glow.uix.checkbox import GlowCheckbox
from kivy.uix.behaviors import ButtonBehavior
from kivy_glow.uix.button import GlowButton
from kivy_glow import kivy_glow_uix_dir
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.metrics import dp
from typing import Self
import uuid
import os
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
    os.path.join(kivy_glow_uix_dir, 'table', 'table.kv'), encoding='utf-8'
) as kv_file:
    Builder.load_string(kv_file.read())


def get_cell_property_connection(cell_idx, cell_property, cell_property_type, offset):
    if cell_property_type == 'str':
        return ' ' * offset + f'{cell_property}: str(root.col_{cell_idx}_{cell_property}) if root.col_{cell_idx}_{cell_property} is not None else ""\n'
    elif cell_property_type == 'int':
        return ' ' * offset + f'{cell_property}: int(root.col_{cell_idx}_{cell_property}) if root.col_{cell_idx}_{cell_property} is not None else 0\n'
    elif cell_property_type == 'float':
        return ' ' * offset + f'{cell_property}: float(root.col_{cell_idx}_{cell_property})if root.col_{cell_idx}_{cell_property} is not None else 0.0\n'
    elif cell_property_type == 'bool':
        return ' ' * offset + f'{cell_property}: root.col_{cell_idx}_{cell_property}\n'
    elif cell_property_type == 'tuple':
        return ' ' * offset + f'{cell_property}: tuple(root.col_{cell_idx}_{cell_property}) if root.col_{cell_idx}_{cell_property} is not None else ()\n'
    elif cell_property_type == 'list':
        return ' ' * offset + f'{cell_property}: list(root.col_{cell_idx}_{cell_property}) if root.col_{cell_idx}_{cell_property} is not None else []\n'
    elif cell_property_type == 'color':
        return ' ' * offset + f'{cell_property}: tuple(root.col_{cell_idx}_{cell_property}) if root.col_{cell_idx}_{cell_property} is not None else (0, 0, 0, 0)\n'
    elif cell_property_type == 'function':
        return ' ' * offset + f'{cell_property}:\n' \
            + ' ' * (offset + 4) + f'root.col_{cell_idx}_{cell_property}(root.table, self) if root.col_{cell_idx}_{cell_property} is not None and not root.refreshing else None\n'
    else:
        return ' ' * offset + f'{cell_property}: root.col_{cell_idx}_{cell_property}\n'


class GlowTableRow(GlowBoxLayout,
                   HoverBehavior,
                   ButtonBehavior,
                   RecycleDataViewBehavior):

    index = NumericProperty(None, allownone=True)
    selected = BooleanProperty(False)

    _clicked = False
    refreshing = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size_hint_y = None

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.opacity = 0
        self.refreshing = True

        setattr(self, 'idx', data['idx'])
        super().refresh_view_attrs(rv, index, data)

        self.bg_color = self.row_bg_color
        self.index = index

        self.do_layout()

        Clock.schedule_once(self._set_visible)

    def _set_visible(self, *args):
        self.height = max(dp(56), self.minimum_height)
        self.opacity = 1
        self.refreshing = False

    def on_touch_down(self, touch):
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

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        if not self._clicked and 'row_checkbox' in self.ids:
            self.ids.row_checkbox.active = self.selected
        else:
            self.table._selected_rows[self.idx] = is_selected

        self._clicked = False

    def on_enter(self):
        self.bg_color = self.hover_row_bg_color

    def on_leave(self):
        self.bg_color = self.row_bg_color


class SelectableRecycleBoxLayout(LayoutSelectionBehavior, GlowRecycleBoxLayout):
    pass


class GlowTable(GlowBoxLayout):
    use_pagination = BooleanProperty(False)
    pagination_pos = OptionProperty(
        'right', options=['left', 'center', 'right']
    )

    rows_per_page = NumericProperty(10)

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

    use_pagination = BooleanProperty(False)

    sorted_on = NumericProperty(None, allownone=True)
    '''
        By which column is the input data sorted
    '''
    sorted_order = OptionProperty('ASC', options=['ASC', 'DSC'])

    selectable = BooleanProperty(False)
    '''
        Use or not use checkboxes for rows.
    '''

    effect_cls = ObjectProperty(StiffScrollEffect)

    header_color = ColorProperty(None, allownone=True)
    odd_row_color = ColorProperty(None, allownone=True)
    even_row_color = ColorProperty(None, allownone=True)
    hover_row_color = ColorProperty(None, allownone=True)

    _header_color = ColorProperty((0, 0, 0, 1))
    _odd_row_color = ColorProperty((0, 0, 0, 1))
    _even_row_color = ColorProperty((0, 0, 0, 1))
    _hover_row_color = ColorProperty((0, 0, 0, 1))

    _viewclass = StringProperty('GlowTableRow')
    _cell_viewclasses = []
    _formatted_table_data = []
    _display_table_data = ListProperty()
    _selected_rows = {}
    _original_rows = {}

    def __init__(self, *args, **kwargs):
        self._header = None
        self.paginator = None
        self.table_checkbox = None

        self.bind(header_color=self.setter('_header_color'))
        self.bind(odd_row_color=self.setter('_odd_row_color'))
        self.bind(even_row_color=self.setter('_even_row_color'))
        self.bind(hover_row_color=self.setter('_hover_row_color'))

        self.bind(_header_color=lambda _, __: self.__update_colors())

        self.bind(_odd_row_color=lambda _, __: self.__update_colors())
        self.bind(_even_row_color=lambda _, __: self.__update_colors())
        self.bind(_hover_row_color=lambda _, __: self.__update_colors())

        self.bind(selectable=lambda _, __: self.__update_table_view())

        super().__init__(*args, **kwargs)

        self.register_event_type('on_row_press')
        self.register_event_type('on_row_selected')

        Clock.schedule_once(self.set_default_colors, -1)
        Clock.schedule_once(self.initialize_table, -1)

        self.orientation = 'vertical'

    def on_parent(self, instance: Self, parent) -> None:
        if parent is None:
            if self._header is not None:
                self._header.unbind(height=self.ids.glow_table_header.setter('height'),
                                    minimum_width=self._header.setter('size_hint_min_x'))
                self._header.unbind(minimum_width=self.ids.glow_table_layout.setter('size_hint_min_x'))
            if 'glow_table_view' in self.ids and 'glow_table_header' in self.ids:
                self.ids.glow_table_view.bind(scroll_x=self.ids.glow_table_header.setter('scroll_x'))
            if self.paginator is not None:
                self.paginator.unbind(on_page_changed=self._update_display_table_data)
            if self.table_checkbox is not None:
                self.table_checkbox.unbind(active=self._on_click_table_checkbox)
        else:
            if self._header is not None:
                self._header.bind(height=self.ids.glow_table_header.setter('height'),
                                  minimum_width=self._header.setter('size_hint_min_x'))
                self._header.bind(minimum_width=self.ids.glow_table_layout.setter('size_hint_min_x'))
            if 'glow_table_view' in self.ids and 'glow_table_header' in self.ids:
                self.ids.glow_table_view.bind(scroll_x=self.ids.glow_table_header.setter('scroll_x'))
            if self.paginator is not None:
                self.paginator.bind(on_page_changed=self._update_display_table_data)
            if self.table_checkbox is not None:
                self.table_checkbox.bind(active=self._on_click_table_checkbox)

        return super().on_parent(instance, parent)

    @property
    def selected_rows(self):
        return [idx for idx, selected in self._selected_rows.items() if selected]

    @property
    def selected_original_rows(self):
        return [self._original_rows[idx] for idx in self.selected_rows]

    @property
    def selected_rows_data(self):
        return [self.table_data[idx] for idx in self.selected_original_rows]

    @property
    def selected_original_rows_data(self):
        return [self.table_data[idx] for idx in self.selected_rows]

    def set_default_colors(self, *args):
        if self.bg_color is None:
            self.bg_color = self.theme_cls.background_darkest_color

        if self.header_color is None:
            self.header_color = self.theme_cls.background_light_color

        if self.odd_row_color is None:
            self.odd_row_color = self.theme_cls.background_darkest_color

        if self.even_row_color is None:
            self.even_row_color = self.theme_cls.background_darkest_color

        if self.hover_row_color is None:
            self.hover_row_color = self.theme_cls.background_dark_color

        self.__update_table_data()

    def initialize_table(self, *args):
        self.ids.glow_table_view.bind(scroll_x=self.ids.glow_table_header.setter('scroll_x'))

        if self.use_pagination:
            self.ids.glow_table_paginator_container.add_widget(self.paginator)

        self.ids.glow_table_header.add_widget(self._header)
        self._header.bind(height=self.ids.glow_table_header.setter('height'),
                          minimum_width=self._header.setter('size_hint_min_x'))
        self._header.bind(minimum_width=self.ids.glow_table_layout.setter('size_hint_min_x'))

    def on_columns_info(self, _, __):
        self.__update_table_view()

    def on_sorted_order(self, _, __):
        if self.selectable:
            columns = self._header.children[::-1][1:]
        else:
            columns = self._header.children[::-1]

        if self.sorted_order == 'ASC':
            columns[self.sorted_on].icon = 'arrow-down'
        else:
            columns[self.sorted_on].icon = 'arrow-up'

    def on_sorted_on(self, _, __):
        if self.selectable:
            columns = self._header.children[::-1][1:]
        else:
            columns = self._header.children[::-1]

        if self.sorted_order == 'ASC':
            columns[self.sorted_on].icon = 'arrow-down'
        else:
            columns[self.sorted_on].icon = 'arrow-up'

    def on_table_data(self, _, __):
        self.__update_table_data()

    def on_rows_per_page(self, table_instance: Self, rows_per_page: int) -> None:
        if self.paginator is not None:
            self.paginator.items_per_page = rows_per_page

    def on_use_pagination(self, _, __):
        self.paginator = GlowPaginator(
            items_per_page=self.rows_per_page,
            pos_hint={'right': 1} if self.pagination_pos == 'right' else ({'left': 0} if self.pagination_pos == 'left' else {'center_x': .5}),
            reset_page=False,
        )
        self.paginator.bind(on_page_changed=self._update_display_table_data)

    def select_all(self, is_selected):
        '''
            Uncselect or select checkboxes on the entire page.
            If update_selected_rows is False then only the visual representation will be produced
              and when the page is refreshed all checkboxes will be returned back.
        '''
        if self.selectable and len(self._display_table_data):
            rows = self.rows_per_page if self.use_pagination else len(self._formatted_table_data)

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

    def update_table_data(self):
        self.__update_table_data(False)

    def __on_click_column(self, instance, column: int):
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

    def _on_click_table_checkbox(self, checkbox_instance: GlowCheckbox, active):
        self.select_all(active)

    def __update_table_view(self):
        if self._header is None:
            self._header = GlowBoxLayout(
                adaptive_height=True,
                orientation='horizontal',
                bg_color=self._header_color,
                padding=['10dp', ],
                spacing='5dp',
            )
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
                    font_style='TitleM',
                    text=column_name,
                    mode='text',
                    icon='blank' if self.sorted_on != cell_idx else ('arrow-down' if self.sorted_order == 'ASC' else 'arrow-up'),
                    adaptive_height=True,
                    pos_hint={'center_y': .5, 'left': 0},
                    size_hint_x=cell_size_hint,
                    size_hint_min_x=cell_min_width,
                    size_hint_max_x=cell_max_width,
                    width=cell_width,
                    text_color=self.theme_cls.text_color,
                    icon_color=self.theme_cls.text_color,
                    padding=[0, ],
                    anchor_x='left',
                    on_press=lambda button, column=cell_idx: self.__on_click_column(button, column)
                )
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

    def __update_table_data(self, update_selected_rows: bool = True):
        if update_selected_rows:
            self.select_all(False)
            self._selected_rows = {i: False for i in range(len(self.table_data))}
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

    def update_table_row_data(self, row_idx: int, row_data):
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

    def __update_colors(self, *args):
        self._header.bg_color = self._header_color
        for row_idx, row_data in enumerate(self._formatted_table_data):
            if row_idx % 2 == 0:
                row_data['row_bg_color'] = self._even_row_color
            else:
                row_data['row_bg_color'] = self._odd_row_color

            row_data['hover_row_bg_color'] = self._hover_row_color

    def _update_display_table_data(self, _, page):
        self._display_table_data = self.paginator.get_page_items()
        item_from, item_to = self.paginator.get_from_to()

        for i, idx in enumerate(range(item_from, item_to)):
            if self._selected_rows[idx]:
                self.ids.glow_table_layout.select_node(i)

        selected_rows = self._selected_rows.copy()
        if self.selectable:
            self.table_checkbox.active = False
        self._selected_rows = selected_rows

    def on_row_press(self, row_instance: GlowTableRow) -> None:
        '''Called when a table row is clicked.'''
        pass

    def on_row_selected(self, row_instance: GlowTableRow) -> None:
        '''Called when the row is checked.'''
        pass
