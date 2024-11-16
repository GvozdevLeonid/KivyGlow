__all__ = ('GradientSourceBehavior', )

from kivy.graphics.texture import Texture
from kivy.properties import (
    AliasProperty,
    DictProperty,
    ListProperty,
    NumericProperty,
    OptionProperty,
    VariableListProperty,
)

from kivy_glow.utils.gradient import (
    LinearGradient,
    RadialGradient,
)


class GradientSourceBehavior:
    '''
    Gradient source behavior class.

    Allow you to get a linear and radial gradient texture
    '''

    gradient_type = OptionProperty(defaultvalue='linear', options=['linear', 'radial'])
    '''Gradient type (radial or linear)

    :attr:`gradient_type` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `linear`.
    '''

    colors = ListProperty(defaultvalue=[])
    '''Colors used in the gradient (can be a hex string, or a list or tuple (r, g, b)

    :attr:`colors` is an :class:`~kivy.properties.ListProperty`
    and defaults to `empty`.
    '''
    stops = DictProperty(defaultvalue={})
    '''Stops for each color.

    All stops must be within the range 0-1.
    You must specify the color index: its ending length.
    Each next color will start from the stop of the previous color.

    :attr:`stops` is an :class:`~kivy.properties.DictProperty`
    and defaults to `empty`.
    '''

    linear_gradient_angle = NumericProperty(defaultvalue=0)
    '''Angle for linear gradient direction 0 - left to right. 90 - botton to top

    :attr:`linear_gradient_angle` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `0`.
    '''

    radial_gradient_center = VariableListProperty(defaultvalue=[.5], length=2)
    '''Center coords in range(0-1)

    :attr:`radial_gradient_center` is an :class:`~kivy.properties.VariableListProperty`
    and defaults to `(.5, .5)`.
    '''

    crop_factor = NumericProperty(defaultvalue=8)
    '''How much to reduce the texture size relative to the widget size.
    The smaller the size, the faster the rendering works, but the worse the gradient quality.

    :attr:`crop_factor` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `8`.
    '''

    def __init__(self, *args, **kwargs) -> None:
        self._texture = None
        super().__init__(*args, **kwargs)

    def _get_texture(self) -> Texture:
        self._set_texture()
        return self._texture

    def _set_texture(self) -> None:
        if self.gradient_type == 'linear':
            self._texture = LinearGradient(self.colors, self.linear_gradient_angle, self.stops, self.size, self.crop_factor)
        elif self.gradient_type == 'radial':
            self._texture = RadialGradient(self.colors, self.radial_gradient_center, self.stops, self.size, self.crop_factor)

    gradient_texture = AliasProperty(_get_texture, _set_texture, bind=('gradient_type', 'colors', 'stops', 'linear_gradient_angle', 'radial_gradient_center', 'crop_factor', 'size'))
