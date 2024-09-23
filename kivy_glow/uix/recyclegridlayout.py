__all__ = ('GlowRecycleGridLayout', )

from kivy.uix.recyclegridlayout import RecycleGridLayout

from kivy_glow.uix.behaviors import (
    DeclarativeBehavior,
    AdaptiveBehavior,
    StyleBehavior,
    ThemeBehavior,
)


class GlowRecycleGridLayout(DeclarativeBehavior,
                            AdaptiveBehavior,
                            ThemeBehavior,
                            StyleBehavior,
                            RecycleGridLayout,
                            ):
    pass
