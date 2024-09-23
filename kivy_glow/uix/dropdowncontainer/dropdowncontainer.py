__all__ = ('GlowDropDownContainer', )

from kivy_glow.uix.scrollview import GlowScrollView
from kivy_glow.uix.boxlayout import GlowBoxLayout
from kivy.input.motionevent import MotionEvent
from kivy_glow.uix.widget import GlowWidget
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.metrics import dp
from typing import Self
from kivy.core.window import (
    WindowBase,
    Window,
)
from kivy.properties import (
    VariableListProperty,
    BooleanProperty,
    NumericProperty,
    ObservableList,
    OptionProperty,
    StringProperty,
    ListProperty,
)


class GlowDropDownException(Exception):
    pass


class GlowDropDownContainer(GlowBoxLayout):
    '''Dropdown list widget. You can use it for any content, but you must call the list's open and close functions yourself.

    :Events:
        :attr:`on_open`
            Called when container is opened
        :attr:`on_dismiss`
            Called when container is closed

    Usage example
        .. code-block:: kv
        def select_item(dropdown, item):
            print('selected item:', item.text)
            dropdown.dismiss()

        button = GlowButton(text='Open dropdown')
        custom_dropdown = GlowDropDownContainer(
            items=[
                GlowButton(adaptive_height=True,
                        mode='text',
                        text=f'item_{i}',
                        on_release=lambda _, item=f'item_{i}': select_item(custom_dropdown, item)
                        )
                for i in range(10)
            ]
        )
        button.on_release = lambda _: custom_dropdown.open(button)
    '''

    items = ListProperty()
    '''Widget items

    :attr:`items` is an :class:`~kivy.properties.ListProperty`.
    '''
    direction = OptionProperty('down', options=('down', 'up'))
    '''Expansion direction

    :attr:`direction` is an :class:`~kivy.properties.OptionProperty`
    and default to `down`.
    '''

    position = OptionProperty('center', options=('left', 'center', 'right'))
    '''Expansion position

    :attr:`position` is an :class:`~kivy.properties.OptionProperty`
    and default to `center`.
    '''

    use_separator = BooleanProperty(True)
    '''Whether to add a separator between elements

    :attr:`use_separator` is an :class:`~kivy.properties.BooleanProperty`.
    and default to `True`.
    '''

    min_width = NumericProperty(None, allownone=True)
    '''Mimimum expansion width

    :attr:`min_width` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `None`.
    '''

    max_height = NumericProperty(None, allownone=True)
    '''Maximum expansion height

    :attr:`max_height` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `None`.
    '''

    auto_dismiss = BooleanProperty(True)
    '''Hide expandable panel when clicking outside of element (even if new element is not selected)

    :attr:`max_height` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `True`.
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

    border_radius = VariableListProperty(['10dp', ], length=4)
    '''Canvas radius.

    :attr:`border_radius` is an :class:`~kivy.properties.VariableListProperty`
    and defaults to `[10, 10, 10, 10]`.
    '''

    _anim_playing = False
    _touch_started_inside = None
    _attach_to = None
    _attach_to_pos = None
    _state = 'closed'

    _height = None

    def __init__(self, *args, **kwargs) -> None:
        self.container = GlowBoxLayout(adaptive_height=True, spacing='4dp', padding=[0, 0, '5dp', 0], orientation='vertical', opacity=0)
        self.scroll = GlowScrollView(always_overscroll=False)

        self.fbind('size', self._reposition)

        self._window = None
        super().__init__(*args, **kwargs)

        self.size_hint = None, None
        self.size = 1, 1
        self.padding = ['10dp', '10dp', '5dp', '10dp']

        self.register_event_type('on_open')
        self.register_event_type('on_dismiss')
        if 'do_scroll_x' not in kwargs:
            self.do_scroll_x = False

        Clock.schedule_once(self.set_default_colors, -1)

    def on_parent(self, instance: Self, parent) -> None:
        if parent is None:
            Window.unbind(
                on_key_down=self._on_keyboard_down,
                size=self._reposition,
            )
        else:
            Window.bind(
                on_key_down=self._on_keyboard_down,
                size=self._reposition,
            )

        return super().on_parent(instance, parent)

    def on_min_width(self, dropdowncontainer_instance: Self, min_width: int | float) -> None:
        '''Fired when the :attr:`min_width` value changes.'''
        self.width = self._get_width()

    def on_items(self, dropdowncontainer_instance: Self, items: list) -> None:
        '''Fired when the :attr:`items` value changes.'''
        self.container.clear_widgets()
        for item in items:
            self.container.add_widget(item)

    def open(self, attach_to: Widget = None, attach_to_pos: tuple = None) -> None:
        '''Open DropDownContainer.'''
        if self._state == 'closed' and not self._anim_playing:
            self._state = 'opened'
            self._anim_playing = True

            if attach_to is not None:
                self._window = attach_to.get_parent_window()
                if self._window is None:
                    raise GlowDropDownException(
                        'Can\'t attach dropdown container to hidden widget')

                self._attach_to = attach_to
                self._attach_to.bind(pos=self._reposition, size=self._reposition)

            else:
                if attach_to_pos is None:
                    raise GlowDropDownException('Specify widget or position')
                self._window = Window
                self._attach_to_pos = attach_to_pos

            if self.use_separator:
                self._add_separator()

            self._window.add_widget(self)
            self._window.add_widget(self.container)

            self._reposition()
            Clock.schedule_once(self._continue_open)

    def dismiss(self) -> None:
        '''Close DropDownContainer.'''
        if self._state == 'opened' and not self._anim_playing:
            self._anim_playing = True
            self._state = 'closed'

            animation = Animation(
                opacity=0.0,
                d=self.closing_time / 2,
                t=self.closing_transition,
            )
            animation.bind(on_complete=self._remove_container)
            animation.start(self.container)

    def on_open(self) -> None:
        '''Fired at the DropDownContainer open event.'''
        pass

    def on_dismiss(self) -> None:
        '''Fired at the DropDownContainer on_dismiss event.'''
        pass

    def on_touch_down(self, touch: MotionEvent) -> bool:
        '''Fired at the DropDownContainer on_touch_down event.'''
        self._touch_started_inside = self.collide_point(*touch.pos)
        if not self.auto_dismiss or self._touch_started_inside:
            return super().on_touch_down(touch)

        return False

    def on_touch_move(self, touch: MotionEvent) -> bool:
        '''Fired at the DropDownContainer on_touch_move event.'''
        if not self.auto_dismiss or self._touch_started_inside:
            return super().on_touch_move(touch)

        return False

    def on_touch_up(self, touch: MotionEvent) -> bool:
        '''Fired at the DropDownContainer on_touch_up event.'''
        if self.auto_dismiss and self._touch_started_inside is False:
            self.dismiss()
        else:
            self._touch_started_inside = None
            return super().on_touch_up(touch)

        return False

    def _on_keyboard_down(self, window: WindowBase, key: int, scancode: int, codepoint: str, modifiers: ObservableList) -> None:
        '''Fired when a key pressed.'''
        if key == 27 and self.get_parent_window():
            self.dismiss()

    def _continue_open(self, *args) -> None:
        '''Continue opening DropDownContainer.'''
        self._window.remove_widget(self.container)

        self.width = self._get_width()
        height = self._get_height()

        if self.direction == 'down':
            animation = Animation(
                height=height,
                d=self.opening_time / 2,
                t=self.opening_transition,
            )
        elif self.direction == 'up':
            animation = Animation(
                height=height,
                y=self._attach_to.to_window(0, self._attach_to.top)[1] if self._attach_to is not None else self._attach_to_pos[1],
                d=self.opening_time / 2,
                t=self.opening_transition,
            )
        animation.bind(on_complete=self._add_container)
        animation.start(self)

    def _add_container(self, *args) -> None:
        '''Continue opening DropDownContainer.'''
        self.scroll.add_widget(self.container)
        self.add_widget(self.scroll)

        animation = Animation(
            opacity=1,
            d=self.opening_time / 2,
            t=self.opening_transition,
        )
        animation.bind(on_complete=self._cancel_anim)
        animation.start(self.container)

    def _remove_container(self, *args) -> None:
        '''Continue closing DropDownContainer.'''
        self.scroll.remove_widget(self.container)
        self.remove_widget(self.scroll)

        if self.direction == 'down':
            animation = Animation(
                height=0,
                d=self.closing_time / 2,
                t=self.closing_transition,
            )
        elif self.direction == 'up':
            animation = Animation(
                height=0,
                d=self.closing_time / 2,
                t=self.closing_transition,
            )
        animation.bind(on_complete=self._cancel_anim)
        animation.start(self)

    def _cancel_anim(self, *args) -> None:
        '''Final step for closing and oppening.'''
        self._anim_playing = False
        if self._state == 'closed' and (self._attach_to or self._attach_to_pos):
            self._window.remove_widget(self)
            if self._attach_to:
                self._attach_to.unbind(pos=self._reposition, size=self._reposition)
                self._attach_to = None
            elif self._attach_to_pos:
                self._attach_to_pos = None
            self.dispatch('on_dismiss')
        elif self._state == 'opened':
            self.dispatch('on_open')

    def _get_width(self) -> int | float:
        '''Calculate win width'''
        width = 0
        for child in self.container.children:
            if hasattr(child, 'minimum_width'):
                width = max(width, child.minimum_width)
            elif hasattr(child, 'texture_size'):
                width = max(width, child.texture_size[0])
            else:
                width = max(width, child.width)

        if self.min_width is not None:
            return max(self.min_width, width + dp(20))

        return width + dp(20)

    def _get_height(self) -> int | float:
        '''Calculate win height'''
        Window.update_viewport()
        if self.max_height is not None:
            return min(self.container.minimum_height, self.max_height)
        return self.container.minimum_height + dp(20)

    def _reposition(self, *args) -> None:
        '''Position adjustment.'''
        if self._attach_to is not None:
            if self.direction == 'up':
                self.y = self._attach_to.to_window(0, self._attach_to.top)[1]
            elif self.direction == 'down':
                self.top = self._attach_to.to_window(0, self._attach_to.y)[1]

            if self.position == 'left':
                self.x = self._attach_to.to_window(self._attach_to.x, 0)[0]
            elif self.position == 'center':
                self.center_x = self._attach_to.to_window(self._attach_to.center_x, 0)[0]
            elif self.position == 'right':
                self.right = self._attach_to.to_window(self._attach_to.right, 0)[0]

        if self._attach_to_pos is not None:
            if self.direction == 'up':
                self.y = self._attach_to_pos[1]
            elif self.direction == 'down':
                self.top = self._attach_to_pos[1]

            if self.position == 'left':
                self.x = self._attach_to_pos[0]
            elif self.position == 'center':
                self.center_x = self._attach_to_pos[0]
            elif self.position == 'right':
                self.right = self._attach_to_pos[0]

        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0

        if self.top > Window.height:
            self.top = Window.height
        if self.right > Window.width:
            self.right = Window.width

    def _add_separator(self) -> None:
        '''Add separator between items.'''
        items = len(self.container.children)
        for i in range(items - 1):
            self.container.add_widget(
                GlowWidget(
                    size_hint_y=None,
                    pos_hint={'center_y': .5},
                    height='2dp',
                    bg_color=self.theme_cls.divider_color
                ),
                index=i * 2 + 1)

    def add_widget(self, widget: Widget, index: int = 0, canvas=None) -> None:
        '''Modified default function'''
        if widget != self.scroll:
            self.container.add_widget(widget)
        else:
            GlowBoxLayout.add_widget(self, widget, index, canvas)

    def set_default_colors(self, *args) -> None:
        '''Set defaults colors.'''
        if self.bg_color is None:
            self.bg_color = self.theme_cls.background_darkest_color
