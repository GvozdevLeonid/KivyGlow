__all__ = ('GlowRecycleView', )

from kivy.uix.recycleview import RecycleView

from kivy_glow.uix.behaviors import (
    AdaptiveBehavior,
    DeclarativeBehavior,
    StyleBehavior,
    ThemeBehavior,
)


class GlowRecycleView(DeclarativeBehavior,
                      AdaptiveBehavior,
                      ThemeBehavior,
                      StyleBehavior,
                      RecycleView,
                      ):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bar_inactive_color = self.theme_cls.primary_color[:3] + [.2]
        self.bar_color = self.theme_cls.primary_color
        self.scroll_type = ['bars', 'content']
        self.always_overscroll = False
        self.bar_margin = '3dp'
        self.bar_width = '5dp'
