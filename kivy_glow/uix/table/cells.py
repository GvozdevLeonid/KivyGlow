__all__ = ('GlowLabelCell', 'GlowIconCell', 'GlowButtonCell', 'GlowIconButtonCell', 'GlowSwitchCell', 'GlowCheckboxCell')
from kivy_glow.uix.checkbox import GlowCheckbox
from kivy_glow.uix.button import GlowButton
from kivy_glow.uix.switch import GlowSwitch
from kivy_glow.uix.label import GlowLabel
from kivy_glow.uix.icon import GlowIcon


class GlowLabelCell(GlowLabel):
    value_property = ('text', 'str')
    use_wrapper = False
    allowed_properties = [
        ('cell_id', 'str'),
        ('text', 'str'),
        ('halign', 'str'),
        ('hidden', 'bool'),
        ('color', 'color'),
        ('theme_color', 'str'),
        ('font_style', 'str'),
        ('font_name', 'str'),
        ('font_size', 'int'),
        ('line_height', 'int'),
        ('selection_color', 'color'),
        ('bold', 'bool'),
        ('italic', 'bool'),
        ('disabled', 'bool'),
        ('allow_selection', 'bool')
    ]


class GlowIconCell(GlowIcon):
    value_property = ('icon', 'str')
    use_wrapper = False
    allowed_properties = [
        ('cell_id', 'str'),
        ('icon', 'str'),
        ('hidden', 'bool'),
        ('icon_size', 'int'),
        ('color', 'color'),
        ('disabled', 'bool'),
    ]


class GlowButtonCell(GlowButton):
    value_property = ('text', 'str')
    use_wrapper = False
    allowed_properties = [
        ('cell_id', 'str'),
        ('text', 'str'),
        ('hidden', 'bool'),
        ('icon', 'str'),
        ('icon_size', 'int'),
        ('icon_position', 'str'),
        ('mode', 'str'),
        ('font_style', 'str'),
        ('text_color', 'color'),
        ('icon_color', 'color'),
        ('spacing', 'int'),
        ('on_press', 'function'),
        ('on_release', 'function'),
        ('disabled', 'bool'),
    ]


class GlowIconButtonCell(GlowButton):
    value_property = ('icon', 'str')
    use_wrapper = False
    allowed_properties = [
        ('cell_id', 'str'),
        ('text', 'str'),
        ('hidden', 'bool'),
        ('icon', 'str'),
        ('icon_size', 'int'),
        ('icon_position', 'str'),
        ('mode', 'str'),
        ('font_style', 'str'),
        ('text_color', 'color'),
        ('icon_color', 'color'),
        ('spacing', 'int'),
        ('on_press', 'function'),
        ('on_release', 'function'),
        ('disabled', 'bool'),
    ]


class GlowSwitchCell(GlowSwitch):
    value_property = ('active', 'bool')
    use_wrapper = True
    use_animation = False
    allowed_properties = [
        ('cell_id', 'str'),
        ('active', 'bool'),
        ('hidden', 'bool'),
        ('icon_active', 'str'),
        ('icon_inactive', 'str'),
        ('active_color', 'color'),
        ('inactive_color', 'color'),
        ('thumb_color', 'color'),
        ('thumb_size', 'int'),
        ('mode', 'str'),
        ('on_active', 'function'),
        ('disabled', 'bool'),
    ]


class GlowCheckboxCell(GlowCheckbox):
    value_property = ('active', 'bool')
    use_wrapper = True
    allowed_properties = [
        ('cell_id', 'str'),
        ('active', 'bool'),
        ('hidden', 'bool'),
        ('checkbox_icon_inactive', 'str'),
        ('checkbox_icon_active', 'str'),
        ('active_color', 'color'),
        ('inactive_color', 'color'),
        ('animation', 'color'),
        ('on_active', 'function'),
        ('disabled', 'bool'),
    ]
