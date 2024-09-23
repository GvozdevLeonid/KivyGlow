__all__ = ('GlowRecycleBoxLayout', )

from kivy.uix.recycleboxlayout import RecycleBoxLayout

from kivy_glow.uix.behaviors import (
    DeclarativeBehavior,
    AdaptiveBehavior,
    StyleBehavior,
    ThemeBehavior,
)


class GlowRecycleBoxLayout(DeclarativeBehavior,
                           AdaptiveBehavior,
                           ThemeBehavior,
                           StyleBehavior,
                           RecycleBoxLayout,
                           ):
    pass
