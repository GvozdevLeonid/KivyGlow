__all__ = ('GlowApp', )

from kivy_glow.config_parser import ExtendedKivyConfigParser as ConfigParser
from kivy_glow.uix.behaviors import ThemeBehavior
from kivy_glow.theme import ThemeManager
from kivy.utils import platform
from kivy.logger import Logger
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.app import App
import os
from kivy.properties import (
    StringProperty,
    ObjectProperty,
)


class GlowApp(App, ThemeBehavior):

    icon = StringProperty(os.path.dirname(__file__) + f'/assets/images/logo/kivy_glow-icon-{512 if platform == "macosx" else (64 if platform == "win" else 32)}.png')
    config = ConfigParser(name='app')
    theme_cls = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.theme_cls = ThemeManager()

    def load_all_kv_files(self, path_to_directory: str) -> None:
        '''Recursively loads KV files from the selected directory.'''

        for path_to_dir, dirs, files in os.walk(path_to_directory):
            # When using the `load_all_kv_files` method, all KV files
            # from the `KivyGlow` library were loaded twice, which leads to
            # failures when using application built using `PyInstaller`.
            if 'kivy_glow' in path_to_directory:
                Logger.critical(
                    'KivyGlow'
                    'Do not use the word "kivy_glow" in the name of the directory '
                    'from where you download KV files'
                )
            if (
                'venv' in path_to_dir
                or '.buildozer' in path_to_dir
                or os.path.join('kivy_glow') in path_to_dir
            ):
                continue
            for name_file in files:
                if (
                    os.path.splitext(name_file)[1] == '.kv'
                    and name_file != 'style.kv'  # if use PyInstaller
                    and '__MACOS' not in path_to_dir  # if use Mac OS
                ):
                    path_to_kv_file = os.path.join(path_to_dir, name_file)
                    Builder.load_file(path_to_kv_file)

    def fps_monitor_start(self, anchor: str = 'top') -> None:
        '''Add a monitor to the main application window.'''

        from kivy.core.window import Window
        from kivy_glow.uix.label import GlowLabel

        def start(fps_monitor):
            Clock.schedule_interval(lambda _: update_fps(fps_monitor), .5)

        def update_fps(fps_monitor):
            fps_monitor.text = f'FPS: {Clock.get_fps():.2f}'

        fps_monitor = GlowLabel(pos_hint={anchor: 1}, bg_color=self.theme_cls.primary_dark_color, halign='center', adaptive_height=True, font_style='LabelS')
        Window.add_widget(fps_monitor)
        start(fps_monitor)
