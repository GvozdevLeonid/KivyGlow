__all__ = ('GlowTableLayout', )

from kivy.uix.layout import Layout
from kivy_glow.uix.behaviors import (
    DeclarativeBehavior,
    AdaptiveBehavior,
    StyleBehavior,
    ThemeBehavior,
)
from kivy.properties import (
    ReferenceListProperty,
    VariableListProperty,
    BooleanProperty,
    NumericProperty,
)


def nmax(*args):
    # merge into one list
    args = [x for x in args if x is not None]
    return max(args)


def nmin(*args):
    # merge into one list
    args = [x for x in args if x is not None]
    return min(args)


class GlowTableLayout(DeclarativeBehavior,
                      AdaptiveBehavior,
                      ThemeBehavior,
                      StyleBehavior,
                      Layout):

    col_default_width = NumericProperty(0)
    row_default_height = NumericProperty(0)

    col_force_default = BooleanProperty(False)
    row_force_default = BooleanProperty(False)

    minimum_width = NumericProperty(0)
    minimum_height = NumericProperty(0)
    minimum_size = ReferenceListProperty(minimum_width, minimum_height)

    spacing = VariableListProperty([0, 0], length=2)
    padding = VariableListProperty([0, 0, 0, 0], length=4)

    def __init__(self, *args, **kwargs):
        self._rows = 1
        self._cols = 1

        super().__init__(*args, **kwargs)
        fbind = self.fbind
        update = self._trigger_layout
        fbind('col_default_width', update)
        fbind('row_default_height', update)
        fbind('col_force_default', update)
        fbind('row_force_default', update)
        fbind('parent', update)
        fbind('spacing', update)
        fbind('padding', update)
        fbind('children', update)
        fbind('size', update)
        fbind('pos', update)
        fbind('pos_hint', update)

    def add_widget(self, widget, row: int = None, col: int = None, rowspan: int = None, colspan: int = None, index: int = 0):
        if not hasattr(widget, 'rowspan') or rowspan is not None:
            widget.rowspan = rowspan if rowspan is not None else 1

        if not hasattr(widget, 'colspan') or colspan is not None:
            widget.colspan = colspan if colspan is not None else 1

        if not hasattr(widget, 'row') or row is not None:
            widget.row = row if row is not None else 0

        if not hasattr(widget, 'col') or col is not None:
            widget.col = col if col is not None else 0

        return super().add_widget(widget, index=index)

    def _calculate_grid_size(self):
        self._rows = 1
        self._cols = 1
        for child in self.children:
            self._rows = max(self._rows, child.row + child.rowspan)
            self._cols = max(self._cols, child.col + child.colspan)

    def _init_rows_cols_sizes(self):
        current_cols = self._cols
        current_rows = self._rows

        self._has_hint_bound_x = False
        self._has_hint_bound_y = False
        self._cols_min_size_none = 0.  # min size from all the None hint
        self._rows_min_size_none = 0.  # min size from all the None hint
        self._cols_w = [self.col_default_width] * current_cols
        self._cols_sh = [None] * current_cols
        self._cols_sh_min = [None] * current_cols
        self._cols_sh_max = [None] * current_cols
        self._rows_h = [self.row_default_height] * current_rows
        self._rows_sh = [None] * current_rows
        self._rows_sh_min = [None] * current_rows
        self._rows_sh_max = [None] * current_rows

    def _fill_rows_cols_sizes(self):
        cols_w, rows_h = self._cols_w, self._rows_h
        cols_sh, rows_sh = self._cols_sh, self._rows_sh
        cols_sh_min, rows_sh_min = self._cols_sh_min, self._rows_sh_min
        cols_sh_max, rows_sh_max = self._cols_sh_max, self._rows_sh_max

        # calculate minimum size for each columns and rows
        has_bound_y = has_bound_x = False
        for child in reversed(self.children):
            (shw, shh), (w, h) = child.size_hint, child.size
            shw_min, shh_min = child.size_hint_min
            shw_max, shh_max = child.size_hint_max

            # compute minimum size / maximum stretch needed
            for col_iteration in range(child.colspan):
                if shw is None:
                    cols_w[child.col + col_iteration] = nmax(cols_w[child.col + col_iteration], w / child.colspan)
                else:
                    cols_sh[child.col + col_iteration] = nmax(cols_sh[child.col + col_iteration], shw)
                    if shw_min is not None:
                        has_bound_x = True
                        cols_sh_min[child.col + col_iteration] = nmax(cols_sh_min[child.col + col_iteration], shw_min / child.colspan)
                    if shw_max is not None:
                        has_bound_x = True
                        cols_sh_max[child.col + col_iteration] = nmin(cols_sh_max[child.col + col_iteration], shw_max / child.colspan)

            for row_iteration in range(child.rowspan):
                if shh is None:
                    rows_h[child.row + row_iteration] = nmax(rows_h[child.row + row_iteration], h / child.rowspan)
                else:
                    rows_sh[child.row + row_iteration] = nmax(rows_sh[child.row + row_iteration], shh)
                    if shh_min is not None:
                        has_bound_y = True
                        rows_sh_min[child.row + row_iteration] = nmax(rows_sh_min[child.row + row_iteration], shh_min / child.rowspan)
                    if shh_max is not None:
                        has_bound_y = True
                        rows_sh_max[child.row + row_iteration] = nmin(rows_sh_max[child.row + row_iteration], shh_max / child.rowspan)

        self._has_hint_bound_x = has_bound_x
        self._has_hint_bound_y = has_bound_y

    def _update_minimum_size(self):
        # calculate minimum width/height needed, starting from padding +
        # spacing
        l, t, r, b = self.padding
        spacing_x, spacing_y = self.spacing
        cols_w, rows_h = self._cols_w, self._rows_h

        width = l + r + spacing_x * (len(cols_w) - 1)
        self._cols_min_size_none = sum(cols_w) + width
        # we need to subtract for the sh_max/min the already guaranteed size
        # due to having a None in the col. So sh_min gets smaller by that size
        # since it's already covered. Similarly for sh_max, because if we
        # already exceeded the max, the subtracted max will be zero, so
        # it won't get larger
        if self._has_hint_bound_x:
            cols_sh_min = self._cols_sh_min
            cols_sh_max = self._cols_sh_max

            for i, (cw, sh_min, sh_max) in enumerate(
                    zip(cols_w, cols_sh_min, cols_sh_max)):
                if sh_min is not None:
                    width += max(cw, sh_min)
                    cols_sh_min[i] = max(0., sh_min - cw)
                else:
                    width += cw

                if sh_max is not None:
                    cols_sh_max[i] = max(0., sh_max - cw)
        else:
            width = self._cols_min_size_none

        height = t + b + spacing_y * (len(rows_h) - 1)
        self._rows_min_size_none = sum(rows_h) + height
        if self._has_hint_bound_y:
            rows_sh_min = self._rows_sh_min
            rows_sh_max = self._rows_sh_max

            for i, (rh, sh_min, sh_max) in enumerate(
                    zip(rows_h, rows_sh_min, rows_sh_max)):
                if sh_min is not None:
                    height += max(r, sh_min)
                    rows_sh_min[i] = max(0., sh_min - rh)
                else:
                    height += rh

                if sh_max is not None:
                    rows_sh_max[i] = max(0., sh_max - rh)
        else:
            height = self._rows_min_size_none

        # finally, set the minimum size
        self.minimum_size = (width, height)

    def _finalize_rows_cols_sizes(self):
        selfw = self.width
        selfh = self.height

        # resolve size for each column
        if self.col_force_default:
            cols_w = [self.col_default_width] * len(self._cols_w)
            for col in range(self._cols):
                cols_w[col] = self.col_default_width
            self._cols_w = cols_w
        else:
            cols_w = self._cols_w
            cols_sh = self._cols_sh
            cols_sh_min = self._cols_sh_min
            cols_weight = float(sum((x for x in cols_sh if x is not None)))
            stretch_w = max(0., selfw - self._cols_min_size_none)

            if stretch_w > 1e-9:
                if self._has_hint_bound_x:
                    # fix the hints to be within bounds
                    self.layout_hint_with_bounds(
                        cols_weight, stretch_w,
                        sum((c for c in cols_sh_min if c is not None)),
                        cols_sh_min, self._cols_sh_max, cols_sh)

                for index, col_stretch in enumerate(cols_sh):
                    # if the col don't have stretch information, nothing to do
                    if not col_stretch:
                        continue
                    # add to the min width whatever remains from size_hint
                    cols_w[index] += stretch_w * col_stretch / cols_weight

        # same algo for rows
        if self.row_force_default:
            rows_h = [self.row_default_height] * len(self._rows_h)
            for col in range(self._cols):
                rows_h[index] = self.row_default_height
            self._rows_h = rows_h
        else:
            rows_h = self._rows_h
            rows_sh = self._rows_sh
            rows_sh_min = self._rows_sh_min
            rows_weight = float(sum((x for x in rows_sh if x is not None)))
            stretch_h = max(0., selfh - self._rows_min_size_none)

            if stretch_h > 1e-9:
                if self._has_hint_bound_y:
                    # fix the hints to be within bounds
                    self.layout_hint_with_bounds(
                        rows_weight, stretch_h,
                        sum((r for r in rows_sh_min if r is not None)),
                        rows_sh_min, self._rows_sh_max, rows_sh)

                for index, row_stretch in enumerate(rows_sh):
                    # if the row don't have stretch information, nothing to do
                    if not row_stretch:
                        continue
                    # add to the min height whatever remains from size_hint
                    rows_h[index] += stretch_h * row_stretch / rows_weight

    def _get_row_col_attrs(self, row, col, rowspan, colspan):
        spacing_x, spacing_y = self.spacing

        x, y = self.x + self.padding[0], self.top - self.padding[3]
        w, h = 0, 0

        x += sum(self._cols_w[:col])
        x += spacing_x * col

        y -= sum(self._rows_h[:row + rowspan])
        y -= spacing_y * (row + rowspan - 1)

        w += sum(self._cols_w[col: col + colspan])
        w += spacing_x * (colspan - 1)

        h += sum(self._rows_h[row: row + rowspan])
        h += spacing_y * (rowspan - 1)

        return x, y, w, h

    def do_layout(self, *args):
        children = self.children
        if not children:
            l, t, r, b = self.padding
            self.minimum_size = l + r, t + b
            return

        self._calculate_grid_size()
        self._init_rows_cols_sizes()
        self._fill_rows_cols_sizes()
        self._update_minimum_size()
        self._finalize_rows_cols_sizes()

        for child in reversed(self.children):
            x, y, w, h = self._get_row_col_attrs(child.row, child.col, child.rowspan, child.colspan)
            shw, shh = child.size_hint
            shw_min, shh_min = child.size_hint_min
            shw_max, shh_max = child.size_hint_max

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
                    child.height = h
            else:
                if shh is None:
                    child.width = w
                else:
                    child.size = (w, h)

            if child.height < h:
                for key, value in child.pos_hint.items():
                    posy = value * h
                    if key == 'y':
                        y += posy
                    elif key == 'top':
                        y += posy - child.height
                    elif key == 'center_y':
                        y += posy - (child.height / 2.)

            if child.width < w:
                for key, value in child.pos_hint.items():
                    posx = value * w
                    if key == 'x':
                        x += posx
                    elif key == 'right':
                        x += posx - child.width
                    elif key == 'center_x':
                        x += posx - (child.width / 2.)

            child.pos = (x, y)
