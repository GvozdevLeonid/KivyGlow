__all__ = ('GlowBoxLayout', )

from kivy.uix.boxlayout import BoxLayout

from kivy_glow.uix.behaviors import (
    DeclarativeBehavior,
    AdaptiveBehavior,
    StyleBehavior,
    ThemeBehavior,
)


class GlowBoxLayout(DeclarativeBehavior,
                    AdaptiveBehavior,
                    ThemeBehavior,
                    StyleBehavior,
                    BoxLayout,
                    ):
    pass
