__all__ = ('GlowImage', )

from kivy_glow.uix.widget import GlowWidget
from kivy.uix.image import AsyncImage


class GlowImage(GlowWidget,
                AsyncImage):
    '''Simple wrapper for AsyncImage

    For more information, see in the
    :class:`~kivy_glow.uix.widget.GlowWidget` and
    :class:`~kivy.uix.image.AsyncImage`
    classes documentation.
    '''
