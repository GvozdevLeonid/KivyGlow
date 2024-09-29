__all__ = ('GlowIcon', )

from kivy_glow.uix.label import GlowLabel
from kivy_glow import kivy_glow_uix_dir
from kivy.lang import Builder
import os
from kivy_glow.icons import (
    material_icons,
    icons,
)
from kivy.properties import (
    VariableListProperty,
    BooleanProperty,
    NumericProperty,
    StringProperty,
    OptionProperty,
    AliasProperty,
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
    allowed_icon_styles = ('outlined', 'rounded', 'sharp')
    allowed_icon_weights = ('100', '200', '300', '400', '500', '600', '700')

    allow_selection = False
    '''Do not allow select the icon'''

    icon = StringProperty('blank')
    '''Icon name.

    For variable icons use:
        `{icon_name}:{icon_style}:{icon_weight}`
        or
        `{icon_name}:{icon_style}:{icon_weight}:filled`

        icon_style = 'outlined', 'rounded', 'sharp'
        icon_weight = '100', '200', '300', '400', '500', '600', '700'

    :attr:`icon` is an :class:`~kivy.properties.StringProperty`
    and defaults to `blank`.
    '''

    icon_size = NumericProperty('24dp')
    '''Icon size.

    :attr:`icon_size` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `24dp`.
    '''

    badge_content = StringProperty('')
    '''Icon badge content. Can be icon or text.

    For icon set :attr:`badge_font_name` as `'Icons'`

    :attr:`badge_content` is an :class:`~kivy.properties.StringProperty`
    and defaults to `empty`.
    '''

    badge_font_name = StringProperty('MontserratLight')
    '''Icon badge font name.

    For icon in badge set `'Icons'`

    :attr:`badge_font_name` is an :class:`~kivy.properties.StringProperty`
    and defaults to `MontserratLight`.
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

    def _get_icon_font_name(self):
        if len(self.icon.split(':')) == 3:
            icon_name, icon_style, icon_weight = self.icon.split(':')
            if (
                icon_style in self.allowed_icon_styles
                and icon_weight in self.allowed_icon_weights
            ):
                return f'MaterialIcons_{icon_style}_{icon_weight}'
        elif len(self.icon.split(':')) == 4:
            icon_name, icon_style, icon_weight, filled = self.icon.split(':')
            if (
                icon_style in self.allowed_icon_styles
                and icon_weight in self.allowed_icon_weights
            ):
                return f'MaterialIcons_{icon_style}_{icon_weight}_{filled}'
        else:
            return 'Icons'

    _icon_font_name = AliasProperty(
        _get_icon_font_name, bind=('icon', )
    )

    def _get_formated_icon(self):
        if (
            len(self.icon.split(':')) == 1
            and self.icon in icons.keys()
        ):
            return u'{}'.format(icons[self.icon])

        elif len(self.icon.split(':')) == 3:
            icon_name, icon_style, icon_weight = self.icon.split(':')
            if (
                icon_style in self.allowed_icon_styles
                and icon_weight in self.allowed_icon_weights
                and icon_name in material_icons.keys()
            ):
                return u'{}'.format(material_icons[icon_name])

        elif len(self.icon.split(':')) == 4:
            icon_name, icon_style, icon_weight, filled = self.icon.split(':')
            if (
                icon_style in self.allowed_icon_styles
                and icon_weight in self.allowed_icon_weights
                and icon_name in material_icons.keys()
            ):
                return u'{}'.format(material_icons[icon_name])

        return 'blank'

    _formatted_icon = AliasProperty(
        _get_formated_icon, bind=('icon', )
    )
