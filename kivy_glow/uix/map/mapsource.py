__all__ = ('MapSource', )

from .mapdownloader import MapDownloader
from kivy.metrics import dp
from math import (
    atan,
    cos,
    tan,
    exp,
    log,
    pi,
)


def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))


class MapSource:
    providers = {
        'osm': {
            'min_zoom': 0,
            'max_zoom': 19,
            'sub_domains': ['a', 'b', 'c'],
            'url_template': 'http://{sub_domain}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            'attribution': 'Maps & Data © [i][ref=http://www.osm.org/copyright]OpenStreetMap[/ref][/i] contributors.',
        },
        'osm-hot': {
            'min_zoom': 0,
            'max_zoom': 19,
            'sub_domains': ['a', 'b', 'c'],
            'url_template': 'http://{sub_domain}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
            'attribution': '[i][ref=https://www.openstreetmap.org/copyright]OpenStreetMap[/ref][/i] contributors, Tiles style by [i][ref=https://www.hotosm.org/]Humanitarian OpenStreetMap Team[/ref][/i] hosted by [i][ref=https://openstreetmap.fr/]OpenStreetMap France[/ref][/i]'
        },
        'opnv': {
            'min_zoom': 0,
            'max_zoom': 18,
            'url_template': 'https://tileserver.memomaps.de/tilegen/{z}/{x}/{y}.png',
            'attribution': 'Map [i][ref=https://memomaps.de/]memomaps.de[/ref][/i] [i][ref=http://creativecommons.org/licenses/by-sa/2.0/]CC-BY-SA[/ref][/i], map data [i][ref=https://www.openstreetmap.org/copyright]OpenStreetMap[/ref][/i] contributors'
        },
        'stadia-smooth': {
            'min_zoom': 0,
            'max_zoom': 20,
            'url_template': 'https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}.png?api_key={api_key}',
            'attribution': '[i][ref=https://www.stadiamaps.com/]Stadia Maps[/ref][/i] [i][ref=https://openmaptiles.org/]OpenMapTiles[/ref][/i] [i][ref=https://www.openstreetmap.org/copyright]OpenStreetMap[/ref][/i] contributors'
        },
        'stadia-smooth-dark': {
            'min_zoom': 0,
            'max_zoom': 20,
            'url_template': 'https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}.png?api_key={api_key}',
            'attribution': '[i][ref=https://www.stadiamaps.com/]Stadia Maps[/ref][/i] [i][ref=https://openmaptiles.org/]OpenMapTiles[/ref][/i] [i][ref=https://www.openstreetmap.org/copyright]OpenStreetMap[/ref][/i] contributors'
        },
        'stadia-satellite': {
            'min_zoom': 0,
            'max_zoom': 20,
            'url_template': 'https://tiles.stadiamaps.com/tiles/alidade_satellite/{z}/{x}/{y}.png?api_key={api_key}',
            'attribution': 'CNES, Distribution Airbus DS, © Airbus DS, © PlanetObserver (Contains Copernicus Data) [i][ref=https://www.stadiamaps.com/]Stadia Maps[/ref][/i] [i][ref=https://openmaptiles.org/]OpenMapTiles[/ref][/i] [i][ref=https://www.openstreetmap.org/copyright]OpenStreetMap[/ref][/i] contributors'
        },
        'stadia-bright': {
            'min_zoom': 0,
            'max_zoom': 20,
            'url_template': 'https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}.png?api_key={api_key}',
            'attribution': '[i][ref=https://www.stadiamaps.com/]Stadia Maps[/ref][/i] [i][ref=https://openmaptiles.org/]OpenMapTiles[/ref][/i] [i][ref=https://www.openstreetmap.org/copyright]OpenStreetMap[/ref][/i] contributors'
        },
        'stadia-outdoors': {
            'min_zoom': 0,
            'max_zoom': 20,
            'url_template': 'https://tiles.stadiamaps.com/tiles/outdoors/{z}/{x}/{y}.png?api_key={api_key}',
            'attribution': '[i][ref=https://www.stadiamaps.com/]Stadia Maps[/ref][/i] [i][ref=https://openmaptiles.org/]OpenMapTiles[/ref][/i] [i][ref=https://www.openstreetmap.org/copyright]OpenStreetMap[/ref][/i] contributors'
        },
        'stadia-toner': {
            'min_zoom': 0,
            'max_zoom': 20,
            'url_template': 'https://tiles.stadiamaps.com/tiles/stamen_toner/{z}/{x}/{y}.png?api_key={api_key}',
            'attribution': '[i][ref=https://www.stadiamaps.com/]Stadia Maps[/ref][/i] [i][ref=https://www.stamen.com/]Stamen Design[/ref][/i] [i][ref=https://openmaptiles.org/]OpenMapTiles[/ref][/i] [i][ref=https://www.openstreetmap.org/copyright]OpenStreetMap[/ref][/i] contributors'
        },
        'stadia-toner-light': {
            'min_zoom': 0,
            'max_zoom': 20,
            'url_template': 'https://tiles.stadiamaps.com/tiles/stamen_toner_lite/{z}/{x}/{y}.png?api_key={api_key}',
            'attribution': '[i][ref=https://www.stadiamaps.com/]Stadia Maps[/ref][/i] [i][ref=https://www.stamen.com/]Stamen Design[/ref][/i] [i][ref=https://openmaptiles.org/]OpenMapTiles[/ref][/i] [i][ref=https://www.openstreetmap.org/copyright]OpenStreetMap[/ref][/i] contributors'
        },
        'stadia-terrain': {
            'min_zoom': 0,
            'max_zoom': 18,
            'url_template': 'https://tiles.stadiamaps.com/tiles/stamen_terrain/{z}/{x}/{y}.png?api_key={api_key}',
            'attribution': '[i][ref=https://www.stadiamaps.com/]Stadia Maps[/ref][/i] [i][ref=https://www.stamen.com/]Stamen Design[/ref][/i] [i][ref=https://openmaptiles.org/]OpenMapTiles[/ref][/i] [i][ref=https://www.openstreetmap.org/copyright]OpenStreetMap[/ref][/i] contributors'
        },
        'thunderforest-transport': {
            'min_zoom': 0,
            'max_zoom': 22,
            'sub_domains': ['a', 'b', 'c', 'd'],
            'url_template': 'https://{sub_domain}.tile.thunderforest.com/transport/{z}/{x}/{y}.png?apikey={api_key}',
            'attribution': '[i][ref=http://www.thunderforest.com/]Thunderforest[/ref][/i], [i][ref=https://www.openstreetmap.org/copyright">OpenStreetMap[/ref][/i] contributors'
        },
        'thunderforest-transport-dark': {
            'min_zoom': 0,
            'max_zoom': 22,
            'sub_domains': ['a', 'b', 'c', 'd'],
            'url_template': 'https://{sub_domain}.tile.thunderforest.com/transport-dark/{z}/{x}/{y}.png?apikey={api_key}',
            'attribution': '[i][ref=http://www.thunderforest.com/]Thunderforest[/ref][/i], [i][ref=https://www.openstreetmap.org/copyright">OpenStreetMap[/ref][/i] contributors'
        },
        'thunderforest-landscape': {
            'min_zoom': 0,
            'max_zoom': 22,
            'sub_domains': ['a', 'b', 'c', 'd'],
            'url_template': 'https://{sub_domain}.tile.thunderforest.com/landscape/{z}/{x}/{y}.png?apikey={api_key}',
            'attribution': '[i][ref=http://www.thunderforest.com/]Thunderforest[/ref][/i], [i][ref=https://www.openstreetmap.org/copyright">OpenStreetMap[/ref][/i] contributors'
        },
        'thunderforest-outdoors': {
            'min_zoom': 0,
            'max_zoom': 22,
            'sub_domains': ['a', 'b', 'c', 'd'],
            'url_template': 'https://{sub_domain}.tile.thunderforest.com/outdoors/{z}/{x}/{y}.png?apikey={api_key}',
            'attribution': '[i][ref=http://www.thunderforest.com/]Thunderforest[/ref][/i], [i][ref=https://www.openstreetmap.org/copyright">OpenStreetMap[/ref][/i] contributors'
        },
        'thunderforest-pioneer': {
            'min_zoom': 0,
            'max_zoom': 22,
            'sub_domains': ['a', 'b', 'c', 'd'],
            'url_template': 'https://{sub_domain}.tile.thunderforest.com/pioneer/{z}/{x}/{y}.png?apikey={api_key}',
            'attribution': '[i][ref=http://www.thunderforest.com/]Thunderforest[/ref][/i], [i][ref=https://www.openstreetmap.org/copyright">OpenStreetMap[/ref][/i] contributors'
        },
        'thunderforest-mobile-atlas': {
            'min_zoom': 0,
            'max_zoom': 22,
            'sub_domains': ['a', 'b', 'c', 'd'],
            'url_template': 'https://{sub_domain}.tile.thunderforest.com/mobile-atlas/{z}/{x}/{y}.png?apikey={api_key}',
            'attribution': '[i][ref=http://www.thunderforest.com/]Thunderforest[/ref][/i], [i][ref=https://www.openstreetmap.org/copyright">OpenStreetMap[/ref][/i] contributors'
        },
        'thunderforest-neighbourhood': {
            'min_zoom': 0,
            'max_zoom': 22,
            'sub_domains': ['a', 'b', 'c', 'd'],
            'url_template': 'https://{sub_domain}.tile.thunderforest.com/neighbourhood/{z}/{x}/{y}.png?apikey={api_key}',
            'attribution': '[i][ref=http://www.thunderforest.com/]Thunderforest[/ref][/i], [i][ref=https://www.openstreetmap.org/copyright">OpenStreetMap[/ref][/i] contributors'
        },
        'google-road': {
            'min_zoom': 0,
            'max_zoom': 19,
            'sub_domains': ['1', '2', '3'],
            'url_template': 'https://mt{sub_domain}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
            'attribution': 'Maps & Data [i][ref=https://www.google.com/maps]GoogleMaps[/ref][/i]'
        },
        'google-hybrid': {
            'min_zoom': 0,
            'max_zoom': 19,
            'sub_domains': ['1', '2', '3'],
            'url_template': 'https://mt{sub_domain}.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
            'attribution': 'Maps & Data [i][ref=https://www.google.com/maps]GoogleMaps[/ref][/i]'
        },
        'google-satellite': {
            'min_zoom': 0,
            'max_zoom': 19,
            'sub_domains': ['1', '2', '3'],
            'url_template': 'https://mt{sub_domain}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
            'attribution': 'Maps & Data [i][ref=https://www.google.com/maps]GoogleMaps[/ref][/i]'
        },
    }

    def __init__(self, provider: str = 'osm', tile_size: int = 256, api_key: str = None, cache_dir: str = 'map_cache'):
        self.sub_domains = self.providers[provider]['sub_domains'] if 'sub_domains' in self.providers[provider] else None
        self.attribution = self.providers[provider]['attribution']
        self.min_zoom = self.providers[provider]['min_zoom']
        self.max_zoom = self.providers[provider]['max_zoom']
        self.url = self.providers[provider]['url_template']
        self.api_key = api_key

        self.dp_tile_size = min(dp(tile_size), tile_size * 2)
        self.cache_fmt = '{cache_key}_{zoom}_{tile_x}_{tile_y}.png'
        self.tile_size = tile_size
        self.cache_dir = cache_dir
        self.cache_key = provider
        self.bounds = None

    def get_x(self, zoom, lon):
        '''Get the x position on the map using this map source's projection
        (0, 0) is located at the top left.
        '''
        lon = clamp(lon, -180.0, 180.0)
        return ((lon + 180.0) / 360.0 * pow(2.0, zoom)) * self.dp_tile_size

    def get_y(self, zoom, lat):
        '''Get the y position on the map using this map source's projection
        (0, 0) is located at the top left.
        '''
        lat = clamp(-lat, -90.0, 90.0)
        lat = lat * pi / 180.0
        return ((1.0 - log(tan(lat) + 1.0 / cos(lat)) / pi) / 2.0 * pow(2.0, zoom)) * self.dp_tile_size

    def get_lon(self, zoom, x):
        '''Get the longitude to the x position in the map source's projection.'''
        dx = x / float(self.dp_tile_size)
        lon = dx / pow(2.0, zoom) * 360.0 - 180.0
        return clamp(lon, -180.0, 180.0)

    def get_lat(self, zoom, y):
        '''Get the latitude to the y position in the map source's projection.'''
        dy = y / float(self.dp_tile_size)
        n = pi - 2 * pi * dy / pow(2.0, zoom)
        lat = -180.0 / pi * atan(0.5 * (exp(n) - exp(-n)))
        return clamp(lat, -90.0, 90.0)

    def get_row_count(self, zoom):
        '''Get the number of tiles in a row at this zoom level.'''
        if zoom == 0:
            return 1
        return 2 << (zoom - 1)

    def get_col_count(self, zoom):
        '''Get the number of tiles in a col at this zoom level.'''
        if zoom == 0:
            return 1
        return 2 << (zoom - 1)

    def get_min_zoom(self):
        '''Return the minimum zoom of this source.'''
        return self.min_zoom

    def get_max_zoom(self):
        '''Return the maximum zoom of this source.'''
        return self.max_zoom

    def fill_tile(self, tile):
        '''Add this tile to load within the downloader.'''

        if tile.state == 'done':
            return

        MapDownloader.instance(cache_dir=self.cache_dir).download_tile(tile)
