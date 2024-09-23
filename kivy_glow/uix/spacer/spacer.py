__all__ = ('GlowHSpacer', 'GlowVSpacer')

from kivy_glow.uix.widget import GlowWidget


class GlowHSpacer(GlowWidget):
    adaptive_height = True


class GlowVSpacer(GlowWidget):
    adaptive_width = True
