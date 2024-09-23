__all__ = ('GlowSplitter', )

from kivy.uix.behaviors import ButtonBehavior
from kivy_glow.uix.widget import GlowWidget
from kivy_glow import kivy_glow_uix_dir
from kivy.uix.splitter import Splitter
from kivy.core.window import Window
from kivy.uix.layout import Layout
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.metrics import dp
import os
from kivy_glow.uix.behaviors import (
    DeclarativeBehavior,
    AdaptiveBehavior,
    StyleBehavior,
    HoverBehavior,
    ThemeBehavior,
)
from kivy.properties import (
    VariableListProperty,
    NumericProperty,
    OptionProperty,
)

with open(
    os.path.join(kivy_glow_uix_dir, 'splitter', 'splitter.kv'), encoding='utf-8'
) as kv_file:
    Builder.load_string(kv_file.read())


class GlowSplitterStrip(ButtonBehavior,
                        HoverBehavior,
                        GlowWidget):
    def on_enter(self):
        Window.set_system_cursor('hand')

    def on_leave(self):
        Window.set_system_cursor('arrow')


class GlowSplitter(DeclarativeBehavior,
                   AdaptiveBehavior,
                   StyleBehavior,
                   ThemeBehavior,
                   Splitter):

    def __init__(self, *args, **kwargs):
        self.strip_cls = GlowSplitterStrip
        super().__init__(*args, **kwargs)


class GlowSplitterWidgetStrip(ButtonBehavior,
                              HoverBehavior,
                              GlowWidget):
    def on_enter(self):
        Window.set_system_cursor('hand')

    def on_leave(self):
        Window.set_system_cursor('arrow')


class GlowSplitterWidget(DeclarativeBehavior,
                         AdaptiveBehavior,
                         ThemeBehavior,
                         StyleBehavior,
                         Layout):

    orientation = OptionProperty('horizontal', options=('horizontal', 'vertical'))
    padding = VariableListProperty([0, 0, 0, 0], length=4)
    strip_size = NumericProperty('10dp')
    toggle_distance = NumericProperty('40dp')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.register_event_type('on_child_resized')

        self.allow_recalculate = True
        self.scheduled_update = None
        update = self._trigger_layout
        fbind = self.fbind
        fbind('padding', update)
        fbind('children', update)
        fbind('parent', update)
        fbind('size', update)
        fbind('pos', update)

    def add_widget(self, widget, index=0, *args, **kwargs):
        if len(self.children) > 0:
            strip = GlowSplitterWidgetStrip(size_hint=(None, 1) if self.orientation == 'horizontal' else (1, None), size=(self.strip_size, self.strip_size))
            strip.bind(on_touch_move=self.on_strip_move,
                       on_touch_down=self.on_strip_down,
                       on_touch_up=self.on_strip_up)
            super().add_widget(strip)

        super().add_widget(widget, index, *args, **kwargs)
        widget.bind(size_hint=self.change_child_size_hint)
        self._update_stretch()

    def remove_widget(self, widget, *args, **kwargs):
        if len(self.children) > 1:
            strip = self.children[self.children.index(widget) - 1]
            strip.unbind(on_touch_move=self.on_strip_move,
                         on_touch_down=self.on_strip_down,
                         on_touch_up=self.on_strip_up)
            super().remove_widget(strip)

        widget.unbind(size_hint=self.change_child_size_hint)
        super().remove_widget(widget, *args, **kwargs)
        self._update_stretch()

    def change_child_size_hint(self, instance, _):
        if self.allow_recalculate and not self.hidden:
            self.allow_recalculate = False
            size_hint_property = 'size_hint_x' if self.orientation == 'horizontal' else 'size_hint_y'
            relevant_children = [child for child in self.children if not isinstance(child, GlowSplitterWidgetStrip)]

            empty_size_hint = 1
            for child in relevant_children:
                empty_size_hint -= getattr(child, size_hint_property)

            empty_size_hint /= (len(relevant_children) - 1)

            for child in relevant_children:
                if child != instance:
                    current_size_hint = getattr(child, size_hint_property)
                    setattr(child, size_hint_property, current_size_hint + empty_size_hint)

            self.allow_recalculate = True

    def on_orientation(self, _, __):
        self.allow_recalculate = False
        for child in self.children:
            if isinstance(child, GlowSplitterWidgetStrip):
                child.size_hint = (None, 1) if self.orientation == 'horizontal' else (1, None)
                child.size = (self.strip_size, self.strip_size)
            else:
                child.size_hint = 1, 1

        self.allow_recalculate = True

        self._update_stretch()
        self._trigger_layout()

    def _update_stretch(self):
        self.allow_recalculate = False
        size_hint_property = 'size_hint_x' if self.orientation == 'horizontal' else 'size_hint_y'
        relevant_children = [child for child in self.children if not isinstance(child, GlowSplitterWidgetStrip)]

        num_widgets = len(relevant_children)
        if num_widgets == 0:
            return

        new_size_hint = 1.0 / num_widgets

        for child in relevant_children:
            setattr(child, size_hint_property, new_size_hint)

        self.allow_recalculate = True

    def on_strip_down(self, instance, touch):
        if touch.grab_current == instance:
            if self.scheduled_update:
                Clock.unschedule(self.scheduled_update)
            self.scheduled_update = Clock.schedule_once(lambda _: self._recalculate_child_with_strip_pos(instance, touch))

    def on_strip_up(self, instance, touch):
        if touch.grab_current == instance:
            if self.scheduled_update:
                Clock.unschedule(self.scheduled_update)
            self.scheduled_update = Clock.schedule_once(lambda _: self._recalculate_child_with_strip_pos(instance, touch))

    def on_strip_move(self, instance, touch):
        if touch.grab_current == instance:
            if self.scheduled_update:
                Clock.unschedule(self.scheduled_update)
            self.scheduled_update = Clock.schedule_once(lambda _: self._recalculate_child_with_strip_pos(instance, touch))

    def _recalculate_child_with_strip_pos(self, instance, touch):
        self.allow_recalculate = False

        child_before = self.children[self.children.index(instance) + 1]
        child_after = self.children[self.children.index(instance) - 1]

        size_hint_property = 'size_hint_x' if self.orientation == 'horizontal' else 'size_hint_y'
        size_hint_min_property = 'size_hint_min_x' if self.orientation == 'horizontal' else 'size_hint_min_y'
        position_property = 'center_x' if self.orientation == 'horizontal' else 'center_y'
        touch_property = 'x' if self.orientation == 'horizontal' else 'y'
        size_property = 'width' if self.orientation == 'horizontal' else 'height'

        current_size_hint_before = getattr(child_before, size_hint_property)
        current_size_hint_after = getattr(child_after, size_hint_property)

        child_stretch_sum = current_size_hint_before + current_size_hint_after

        proportion_change = (dp(touch.dx) if self.orientation == 'horizontal' else dp(touch.dy)) / self._stretch_space

        if self.orientation == 'vertical':
            proportion_change *= -1

        new_size_hint_before = max(0, min(child_stretch_sum, current_size_hint_before + proportion_change / 2))
        new_size_hint_after = max(0, min(child_stretch_sum, current_size_hint_after - proportion_change / 2))

        if round(getattr(child_before, size_property), 2) == getattr(child_before, size_hint_min_property) and new_size_hint_before < current_size_hint_before:
            if not hasattr(child_before, '_' + size_hint_property):
                setattr(child_before, '_' + size_hint_property, current_size_hint_before)
            if abs(getattr(instance, position_property) - getattr(touch, touch_property)) > self.toggle_distance:
                setattr(child_before, '_' + size_hint_min_property, getattr(child_before, size_hint_min_property))
                setattr(child_before, size_hint_min_property, None)
                new_size_hint_after = child_stretch_sum
                new_size_hint_before = 0
                touch.ungrab(instance)

        if hasattr(child_before, '_' + size_hint_min_property):
            if abs(getattr(instance, position_property) - getattr(touch, touch_property)) > self.toggle_distance and new_size_hint_before > current_size_hint_before:
                new_size_hint_before = getattr(child_before, '_' + size_hint_property)
                new_size_hint_after = child_stretch_sum - new_size_hint_before
                setattr(child_before, size_hint_min_property, getattr(child_before, '_' + size_hint_min_property))
                delattr(child_before, '_' + size_hint_min_property)
                delattr(child_before, '_' + size_hint_property)
                touch.ungrab(instance)
            else:
                new_size_hint_after = child_stretch_sum
                new_size_hint_before = 0

        if round(getattr(child_after, size_property), 2) == getattr(child_after, size_hint_min_property) and new_size_hint_after < current_size_hint_after:
            if not hasattr(child_after, '_' + size_hint_property):
                setattr(child_after, '_' + size_hint_property, current_size_hint_after)
            if abs(getattr(instance, position_property) - getattr(touch, touch_property)) > self.toggle_distance:
                setattr(child_after, '_' + size_hint_min_property, getattr(child_after, size_hint_min_property))
                setattr(child_after, size_hint_min_property, None)
                new_size_hint_before = child_stretch_sum
                new_size_hint_after = 0
                touch.ungrab(instance)

        if hasattr(child_after, '_' + size_hint_min_property):
            if abs(getattr(instance, position_property) - getattr(touch, touch_property)) > self.toggle_distance and new_size_hint_after > current_size_hint_after:
                new_size_hint_after = getattr(child_after, '_' + size_hint_property)
                new_size_hint_before = child_stretch_sum - new_size_hint_after
                setattr(child_after, size_hint_min_property, getattr(child_after, '_' + size_hint_min_property))
                delattr(child_after, '_' + size_hint_min_property)
                delattr(child_after, '_' + size_hint_property)
                touch.ungrab(instance)
            else:
                new_size_hint_before = child_stretch_sum
                new_size_hint_after = 0

        setattr(child_before, size_hint_property, new_size_hint_before)
        setattr(child_after, size_hint_property, new_size_hint_after)

        self.allow_recalculate = True

    def on_child_resized(self) -> None:
        pass

    def _iterate_layout(self, sizes):
        len_children = len(sizes)
        padding_left, padding_top, padding_right, padding_bottom = self.padding
        orientation = self.orientation
        padding_x = padding_left + padding_right
        padding_y = padding_top + padding_bottom

        # calculate maximum space used by size_hint
        has_bound = False
        hint = [None] * len_children
        # min size from all the None hint, and from those with sh_min
        minimum_size_bounded = 0
        if orientation == 'horizontal':
            minimum_size_y = 0
            minimum_size_none = padding_x

            for i, ((w, h), (shw, shh), _, (shw_min, shh_min),
                    (shw_max, _)) in enumerate(sizes):
                if shw is None:
                    minimum_size_none += w
                else:
                    hint[i] = shw
                    if shw_min:
                        has_bound = True
                        minimum_size_bounded += shw_min
                    elif shw_max is not None:
                        has_bound = True

                if shh is None:
                    minimum_size_y = max(minimum_size_y, h)
                elif shh_min:
                    minimum_size_y = max(minimum_size_y, shh_min)

            minimum_size_x = minimum_size_bounded + minimum_size_none
            minimum_size_y += padding_y
        else:
            minimum_size_x = 0
            minimum_size_none = padding_y

            for i, ((w, h), (shw, shh), _, (shw_min, shh_min),
                    (_, shh_max)) in enumerate(sizes):
                if shh is None:
                    minimum_size_none += h
                else:
                    hint[i] = shh
                    if shh_min:
                        has_bound = True
                        minimum_size_bounded += shh_min
                    elif shh_max is not None:
                        has_bound = True

                if shw is None:
                    minimum_size_x = max(minimum_size_x, w)
                elif shw_min:
                    minimum_size_x = max(minimum_size_x, shw_min)

            minimum_size_y = minimum_size_bounded + minimum_size_none
            minimum_size_x += padding_x

        self.minimum_size = minimum_size_x, minimum_size_y
        # do not move the w/h get above, it's likely to change on above line
        selfx = self.x
        selfy = self.y

        if orientation == 'horizontal':
            stretch_space = max(0.0, self.width - minimum_size_none)
            dim = 0
        else:
            stretch_space = max(0.0, self.height - minimum_size_none)
            dim = 1

        if has_bound:
            # make sure the size_hint_min/max are not violated
            if stretch_space < 1e-9:
                # there's no space, so just set to min size or zero

                for i, val in enumerate(sizes):
                    sh = val[1][dim]
                    if sh is None:
                        continue

                    sh_min = val[3][dim]
                    if sh_min is not None:
                        hint[i] = sh_min
                    else:
                        hint[i] = 0.  # everything else is zero
            else:
                # hint gets updated in place
                self.layout_hint_with_bounds(
                    1, stretch_space, minimum_size_bounded,
                    (val[3][dim] for val in sizes),
                    (elem[4][dim] for elem in sizes), hint)

        if orientation == 'horizontal':
            x = padding_left + selfx
            size_y = self.height - padding_y
            for i, (sh, ((w, h), (_, shh), pos_hint, _, _)) in enumerate(
                    zip(reversed(hint), reversed(sizes))):
                cy = selfy + padding_bottom
                if sh is not None:
                    w = max(0., stretch_space * sh)
                if shh:
                    h = max(0, shh * size_y)

                yield len_children - i - 1, x, cy, w, h
                x += w

        else:
            y = padding_bottom + selfy
            size_x = self.width - padding_x
            for i, (sh, ((w, h), (shw, _), pos_hint, _, _)) in enumerate(
                    zip(hint, sizes)):
                cx = selfx + padding_left

                if sh is not None:
                    h = max(0., stretch_space * sh)
                if shw:
                    w = max(0, shw * size_x)

                yield i, cx, y, w, h
                y += h

        self._stretch_space = stretch_space

    def do_layout(self, *largs):
        children = self.children
        if not children:
            l, t, r, b = self.padding
            self.minimum_size = l + r, t + b
            return

        for i, x, y, w, h in self._iterate_layout(
                [(c.size, c.size_hint, c.pos_hint, c.size_hint_min,
                  c.size_hint_max) for c in children]):
            c = children[i]
            c.pos = x, y
            shw, shh = c.size_hint
            if shw is None:
                if shh is not None:
                    c.height = (h if w > 0 else 0)
            else:
                if shh is None:
                    c.width = (w if h > 0 else 0)
                else:
                    c.size = (w, h) if (w > 0 and h > 0) else (0, 0)

        self.dispatch('on_child_resized')
