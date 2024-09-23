__all__ = ('GlowPaginator', )

from kivy_glow.uix.boxlayout import GlowBoxLayout
from kivy_glow import kivy_glow_uix_dir
from kivy.lang import Builder
from kivy.clock import Clock
import os
from kivy.properties import (
    NumericProperty,
    BooleanProperty,
    ListProperty,
)
from typing import (
    Self,
    Any,
)

with open(
    os.path.join(kivy_glow_uix_dir, 'paginator', 'paginator.kv'), encoding='utf-8'
) as kv_file:
    Builder.load_string(kv_file.read())


class GlowPaginator(GlowBoxLayout):
    '''A simple widget to control content pagination.

    :Events:
        :attr:`on_page_items_changed`
            Called when page data is changed (changed page or items)
        :attr:`on_page_changed`
            Called when page is changed
    '''

    items_per_page = NumericProperty(10)
    '''How to split items

    :attr:`items_per_page` is an :class:`~kivy.properties.NumericProperty`
    and default to `10`.
    '''

    items = ListProperty([])
    '''Any iterable objects

    :attr:`items` is an :class:`~kivy.properties.ListProperty`
    and default to `empty`.
    '''

    reset_page = BooleanProperty(True)
    '''Reset page if :attr:`items` value changed.

    The page will still be reset if the current page is larger than the maximum possible.

    :attr:`reset_page` is an :class:`~kivy.properties.BooleanProperty`
    and default to `True`.
    '''

    _page = 0
    _pages = 0

    def __init__(self, *args, **kwargs):
        self.register_event_type('on_page_items_changed')
        self.register_event_type('on_page_changed')

        super().__init__(*args, **kwargs)
        Clock.schedule_once(self._update_view)

    def on_items(self, paginator_instance: Self, items: list) -> None:
        '''Fired when the :attr:`items` value changes.'''
        self._pages = 1 + (len(items) - 1) // self.items_per_page

        if self._page >= self._pages or self.reset_page:
            self._page = 0
            self.dispatch('on_page_changed', self._page)

        self.dispatch('on_page_items_changed', self.get_page_items())
        Clock.schedule_once(self._update_view)

    @property
    def page(self) -> int:
        '''Get current page.'''
        return self._page

    @property
    def pages(self) -> int:
        '''Get last page.'''
        return self._pages

    @property
    def has_next_page(self) -> bool:
        '''Return True if Paginator has next page.'''
        return self._page < self._pages - 1

    @property
    def has_previous_page(self) -> bool:
        '''Return True if Paginator has previous page.'''
        return self._page > 0

    def on_page_items_changed(self, page_items: Any):
        '''Fired at the Paginator page items changed event.'''
        pass

    def on_page_changed(self, page: int):
        '''Fired at the Paginator page changed event.'''
        pass

    def get_page_items(self):
        '''Return current page items'''
        return self.items[self._page * self.items_per_page: (self._page + 1) * self.items_per_page]

    def get_from_to(self):
        '''Returns the current page indexes in the items.'''
        return self._page * self.items_per_page, min(len(self.items), (self._page + 1) * self.items_per_page)

    def _next_page(self) -> None:
        '''Set next page.'''
        self._page += 1
        self._update_view()
        self.dispatch('on_page_changed', self._page)
        self.dispatch('on_page_items_changed', self.get_page_items())

    def _previous_page(self) -> None:
        '''Set previous page.'''
        self._page -= 1
        self._update_view()
        self.dispatch('on_page_changed', self._page)
        self.dispatch('on_page_items_changed', self.get_page_items())

    def _update_view(self, *args) -> None:
        '''Update buttons and paginator info'''
        self.ids.glow_paginator_info.text = f'{self._page * self.items_per_page + 1 if len(self.items) else 0}-{min(len(self.items), (self._page + 1) * self.items_per_page)} : {len(self.items)}'

        self.ids.glow_paginator_button_next.disabled = False if self.has_next_page else True
        self.ids.glow_paginator_button_previous.disabled = False if self.has_previous_page else True
