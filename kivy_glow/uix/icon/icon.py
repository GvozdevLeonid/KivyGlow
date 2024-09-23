__all__ = ('GlowIcon', )

from kivy_glow.uix.label import GlowLabel
from kivy_glow import kivy_glow_uix_dir
from kivy.lang import Builder
import os
from kivy.properties import (
    VariableListProperty,
    NumericProperty,
    StringProperty,
    ColorProperty,
)
with open(
    os.path.join(kivy_glow_uix_dir, 'icon', 'icon.kv'), encoding='utf-8'
) as kv_file:
    Builder.load_string(kv_file.read())


class GlowIcon(GlowLabel):
    '''Icon widget

    For more information, see in the :class:`~kivy_glow.uix.label.GlowLabel` class documentation.
    '''

    allow_selection = False
    '''Do not allow select the icon'''

    icon = StringProperty('blank')
    '''Label icon name.

    :attr:`icon` is an :class:`~kivy.properties.StringProperty`
    and defaults to `blank`.
    '''

    icon_size = NumericProperty('24dp')
    '''Label icon size.

    :attr:`icon_size` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `24dp`.
    '''

    badge_content = StringProperty('')
    '''Icon badge content. Can be icon or text.

    For icon set :attr:`badge_font_name` as `'Icons'`

    :attr:`badge_content` is an :class:`~kivy.properties.StringProperty`
    and defaults to `empty`.
    '''

    badge_font_name = StringProperty('Montserrat')
    '''Icon badge font name.

    For icon in badge set `'Icons'`

    :attr:`badge_font_name` is an :class:`~kivy.properties.StringProperty`
    and defaults to `MontserratThin`.
    '''

    badge_border_radius = VariableListProperty([0], length=4)
    '''Badge canvas radius.

    :attr:`badge_border_radius` is an :class:`~kivy.properties.VariableListProperty`
    and defaults to `[0, 0, 0, 0]`.
    '''

    badge_border_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the badge border

    :attr:`badge_border_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    badge_border_width = VariableListProperty([0], length=4)
    '''Badge border width.

    :attr:`badge_border_width` is an :class:`~kivy.properties.VariableListProperty`
    and defaults to `[0, 0, 0, 0]`.
    '''

    badge_bg_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the badge background

    :attr:`badge_bg_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    badge_color = ColorProperty(None, allownone=True)
    '''The color in (r, g, b, a) or string format of the badge content

    :attr:`badge_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    badge_padding = VariableListProperty(['3dp'], length=4)
    '''Badge padding.

    :attr:`badge_padding` is an :class:`~kivy.properties.VariableListProperty`
    and defaults to `['3dp', '3dp', '3dp', '3dp']`.
    '''
