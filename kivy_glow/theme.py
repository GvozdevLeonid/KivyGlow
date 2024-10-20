from kivy.properties import (
    BooleanProperty,
    NumericProperty,
    OptionProperty,
    AliasProperty,
    ColorProperty,
    DictProperty,
)
from kivy.utils import get_color_from_hex
from kivy.event import EventDispatcher
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.app import App
from typing import Self
from kivy_glow.colors import (
    available_palette,
    available_hue,
    colors,
)


class ThemeManager(EventDispatcher):
    # Primary color
    primary_palette = OptionProperty('Indigo', options=available_palette)
    primary_hue = OptionProperty('500', options=available_hue)
    primary_light_hue = OptionProperty('300', options=available_hue)
    primary_dark_hue = OptionProperty('700', options=available_hue)

    def _get_primary_color(self) -> list:
        return get_color_from_hex(
            self.colors[self.primary_palette][self.primary_hue]
        )

    primary_color = AliasProperty(
        _get_primary_color, bind=('primary_palette', 'primary_hue')
    )

    def _get_primary_light_color(self) -> list:
        return get_color_from_hex(
            self.colors[self.primary_palette][self.primary_light_hue]
        )

    primary_light_color = AliasProperty(
        _get_primary_light_color, bind=('primary_palette', 'primary_light_hue')
    )

    def _get_primary_dark_color(self) -> list:
        return get_color_from_hex(
            self.colors[self.primary_palette][self.primary_dark_hue]
        )

    primary_dark_color = AliasProperty(
        _get_primary_dark_color, bind=('primary_palette', 'primary_dark_hue')
    )

    # Accent color
    accent_palette = OptionProperty('Orange', options=available_palette)
    accent_hue = OptionProperty('500', options=available_hue)
    accent_light_hue = OptionProperty('300', options=available_hue)
    accent_dark_hue = OptionProperty('700', options=available_hue)

    def _get_accent_color(self) -> list:
        return get_color_from_hex(
            self.colors[self.accent_palette][self.accent_hue]
        )

    accent_color = AliasProperty(
        _get_accent_color, bind=('accent_palette', 'accent_hue')
    )

    def _get_accent_light_color(self) -> list:
        return get_color_from_hex(
            self.colors[self.accent_palette][self.accent_light_hue]
        )

    accent_light_color = AliasProperty(
        _get_accent_light_color, bind=('accent_palette', 'accent_light_hue')
    )

    def _get_accent_dark_color(self) -> list:
        return get_color_from_hex(
            self.colors[self.accent_palette][self.accent_dark_hue]
        )

    accent_dark_color = AliasProperty(
        _get_accent_dark_color, bind=('accent_palette', 'accent_dark_hue')
    )

    # Background color
    background_palette = OptionProperty('Neutral', options=available_palette)

    # Theme
    theme_style = OptionProperty('Light', options=('Light', 'Dark'))
    theme_style_switch_animation_duration = NumericProperty(0.2)
    theme_style_switch_animation = BooleanProperty(False)

    def _get_opposite_theme_style(self, theme_style: str):
        if theme_style == 'Dark':
            return 'Light'
        elif theme_style == 'Light':
            return 'Dark'

    def _get_background_light_color(self, theme_style: str = None) -> list:
        if theme_style is None:
            theme_style = self.theme_style

        if theme_style == 'Light':
            return get_color_from_hex(
                self.colors[self.background_palette]['50']
            )
        elif theme_style == 'Dark':
            return get_color_from_hex(
                self.colors[self.background_palette]['700']
            )

    background_light_color = AliasProperty(
        _get_background_light_color, bind=('background_palette', 'theme_style')
    )

    def _get_background_color(self, theme_style: str = None) -> list:
        if theme_style is None:
            theme_style = self.theme_style

        if theme_style == 'Light':
            return get_color_from_hex(
                self.colors[self.background_palette]['100']
            )
        elif theme_style == 'Dark':
            return get_color_from_hex(
                self.colors[self.background_palette]['800']
            )

    background_color = AliasProperty(
        _get_background_color, bind=('background_palette', 'theme_style')
    )

    def _get_background_dark_color(self, theme_style: str = None) -> list:
        if theme_style is None:
            theme_style = self.theme_style

        if theme_style == 'Light':
            return get_color_from_hex(
                self.colors[self.background_palette]['200']
            )
        elif theme_style == 'Dark':
            return get_color_from_hex(
                self.colors[self.background_palette]['900']
            )

    background_dark_color = AliasProperty(
        _get_background_dark_color, bind=('background_palette', 'theme_style')
    )

    def _get_background_darkest_color(self, theme_style: str = None) -> list:
        if theme_style is None:
            theme_style = self.theme_style

        if theme_style == 'Light':
            return get_color_from_hex(
                self.colors[self.background_palette]['300']
            )
        elif theme_style == 'Dark':
            return get_color_from_hex(
                self.colors[self.background_palette]['950']
            )

    background_darkest_color = AliasProperty(
        _get_background_darkest_color, bind=('background_palette', 'theme_style')
    )

    # Text & Devider color
    def _get_text_color(self, theme_style: str = None, opposite: bool = False):
        if theme_style is None:
            theme_style = self.theme_style

        if opposite:
            theme_style = self._get_opposite_theme_style(theme_style)

        if theme_style == 'Light':
            return get_color_from_hex(
                self.colors[self.background_palette]['950']
            )
        elif theme_style == 'Dark':
            return get_color_from_hex(
                self.colors[self.background_palette]['50']
            )

    text_color = AliasProperty(
        _get_text_color, bind=('background_palette', 'theme_style')
    )

    def _get_opposite_text_color(self, theme_style: str = None):
        if theme_style is None:
            theme_style = self.theme_style

        return self._get_text_color(theme_style, True)

    opposite_text_color = AliasProperty(
        _get_opposite_text_color, bind=('background_palette', 'theme_style')
    )

    def _get_secondary_text_color(self, theme_style: str = None, opposite: bool = False):
        if theme_style is None:
            theme_style = self.theme_style

        if opposite:
            theme_style = self._get_opposite_theme_style(theme_style)

        if theme_style == 'Light':
            return get_color_from_hex(
                self.colors[self.background_palette]['700']
            )
        elif theme_style == 'Dark':
            return get_color_from_hex(
                self.colors[self.background_palette]['300']
            )

    secondary_text_color = AliasProperty(
        _get_secondary_text_color, bind=('background_palette', 'theme_style')
    )

    def _get_opposite_secondary_text_color(self, theme_style: str = None):
        if theme_style is None:
            theme_style = self.theme_style

        return self._get_secondary_text_color(theme_style, True)

    opposite_secondary_text_color = AliasProperty(
        _get_opposite_secondary_text_color, bind=('background_palette', 'theme_style')
    )

    def _get_disabled_color(self, theme_style: str = None):
        if theme_style is None:
            theme_style = self.theme_style

        if theme_style == 'Light':
            return get_color_from_hex(
                self.colors[self.background_palette]['500']
            )
        elif theme_style == 'Dark':
            return get_color_from_hex(
                self.colors[self.background_palette]['500']
            )

    disabled_color = AliasProperty(
        _get_disabled_color, bind=('background_palette', 'theme_style')
    )

    def _get_divider_color(self, theme_style: str = None, opposite: bool = False):
        if theme_style is None:
            theme_style = self.theme_style

        if opposite:
            theme_style = self._get_opposite_theme_style(theme_style)

        if theme_style == 'Light':
            return get_color_from_hex(
                self.colors[self.background_palette]['600']
            )
        elif theme_style == 'Dark':
            return get_color_from_hex(
                self.colors[self.background_palette]['400']
            )

    divider_color = AliasProperty(
        _get_divider_color, bind=('background_palette', 'theme_style')
    )

    def _get_opposite_divider_color(self, theme_style: str = None):
        if theme_style is None:
            theme_style = self.theme_style

        return self._get_divider_color(theme_style, True)

    opposite_divider_color = AliasProperty(
        _get_opposite_divider_color, bind=('background_palette', 'theme_style')
    )

    def _get_error_color(self, theme_style: str = None):
        if theme_style is None:
            theme_style = self.theme_style

        if theme_style == 'Light':
            return get_color_from_hex(
                self.colors['Red']['600']
            )
        elif theme_style == 'Dark':
            return get_color_from_hex(
                self.colors['Red']['400']
            )

    error_color = AliasProperty(
        _get_error_color, bind=('theme_style', )
    )

    def _get_success_color(self, theme_style: str = None):
        if theme_style is None:
            theme_style = self.theme_style

        if theme_style == 'Light':
            return get_color_from_hex(
                self.colors['Green']['600']
            )
        elif theme_style == 'Dark':
            return get_color_from_hex(
                self.colors['Green']['400']
            )

    success_color = AliasProperty(
        _get_success_color, bind=('theme_style', )
    )

    def _get_warning_color(self, theme_style: str = None):
        if theme_style is None:
            theme_style = self.theme_style

        if theme_style == 'Light':
            return get_color_from_hex(
                self.colors['Amber']['600']
            )
        elif theme_style == 'Dark':
            return get_color_from_hex(
                self.colors['Amber']['400']
            )

    warning_color = AliasProperty(
        _get_warning_color, bind=('theme_style', )
    )

    font_styles = DictProperty(
        {
            'DisplayL': {
                'font_name': 'MontserratBold',
                'font_size': 34,
                'letter_spacing': 0.5,
                'line_height': 48,
                'bold': True,
                'italic': False,
            },
            'DisplayM': {
                'font_name': 'MontserratBold',
                'font_size': 30,
                'letter_spacing': 0.5,
                'line_height': 42,
                'bold': False,
                'italic': False,
            },
            'DisplayS': {
                'font_name': 'MontserratMedium',
                'font_size': 26,
                'letter_spacing': 0.5,
                'line_height': 36,
                'bold': True,
                'italic': False,
            },
            'HeadlineL': {
                'font_name': 'Montserrat',
                'font_size': 22,
                'letter_spacing': 0.5,
                'line_height': 32,
                'bold': True,
                'italic': False,
            },
            'HeadlineM': {
                'font_name': 'MontserratMedium',
                'font_size': 20,
                'letter_spacing': 0.5,
                'line_height': 28,
                'bold': True,
                'italic': False,
            },
            'HeadlineS': {
                'font_name': 'MontserratMedium',
                'font_size': 18,
                'letter_spacing': 0.5,
                'line_height': 26,
                'bold': False,
                'italic': False,
            },
            'TitleL': {
                'font_name': 'MontserratMedium',
                'font_size': 18,
                'letter_spacing': 0.5,
                'line_height': 24,
                'bold': True,
                'italic': False,
            },
            'TitleM': {
                'font_name': 'MontserratMedium',
                'font_size': 16,
                'letter_spacing': 0.5,
                'line_height': 22,
                'bold': False,
                'italic': False,
            },
            'TitleS': {
                'font_name': 'MontserratMedium',
                'font_size': 14,
                'letter_spacing': 0.5,
                'line_height': 18,
                'bold': False,
                'italic': False,
            },
            'BodyL': {
                'font_name': 'Montserrat',
                'font_size': 16,
                'letter_spacing': 0.5,
                'line_height': 22,
                'bold': False,
                'italic': False,
            },
            'BodyLBold': {
                'font_name': 'Montserrat',
                'font_size': 16,
                'letter_spacing': 0.5,
                'line_height': 22,
                'bold': True,
                'italic': False,
            },
            'BodyM': {
                'font_name': 'Montserrat',
                'font_size': 14,
                'letter_spacing': 0.5,
                'line_height': 18,
                'bold': False,
                'italic': False,
            },
            'BodyMBold': {
                'font_name': 'Montserrat',
                'font_size': 14,
                'letter_spacing': 0.5,
                'line_height': 18,
                'bold': True,
                'italic': False,
            },
            'BodyS': {
                'font_name': 'Montserrat',
                'font_size': 12,
                'letter_spacing': 0.5,
                'line_height': 16,
                'bold': False,
                'italic': False,
            },
            'BodySBold': {
                'font_name': 'Montserrat',
                'font_size': 12,
                'letter_spacing': 0.5,
                'line_height': 16,
                'bold': True,
                'italic': False,
            },
            'LabelL': {
                'font_name': 'MontserratMedium',
                'font_size': 14,
                'letter_spacing': 0.5,
                'line_height': 18,
                'bold': False,
                'italic': False,
            },
            'LabelLBold': {
                'font_name': 'Montserrat',
                'font_size': 14,
                'letter_spacing': 0.5,
                'line_height': 18,
                'bold': True,
                'italic': False,
            },
            'LabelM': {
                'font_name': 'MontserratMedium',
                'font_size': 12,
                'letter_spacing': 0.5,
                'line_height': 16,
                'bold': False,
                'italic': False,
            },
            'LabelMBold': {
                'font_name': 'Montserrat',
                'font_size': 12,
                'letter_spacing': 0.5,
                'line_height': 16,
                'bold': True,
                'italic': False,
            },
            'LabelS': {
                'font_name': 'MontserratMedium',
                'font_size': 11,
                'letter_spacing': 0.5,
                'line_height': 15,
                'bold': False,
                'italic': False,
            },
            'LabelSBold': {
                'font_name': 'Montserrat',
                'font_size': 11,
                'letter_spacing': 0.5,
                'line_height': 15,
                'bold': True,
                'italic': False,
            },
            'Icon': {
                'font_name': 'Icons',
                'font_size': 24,
                'letter_spacing': 0,
                'line_height': 1,
                'bold': False,
                'italic': False,
            }
        }
    )

    app_bg_color = ColorProperty(None, allownone=True)
    _app_bg_color = ColorProperty((0, 0, 0, 0))

    def __init__(self, **kwargs):
        self.bind(app_bg_color=self.setter('_app_bg_color'))
        self.colors = colors

        super().__init__(**kwargs)

        self._app_bg_color = self.background_color

    def on_theme_style(self, theme_manager: Self, theme_style: str) -> None:
        if (
            hasattr(App.get_running_app(), 'theme_cls')
            and App.get_running_app().theme_cls == self
        ):
            if self.app_bg_color is None:
                if self.theme_style_switch_animation:
                    Animation(
                        _app_bg_color=self.background_color,
                        d=self.theme_style_switch_animation_duration,
                        t='linear',
                    ).start(self)
                else:
                    self._app_bg_color = self.background_color

    def on__app_bg_color(self, app, app_bg_color):
        Window.clearcolor = app_bg_color

    def lighten_color(self, color, factor=0.3):
        r, g, b, a = 0, 0, 0, 0
        if isinstance(color, str):
            r, g, b, a = get_color_from_hex(color)
        else:
            if len(color) == 3:
                r, g, b = color
            else:
                r, g, b, a = color

        r = min(1, r + r * factor)
        g = min(1, g + g * factor)
        b = min(1, b + b * factor)

        return float(r), float(g), float(b), a

    def darken_color(self, color, factor=0.3):
        r, g, b, a = 0, 0, 0, 0
        if isinstance(color, str):
            r, g, b, a = get_color_from_hex(color)
        else:
            if len(color) == 3:
                r, g, b = color
            else:
                r, g, b, a = color

        r = max(0, r - r * factor)
        g = max(0, g - g * factor)
        b = max(0, b - b * factor)

        return float(r), float(g), float(b), a

    def darken_or_lighten_color(self, color, factor=0.3):

        def normalized_channel(color):
            if color <= 0.03928:
                return color / 12.92
            else:
                return ((color + 0.055) / 1.055) ** 2.4

        r, g, b, a = 0, 0, 0, 0
        if isinstance(color, str):
            r, g, b, a = get_color_from_hex(color)
        else:
            if len(color) == 3:
                r, g, b = color
            else:
                r, g, b, a = color

        luminance = 0.2126 * normalized_channel(r) + 0.7152 * normalized_channel(g) + 0.0722 * normalized_channel(b)
        if luminance < .5:
            return self.lighten_color(color, factor)
        return self.darken_color(color, factor)
