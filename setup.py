from setuptools import find_packages, setup
from kivy_glow import __version__
from pathlib import Path
import sys
import os

assert sys.version_info >= (3, 7, 0), 'KivyGlow requires Python 3.7+'


def glob_paths(pattern):
    out_files = []
    src_path = os.path.join(os.path.dirname(__file__), 'kivy_glow')

    for root, dirs, files in os.walk(src_path):
        for file in files:
            if file.endswith(pattern):
                filepath = os.path.join(str(Path(*Path(root).parts[1:])), file)

                try:
                    out_files.append(filepath.split(f'kivy_glow{os.sep}')[1])
                except IndexError:
                    out_files.append(filepath)

    return out_files


if __name__ == '__main__':
    setup(
        version=__version__,
        packages=find_packages(
            include=['kivy_glow', 'kivy_glow.*'],
        ),
        package_dir={'kivy_glow': 'kivy_glow'},
        package_data={
            'kivy_glow': [
                'assets/images/*.png',
                'assets/images/logo/*.png',
                'assets/images/map/*.png',
                'assets/fonts/*.ttf',
                'assets/fonts/MaterialIcons/Outlined/*.ttf',
                'assets/fonts/MaterialIcons/Rounded/*.ttf',
                'assets/fonts/MaterialIcons/Sharp/*.ttf',
                *glob_paths('.kv'),
                *glob_paths('.py'),
            ]
        },
    )
