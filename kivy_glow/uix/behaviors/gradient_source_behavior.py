__all__ = ('GradientSourceBehavior', )

from kivy_glow.utils.gradient import (
    LinearGradient,
    RadialGradient,
)
from kivy.properties import (
    VariableListProperty,
    NumericProperty,
    OptionProperty,
    AliasProperty,
    ListProperty,
    DictProperty,
)


class GradientSourceBehavior:
    gradient_type = OptionProperty('linear', options=['linear', 'radial'])
    colors = ListProperty([])
    stops = DictProperty({})
    linear_gradient_angle = NumericProperty(0.0)
    '''Angle for linear gradient direction 0 - left to right. 90 - botton to top'''
    radial_gradient_center = VariableListProperty([.5,], length=2)
    '''Center coords in range(0-1)'''

    crop_factor = NumericProperty(8)

    def __init__(self, *args, **kwargs):
        self._texture = None
        super().__init__(*args, **kwargs)

    def _get_texture(self):
        self._set_texture()
        return self._texture

    def _set_texture(self):
        if self.gradient_type == 'linear':
            self._texture = LinearGradient(self.colors, self.linear_gradient_angle, self.stops, self.size, self.crop_factor)
        elif self.gradient_type == 'radial':
            self._texture = RadialGradient(self.colors, self.radial_gradient_center, self.stops, self.size, self.crop_factor)

    gradient_texture = AliasProperty(_get_texture, _set_texture, bind=('gradient_type', 'colors', 'stops', 'linear_gradient_angle', 'radial_gradient_center', 'crop_factor', 'size'))
