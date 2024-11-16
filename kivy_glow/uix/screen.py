__all__ = ('GlowScreen', )

from kivy.uix.screenmanager import Screen

from kivy_glow.uix.behaviors import (
    AdaptiveBehavior,
    DeclarativeBehavior,
    StyleBehavior,
    ThemeBehavior,
)


class GlowScreen(DeclarativeBehavior,
                 AdaptiveBehavior,
                 ThemeBehavior,
                 StyleBehavior,
                 Screen,
                 ):
    pass
