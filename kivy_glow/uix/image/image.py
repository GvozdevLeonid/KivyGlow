__all__ = ('GlowImage', )

from kivy.uix.image import AsyncImage

from kivy_glow.uix.widget import GlowWidget


class GlowImage(GlowWidget,
                AsyncImage):
    '''Simple wrapper for AsyncImage

    For more information, see in the
    :class:`~kivy_glow.uix.widget.GlowWidget` and
    :class:`~kivy.uix.image.AsyncImage`
    classes documentation.
    '''
