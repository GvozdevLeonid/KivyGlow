__all__ = ('GlowScreenManager', )

from kivy.uix.screenmanager import ScreenManager

from kivy_glow.uix.behaviors import (
    AdaptiveBehavior,
    DeclarativeBehavior,
)


class GlowScreenManager(DeclarativeBehavior,
                        AdaptiveBehavior,
                        ScreenManager,
                        ):
    pass
