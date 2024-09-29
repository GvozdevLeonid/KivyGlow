import os

import kivy
from kivy.logger import Logger

__version__ = '1.0.5'
"""KivyGlow version."""
kivy.require('2.3.0')

kivy_glow_base_dir = os.path.dirname(__file__)

kivy_glow_assets_dir = os.path.join(kivy_glow_base_dir, f'assets{os.sep}')
kivy_glow_uix_dir = os.path.join(kivy_glow_base_dir, 'uix')

kivy_glow_fonts_dir = os.path.join(kivy_glow_assets_dir, f'fonts{os.sep}')
kivy_glow_icons_dir = os.path.join(kivy_glow_assets_dir, f'icons{os.sep}')
kivy_glow_images_dir = os.path.join(kivy_glow_assets_dir, f'images{os.sep}')


_log_message = (
    f'KivyGlow: KivyGlow version: <{__version__}>'
    + f' (installed at "{kivy_glow_base_dir}")'
)
Logger.info(_log_message)

import kivy_glow.factory_registers  # noqa F401
import kivy_glow.fonts  # noqa F401
