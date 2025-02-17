'''
SideBehavior was written by Andrés Rodríguez, Ivanov Yuri, Artem Bulgakov and KivyMD contributors. (MDNavigationDrawer)
https://github.com/kivymd/KivyMD
'''
__all__ = ('GlowSidePanel', 'GlowSidePanelButton', 'GlowSidePanelLayout')

import os
from typing import Self

from kivy.animation import (
    Animation,
    AnimationTransition,
)
from kivy.clock import Clock
from kivy.core.window import (
    Window,
    WindowBase,
)
from kivy.graphics import (
    Color,
    Rectangle,
)
from kivy.input.motionevent import MotionEvent
from kivy.lang import Builder
from kivy.properties import (
    AliasProperty,
    BooleanProperty,
    ColorProperty,
    NumericProperty,
    ObjectProperty,
    ObservableList,
    OptionProperty,
    StringProperty,
)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.widget import Widget

from kivy_glow import kivy_glow_uix_dir
from kivy_glow.theme import ThemeManager
from kivy_glow.uix.boxlayout import GlowBoxLayout
from kivy_glow.uix.button import GlowButton
from kivy_glow.uix.floatlayout import GlowFloatLayout
from kivy_glow.uix.icon import GlowIcon
from kivy_glow.uix.label import GlowLabel
from kivy_glow.uix.scrollview import GlowScrollView

with open(
    os.path.join(kivy_glow_uix_dir, 'sidepanel', 'sidepanel.kv'), encoding='utf-8',
) as kv_file:
    Builder.load_string(kv_file.read())


class GlowSidePanelException(Exception):
    pass


class GlowSidePanelButton(GlowButton):

    right_text = StringProperty(defaultvalue='')
    '''Additional text located in the right corner

    :attr:`right_text` is an :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    '''

    selected = BooleanProperty(defaultvalue=False)
    '''True if panel item selected

    :attr:`selected` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    '''

    hover_color = ColorProperty(defaultvalue=None, allownone=True)
    '''The color in (r, g, b, a) or string format of the hovered panel item

    :attr:`selected_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    selected_color = ColorProperty(defaultvalue=None, allownone=True)
    '''The color in (r, g, b, a) or string format of the selected panel item

    :attr:`selected_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    _hover_color = ColorProperty(defaultvalue=None, allownone=True)
    _selected_color = ColorProperty(defaultvalue=None, allownone=True)

    def __init__(self, *args, **kwargs) -> None:
        self.bind(hover_color=self.setter('_hover_color'))
        self.bind(selected_color=self.setter('_selected_color'))

        super().__init__(*args, **kwargs)

        self.right_text_label = None
        self.adaptive_height = True

        Clock.schedule_once(self.initialize_sidepanelbutton, -1)

    def on_parent(self, instance: Self, parent: Widget) -> None:
        if self.right_text_label is not None:
            if parent is None:
                self.unbind(right_text=self.right_text_label.setter('text'),
                            _text_color=self.right_text_label.setter('color'),
                            font_style=self.right_text_label.setter('font_style'))
            else:
                self.bind(right_text=self.right_text_label.setter('text'),
                          _text_color=self.right_text_label.setter('color'),
                          font_style=self.right_text_label.setter('font_style'))

        return super().on_parent(instance, parent)

    def on_enter(self) -> None:
        '''Fired at the Button hover enter event.'''
        Window.set_system_cursor('hand')
        self._bg_color = self._hover_color

    def on_leave(self) -> None:
        '''Fired at the Button hover leave event.'''
        Window.set_system_cursor('arrow')
        self._bg_color = (0, 0, 0, 0)

    def _set_icon(self, *args) -> None:
        '''Add icon to the Button'''
        if self.glow_icon is not None:
            self.unbind(icon_size=self.glow_icon.setter('font_size'),
                        _icon_color=self.glow_icon.setter('color'),
                        icon=self.glow_icon.setter('icon'))
            self.ids.glow_button_container.remove_widget(self.glow_icon)

        if self.icon != 'blank':
            self.glow_icon = GlowIcon(
                pos_hint={'center_y': 0.5, 'center_x': .5},
                icon_size=self.icon_size,
                color=self._icon_color,
                icon=self.icon,
            )
            self.bind(icon_size=self.glow_icon.setter('font_size'),
                      _icon_color=self.glow_icon.setter('color'),
                      icon=self.glow_icon.setter('icon'))

            if self.icon_position in {'left', 'top'}:
                self.ids.glow_button_container.add_widget(self.glow_icon, index=2)
            elif self.icon_position in {'right', 'bottom'}:
                self.ids.glow_button_container.add_widget(self.glow_icon)

            if self.icon_position in {'top', 'bottom'}:
                self.ids.glow_button_container.orientation = 'vertical'

            if self.text is None:
                if 'glow_button_text' in self.ids:
                    self.ids.glow_button_container.remove_widget(self.ids.glow_button_text)
                    self.ids.pop('glow_button_text')

    def on_selected(self, sidepanelbutton: Self, selected: bool) -> None:
        if self._selected_color is None:
            self.set_default_colors()

        if selected:
            self._text_color = self._selected_color
            self._icon_color = self._selected_color
        else:
            self._text_color = self.text_color if self.text_color else self.theme_cls.text_color
            self._icon_color = self.icon_color if self.icon_color else self.theme_cls.text_color

    def on_touch_down(self, touch: MotionEvent) -> bool:
        '''Fired at the Button on_touch_down event.'''
        if self.collide_point(*touch.pos):
            if not self.disabled and not touch.is_mouse_scrolling:
                animation = Animation(
                    _text_color=self.theme_cls.darken_or_lighten_color(self._text_color),
                    _icon_color=self.theme_cls.darken_or_lighten_color(self._icon_color),
                    d=.01,
                )
                animation.start(self)

        return ButtonBehavior.on_touch_down(self, touch)

    def on_touch_up(self, touch: MotionEvent) -> bool:
        def update_colors() -> None:
            if not self.disabled:
                parent = self.parent
                while not isinstance(parent, GlowSidePanel):
                    parent = parent.parent
                parent.select_button(self)

                if self.selected:
                    self._text_color = self._selected_color
                    self._icon_color = self._selected_color
                else:
                    self._text_color = self.text_color if self.text_color else self.theme_cls.text_color
                    self._icon_color = self.icon_color if self.icon_color else self.theme_cls.text_color
            else:
                self.set_disabled_colors()

        if touch.grab_current == self:
            Clock.schedule_once(lambda _: update_colors(), 0.1)

        return ButtonBehavior.on_touch_up(self, touch)

    def initialize_sidepanelbutton(self, *args) -> None:
        '''Initializing the SidePanelButton.'''
        self.ids.glow_button_container.adaptive_size = False
        self.ids.glow_button_container.adaptive_height = True

        self.right_text_label = GlowLabel(text=self.right_text, halign='right', font_style=self.font_style)
        self.bind(right_text=self.right_text_label.setter('text'),
                  _text_color=self.right_text_label.setter('color'),
                  font_style=self.right_text_label.setter('font_style'))
        self.ids.glow_button_container.add_widget(
            self.right_text_label,
        )

    def set_default_colors(self, *args) -> None:
        '''Set defaults colors. Based on mode.'''

        if self.bg_color is not None:
            self._bg_color = (0, 0, 0, 0)

        if self.hover_color is None:
            self._hover_color = self.theme_cls.primary_light_color

        if self.border_color is not None:
            self._border_color = (0, 0, 0, 0)

        if self.text_color is None:
            self._text_color = self.theme_cls.text_color

        if self.icon_color is None:
            self._icon_color = self.theme_cls.text_color

        if self.selected_color is None:
            self._selected_color = self.theme_cls.primary_color

        if self.selected:
            self._text_color = self._selected_color
            self._icon_color = self._selected_color

    def on_theme_style(self, theme_manager: ThemeManager, theme_style: str) -> None:
        if self.disabled:
            self.set_disabled_colors()

        if self.text_color is None:
            if self.theme_cls.theme_style_switch_animation:
                Animation(
                    _text_color=self.theme_cls.text_color,
                    d=self.theme_cls.theme_style_switch_animation_duration,
                    t='linear',
                ).start(self)
            else:
                self._text_color = self.theme_cls.text_color

        if self.icon_color is None:
            if self.theme_cls.theme_style_switch_animation:
                Animation(
                    _icon_color=self.theme_cls.text_color,
                    d=self.theme_cls.theme_style_switch_animation_duration,
                    t='linear',
                ).start(self)
            else:
                self._icon_color = self.theme_cls.text_color

    def set_disabled_colors(self, *args) -> None:
        if self.disabled:
            self._text_color = self.theme_cls.disabled_color
            self._icon_color = self.theme_cls.disabled_color
        else:
            self._text_color = self.text_color if self.text_color else self.theme_cls.text_color
            self._icon_color = self.icon_color if self.icon_color else self.theme_cls.text_color


class GlowSidePanel(GlowBoxLayout):
    mode = OptionProperty(defaultvalue='overlay', options=('overlay', 'embedded'))
    '''Sidepanel mode

    :attr:`mode` is a :class:`~kivy.properties.OptionProperty`
    and defaults to `overlay`.
    '''

    anchor = OptionProperty(defaultvalue='left', options=('left', 'right'))
    '''Sidepanel anchor

    :attr:`anchor` is a :class:`~kivy.properties.OptionProperty`
    and defaults to `left`.
    '''

    scrim_color = ColorProperty(defaultvalue=(0, 0, 0, .7))
    '''The color in (r, g, b, a) or string format of the hovered scrim

    :attr:`scrim_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `(0, 0, 0, .7)`.
    '''

    close_on_click = BooleanProperty(defaultvalue=True)
    '''Close when click on scrim or keyboard escape. It automatically sets to
    False for 'embedded' mode.

    :attr:`close_on_click` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to `True`.
    '''

    state = OptionProperty(defaultvalue='close', options=('close', 'open'))
    '''Indicates if panel closed or opened. Sets after :attr:`status` change.
    Available options are: `'close'`, `'open'`.

    :attr:`state` is a :class:`~kivy.properties.OptionProperty`
    and defaults to `'close'`.
    '''

    status = OptionProperty(
        defaultvalue='closed',
        options=(
            'closed',
            'opening_with_swipe',
            'opening_with_animation',
            'opened',
            'closing_with_swipe',
            'closing_with_animation',
        ),
    )
    '''Detailed state. Sets before :attr:`state`. Bind to :attr:`state` instead
    of :attr:`status`. Available options are: `'closed'`,
    `'opening_with_swipe'`, `'opening_with_animation'`, `'opened'`,
    `'closing_with_swipe'`, `'closing_with_animation'`.

    :attr:`status` is a :class:`~kivy.properties.OptionProperty`
    and defaults to `'closed'`.
    '''

    open_progress = NumericProperty(defaultvalue=0.0)
    '''Percent of visible part of side panel. The percent is specified as a
    floating point number in the range 0-1. 0.0 if panel is closed and 1.0 if
    panel is opened.

    :attr:`open_progress` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `0.0`.
    '''

    enable_swiping = BooleanProperty(defaultvalue=True)
    '''Allow to open or close navigation drawer with swipe. It automatically
    sets to False for 'embedded' mode.

    :attr:`enable_swiping` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to `True`.
    '''

    swipe_distance = NumericProperty(defaultvalue=10)
    '''The distance of the swipe with which the movement of navigation drawer
    begins.

    :attr:`swipe_distance` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `10`.
    '''

    swipe_edge_width = NumericProperty(defaultvalue=20)
    '''The size of the area in px inside which should start swipe to drag
    navigation drawer.

    :attr:`swipe_edge_width` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `20`.
    '''

    opening_transition = StringProperty(defaultvalue='out_cubic')
    '''The name of the animation transition type to use when animating to
    the :attr:`state` `'open'`.

    :attr:`opening_transition` is a :class:`~kivy.properties.StringProperty`
    and defaults to `'out_cubic'`.
    '''

    opening_time = NumericProperty(defaultvalue=0.2)
    '''The time taken for the panel to slide to the :attr:`state` `'open'`.

    :attr:`opening_time` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `0.2`.
    '''

    closing_transition = StringProperty(defaultvalue='out_sine')
    '''The name of the animation transition type to use when animating to
    the :attr:`state` 'close'.

    :attr:`closing_transition` is a :class:`~kivy.properties.StringProperty`
    and defaults to `'out_sine'`.
    '''

    closing_time = NumericProperty(defaultvalue=0.2)
    '''The time taken for the panel to slide to the :attr:`state` `'close'`.

    :attr:`closing_time` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `0.2`.
    '''

    def _get_scrim_alpha(self) -> float:
        _scrim_alpha = 0
        if self.mode == 'overlay':
            _scrim_alpha = self._scrim_alpha_transition(self.open_progress)
        if (
            isinstance(self.parent, GlowSidePanelLayout)
            and self.parent._scrim_color
        ):
            self.parent._scrim_color.rgba = self.scrim_color[:3] + [
                self.scrim_color[3] * _scrim_alpha,
            ]
        return _scrim_alpha

    _scrim_alpha = AliasProperty(
        _get_scrim_alpha,
        None,
        bind=('_scrim_alpha_transition', 'open_progress', 'scrim_color', 'mode'),
    )
    '''Multiplier for alpha channel of :attr:`scrim_color`. For internal
    usage only.
    '''

    scrim_alpha_transition = StringProperty(defaultvalue='linear')
    '''The name of the animation transition type to use for changing
    :attr:`scrim_alpha`.

    :attr:`scrim_alpha_transition` is a :class:`~kivy.properties.StringProperty`
    and defaults to `'linear'`.
    '''

    def _get_scrim_alpha_transition(self) -> float:
        return getattr(AnimationTransition, self.scrim_alpha_transition)

    _scrim_alpha_transition = AliasProperty(
        _get_scrim_alpha_transition,
        None,
        bind=('scrim_alpha_transition',),
        cache=True,
    )

    def __init__(self, *args, **kwargs) -> None:
        self.bind(
            x=self.update_status,
            status=self.update_status,
            state=self.update_status,
        )

        super().__init__(*args, **kwargs)

    def on_parent(self, instance: Self, parent: Widget) -> None:
        if parent is None:
            Window.unbind(on_keyboard=self._on_keyboard_down)
        else:
            Window.bind(on_keyboard=self._on_keyboard_down)

        return super().on_parent(instance, parent)

    def on_mode(self, instance: Self, mode: str) -> None:
        if mode == 'embedded':
            self.enable_swiping = False
            self.close_on_click = False
        else:
            self.enable_swiping = True
            self.close_on_click = True

    def set_state(self, new_state: str = 'toggle', animation: bool = True) -> None:
        '''Change state of the side panel.
        New_state can be one of `'toggle`, `'open` or `'close'`.
        '''

        if new_state == 'toggle':
            new_state = 'close' if self.state == 'open' else 'open'

        if new_state == 'open':
            Animation.cancel_all(self, 'open_progress')
            self.status = 'opening_with_animation'
            if animation:
                Animation(
                    open_progress=1,
                    d=self.opening_time * (1 - self.open_progress),
                    t=self.opening_transition,
                ).start(self)
            else:
                self.open_progress = 1

        else:  # 'close'
            Animation.cancel_all(self, 'open_progress')
            self.status = 'closing_with_animation'
            if animation:
                Animation(
                    open_progress=0,
                    d=self.closing_time * self.open_progress,
                    t=self.closing_transition,
                ).start(self)
            else:
                self.open_progress = 0

    def update_status(self, *args) -> None:
        if self.status == 'closed':
            self.state = 'close'
        elif self.status == 'opened':
            self.state = 'open'
        elif self.open_progress == 1 and self.status == 'opening_with_animation':
            self.status = 'opened'
            self.state = 'open'
        elif self.open_progress == 0 and self.status == 'closing_with_animation':
            self.status = 'closed'
            self.state = 'close'
        elif self.status in {
            'opening_with_swipe',
            'opening_with_animation',
            'closing_with_swipe',
            'closing_with_animation',
        }:
            pass
        if self.status == 'closed':
            self.opacity = 0
        else:
            self.opacity = 1

    def get_dist_from_side(self, x: float) -> float:
        if self.anchor == 'left':
            return 0 if x < 0 else x
        return 0 if x > Window.width else Window.width - x

    def on_touch_up(self, touch: MotionEvent) -> bool:
        if self.status == 'opening_with_swipe':
            if self.open_progress > 0.5:
                self.set_state('open', animation=True)
            else:
                self.set_state('close', animation=True)
        elif self.status == 'closing_with_swipe':
            if self.open_progress < 0.5:
                self.set_state('close', animation=True)
            else:
                self.set_state('open', animation=True)
        elif self.status == 'opened':
            if self.close_on_click and not self.collide_point(
                touch.ox, touch.oy,
            ):
                self.set_state('close', animation=True)
            elif self.mode == 'embedded' and not self.collide_point(
                touch.ox, touch.oy,
            ):
                return False
        elif self.status == 'closed':
            return False
        return True

    def on_touch_down(self, touch: MotionEvent) -> bool:
        if self.status == 'closed':
            return False
        if self.status == 'opened':
            for child in self.children[:]:
                if child.dispatch('on_touch_down', touch):
                    return True
        if self.mode == 'embedded' and not self.collide_point(touch.ox, touch.oy):
            return False
        return True

    def on_touch_move(self, touch: MotionEvent) -> bool:
        if self.enable_swiping:
            if self.status == 'closed':
                if (
                    self.get_dist_from_side(touch.ox) <= self.swipe_edge_width
                    and abs(touch.x - touch.ox) > self.swipe_distance
                ):
                    self.status = 'opening_with_swipe'
            elif self.status == 'opened':
                if abs(touch.x - touch.ox) > self.swipe_distance:
                    self.status = 'closing_with_swipe'

        if self.status in {'opening_with_swipe', 'closing_with_swipe'}:
            self.open_progress = max(
                min(
                    self.open_progress
                    + (touch.dx if self.anchor == 'left' else -touch.dx)
                    / self.width,
                    1,
                ),
                0,
            )
            return True
        return super().on_touch_move(touch)

    def _on_keyboard_down(self, window: WindowBase, key: int, scancode: int, codepoint: str, modifiers: ObservableList) -> None:
        if key == 27 and self.status == 'opened' and self.close_on_click:
            self.set_state('close')
            return

    def select_button(self, button: GlowSidePanelButton) -> None:
        for child in self.children:
            if isinstance(child, GlowSidePanelButton):
                if child.selected and child != button:
                    child.selected = False
            elif isinstance(child, GlowScrollView):
                for sub_child in child.children[0].children:
                    if isinstance(sub_child, GlowSidePanelButton):
                        if sub_child.selected and sub_child != button:
                            sub_child.selected = False

        button.selected = True


class GlowSidePanelLayout(GlowFloatLayout):

    _scrim_color = ObjectProperty(defaultvalue=None)
    _scrim_rectangle = ObjectProperty(defaultvalue=None)
    _screen_manager = ObjectProperty(defaultvalue=None)
    _side_panel = ObjectProperty(defaultvalue=None)

    def __init__(self, *args, **kwargs) -> None:
        self.bind(width=self.update_pos)

        super().__init__(*args, **kwargs)

    def add_widget(self, widget: Widget, index: int = 0, canvas: str | None = None) -> None:
        """
        Only two widgets are allowed:
        :class:`~kivy.uix.screenmanager.ScreenManager` and
        :class:`~GlowSidePanel`.
        """

        if not isinstance(widget, (GlowSidePanel, ScreenManager)):
            raise GlowSidePanelException(
                'The GlowSidePanelLayout must contain only `GlowSidePanel` and `ScreenManager`',
            )

        if isinstance(widget, ScreenManager):
            self._screen_manager = widget
            self.add_scrim(widget)

        if isinstance(widget, GlowSidePanel):
            self._side_panel = widget
            widget.bind(
                open_progress=self.update_pos,
                mode=self.update_pos,
                width=self.update_pos,
                anchor=self.update_pos,
            )
        if len(self.children) > 2:
            raise GlowSidePanelException(
                'The GlowSidePanelLayout must contain only `GlowSidePanel` and `ScreenManager`',
            )

        return super().add_widget(widget)

    def update_pos(self, *args) -> None:
        if self._side_panel is None and self._screen_manager is None:
            return

        if self._side_panel.mode == 'embedded':
            self._screen_manager.size_hint_x = None
            if self._side_panel.anchor == 'left':
                self._screen_manager.x = self._side_panel.width * self._side_panel.open_progress
                self._screen_manager.width = self.width - self._screen_manager.x
            else:
                self._screen_manager.x = 0
                self._screen_manager.width = self._side_panel.x

        elif self._side_panel.mode == 'overlay':
            self._screen_manager.size_hint_x = None
            self._screen_manager.x = 0
            if self._side_panel.anchor == 'left':
                self._screen_manager.width = self.width - self._screen_manager.x
            else:
                self._screen_manager.width = self.width

    def update_scrim_rectangle(self, *args) -> None:
        self._scrim_rectangle.pos = self.pos
        self._scrim_rectangle.size = self.size

    def add_scrim(self, instance: ScreenManager) -> None:
        with instance.canvas.after:
            self._scrim_color = Color(rgba=(0, 0, 0, 0))
            self._scrim_rectangle = Rectangle(
                pos=instance.pos,
                size=instance.size,
            )
            instance.bind(
                pos=self.update_scrim_rectangle,
                size=self.update_scrim_rectangle,
            )
