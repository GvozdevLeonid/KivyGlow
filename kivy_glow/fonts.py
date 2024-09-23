'''
List of default fonts.
'''
from kivy_glow import kivy_glow_fonts_dir
from kivy.core.text import LabelBase


fonts = [
    {
        'name': 'Montserrat',
        'fn_regular': kivy_glow_fonts_dir + 'Montserrat-Regular.ttf',
        'fn_bold': kivy_glow_fonts_dir + 'Montserrat-Bold.ttf',
        'fn_italic': kivy_glow_fonts_dir + 'Montserrat-Italic.ttf',
        'fn_bolditalic': kivy_glow_fonts_dir + 'Montserrat-BoldItalic.ttf',
    },
    {
        'name': 'MontserratThin',
        'fn_regular': kivy_glow_fonts_dir + 'Montserrat-Thin.ttf',
        'fn_italic': kivy_glow_fonts_dir + 'Montserrat-ThinItalic.ttf',
    },
    {
        'name': 'MontserratExtraLight',
        'fn_regular': kivy_glow_fonts_dir + 'Montserrat-ExtraLight.ttf',
        'fn_italic': kivy_glow_fonts_dir + 'Montserrat-ExtraLightItalic.ttf',
    },
    {
        'name': 'MontserratLight',
        'fn_regular': kivy_glow_fonts_dir + 'Montserrat-Light.ttf',
        'fn_italic': kivy_glow_fonts_dir + 'Montserrat-LightItalic.ttf',
    },
    {
        'name': 'MontserratMedium',
        'fn_regular': kivy_glow_fonts_dir + 'Montserrat-Medium.ttf',
        'fn_italic': kivy_glow_fonts_dir + 'Montserrat-MediumItalic.ttf',
    },
    {
        'name': 'MontserratSemiBold',
        'fn_regular': kivy_glow_fonts_dir + 'Montserrat-SemiBold.ttf',
        'fn_italic': kivy_glow_fonts_dir + 'Montserrat-SemiBoldItalic.ttf',
    },
    {
        'name': 'MontserratExtraBold',
        'fn_regular': kivy_glow_fonts_dir + 'Montserrat-ExtraBold.ttf',
        'fn_italic': kivy_glow_fonts_dir + 'Montserrat-ExtraBoldItalic.ttf',
    },
    {
        'name': 'MontserratBlack',
        'fn_regular': kivy_glow_fonts_dir + 'Montserrat-Black.ttf',
        'fn_italic': kivy_glow_fonts_dir + 'Montserrat-BlackItalic.ttf',
    },
    {
        'name': 'Icons',
        'fn_regular': kivy_glow_fonts_dir + 'materialdesignicons-webfont.ttf',
    },
]

for font in fonts:
    LabelBase.register(**font)
