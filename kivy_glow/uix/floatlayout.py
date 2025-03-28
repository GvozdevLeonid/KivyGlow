__all__ = ('GlowFloatLayout', )

from kivy.uix.floatlayout import FloatLayout

from kivy_glow.uix.behaviors import (
    AdaptiveBehavior,
    DeclarativeBehavior,
    StyleBehavior,
    ThemeBehavior,
)


class GlowFloatLayout(DeclarativeBehavior,
                      AdaptiveBehavior,
                      ThemeBehavior,
                      StyleBehavior,
                      FloatLayout,
                      ):
    pass
