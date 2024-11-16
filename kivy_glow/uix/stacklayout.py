__all__ = ('GlowStackLayout', )

from kivy.uix.stacklayout import StackLayout

from kivy_glow.uix.behaviors import (
    AdaptiveBehavior,
    DeclarativeBehavior,
    StyleBehavior,
    ThemeBehavior,
)


class GlowStackLayout(DeclarativeBehavior,
                      AdaptiveBehavior,
                      ThemeBehavior,
                      StyleBehavior,
                      StackLayout,
                      ):
    pass
