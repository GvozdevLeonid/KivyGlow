__all__ = ('GlowRelativeLayout', )

from kivy.uix.relativelayout import RelativeLayout

from kivy_glow.uix.behaviors import (
    AdaptiveBehavior,
    DeclarativeBehavior,
    StyleBehavior,
    ThemeBehavior,
)


class GlowRelativeLayout(DeclarativeBehavior,
                         AdaptiveBehavior,
                         ThemeBehavior,
                         StyleBehavior,
                         RelativeLayout,
                         ):
    pass
