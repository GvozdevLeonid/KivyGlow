__all__ = ('GlowScrollView', )

from kivy.uix.scrollview import ScrollView

from kivy_glow.uix.behaviors import (
    AdaptiveBehavior,
    DeclarativeBehavior,
    StyleBehavior,
    ThemeBehavior,
)


class GlowScrollView(DeclarativeBehavior,
                     AdaptiveBehavior,
                     ThemeBehavior,
                     StyleBehavior,
                     ScrollView,
                     ):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bar_inactive_color = self.theme_cls.primary_color[:3] + [.2]
        self.bar_color = self.theme_cls.primary_color
        self.scroll_type = ['bars', 'content']
        self.always_overscroll = False
        self.bar_margin = '3dp'
        self.bar_width = '5dp'
