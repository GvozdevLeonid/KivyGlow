__all__ = ('GlowAnchorLayout', )

from kivy.uix.anchorlayout import AnchorLayout

from kivy_glow.uix.behaviors import (
    DeclarativeBehavior,
    AdaptiveBehavior,
    StyleBehavior,
    ThemeBehavior,
)


class GlowAnchorLayout(DeclarativeBehavior,
                       AdaptiveBehavior,
                       ThemeBehavior,
                       StyleBehavior,
                       AnchorLayout,
                       ):
    pass
