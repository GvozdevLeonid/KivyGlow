__all__ = ('GlowCircleLayout', )


from math import (
    atan2,
    cos,
    degrees,
    radians,
    sin,
)

from kivy.properties import (
    BooleanProperty,
    NumericProperty,
)
from kivy.uix.widget import Widget

from kivy_glow.uix.floatlayout import GlowFloatLayout


class GlowCircleLayout(GlowFloatLayout):
    degree_spacing = NumericProperty(defaultvalue=30)
    circular_radius = NumericProperty(defaultvalue=None, allownone=True)
    start_from = NumericProperty(defaultvalue=0)

    max_degree = NumericProperty(defaultvalue=360)
    circular_padding = NumericProperty(defaultvalue='25dp')

    row_spacing = NumericProperty(defaultvalue='50dp')

    clockwise = BooleanProperty(defaultvalue=True)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
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

    def remove_widget(self, widget: Widget, **kwargs) -> None:
        super().remove_widget(widget, **kwargs)
        self._update_layout()

    def do_layout(self, *largs, **kwargs) -> None:
        self._update_layout()
        return super().do_layout(*largs, **kwargs)

    def _max_per_row(self) -> int:
        return int(self.max_degree / self.degree_spacing)

    def _update_layout(self, *args) -> None:
        for index, child in enumerate(reversed(self.children)):
            pos = self._point_on_circle(
                self._calculate_radius(index),
                self._calculate_degree(index),
            )
            child.center = pos

    def _calculate_radius(self, index: int) -> float | int:
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

    def _calculate_degree(self, index: int) -> float | int:
        '''Calculates the angle for given index.'''

        if self.clockwise:
            degree = self.start_from - index * self.degree_spacing
        else:
            degree = self.start_from + index * self.degree_spacing

        return degree

    def _point_on_circle(self, radius: float | int, degree: float | int) -> tuple[float | int, float | int]:
        angle = radians(degree)
        center = [self.pos[0] + self.width / 2, self.pos[1] + self.height / 2]
        x = center[0] + (radius * cos(angle))
        y = center[1] + (radius * sin(angle))
        return x, y
