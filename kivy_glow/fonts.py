'''
List of default fonts.
'''
from kivy_glow import kivy_glow_fonts_dir
from kivy.core.text import LabelBase
import os


fonts = [
    {
        'name': 'Montserrat',
        'fn_regular': kivy_glow_fonts_dir + 'Montserrat-Regular.ttf',
        'fn_italic': kivy_glow_fonts_dir + 'Montserrat-Italic.ttf',

        'fn_bold': kivy_glow_fonts_dir + 'Montserrat-Bold.ttf',
        'fn_bolditalic': kivy_glow_fonts_dir + 'Montserrat-BoldItalic.ttf',
    },
    {
        'name': 'MontserratThin',
        'fn_regular': kivy_glow_fonts_dir + 'Montserrat-Thin.ttf',
        'fn_italic': kivy_glow_fonts_dir + 'Montserrat-ThinItalic.ttf',
    },
    {
        'name': 'MontserratLight',
        'fn_regular': kivy_glow_fonts_dir + 'Montserrat-ExtraLight.ttf',
        'fn_italic': kivy_glow_fonts_dir + 'Montserrat-ExtraLightItalic.ttf',

        'fn_bold': kivy_glow_fonts_dir + 'Montserrat-Light.ttf',
        'fn_bolditalic': kivy_glow_fonts_dir + 'Montserrat-LightItalic.ttf',
    },
    {
        'name': 'MontserratMedium',
        'fn_regular': kivy_glow_fonts_dir + 'Montserrat-Medium.ttf',
        'fn_italic': kivy_glow_fonts_dir + 'Montserrat-MediumItalic.ttf',

        'fn_bold': kivy_glow_fonts_dir + 'Montserrat-SemiBold.ttf',
        'fn_bolditalic': kivy_glow_fonts_dir + 'Montserrat-SemiBoldItalic.ttf',
    },
    {
        'name': 'MontserratBold',
        'fn_regular': kivy_glow_fonts_dir + 'Montserrat-ExtraBold.ttf',
        'fn_italic': kivy_glow_fonts_dir + 'Montserrat-ExtraBoldItalic.ttf',

        'fn_bold': kivy_glow_fonts_dir + 'Montserrat-Black.ttf',
        'fn_bolditalic': kivy_glow_fonts_dir + 'Montserrat-BlackItalic.ttf',
    },
    {
        'name': 'Icons',
        'fn_regular': kivy_glow_fonts_dir + 'materialdesignicons.ttf',
    },
    {
        'name': 'MaterialIcons_outlined_100',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Outlined' + os.sep + 'MaterialIconsOutlined-Thin.ttf',
    },
    {
        'name': 'MaterialIcons_outlined_200',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Outlined' + os.sep + 'MaterialIconsOutlined-ExtraLight.ttf',
    },
    {
        'name': 'MaterialIcons_outlined_300',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Outlined' + os.sep + 'MaterialIconsOutlined-Light.ttf',
    },
    {
        'name': 'MaterialIcons_outlined_400',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Outlined' + os.sep + 'MaterialIconsOutlined-Regular.ttf',
    },
    {
        'name': 'MaterialIcons_outlined_500',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Outlined' + os.sep + 'MaterialIconsOutlined-Medium.ttf',
    },
    {
        'name': 'MaterialIcons_outlined_600',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Outlined' + os.sep + 'MaterialIconsOutlined-SemiBold.ttf',
    },
    {
        'name': 'MaterialIcons_outlined_700',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Outlined' + os.sep + 'MaterialIconsOutlined-Bold.ttf',
    },
    {
        'name': 'MaterialIcons_outlined_100_filled',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Outlined' + os.sep + 'MaterialIconsOutlined_Filled-Thin.ttf',
    },
    {
        'name': 'MaterialIcons_outlined_200_filled',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Outlined' + os.sep + 'MaterialIconsOutlined_Filled-ExtraLight.ttf',
    },
    {
        'name': 'MaterialIcons_outlined_300_filled',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Outlined' + os.sep + 'MaterialIconsOutlined_Filled-Light.ttf',
    },
    {
        'name': 'MaterialIcons_outlined_400_filled',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Outlined' + os.sep + 'MaterialIconsOutlined_Filled-Regular.ttf',
    },
    {
        'name': 'MaterialIcons_outlined_500_filled',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Outlined' + os.sep + 'MaterialIconsOutlined_Filled-Medium.ttf',
    },
    {
        'name': 'MaterialIcons_outlined_600_filled',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Outlined' + os.sep + 'MaterialIconsOutlined_Filled-SemiBold.ttf',
    },
    {
        'name': 'MaterialIcons_outlined_700_filled',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Outlined' + os.sep + 'MaterialIconsOutlined_Filled-Bold.ttf',
    },
    {
        'name': 'MaterialIcons_rounded_100',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Rounded' + os.sep + 'MaterialIconsRounded-Thin.ttf',
    },
    {
        'name': 'MaterialIcons_rounded_200',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Rounded' + os.sep + 'MaterialIconsRounded-ExtraLight.ttf',
    },
    {
        'name': 'MaterialIcons_rounded_300',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Rounded' + os.sep + 'MaterialIconsRounded-Light.ttf',
    },
    {
        'name': 'MaterialIcons_rounded_400',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Rounded' + os.sep + 'MaterialIconsRounded-Regular.ttf',
    },
    {
        'name': 'MaterialIcons_rounded_500',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Rounded' + os.sep + 'MaterialIconsRounded-Medium.ttf',
    },
    {
        'name': 'MaterialIcons_rounded_600',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Rounded' + os.sep + 'MaterialIconsRounded-SemiBold.ttf',
    },
    {
        'name': 'MaterialIcons_rounded_700',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Rounded' + os.sep + 'MaterialIconsRounded-Bold.ttf',
    },
    {
        'name': 'MaterialIcons_rounded_100_filled',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Rounded' + os.sep + 'MaterialIconsRounded_Filled-Thin.ttf',
    },
    {
        'name': 'MaterialIcons_rounded_200_filled',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Rounded' + os.sep + 'MaterialIconsRounded_Filled-ExtraLight.ttf',
    },
    {
        'name': 'MaterialIcons_rounded_300_filled',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Rounded' + os.sep + 'MaterialIconsRounded_Filled-Light.ttf',
    },
    {
        'name': 'MaterialIcons_rounded_400_filled',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Rounded' + os.sep + 'MaterialIconsRounded_Filled-Regular.ttf',
    },
    {
        'name': 'MaterialIcons_rounded_500_filled',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Rounded' + os.sep + 'MaterialIconsRounded_Filled-Medium.ttf',
    },
    {
        'name': 'MaterialIcons_rounded_600_filled',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Rounded' + os.sep + 'MaterialIconsRounded_Filled-SemiBold.ttf',
    },
    {
        'name': 'MaterialIcons_rounded_700_filled',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Rounded' + os.sep + 'MaterialIconsRounded_Filled-Bold.ttf',
    },
    {
        'name': 'MaterialIcons_sharp_100',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Sharp' + os.sep + 'MaterialIconsSharp-Thin.ttf',
    },
    {
        'name': 'MaterialIcons_sharp_200',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Sharp' + os.sep + 'MaterialIconsSharp-ExtraLight.ttf',
    },
    {
        'name': 'MaterialIcons_sharp_300',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Sharp' + os.sep + 'MaterialIconsSharp-Light.ttf',
    },
    {
        'name': 'MaterialIcons_sharp_400',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Sharp' + os.sep + 'MaterialIconsSharp-Regular.ttf',
    },
    {
        'name': 'MaterialIcons_sharp_500',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Sharp' + os.sep + 'MaterialIconsSharp-Medium.ttf',
    },
    {
        'name': 'MaterialIcons_sharp_600',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Sharp' + os.sep + 'MaterialIconsSharp-SemiBold.ttf',
    },
    {
        'name': 'MaterialIcons_sharp_700',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Sharp' + os.sep + 'MaterialIconsSharp-Bold.ttf',
    },
    {
        'name': 'MaterialIcons_sharp_100_filled',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Sharp' + os.sep + 'MaterialIconsSharp_Filled-Thin.ttf',
    },
    {
        'name': 'MaterialIcons_sharp_200_filled',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Sharp' + os.sep + 'MaterialIconsSharp_Filled-ExtraLight.ttf',
    },
    {
        'name': 'MaterialIcons_sharp_300_filled',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Sharp' + os.sep + 'MaterialIconsSharp_Filled-Light.ttf',
    },
    {
        'name': 'MaterialIcons_sharp_400_filled',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Sharp' + os.sep + 'MaterialIconsSharp_Filled-Regular.ttf',
    },
    {
        'name': 'MaterialIcons_sharp_500_filled',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Sharp' + os.sep + 'MaterialIconsSharp_Filled-Medium.ttf',
    },
    {
        'name': 'MaterialIcons_sharp_600_filled',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Sharp' + os.sep + 'MaterialIconsSharp_Filled-SemiBold.ttf',
    },
    {
        'name': 'MaterialIcons_sharp_700_filled',
        'fn_regular': kivy_glow_fonts_dir + 'MaterialIcons' + os.sep + 'Sharp' + os.sep + 'MaterialIconsSharp_Filled-Bold.ttf',
    },
]

for font in fonts:
    LabelBase.register(**font)
