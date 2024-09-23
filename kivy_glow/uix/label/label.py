__all__ = ('GlowLabel', )

from kivy.core.text.markup import MarkupLabel as CoreMarkupLabel
from kivy.input.motionevent import MotionEvent
from kivy.core.text import Label as CoreLabel
from kivy.core.clipboard import Clipboard
from kivy.utils import get_hex_from_color
from kivy_glow import kivy_glow_uix_dir
from kivy.uix.textinput import Selector
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.uix.bubble import Bubble
from kivy.uix.label import Label
from kivy.base import EventLoop
from kivy.lang import Builder
from kivy.clock import Clock
from typing import Self
from weakref import ref
import os
from kivy_glow.uix.behaviors import (
    DeclarativeBehavior,
    AdaptiveBehavior,
    HoverBehavior,
    StyleBehavior,
    ThemeBehavior,
)
from kivy.core.window import (
    WindowBase,
    Window,
)
from kivy.properties import (
    BooleanProperty,
    ObservableList,
    StringProperty,
    OptionProperty,
    ObjectProperty,
    ColorProperty,
)
from kivy.graphics import (
    Rectangle,
    Color,
)
from kivy.metrics import (
    inch,
    sp,
)

with open(
    os.path.join(kivy_glow_uix_dir, 'label', 'label.kv'), encoding='utf-8'
) as kv_file:
    Builder.load_string(kv_file.read())


class GlowLabelSelectCopy(Bubble):
    '''Bubble with actions copy and select all text

    For more information, see in the :class:`~kivy.uix.bubble.Bubble` class documentation.
    '''

    label = ObjectProperty(None)
    '''
        Holds a reference to the Label this Bubble belongs to.
    '''
    but_copy = ObjectProperty(None)
    '''
        Reference to the button copy.
    '''
    but_selectall = ObjectProperty(None)
    '''
        Reference to the button select all.
    '''

    _check_parent_ev = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_touch_up(self, touch: MotionEvent) -> bool:
        '''Fired at the Bubble on_touch_up event.'''
        for child in self.content.children:
            if ref(child) in touch.grab_list:
                touch.grab_current = child
                break
        return super().on_touch_up(touch)

    def on_parent(self, instance: Self, parent: Widget) -> None:
        '''Fired when the :attr:`parent` value changes.'''
        self.but_selectall.opacity = 1

    def do(self, action: str) -> None:
        '''Call action'''
        label = self.label

        if action == 'copy':
            label._copy()
        elif action == 'selectall':
            label._select_text()
            label._update_selection()
            anim = Animation(opacity=0, d=.333)
            anim.start(self.but_selectall)
            return

        self.hide()

    def hide(self) -> None:
        '''Hide Bubble'''
        parent = self.parent
        if not parent:
            return

        anim = Animation(opacity=0, d=.225)
        anim.bind(on_complete=lambda *args: parent.remove_widget(self))
        anim.start(self)


class GlowLabel(DeclarativeBehavior,
                AdaptiveBehavior,
                ThemeBehavior,
                StyleBehavior,
                HoverBehavior,
                Label):

    '''Label widget.

    It has support for selecting text both for computers using the mouse and for mobile devices (hadles and buble with actions for selecting all text and copying).
    Also supports double tap event (select a word) and triple tap event (select all text).

    :Events:
        :attr:`on_double_tap`
            Called on double tap event
        :attr:`on_triple_tap`
            Called on triple tap event

    For more information, see in the
    :class:`~kivy_glow.uix.behaviors.DeclarativeBehavior` and
    :class:`~kivy_glow.uix.behaviors.AdaptiveBehavior` and
    :class:`~kivy_glow.uix.behaviors.ThemeBehavior` and
    :class:`~kivy_glow.uix.behaviors.StyleBehavior` and
    :class:`~kivy_glow.uix.behaviors.HoverBehavior` and
    :class:`~kivy.uix.label.Label`
    classes documentation.
    '''

    color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the text

    :attr:`color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    selection_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the background color for highlight selected text.

    :attr:`selection_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    allow_selection = BooleanProperty(False)
    '''If selection is enabled

    :attr:`allow_selection` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    '''

    font_style = StringProperty('BodyM')
    '''Font style (font, size, bold and/or italic, letter spacing, line height). Check out the available styles.

    :attr:`font_style` is an :class:`~kivy.properties.StringProperty`
    and defaults to `BodyM`.
    '''

    theme_color = OptionProperty(
        'Primary',
        options=(
            'Primary',
            'Secondary',
            'PrimaryOpposite',
            'SecondaryOpposite',
            'Error',
        )
    )
    '''Available standard text color schemes.

    :attr:`theme_color` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `Primary`.
    '''

    handle_image_left = StringProperty('atlas://data/images/defaulttheme/selector_left')
    '''Image used to display the Left handle on the Label for selection.

    :attr:`handle_image_left` is an :class:`~kivy.properties.StringProperty`
    and defaults to `atlas://data/images/defaulttheme/selector_left`.
    '''

    handle_image_right = StringProperty('atlas://data/images/defaulttheme/selector_right')
    '''Image used to display the Right handle on the Label for selection.

    :attr:`handle_image_right` is an :class:`~kivy.properties.StringProperty`
    and defaults to `atlas://data/images/defaulttheme/selector_right`.
    '''

    _color = ColorProperty((1, 1, 1, 1))
    _selection_color = ColorProperty((1, 1, 1, 1))
    _focus = BooleanProperty(False)

    def __init__(self, *args, **kwargs):
        self.bind(color=self.setter('_color'))
        self.bind(selection_color=self.setter('_selection_color'))

        self.selected_text = ''
        self._selection_from = None
        self._selection_to = None

        self._handle_left = None
        self._handle_right = None
        self._bubble = None

        super().__init__(*args, **kwargs)

        self.register_event_type('on_double_tap')
        self.register_event_type('on_triple_tap')

        Clock.schedule_once(lambda _: self._remove_bg_color_instruction(), -1)
        Clock.schedule_once(lambda _: self.on_font_style(self, self.font_style), -1)
        Clock.schedule_once(lambda _: self.on_theme_color(self, self.theme_color), -1)

    def _create_label(self) -> None:
        '''Modified default function'''
        # create the core label class according to markup value
        if self._label is not None:
            cls = self._label.__class__
        else:
            cls = None
        markup = self.markup
        if (markup and cls is not CoreMarkupLabel) or \
           (not markup and cls is not CoreLabel):
            # markup have change, we need to change our rendering method.
            dkw = {x: getattr(self, x) for x in self._font_properties}
            dkw['usersize'] = self.text_size
            if self.disabled:
                dkw['color'] = self.disabled_color
                dkw['outline_color'] = self.disabled_outline_color
            else:
                dkw['color'] = self._color

            if markup:
                self._label = CoreMarkupLabel(**dkw)
            else:
                self._label = CoreLabel(**dkw)

    def _trigger_texture_update(self, name=None, source=None, value=None) -> None:
        '''Modified default function'''
        # check if the label core class need to be switch to a new one
        if name == 'markup':
            self._create_label()
        if source:
            if name == 'text':
                self._label.text = value
            elif name == 'text_size':
                self._label.usersize = value
            elif name == 'font_size':
                self._label.options[name] = value
            elif name == 'disabled_color' and self.disabled:
                self._label.options['color'] = value
            elif name == 'disabled_outline_color' and self.disabled:
                self._label.options['outline_color'] = value
            elif name == 'color':
                self._label.options['color'] = value if not self.disabled else self.disabled_color
            elif name == 'outline_color':
                self._label.options['outline_color'] = value if not self.disabled else self.disabled_outline_color
            elif name == 'disabled':
                self._label.options['color'] = self.disabled_color if value else self._color
                self._label.options['outline_color'] = self.disabled_outline_color if value else self.outline_color

            # NOTE: Compatibility code due to deprecated properties
            # Must be removed along with padding_x and padding_y
            elif name == 'padding_x':
                self._label.options['padding'][::2] = [value] * 2
            elif name == 'padding_y':
                self._label.options['padding'][1::2] = [value] * 2

            else:
                self._label.options[name] = value

        self._trigger_texture()

    def texture_update(self, *largs) -> None:
        '''Modified default function'''

        mrkup = self._label.__class__ is CoreMarkupLabel
        self.texture = None

        if (
            not self._label.text
            or (self.halign == 'justify' or self.strip)
            and not self._label.text.strip()
        ):
            self.texture_size = (0, 0)
            self.is_shortened = False
            if mrkup:
                self.refs, self._label._refs = {}, {}
                self.anchors, self._label._anchors = {}, {}
        else:
            if mrkup:
                text = self.text
                # we must strip here, otherwise, if the last line is empty,
                # markup will retain the last empty line since it only strips
                # line by line within markup
                if self.halign == 'justify' or self.strip:
                    text = text.strip()
                self._label.text = ''.join(('[color=',
                                            get_hex_from_color(
                                                self.disabled_color if
                                                self.disabled else self._color),
                                            ']', text, '[/color]'))
                self._label.refresh()
                # force the rendering to get the references
                if self._label.texture:
                    self._label.texture.bind()
                self.refs = self._label.refs
                self.anchors = self._label.anchors
            else:
                self._label.refresh()
            texture = self._label.texture
            if texture is not None:
                self.texture = self._label.texture
                self.texture_size = list(self.texture.size)
            self.is_shortened = self._label.is_shortened

    def on_font_style(self, label_instance: Self, font_style: str) -> None:
        '''Fired when the :attr:`font_style` value changes.'''
        if font_style in self.theme_cls.font_styles.keys():
            _font_style = self.theme_cls.font_styles[font_style]
            self.font_name = _font_style['font_name']
            self.font_size = sp(_font_style['font_size'])
            self.line_height = sp(_font_style['font_size']) / sp(_font_style['line_height'])
            self.bold = _font_style['bold']
            self.italic = _font_style['italic']

    def on_allow_selection(self, label_instance: Self, allow_selection: bool) -> None:
        '''Fired when the :attr:`allow_selection` value changes.'''
        if allow_selection:
            Window.bind(on_key_down=self._on_keyboard_down,
                        on_touch_down=self._on_window_touch_down)
        else:
            Window.unbind(on_key_down=self._on_keyboard_down,
                          on_touch_down=self._on_window_touch_down)

    def on_theme_color(self, label_instance: Self, theme_color: str) -> None:
        '''Fired when the :attr:`theme_color` value changes.'''
        if self.color is None:
            if theme_color == 'Primary':
                self.color = self.theme_cls.text_color
            elif theme_color == 'Secondary':
                self.color = self.theme_cls.secondary_text_color
            elif theme_color == 'PrimaryOpposite':
                self.color = self.theme_cls.opposite_text_color
            elif theme_color == 'SecondaryOpposite':
                self.color = self.theme_cls.opposite_secondary_text_color
            elif theme_color == 'Error':
                self.color = self.theme_cls.error_color

        if self.selection_color is None:
            self.selection_color = self.theme_cls.primary_light_color[:3] + [.5]

    def on_handle_image_left(self, label_instance: Self, handle_image_left: str) -> None:
        '''Fired when the :attr:`handle_image_left` value changes.'''
        if self._handle_left:
            self._handle_left.source = handle_image_left

    def on_handle_image_right(self, label_instance: Self, handle_image_right: str) -> None:
        '''Fired when the :attr:`handle_image_right` value changes.'''
        if self._handle_right:
            self._handle_right.source = handle_image_right

    def on_touch_down(self, touch: MotionEvent) -> bool:
        '''Fired at the Label on_touch_down event.'''
        touch_pos = touch.pos
        if not self.collide_point(*touch_pos):
            self._focus = False
            self._selection_from = self._selection_to = None
            self._update_selection()
            return False

        if self.allow_selection:
            self._focus = True
            self._selection_from = self._selection_to = self._get_index_at(touch_pos)

            if touch.is_double_tap:
                self.dispatch('on_double_tap')

            if touch.is_triple_tap:
                self.dispatch('on_triple_tap')

            self._update_selection()
            return True

        return super().on_touch_down(touch)

    def on_touch_move(self, touch: MotionEvent) -> bool:
        '''Fired at the Label on_touch_move event.'''
        touch_pos = touch.pos
        if not self.collide_point(*touch_pos):
            return False

        if self.allow_selection:
            if self._selection_from is not None and self._selection_to is not None:
                self._selection_to = self._get_index_at(touch_pos)
            else:
                self._selection_from = self._selection_to = self._get_index_at(touch_pos)
            self._update_selection()
            return True

        return super().on_touch_move(touch)

    def _on_window_motion(self, window: WindowBase, etype: str, motionevent: MotionEvent) -> bool:
        '''Fired at the Window motion event.'''
        motionevent.scale_for_screen(window.width, window.height)
        if 'hover' == motionevent.type_id:
            if not self.disabled and self.allow_selection and self.get_root_window():
                pos = self.to_widget(*motionevent.pos)
                if self.collide_point(*pos):

                    if self not in Window.children[0].walk():
                        return False

                    if not self._is_visible():
                        return False

                    x, y = motionevent.pos
                    label_x, label_y = self.to_window(*self.pos)

                    local_x = x - label_x
                    local_y = y - label_y

                    x, y = float('inf'), float('inf')
                    w, h = self._label._internal_size
                    for line in self._label._cached_lines:
                        if line.w > 0:
                            x = min(line.x, x)
                            y = min(line.y, y)

                    if x <= local_x <= x + w and y <= local_y <= y + h:
                        if not self.hover:
                            self.hover = True
                            if HoverBehavior.hovered_widget is not None:
                                HoverBehavior.hovered_widget.hover = False
                                HoverBehavior.hovered_widget.dispatch('on_leave')

                            HoverBehavior.hovered_widget = self
                            self.dispatch('on_enter')

                    else:
                        if self.hover:
                            HoverBehavior.hovered_widget = None
                            self.hover = False
                            self.dispatch('on_leave')
                else:
                    if self.hover:
                        HoverBehavior.hovered_widget = None
                        self.hover = False
                        self.dispatch('on_leave')

        return False

    def _on_window_touch_down(self, window: WindowBase, touch: MotionEvent) -> None:
        '''Fired at the window on_touch_down event.'''

        local_x, local_y = self.to_local(*touch.pos)
        if not self.collide_point(local_x, local_y):
            local_y -= self.y
            local_x -= self.x
            if self._handle_left is not None:
                if self._handle_left.collide_point(local_x, local_y):
                    return

            if self._handle_right is not None:
                if self._handle_right.collide_point(local_x, local_y):
                    return

            if self._bubble is not None:
                if self._bubble.collide_point(*self._bubble.to_local(*touch.pos)):
                    return

            self._focus = False
            self._selection_from = self._selection_to = None
            self._update_selection()

    def _on_keyboard_down(self, window: WindowBase, key: int, scancode: int, codepoint: str, modifiers: ObservableList) -> None:
        '''Fired when a key pressed.'''
        if self.allow_selection and self._focus and ('ctrl' in modifiers or 'meta' in modifiers):
            self._handle_shortcut(key)

    def _handle_shortcut(self, key: int) -> None:
        '''Shortcut bindings.'''
        if key == ord('a'):
            self._select_text()
            self._update_selection()
        elif key == ord('c'):
            self._copy()

    def on_enter(self) -> None:
        '''Fired at the Label hover enter event.'''
        if self.allow_selection:
            Window.set_system_cursor('ibeam')

    def on_leave(self) -> None:
        '''Fired at the Label hover leave event.'''
        if self.allow_selection:
            Window.set_system_cursor('arrow')

    def on_double_tap(self) -> None:
        '''Fired by double-clicking on the Label.'''
        self._select_word()

    def on_triple_tap(self) -> None:
        '''Fired by triple-clicking on the Label.'''
        self._select_text()

    def _copy(self) -> None:
        '''Copy selected text to clipboard'''
        if self.allow_selection:
            return Clipboard.copy(self.selected_text)

    def _select_text(self) -> None:
        '''Select all text. Connected to tripple tap.'''
        self._selection_from = (0, 0)
        self._selection_to = len(self._label._cached_lines[-1].words[0].text) if self._label._cached_lines[-1].w > 0 else 0, self._label._cached_lines.index(self._label._cached_lines[-1])

    def _select_word(self, delimiters: str = u' .,:;!?\'"<>()[]{}') -> None:
        '''Select word. Connected to double tap.'''
        if self._selection_from is not None and self._selection_to is not None:
            if self._label._cached_lines[self._selection_from[1]].w > 0:
                line = self._label._cached_lines[self._selection_from[1]].words[0].text

                start_delimeters = [line[:self._selection_from[0]].rfind(s) + 1 for s in delimiters]
                end_delimiters = [line[self._selection_from[0]:].find(s) for s in delimiters]

                start = max([0] + start_delimeters)
                end = min([len(line)] + [value + self._selection_from[0] for value in end_delimiters if value > -1])

                self._selection_from = (start, self._selection_from[1])
                self._selection_to = (end, self._selection_from[1])

    def _get_index_at(self, pos: tuple) -> tuple[int] | None:
        '''Return text position (col, row) of the cursor from an (x, y) position.'''
        if self.text:
            x, y = pos
            label_x, label_y = self.pos

            local_x = x - label_x
            local_y = self.height - (y - label_y)

            lines = self._label._cached_lines

            row = 0
            row_y = 0
            for line in lines:
                line_y = line.y + line.h * self.line_height

                if line.w > 0:
                    row_y = line_y + line.h
                else:
                    row_y += line.h

                if line_y <= local_y < line_y + line.h and line.w > 0:
                    for i in range(len(line.words[0].text)):
                        if local_x - line.x <= self._label.get_extents(line.words[0].text[:i + 1])[0]:
                            return i, row
                    return len(line.words[0].text), row

                if local_y > row_y:
                    row += 1

            return 0, min(row, len(lines) - 1)

        return None

    def _update_selection(self) -> None:
        '''Added highlight background to selected text.'''
        self.canvas.before.remove_group('selection')
        self.canvas.before.add(Color(*self._selection_color, group='selection', mode='rgba'))
        self.selected_text = ''

        if self._selection_from is not None and self._selection_to is not None:
            if self.widget_style == 'mobile':
                self._show_handles()

            (x_start, y_start), (x_stop, y_stop) = self._selection_from, self._selection_to

            _lines_w = []
            for line in self._label._cached_lines:
                line_width = len(line.words[0].text) if line.w > 0 else 0
                _lines_w.append(line_width)

            a = int(x_start + y_start + sum(w for w in _lines_w[0:max(y_start, 0)]))
            b = int(x_stop + y_stop + sum(w for w in _lines_w[0:max(y_stop, 0)]))

            if a > b:
                a, b = b, a
            self.selected_text = self.text[a:b]

            if y_start == y_stop:
                if x_start > x_stop:
                    x_start, x_stop = x_stop, x_start
                line = self._label._cached_lines[y_start]
                if line.w > 0:
                    self.canvas.before.add(
                        Rectangle(
                            pos=(self.x + line.x + self._label.get_extents(line.words[0].text[:x_start])[0], self.top - (line.y + line.h * self.line_height) - line.h / 2),
                            size=(self._label.get_extents(line.words[0].text[x_start:x_stop])[0], line.h),
                            group='selection'
                        )
                    )
            elif y_start < y_stop:
                line_from = self._label._cached_lines[y_start]
                line_to = self._label._cached_lines[y_stop]
                for line in self._label._cached_lines[y_start + 1: y_stop]:
                    self.canvas.before.add(
                        Rectangle(
                            pos=(self.x + line.x, self.top - (line.y + line.h * self.line_height) - line.h / 2),
                            size=(line.w, line.h),
                            group='selection'
                        )
                    )
                if line_from.w > 0:
                    self.canvas.before.add(
                        Rectangle(
                            pos=(self.x + line_from.x + self._label.get_extents(line_from.words[0].text[:x_start])[0], self.top - (line_from.y + line_from.h * self.line_height) - line_from.h / 2),
                            size=(self._label.get_extents(line_from.words[0].text[x_start:])[0], line_from.h),
                            group='selection'
                        )
                    )
                if line_to.w > 0:
                    self.canvas.before.add(
                        Rectangle(
                            pos=(self.x + line_to.x, self.top - (line_to.y + line_to.h * self.line_height) - line_to.h / 2),
                            size=(self._label.get_extents(line_to.words[0].text[:x_stop])[0], line_to.h),
                            group='selection'
                        )
                    )

            elif y_start > y_stop:
                line_from = self._label._cached_lines[y_start]
                line_to = self._label._cached_lines[y_stop]
                for line in self._label._cached_lines[y_stop + 1: y_start]:
                    self.canvas.before.add(
                        Rectangle(
                            pos=(self.x + line.x, self.top - (line.y + line.h * self.line_height) - line.h / 2),
                            size=(line.w, line.h),
                            group='selection'
                        )
                    )

                if line_to.w > 0:
                    self.canvas.before.add(
                        Rectangle(
                            pos=(self.x + line_to.x + self._label.get_extents(line_to.words[0].text[:x_stop])[0], self.top - (line_to.y + line_to.h * self.line_height) - line_to.h / 2),
                            size=(self._label.get_extents(line_to.words[0].text[x_stop:])[0], line_to.h),
                            group='selection'
                        )
                    )
                if line_from.w > 0:
                    self.canvas.before.add(
                        Rectangle(
                            pos=(self.x + line_from.x, self.top - (line_from.y + line_from.h * self.line_height) - line_from.h / 2),
                            size=(self._label.get_extents(line_from.words[0].text[:x_start])[0], line_from.h),
                            group='selection'
                        )
                    )

        else:
            if self.widget_style == 'mobile':
                self._hide_handles()

    def _hide_handles(self, win: WindowBase = None) -> None:
        '''Hide selection control handlers.'''
        win = win or EventLoop.window
        if win is None:
            return
        win.remove_widget(self._handle_right)
        win.remove_widget(self._handle_left)

        if self._handle_left is not None:
            self._handle_left.unbind(on_press=self._handle_pressed,
                                     on_touch_move=self._handle_move,
                                     on_release=self._handle_released)

        if self._handle_right is not None:
            self._handle_right.unbind(on_press=self._handle_pressed,
                                      on_touch_move=self._handle_move,
                                      on_release=self._handle_released)

    def _show_handles(self) -> None:
        '''Show selection control handlers.'''
        win = EventLoop.window

        handle_right = self._handle_right
        handle_left = self._handle_left
        if self._handle_left is None:
            self._handle_left = handle_left = Selector(
                source=self.handle_image_left,
                target=self,
                window=win,
                size_hint=(None, None),
                size=('45dp', '45dp'))
            handle_left.bind(on_press=self._handle_pressed,
                             on_touch_move=self._handle_move,
                             on_release=self._handle_released)
            self._handle_right = handle_right = Selector(
                source=self.handle_image_right,
                target=self,
                window=win,
                size_hint=(None, None),
                size=('45dp', '45dp'))
            handle_right.bind(on_press=self._handle_pressed,
                              on_touch_move=self._handle_move,
                              on_release=self._handle_released)
        else:
            if self._handle_left.parent:
                self._position_handles()
                return
            if not self.parent:
                return

        if self._selection_from != self._selection_to:
            self._position_handles()
            self._handle_left.opacity = self._handle_right.opacity = 0
            win.add_widget(self._handle_left, canvas='after')
            win.add_widget(self._handle_right, canvas='after')
            anim = Animation(opacity=1, d=.4)
            anim.start(self._handle_right)
            anim.start(self._handle_left)

    def _position_handles(self) -> None:
        '''Update handlers positions.'''
        left_handler_x, left_handler_y = 0, 0
        right_handler_x, right_handler_x = 0, 0

        x = float('inf')
        w = self._label._internal_size[0]
        for line in self._label._cached_lines:
            if line.w > 0:
                x = min(line.x, x)
        center_x = x + w / 2

        _from, _to = self._selection_from, self._selection_to
        if _from[1] > _to[1] or (_from[1] == _to[1] and _from[0] > _to[0]):
            _from, _to = _to, _from

        local_x, local_y = self.to_window(self.x, self.y, relative=True)

        line_from = self._label._cached_lines[_from[1]]
        line_to = self._label._cached_lines[_to[1]]
        if line_from.w > 0:
            left_handler_y = self.height - line_from.y - line_from.h
            left_handler_x = line_from.x + self._label.get_extents(line_from.words[0].text[:_from[0]])[0]

        else:
            left_handler_y = self.height - line_from.h * (_from[1] + 1)
            left_handler_x = center_x

        if line_to.w > 0:
            right_handler_y = self.height - line_to.y - line_to.h
            right_handler_x = line_to.x + self._label.get_extents(line_to.words[0].text[:_to[0]])[0]

        else:
            right_handler_y = line_to.h * (_to[1] + 1)
            right_handler_x = center_x

        self._handle_left.pos = (left_handler_x - self._handle_left.width, left_handler_y - self._handle_left.height)
        self._handle_right.pos = (right_handler_x, right_handler_y - self._handle_right.height)

    def _handle_pressed(self, handle_instance: Selector) -> None:
        '''Fired at the handle on_touch_down event.'''
        self._hide_select_copy()

    def _handle_released(self, handle_instance: Selector) -> None:
        '''Fired at the handle on_touch_release event.'''
        if self._selection_from == self._selection_to:
            return
        x, y = self.to_window(self.x, self.y)
        self._show_select_copy(
            (
                x + handle_instance.right
                if handle_instance is self._handle_left
                else x + handle_instance.x,
                y + handle_instance.top + self.line_height
            ),
            EventLoop.window
        )

    def _handle_move(self, handle_instance: Selector, touch: MotionEvent) -> None:
        '''Fired at the handle on_touch_move event.'''
        if touch.grab_current != handle_instance:
            return

        x, y = self.to_local(*touch.pos)
        if handle_instance == self._handle_left:
            self._selection_from = self._get_index_at((x, y + self.font_size))
        elif handle_instance == self._handle_right:
            self._selection_to = self._get_index_at((x, y + self.font_size))

        self._update_selection()
        self._position_handles()

    def _hide_select_copy(self, win: WindowBase = None) -> None:
        '''Hide bubble with select_all and copy actions.'''
        bubble = self._bubble
        if not bubble:
            return

        bubble.hide()

    def _show_select_copy(self, pos: tuple, win: WindowBase, parent_changed: bool = False, pos_in_window: bool = False) -> None:
        '''Show bubble with select_all and copy actions.'''
        bubble = self._bubble
        if bubble is None:
            self._bubble = bubble = GlowLabelSelectCopy(label=self)
            self.fbind('parent', self._show_select_copy, pos, win, True)

            def hide_(*args):
                return self._hide_select_copy(win)
            self.bind(
                _focus=hide_,
            )

        else:
            win.remove_widget(bubble)
            if not self.parent:
                return
        if parent_changed:
            return

        # Search the position from the touch to the window
        lh, ls = self.line_height, self.font_size

        x, y = pos
        t_pos = (x, y) if pos_in_window else self.to_window(x, y)
        bubble_size = bubble.size
        bubble_hw = bubble_size[0] / 2.
        win_size = win.size
        bubble_pos = (t_pos[0], t_pos[1] + inch(.25))

        if (bubble_pos[0] - bubble_hw) < 0:
            # bubble beyond left of window
            if bubble_pos[1] > (win_size[1] - bubble_size[1]):
                # bubble above window height
                bubble_pos = (bubble_hw, (t_pos[1]) - (lh + ls + inch(.25)))
                bubble.arrow_pos = 'top_left'
            else:
                bubble_pos = (bubble_hw, bubble_pos[1])
                bubble.arrow_pos = 'bottom_left'
        elif (bubble_pos[0] + bubble_hw) > win_size[0]:
            # bubble beyond right of window
            if bubble_pos[1] > (win_size[1] - bubble_size[1]):
                # bubble above window height
                bubble_pos = (
                    win_size[0] - bubble_hw,
                    (t_pos[1]) - (lh + ls + inch(.25))
                )
                bubble.arrow_pos = 'top_right'
            else:
                bubble_pos = (win_size[0] - bubble_hw, bubble_pos[1])
                bubble.arrow_pos = 'bottom_right'
        else:
            if bubble_pos[1] > (win_size[1] - bubble_size[1]):
                # bubble above window height
                bubble_pos = (
                    bubble_pos[0],
                    (t_pos[1]) - (lh + ls + inch(.25))
                )
                bubble.arrow_pos = 'top_mid'
            else:
                bubble.arrow_pos = 'bottom_mid'

        bubble_pos = self.to_local(*bubble_pos)
        bubble.center_x = bubble_pos[0]
        if bubble.arrow_pos[0] == 't':
            bubble.top = bubble_pos[1]
        else:
            bubble.y = bubble_pos[1]
        Animation.cancel_all(bubble)
        bubble.opacity = 0
        win.add_widget(bubble, canvas='after')
        Animation(opacity=1, d=.225).start(bubble)

    def _remove_bg_color_instruction(self, *args):
        '''Remove bg_color_instruction as we have own.'''
        self.canvas.remove_group('bg_color_instruction')
