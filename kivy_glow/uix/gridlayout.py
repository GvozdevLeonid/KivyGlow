__all__ = ('GlowGridLayout', )

from kivy.uix.gridlayout import GridLayout

from kivy_glow.uix.behaviors import (
    DeclarativeBehavior,
    AdaptiveBehavior,
    StyleBehavior,
    ThemeBehavior,
)


class GlowGridLayout(DeclarativeBehavior,
                     AdaptiveBehavior,
                     ThemeBehavior,
                     StyleBehavior,
                     GridLayout,
                     ):

    def do_layout(self, *largs):
        children = self.children
        if not children or not self._init_rows_cols_sizes(len(children)):
            l, t, r, b = self.padding
            self.minimum_size = l + r, t + b
            return
        self._fill_rows_cols_sizes()
        self._update_minimum_size()
        self._finalize_rows_cols_sizes()

        for i, x, y, w, h in self._iterate_layout(len(children)):
            c = children[i]

            shw, shh = c.size_hint
            shw_min, shh_min = c.size_hint_min
            shw_max, shh_max = c.size_hint_max

            if shw_min is not None:
                if shw_max is not None:
                    w = max(min(w, shw_max), shw_min)
                else:
                    w = max(w, shw_min)
            else:
                if shw_max is not None:
                    w = min(w, shw_max)

            if shh_min is not None:
                if shh_max is not None:
                    h = max(min(h, shh_max), shh_min)
                else:
                    h = max(h, shh_min)
            else:
                if shh_max is not None:
                    h = min(h, shh_max)

            if shw is None:
                if shh is not None:
                    c.height = h
            else:
                if shh is None:
                    c.width = w
                else:
                    c.size = (w, h)

            if c.height < h:
                for key, value in c.pos_hint.items():
                    posy = value * h
                    if key == 'y':
                        y += posy
                    elif key == 'top':
                        y += posy - c.height
                    elif key == 'center_y':
                        y += posy - (c.height / 2.)

            if c.width < w:
                for key, value in c.pos_hint.items():
                    posx = value * w
                    if key == 'x':
                        x += posx
                    elif key == 'right':
                        x += posx - c.width
                    elif key == 'center_x':
                        x += posx - (c.width / 2.)

            c.pos = (x, y)
