__all__ = ('GlowRecycleView', )

from kivy.uix.recycleview import RecycleView

from kivy_glow.uix.behaviors import (
    DeclarativeBehavior,
    AdaptiveBehavior,
    StyleBehavior,
    ThemeBehavior,
)


class GlowRecycleView(DeclarativeBehavior,
                      AdaptiveBehavior,
                      ThemeBehavior,
                      StyleBehavior,
                      RecycleView,
                      ):
    pass
