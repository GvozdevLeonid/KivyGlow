__all__ = ('GlowIcon', )

import os

from kivy.lang import Builder
from kivy.properties import (
    AliasProperty,
    ColorProperty,
    NumericProperty,
    StringProperty,
    VariableListProperty,
)

from kivy_glow import kivy_glow_uix_dir
from kivy_glow.icons import (
    icons,
    material_icons,
)
from kivy_glow.uix.label import GlowLabel

with open(
    os.path.join(kivy_glow_uix_dir, 'icon', 'icon.kv'), encoding='utf-8',
) as kv_file:
    Builder.load_string(kv_file.read())


class GlowIcon(GlowLabel):
    '''Icon widget

    For more information, see in the :class:`~kivy_glow.uix.label.GlowLabel` class documentation.
    '''

    allow_selection = False
    '''Do not allow select the icon'''

    icon = StringProperty(defaultvalue='blank')
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

    icon_size = NumericProperty(defaultvalue='24dp')
    '''Icon size.

    :attr:`icon_size` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `24dp`.
    '''

    badge_content = StringProperty(defaultvalue='')
    '''Icon badge content. Can be icon (only static icons) or text.

    :attr:`badge_content` is an :class:`~kivy.properties.StringProperty`
    and defaults to `empty`.
    '''

    badge_font_name = StringProperty(defaultvalue='MontserratLight')
    '''Icon badge font name.

    :attr:`badge_font_name` is an :class:`~kivy.properties.StringProperty`
    and defaults to `MontserratLight`.
    '''

    badge_border_radius = VariableListProperty(defaultvalue=[0], length=4)
    '''Badge canvas radius.

    :attr:`badge_border_radius` is an :class:`~kivy.properties.VariableListProperty`
    and defaults to `(0, 0, 0, 0)`.
    '''

    badge_border_color = ColorProperty(defaultvalue=None, allownone=True)
    '''The color in (r, g, b, a) or string format of the badge border

    :attr:`badge_border_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    badge_border_width = VariableListProperty(defaultvalue=[0], length=4)
    '''Badge border width.

    :attr:`badge_border_width` is an :class:`~kivy.properties.VariableListProperty`
    and defaults to `(0, 0, 0, 0)`.
    '''

    badge_bg_color = ColorProperty(defaultvalue=None, allownone=True)
    '''The color in (r, g, b, a) or string format of the badge background

    :attr:`badge_bg_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    badge_color = ColorProperty(defaultvalue=None, allownone=True)
    '''The color in (r, g, b, a) or string format of the badge content

    :attr:`badge_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    '''

    badge_padding = VariableListProperty(defaultvalue=['3dp'], length=4)
    '''Badge padding.

    :attr:`badge_padding` is an :class:`~kivy.properties.VariableListProperty`
    and defaults to `('3dp', '3dp', '3dp', '3dp')`.
    '''

    allowed_icon_styles = ('outlined', 'rounded', 'sharp')
    allowed_icon_weights = ('100', '200', '300', '400', '500', '600', '700')

    def _get_icon_font_name(self) -> str:
        if len(self.icon.split(':')) == 3:
            icon_name, icon_style, icon_weight = self.icon.split(':')
            if (
                icon_name in material_icons.keys()
                and icon_style in self.allowed_icon_styles
                and icon_weight in self.allowed_icon_weights
            ):
                return f'MaterialIcons_{icon_style}_{icon_weight}'
        elif len(self.icon.split(':')) == 4:
            icon_name, icon_style, icon_weight, filled = self.icon.split(':')
            if (
                icon_name in material_icons.keys()
                and icon_style in self.allowed_icon_styles
                and icon_weight in self.allowed_icon_weights
            ):
                return f'MaterialIcons_{icon_style}_{icon_weight}_{filled}'

        return 'Icons'

    _icon_font_name = AliasProperty(
        _get_icon_font_name, bind=('icon', ),
    )

    def _get_formated_icon(self) -> str:
        if (
            len(self.icon.split(':')) == 1
            and self.icon in icons.keys()
        ):
            return f'{icons[self.icon]}'

        if len(self.icon.split(':')) == 3:
            icon_name, icon_style, icon_weight = self.icon.split(':')
            if (
                icon_style in self.allowed_icon_styles
                and icon_weight in self.allowed_icon_weights
                and icon_name in material_icons.keys()
            ):
                return f'{material_icons[icon_name]}'

        elif len(self.icon.split(':')) == 4:
            icon_name, icon_style, icon_weight, _ = self.icon.split(':')
            if (
                icon_style in self.allowed_icon_styles
                and icon_weight in self.allowed_icon_weights
                and icon_name in material_icons.keys()
            ):
                return f'{material_icons[icon_name]}'

        return 'blank'

    _formatted_icon = AliasProperty(
        _get_formated_icon, bind=('icon', ),
    )
