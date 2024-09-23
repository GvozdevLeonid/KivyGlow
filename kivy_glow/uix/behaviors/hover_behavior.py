__all__ = ('HoverBehavior', )

from kivy.input.motionevent import MotionEvent
from kivy.uix.scrollview import ScrollView
from kivy.event import EventDispatcher
from typing import Self
from kivy.core.window import (
    WindowBase,
    Window,
)
from kivy.properties import (
    BooleanProperty,
)


class HoverBehavior(EventDispatcher):
    '''
    Hover behavior class.

    For more information, see in the :class:`~kivy_glow.uix.behaviors.HoverBehavior`

    :Events:
        :attr:`on_enter`
            Fired when mouse enters the bbox of the widget.
        :attr:`on_leave`
           Fired when the mouse exits the widget.
    '''

    hover = BooleanProperty(False)
    '''True, if the mouse cursor is within the borders of the widget.

    :attr:`hover` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    '''

    hovered_widget = None
    '''Global current hovered widget.'''

    def __init__(self, *args, **kwargs) -> None:
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')

        super().__init__(*args, **kwargs)

    def on_parent(self, instance: Self, parent) -> None:
        if parent is None:
            Window.unbind(on_motion=self._on_window_motion)
        else:
            Window.bind(on_motion=self._on_window_motion)

        if hasattr(super(), 'on_parent'):
            return super().on_parent(instance, parent)

    def _on_window_motion(self, window: WindowBase, etype: str, motionevent: MotionEvent) -> bool:
        '''Fired at the Window motion event.'''
        motionevent.scale_for_screen(window.width, window.height)
        if 'hover' == motionevent.type_id:
            if not self.disabled and self.get_root_window():
                pos = self.to_widget(*motionevent.pos)
                if self.collide_point(*pos):

                    if self not in Window.children[0].walk():
                        return False

                    if not self._is_visible():
                        return False

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

        return False

    def _is_visible(self) -> bool:
        '''Check if the widget is visible within its ScrollView.'''
        widget = self
        while widget is not None and not isinstance(widget, WindowBase):
            if isinstance(widget, ScrollView):
                sv = widget
                widget_x, widget_y = self.to_window(self.x, self.y)
                sv_x, sv_y = sv.to_window(sv.x, sv.y)

                visible_x1 = sv_x
                visible_y1 = sv_y
                visible_x2 = sv_x + sv.width
                visible_y2 = sv_y + sv.height

                if not (visible_x1 <= widget_x <= visible_x2 and
                        visible_y1 <= widget_y <= visible_y2):
                    return False

            widget = widget.parent
        return True

    def on_disabled(self, instance: Self, disabled: bool) -> None:
        '''Fired at the widget disable event.'''
        if self.hover and disabled:
            HoverBehavior.hovered_widget = None
            self.hover = False
            self.dispatch('on_leave')

    def on_enter(self) -> None:
        '''Fired at the widget hover enter event.'''
        pass

    def on_leave(self) -> None:
        '''Fired at the widget hover leave event.'''
        pass
