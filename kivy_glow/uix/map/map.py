'''
GlowMap was written by Kivy Team and other contributors.
https://github.com/kivy-garden/mapview
'''


__all__ = ('GlowMap', 'GlowMapLayer', 'GlowMapMarker', 'GlowMapMarkerPopup', 'GlowMarkerMapLayer')


import os
import webbrowser
from collections import namedtuple
from itertools import takewhile
from math import ceil
from typing import (
    Any,
    Self,
)

from kivy.base import EventLoop
from kivy.clock import Clock
from kivy.compat import string_types
from kivy.graphics import (
    Canvas,
    Color,
    Rectangle,
)
from kivy.graphics.transformation import Matrix
from kivy.input.motionevent import MotionEvent
from kivy.lang import Builder
from kivy.properties import (
    AliasProperty,
    BooleanProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget

from kivy_glow import kivy_glow_uix_dir
from kivy_glow.uix.label import GlowLabel
from kivy_glow.uix.widget import GlowWidget

from .mapsource import MapSource

with open(
    os.path.join(kivy_glow_uix_dir, 'map', 'map.kv'), encoding='utf-8',
) as kv_file:
    Builder.load_string(kv_file.read())


def clamp(x: float | int, minimum: float | int, maximum: float | int) -> float | int:
    return max(minimum, min(x, maximum))


Coordinate = namedtuple('Coordinate', ['lat', 'lon'])


class Bbox(tuple):
    def collide(self, *args) -> bool:
        if isinstance(args[0], Coordinate):
            coord = args[0]
            lat = coord.lat
            lon = coord.lon
        else:
            lat, lon = args
        lat1, lon1, lat2, lon2 = self[:]

        if lat1 < lat2:
            in_lat = lat1 <= lat <= lat2
        else:
            in_lat = lat2 <= lat <= lat2
        if lon1 < lon2:
            in_lon = lon1 <= lon <= lon2
        else:
            in_lon = lon2 <= lon <= lon2

        return in_lat and in_lon


class AttributionLabel(GlowLabel):
    def on_ref_press(self, *args) -> None:
        webbrowser.open(str(args[0]), new=2)


class Tile(Rectangle):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.cache_dir = kwargs.get('cache_dir', 'map_cache')

    @property
    def cache_fn(self) -> str:
        map_source = self.map_source
        fn = map_source.cache_fmt.format(
            cache_key=map_source.cache_key,
            **self.__dict__,
        )
        return os.path.join(self.cache_dir, fn)

    def set_source(self, cache_fn: str) -> None:
        self.source = cache_fn
        self.state = 'need-animation'


class GlowMapMarker(ButtonBehavior, GlowWidget, Image):
    '''A marker on a map, that must be used on a :class:`GlowMapMarker`'''

    anchor_x = NumericProperty(defaultvalue=0.5)
    '''Anchor of the marker on the X axis. Defaults to 0.5, mean the anchor will
    be at the X center of the image.
    '''

    anchor_y = NumericProperty(defaultvalue=0)
    '''Anchor of the marker on the Y axis. Defaults to 0, mean the anchor will
    be at the Y bottom of the image.
    '''

    lat = NumericProperty(defaultvalue=0)
    '''Latitude of the marker'''

    lon = NumericProperty(defaultvalue=0)
    '''Longitude of the marker'''

    source = StringProperty(defaultvalue='kivy_glow/images/map/marker.png')
    '''Source of the marker, defaults to our own marker.png'''

    _layer = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.texture_update()

        if 'texture_size' in kwargs.keys():
            self.texture_size = kwargs['texture_size']

    def detach(self) -> None:
        if self._layer:
            self._layer.remove_widget(self)
            self._layer = None


class GlowMapMarkerPopup(GlowMapMarker):
    is_open = BooleanProperty(defaultvalue=False)
    placeholder = ObjectProperty(defaultvalue=None)

    def add_widget(self, widget: Widget) -> None:
        if not self.placeholder:
            self.placeholder = widget
            if self.is_open:
                super().add_widget(self.placeholder)
        else:
            self.placeholder.add_widget(widget)

    def remove_widget(self, widget: Widget) -> None:
        if widget is not self.placeholder:
            self.placeholder.remove_widget(widget)
        else:
            super().remove_widget(widget)

    def on_is_open(self, *args) -> None:
        self.refresh_open_status()

    def on_release(self, *args) -> None:
        self.is_open = not self.is_open

    def refresh_open_status(self) -> None:
        if not self.is_open and self.placeholder.parent:
            super().remove_widget(self.placeholder)
        elif self.is_open and not self.placeholder.parent:
            super().add_widget(self.placeholder)


class GlowMapLayer(GlowWidget):
    '''A map layer, that is repositionned everytime the :class:`GlowMap` is
    moved.
    '''

    viewport_x = NumericProperty(defaultvalue=0)
    viewport_y = NumericProperty(defaultvalue=0)

    def reposition(self) -> None:
        '''Function called when :class:`MapView` is moved. You must recalculate
        the position of your children.
        '''
        pass

    def unload(self) -> None:
        '''Called when the view want to completly unload the layer.'''
        pass


class GlowMarkerMapLayer(GlowMapLayer):
    '''A map layer for :class:`GlowMapMarker`'''

    order_marker_by_latitude = BooleanProperty(defaultvalue=True)

    def __init__(self, *args, **kwargs) -> None:
        self.markers = []
        super().__init__(*args, **kwargs)

    def insert_marker(self, marker: GlowMapMarker | GlowMapMarkerPopup, **kwargs) -> None:
        if self.order_marker_by_latitude:
            before = list(
                takewhile(lambda i_m: i_m[1].lat < marker.lat, enumerate(self.children)),
            )
            if before:
                kwargs['index'] = before[-1][0] + 1

        super().add_widget(marker, **kwargs)

    def add_widget(self, marker: GlowMapMarker | GlowMapMarkerPopup) -> None:
        marker._layer = self
        self.markers.append(marker)
        self.insert_marker(marker)

    def remove_widget(self, marker: GlowMapMarker | GlowMapMarkerPopup) -> None:
        marker._layer = None
        if marker in self.markers:
            self.markers.remove(marker)
        super().remove_widget(marker)

    def reposition(self) -> None:
        if not self.markers:
            return
        mapview = self.parent
        set_marker_position = self.set_marker_position
        bbox = None
        # reposition the markers depending the latitude
        markers = sorted(self.markers, key=lambda x: -x.lat)
        margin = max(max(marker.size) for marker in markers)
        bbox = mapview.get_bbox(margin)
        for marker in markers:
            if bbox.collide(marker.lat, marker.lon):
                set_marker_position(mapview, marker)
                if not marker.parent:
                    self.insert_marker(marker)
            else:
                super().remove_widget(marker)

    def set_marker_position(self, mapview: Widget, marker: GlowMapMarker | GlowMapMarkerPopup) -> None:
        x, y = mapview.get_window_xy_from(marker.lat, marker.lon, mapview.zoom)
        marker.x = int(x - marker.width * marker.anchor_x)
        marker.y = int(y - marker.height * marker.anchor_y)

    def unload(self) -> None:
        self.clear_widgets()
        del self.markers[:]


class GlowMapViewScatter(GlowWidget, Scatter):
    def on_transform(self, *args) -> None:
        super().on_transform(*args)
        self.parent.on_transform(self.transform)

    def collide_point(self, x: float | int, y: float | int) -> bool:
        return True


class GlowMap(GlowWidget):
    '''MapView is the widget that control the map displaying, navigation, and
    layers management.
    '''

    lon = NumericProperty()
    '''Longitude at the center of the widget
    '''

    lat = NumericProperty()
    '''Latitude at the center of the widget
    '''

    zoom = NumericProperty(defaultvalue=0)
    '''Zoom of the widget. Must be between :meth:`MapSource.get_min_zoom` and
    :meth:`MapSource.get_max_zoom`. Default to 0.
    '''

    map_source = ObjectProperty(defaultvalue=MapSource())
    '''Provider of the map, default to a empty :class:`MapSource`.
    '''

    double_tap_zoom = BooleanProperty(defaultvalue=False)
    '''If True, this will activate the double-tap to zoom.
    '''

    pause_on_action = BooleanProperty(defaultvalue=True)
    '''Pause any map loading / tiles loading when an action is done.
    This allow better performance on mobile, but can be safely deactivated on
    desktop.
    '''

    snap_to_zoom = BooleanProperty(defaultvalue=True)
    '''When the user initiate a zoom, it will snap to the closest zoom for
    better graphics. The map can be blur if the map is scaled between 2 zoom.
    Default to True, even if it doesn't fully working yet.
    '''

    animation_duration = NumericProperty(defaultvalue=100)
    '''Duration to animate Tiles alpha from 0 to 1 when it's ready to show.
    Default to 100 as 100ms. Use 0 to deactivate.
    '''

    delta_x = NumericProperty(defaultvalue=0)
    delta_y = NumericProperty(defaultvalue=0)
    background_color = ListProperty(defaultvalue=[181 / 255.0, 208 / 255.0, 208 / 255.0, 1])
    cache_dir = StringProperty(defaultvalue='map_cache')
    _zoom = NumericProperty(defaultvalue=0)
    _pause = BooleanProperty(defaultvalue=False)
    _scale = 1.0
    _disabled_count = 0

    __events__ = ('on_map_relocated', )

    # Public API

    @property
    def viewport_pos(self) -> tuple[float | int, float | int]:
        vx, vy = self._scatter.to_local(self.x, self.y)
        return vx - self.delta_x, vy - self.delta_y

    @property
    def scale(self) -> float:
        if self._invalid_scale:
            self._invalid_scale = False
            self._scale = self._scatter.scale
        return self._scale

    def get_bbox(self, margin: float | int = 0) -> Bbox:
        '''Returns the bounding box from the bottom/left (lat1, lon1) to
        top/right (lat2, lon2).'''
        x1, y1 = self.to_local(0 - margin, 0 - margin)
        x2, y2 = self.to_local((self.width + margin), (self.height + margin))
        c1 = self.get_latlon_at(x1, y1)
        c2 = self.get_latlon_at(x2, y2)

        return Bbox((c1.lat, c1.lon, c2.lat, c2.lon))

    bbox = AliasProperty(get_bbox, None, bind=['lat', 'lon', '_zoom'])

    def unload(self) -> None:
        '''Unload the view and all the layers.
        It also cancel all the remaining downloads.
        '''
        self.remove_all_tiles()

    def get_window_xy_from(self, lat: float | int, lon: float | int, zoom: int) -> tuple[float | int, float | int]:
        '''Returns the x/y position in the widget absolute coordinates
        from a lat/lon'''
        scale = self.scale
        vx, vy = self.viewport_pos
        ms = self.map_source
        nx = (ms.get_x(zoom, lon) - vx) * scale + self.pos[0]
        ny = (ms.get_y(zoom, lat) - vy) * scale + self.pos[1]
        return nx, ny

    def center_on(self, *args) -> None:
        '''Center the map on the coordinate :class:`Coordinate`, or a (lat, lon)
        '''
        map_source = self.map_source
        zoom = self._zoom

        if len(args) == 1 and isinstance(args[0], Coordinate):
            coord = args[0]
            lat = coord.lat
            lon = coord.lon
        elif len(args) == 2:
            lat, lon = args
        else:
            raise Exception('Invalid argument for center_on')

        lon = clamp(lon, -180.0, 180.0)
        lat = clamp(lat, -90.0, 90.0)
        scale = self._scatter.scale
        x = map_source.get_x(zoom, lon) - self.center_x / scale
        y = map_source.get_y(zoom, lat) - self.center_y / scale
        self.delta_x = -x
        self.delta_y = -y
        self.lon = lon
        self.lat = lat
        self._scatter.pos = 0, 0
        self.trigger_update(full=True)

    def set_zoom_at(self, zoom: int, x: float | int, y: float | int, scale: float | None = None) -> None:
        '''Sets the zoom level, leaving the (x, y) at the exact same point
        in the view.
        '''
        zoom = clamp(
            zoom, self.map_source.get_min_zoom(), self.map_source.get_max_zoom(),
        )
        if int(zoom) == int(self._zoom):
            if scale is None:
                return
            if scale == self.scale:
                return
        scale = scale or 1.0

        # first, rescale the scatter
        scatter = self._scatter
        scale = clamp(scale, scatter.scale_min, scatter.scale_max)
        rescale = scale * 1.0 / scatter.scale

        scatter.apply_transform(
            Matrix().scale(rescale, rescale, rescale),
            post_multiply=True,
            anchor=scatter.to_local(x, y),
        )

        # adjust position if the zoom changed
        c1 = self.map_source.get_col_count(self._zoom)
        c2 = self.map_source.get_col_count(zoom)
        if c1 != c2:
            f = float(c2) / float(c1)
            self.delta_x = scatter.x + self.delta_x * f
            self.delta_y = scatter.y + self.delta_y * f
            # back to 0 every time
            scatter.apply_transform(
                Matrix().translate(-scatter.x, -scatter.y, 0), post_multiply=True,
            )

        # avoid triggering zoom changes.
        self._zoom = zoom
        self.zoom = self._zoom

    def on_zoom(self, instance: Self, zoom: int) -> None:
        if zoom == self._zoom:
            return

        x = self.map_source.get_x(zoom, self.lon) - self.delta_x
        y = self.map_source.get_y(zoom, self.lat) - self.delta_y
        self.set_zoom_at(zoom, x, y)
        self.center_on(self.lat, self.lon)

        if zoom == self.map_source.min_zoom:
            self.trigger_update(full=True)
            self._scatter.scale = 1
            self.center_on(0, 0)
            self._scale = 1

    def get_latlon_at(self, x: int | float, y: int | float, zoom: int | None = None) -> Coordinate:
        '''Return the current :class:`Coordinate` within the (x, y) widget
        coordinate.
        '''
        if zoom is None:
            zoom = self._zoom
        vx, vy = self.viewport_pos
        scale = self._scale
        return Coordinate(
            lat=self.map_source.get_lat(zoom, y / scale + vy),
            lon=self.map_source.get_lon(zoom, x / scale + vx),
        )

    def add_marker(self, marker: GlowMapMarker | GlowMapMarkerPopup, layer: GlowMarkerMapLayer | None = None) -> None:
        '''Add a marker into the layer. If layer is None, it will be added in
        the default marker layer. If there is no default marker layer, a new
        one will be automatically created
        '''
        if layer is None:
            if not self._default_marker_layer:
                layer = GlowMarkerMapLayer()
                self.add_layer(layer)
            else:
                layer = self._default_marker_layer
        layer.add_widget(marker)
        layer.set_marker_position(self, marker)

    def remove_marker(self, marker: GlowMapMarker | GlowMapMarkerPopup) -> None:
        '''Remove a marker from its layer
        '''
        marker.detach()

    def add_layer(self, layer: GlowMarkerMapLayer, mode: str = 'window') -> None:
        '''Add a new layer to update at the same time the base tile layer.
        mode can be either 'scatter' or 'window'. If 'scatter', it means the
        layer will be within the scatter transformation. It's perfect if you
        want to display path / shape, but not for text.
        If 'window', it will have no transformation. You need to position the
        widget yourself: think as Z-sprite / billboard.
        Defaults to 'window'.
        '''
        if mode not in {'scatter', 'window'}:
            raise ValueError('mode should be in (`scatter`, `window`)')

        if self._default_marker_layer is None and isinstance(layer, GlowMarkerMapLayer):
            self._default_marker_layer = layer
        self._layers.append(layer)
        c = self.canvas
        if mode == 'scatter':
            self.canvas = self.canvas_layers
        else:
            self.canvas = self.canvas_layers_out
        layer.canvas_parent = self.canvas
        super().add_widget(layer)
        self.canvas = c

    def remove_layer(self, layer: GlowMarkerMapLayer) -> None:
        '''Remove the layer
        '''
        c = self.canvas
        self._layers.remove(layer)
        self.canvas = layer.canvas_parent
        super().remove_widget(layer)
        self.canvas = c

    def sync_to(self, other: Self) -> None:
        '''Reflect the lat/lon/zoom of the other MapView to the current one.
        '''
        if self._zoom != other._zoom:
            self.set_zoom_at(other._zoom, *self.center)
        self.center_on(other.get_latlon_at(*self.center))

    # Private API

    def __init__(self, *args, **kwargs) -> None:

        EventLoop.ensure_window()
        self._invalid_scale = True
        self._tiles = []
        self._tiles_bg = []
        self._tilemap = {}
        self._layers = []
        self._default_marker_layer = None
        self._need_redraw_full = True
        self._transform_lock = False
        self.trigger_update(full=True)
        self.canvas = Canvas()
        self._scatter = GlowMapViewScatter()
        self.add_widget(self._scatter)
        self._scatter.scale = 2
        with self._scatter.canvas:
            self.canvas_map = Canvas()
            self.canvas_layers = Canvas()
        with self.canvas:
            self.canvas_layers_out = Canvas()
        self._scale_target_anim = False
        self._scale_target = 1.0
        self._touch_count = 0
        self.map_source.cache_dir = self.cache_dir
        Clock.schedule_interval(self._animate_color, 1 / 60.0)
        self.lat = kwargs.get('lat', self.lat)
        self.lon = kwargs.get('lon', self.lon)

        super().__init__(*args, **kwargs)

    def _animate_color(self, dt: float | int) -> None:
        # fast path
        d = self.animation_duration
        if d == 0:
            for tile in self._tiles:
                if tile.state == 'need-animation':
                    tile.g_color.a = 1.0
                    tile.state = 'animated'
            for tile in self._tiles_bg:
                if tile.state == 'need-animation':
                    tile.g_color.a = 1.0
                    tile.state = 'animated'
        else:
            d /= 1000.0
            for tile in self._tiles:
                if tile.state != 'need-animation':
                    continue
                tile.g_color.a += dt / d
                if tile.g_color.a >= 1:
                    tile.state = 'animated'
            for tile in self._tiles_bg:
                if tile.state != 'need-animation':
                    continue
                tile.g_color.a += dt / d
                if tile.g_color.a >= 1:
                    tile.state = 'animated'

    def add_widget(self, widget: Widget) -> None:
        if isinstance(widget, GlowMapMarker):
            self.add_marker(widget)
        elif isinstance(widget, GlowMapLayer):
            self.add_layer(widget)
        else:
            super().add_widget(widget)

    def remove_widget(self, widget: Widget) -> None:
        if isinstance(widget, GlowMapMarker):
            self.remove_marker(widget)
        elif isinstance(widget, GlowMapLayer):
            self.remove_layer(widget)
        else:
            super().remove_widget(widget)

    def on_map_relocated(self, zoom: int, coord: Coordinate) -> None:
        pass

    def animated_diff_scale_at(self, d: float, x: float | int, y: float | int) -> None:
        self._scale_target_time = 1.0
        self._scale_target_pos = x, y
        if self._scale_target_anim is False:
            self._scale_target_anim = True
            self._scale_target = d
        else:
            self._scale_target += d
        Clock.unschedule(self._animate_scale)
        Clock.schedule_interval(self._animate_scale, 1 / 60.0)

    def _animate_scale(self, dt: float) -> bool:
        diff = self._scale_target / 3.0
        if abs(diff) < 0.01:
            diff = self._scale_target
            self._scale_target = 0
        else:
            self._scale_target -= diff
        self._scale_target_time -= dt
        self.diff_scale_at(diff, *self._scale_target_pos)
        ret = self._scale_target != 0
        if not ret:
            self._pause = False
        return ret

    def diff_scale_at(self, d: float, x: float | int, y: float | int) -> None:
        scatter = self._scatter
        scale = scatter.scale * (2 ** d)
        self.scale_at(scale, x, y)

    def scale_at(self, scale: float, x: float | int, y: float | int) -> None:
        scatter = self._scatter
        scale = clamp(scale, scatter.scale_min, scatter.scale_max)
        rescale = scale * 1.0 / scatter.scale
        scatter.apply_transform(
            Matrix().scale(rescale, rescale, rescale),
            post_multiply=True,
            anchor=scatter.to_local(x, y),
        )

    def on_touch_down(self, touch: MotionEvent) -> bool:
        if not self.collide_point(*touch.pos):
            return False

        if self.pause_on_action:
            self._pause = True
        if 'button' in touch.profile and touch.button in {'scrolldown', 'scrollup'}:

            d = 1 if touch.button == 'scrolldown' else -1
            self.animated_diff_scale_at(d, *touch.pos)
            return True

        if touch.is_double_tap and self.double_tap_zoom:
            self.animated_diff_scale_at(1, *touch.pos)
            return True

        touch.grab(self)
        self._touch_count += 1
        if self._touch_count == 1:
            self._touch_zoom = (self.zoom, self._scale)
        return super().on_touch_down(touch)

    def on_touch_up(self, touch: MotionEvent) -> bool:
        if touch.grab_current == self:
            touch.ungrab(self)
            self._touch_count -= 1
            if self._touch_count == 0:

                # animate to the closest zoom
                zoom, scale = self._touch_zoom
                cur_zoom = self.zoom
                cur_scale = self._scale

                if cur_zoom < zoom or round(cur_scale, 3) < round(scale, 3):
                    self.animated_diff_scale_at(1.0 - cur_scale, *touch.pos)
                elif cur_zoom > zoom or round(cur_scale, 3) > round(scale, 3):
                    self.animated_diff_scale_at(2.0 - cur_scale, *touch.pos)

                self._pause = False

            return True

        return super().on_touch_up(touch)

    def on_transform(self, *args) -> None:
        self._invalid_scale = True
        if self._transform_lock:
            return
        self._transform_lock = True
        # recalculate viewport
        map_source = self.map_source
        zoom = self._zoom
        scatter = self._scatter
        scale = scatter.scale

        if (scale - 2.0) > 0.01:
            zoom += 1
            scale /= 2.0
        elif (scale - 1.0) < -0.01:
            zoom -= 1
            scale *= 2.0

        zoom = clamp(zoom, map_source.min_zoom, map_source.max_zoom)
        if zoom != self._zoom:
            self.set_zoom_at(zoom, scatter.x, scatter.y, scale=scale)
            self.trigger_update(full=True)
        elif zoom == map_source.min_zoom and scatter.scale < 1:
            scatter.scale = 1
            self.center_on(0, 0)
            self.trigger_update(full=True)
        else:
            self.trigger_update(full=False)

        if map_source.bounds:
            self._apply_bounds()

        self._transform_lock = False
        self._scale = self._scatter.scale

    def _apply_bounds(self) -> None:
        # if the map_source have any constraints, apply them here.
        map_source = self.map_source
        zoom = self._zoom
        min_lon, min_lat, max_lon, max_lat = map_source.bounds
        xmin = map_source.get_x(zoom, min_lon)
        xmax = map_source.get_x(zoom, max_lon)
        ymin = map_source.get_y(zoom, min_lat)
        ymax = map_source.get_y(zoom, max_lat)

        dx = self.delta_x
        dy = self.delta_y
        oxmin, oymin = self._scatter.to_local(self.x, self.y)
        oxmax, oymax = self._scatter.to_local(self.right, self.top)
        s = self._scale
        cxmin = oxmin - dx
        if cxmin < xmin:
            self._scatter.x += (cxmin - xmin) * s
        cymin = oymin - dy
        if cymin < ymin:
            self._scatter.y += (cymin - ymin) * s
        cxmax = oxmax - dx
        if cxmax > xmax:
            self._scatter.x -= (xmax - cxmax) * s
        cymax = oymax - dy
        if cymax > ymax:
            self._scatter.y -= (ymax - cymax) * s

    def on__pause(self, instance: Self, value: bool) -> None:
        if not value:
            self.trigger_update(full=True)

    def trigger_update(self, full: bool) -> None:
        self._need_redraw_full = full or self._need_redraw_full
        Clock.unschedule(self.do_update)
        Clock.schedule_once(self.do_update, -1)

    def do_update(self, *args) -> None:
        zoom = self._zoom
        scale = self._scale
        self.lon = self.map_source.get_lon(
            zoom, (self.center_x - self._scatter.x) / scale - self.delta_x,
        )
        self.lat = self.map_source.get_lat(
            zoom, (self.center_y - self._scatter.y) / scale - self.delta_y,
        )
        self._scatter.size = self.size

        self.dispatch('on_map_relocated', zoom, Coordinate(self.lon, self.lat))
        for layer in self._layers:
            layer.reposition()

        if self._need_redraw_full:
            self._need_redraw_full = False
            self.move_tiles_to_background()
            self.load_visible_tiles()
        else:
            self.load_visible_tiles()

    def bbox_for_zoom(self, vx: float | int, vy: float | int, w: float | int, h: float | int, zoom: int) -> tuple[int, int, int, int, int, int]:
        # return a tile-bbox for the zoom
        map_source = self.map_source
        size = map_source.dp_tile_size
        scale = self._scale

        max_x_end = map_source.get_col_count(zoom)
        max_y_end = map_source.get_row_count(zoom)

        x_count = int(ceil(w / scale / float(size))) + 1
        y_count = int(ceil(h / scale / float(size))) + 1

        tile_x_first = int(clamp(vx / float(size), 0, max_x_end))
        tile_y_first = int(clamp(vy / float(size), 0, max_y_end))
        tile_x_last = tile_x_first + x_count
        tile_y_last = tile_y_first + y_count
        tile_x_last = int(clamp(tile_x_last, tile_x_first, max_x_end))
        tile_y_last = int(clamp(tile_y_last, tile_y_first, max_y_end))

        x_count = tile_x_last - tile_x_first
        y_count = tile_y_last - tile_y_first
        return (tile_x_first, tile_y_first, tile_x_last, tile_y_last, x_count, y_count)

    def load_visible_tiles(self) -> None:
        map_source = self.map_source
        vx, vy = self.viewport_pos
        zoom = self._zoom
        dirs = [0, 1, 0, -1, 0]
        bbox_for_zoom = self.bbox_for_zoom
        size = map_source.dp_tile_size

        (
            tile_x_first,
            tile_y_first,
            tile_x_last,
            tile_y_last,
            x_count,
            y_count,
        ) = bbox_for_zoom(vx, vy, self.width, self.height, zoom)

        # Adjust tiles behind us
        for tile in self._tiles_bg[:]:
            tile_x = tile.tile_x
            tile_y = tile.tile_y

            f = 2 ** (zoom - tile.zoom)
            w = self.width / f
            h = self.height / f
            (
                btile_x_first,
                btile_y_first,
                btile_x_last,
                btile_y_last,
                _,
                _,
            ) = bbox_for_zoom(vx / f, vy / f, w, h, tile.zoom)

            if (
                tile_x < btile_x_first
                or tile_x >= btile_x_last
                or tile_y < btile_y_first
                or tile_y >= btile_y_last
            ):
                tile.state = 'done'
                self._tiles_bg.remove(tile)
                self.canvas_map.before.remove(tile.g_color)
                self.canvas_map.before.remove(tile)
                continue

            tsize = size * f
            tile.size = tsize, tsize
            tile.pos = (tile_x * tsize + self.delta_x, tile_y * tsize + self.delta_y)

        # Get rid of old tiles first
        for tile in self._tiles[:]:
            tile_x = tile.tile_x
            tile_y = tile.tile_y

            if (
                tile_x < tile_x_first
                or tile_x >= tile_x_last
                or tile_y < tile_y_first
                or tile_y >= tile_y_last
            ):
                tile.state = 'done'
                self.tile_map_set(tile_x, tile_y, value=False)
                self._tiles.remove(tile)
                self.canvas_map.remove(tile)
                self.canvas_map.remove(tile.g_color)
            else:
                tile.size = (size, size)
                tile.pos = (tile_x * size + self.delta_x, tile_y * size + self.delta_y)

        # Load new tiles if needed
        x = tile_x_first + x_count // 2 - 1
        y = tile_y_first + y_count // 2 - 1
        arm_max = max(x_count, y_count) + 2
        arm_size = 1
        turn = 0
        while arm_size < arm_max:
            for _ in range(arm_size):
                if (
                    not self.tile_in_tile_map(x, y)
                    and y >= tile_y_first
                    and y < tile_y_last
                    and x >= tile_x_first
                    and x < tile_x_last
                ):
                    self.load_tile(x, y, size, zoom)

                x += dirs[turn % 4 + 1]
                y += dirs[turn % 4]

            if turn % 2 == 1:
                arm_size += 1

            turn += 1

    def load_tile(self, x: float | int, y: float | int, size: int, zoom: int) -> None:
        if self.tile_in_tile_map(x, y) or zoom != self._zoom:
            return
        self.load_tile_for_source(self.map_source, 1.0, size, x, y, zoom)
        # XXX do overlay support
        self.tile_map_set(x, y, value=True)

    def load_tile_for_source(self, map_source: MapSource, opacity: float, size: int, x: float | int, y: float | int, zoom: int) -> None:
        tile = Tile(size=(size, size), cache_dir=self.cache_dir)
        tile.g_color = Color(1, 1, 1, 0)
        tile.tile_x = x
        tile.tile_y = y
        tile.zoom = zoom
        tile.pos = (x * size + self.delta_x, y * size + self.delta_y)
        tile.map_source = map_source
        tile.state = 'loading'
        if not self._pause:
            map_source.fill_tile(tile)
        self.canvas_map.add(tile.g_color)
        self.canvas_map.add(tile)
        self._tiles.append(tile)

    def move_tiles_to_background(self) -> None:
        # remove all the tiles of the main map to the background map
        # retain only the one who are on the current zoom level
        # for all the tile in the background, stop the download if not yet started.
        zoom = self._zoom
        tiles = self._tiles
        btiles = self._tiles_bg
        canvas_map = self.canvas_map
        tile_size = self.map_source.tile_size

        # move all tiles to background
        while tiles:
            tile = tiles.pop()
            if tile.state == 'loading':
                tile.state = 'done'
                continue
            btiles.append(tile)

        # clear the canvas
        canvas_map.clear()
        canvas_map.before.clear()
        self._tilemap = {}

        # unsure if it's really needed, i personnally didn't get issues right now
        # btiles.sort(key=lambda z: -z.zoom)

        # add all the btiles into the back canvas.
        # except for the tiles that are owned by the current zoom level
        for tile in btiles[:]:
            if tile.zoom == zoom:
                btiles.remove(tile)
                tiles.append(tile)
                tile.size = tile_size, tile_size
                canvas_map.add(tile.g_color)
                canvas_map.add(tile)
                self.tile_map_set(tile.tile_x, tile.tile_y, value=True)
                continue
            canvas_map.before.add(tile.g_color)
            canvas_map.before.add(tile)

    def remove_all_tiles(self) -> None:
        # clear the map of all tiles.
        self.canvas_map.clear()
        self.canvas_map.before.clear()
        for tile in self._tiles:
            tile.state = 'done'
        del self._tiles[:]
        del self._tiles_bg[:]
        self._tilemap = {}

    def tile_map_set(self, tile_x: float | int, tile_y: float | int, value: bool) -> None:
        key = tile_y * self.map_source.get_col_count(self._zoom) + tile_x
        if value:
            self._tilemap[key] = value
        else:
            self._tilemap.pop(key, None)

    def tile_in_tile_map(self, tile_x: float | int, tile_y: float | int) -> bool:
        key = tile_y * self.map_source.get_col_count(self._zoom) + tile_x
        return key in self._tilemap

    def on_size(self, instance: Self, size: tuple[float | int, float | int]) -> None:
        for layer in self._layers:
            layer.size = size
        self.center_on(self.lat, self.lon)
        self.trigger_update(full=True)

    def on_pos(self, instance: Self, pos: tuple[float | int, float | int]) -> None:
        self.center_on(self.lat, self.lon)
        self.trigger_update(full=True)

    def on_map_source(self, instance: Self, source: Any) -> None:
        if isinstance(source, string_types):
            self.map_source = MapSource(source)
        elif isinstance(source, MapSource):
            self.map_source = source
        else:
            raise Exception('Invalid map source provider')

        self.zoom = clamp(self.zoom, self.map_source.min_zoom, self.map_source.max_zoom)
        self.remove_all_tiles()
        self.trigger_update(full=True)
