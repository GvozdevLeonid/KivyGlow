__all__ = ('GlowScrollView', )

from kivy.uix.scrollview import ScrollView

from kivy_glow.uix.behaviors import (
    DeclarativeBehavior,
    AdaptiveBehavior,
    StyleBehavior,
    ThemeBehavior,
)


class GlowScrollView(DeclarativeBehavior,
                     AdaptiveBehavior,
                     ThemeBehavior,
                     StyleBehavior,
                     ScrollView,
                     ):
    pass
