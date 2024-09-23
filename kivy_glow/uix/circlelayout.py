__all__ = ('GlowCircleLayout', )


from kivy_glow.uix.floatlayout import GlowFloatLayout
from kivy.properties import (
    BooleanProperty,
    NumericProperty,
)
from math import (
    degrees,
    radians,
    atan2,
    cos,
    sin,
)


class GlowCircleLayout(GlowFloatLayout):
    degree_spacing = NumericProperty(30)
    circular_radius = NumericProperty(None, allownone=True)
    start_from = NumericProperty(0)

    max_degree = NumericProperty(360)
    circular_padding = NumericProperty('25dp')

    row_spacing = NumericProperty('50dp')

    clockwise = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(
            row_spacing=self._update_layout,
        )

    def get_angle(self, pos: tuple) -> float:
        '''Returns the angle of given pos.'''

        center = [self.pos[0] + self.width / 2, self.pos[1] + self.height / 2]
        (dx, dy) = (center[0] - pos[0], center[1] - pos[1])
        angle = degrees(atan2(float(dy), float(dx)))
        angle += 180
        return angle

    def remove_widget(self, widget, **kwargs):
        super().remove_widget(widget, **kwargs)
        self._update_layout()

    def do_layout(self, *largs, **kwargs):
        self._update_layout()
        return super().do_layout(*largs, **kwargs)

    def _max_per_row(self):
        return int(self.max_degree / self.degree_spacing)

    def _update_layout(self, *args):
        for index, child in enumerate(reversed(self.children)):
            pos = self._point_on_circle(
                self._calculate_radius(index),
                self._calculate_degree(index),
            )
            child.center = pos

    def _calculate_radius(self, index):
        '''Calculates the radius for given index.'''

        idx = int(index / self._max_per_row())

        if not self.circular_radius:
            init_radius = (
                min([self.width / 2, self.height / 2]) - self.circular_padding
            )
        else:
            init_radius = self.circular_radius

        if idx != 0:
            space = self.row_spacing * idx
            init_radius -= space

        return init_radius

    def _calculate_degree(self, index):
        '''Calculates the angle for given index.'''

        if self.clockwise:
            degree = self.start_from - index * self.degree_spacing
        else:
            degree = self.start_from + index * self.degree_spacing

        return degree

    def _point_on_circle(self, radius, degree):
        angle = radians(degree)
        center = [self.pos[0] + self.width / 2, self.pos[1] + self.height / 2]
        x = center[0] + (radius * cos(angle))
        y = center[1] + (radius * sin(angle))
        return [x, y]
