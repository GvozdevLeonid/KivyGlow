__all__ = ('MapDownloader', )

import traceback
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)
from os import makedirs
from os.path import exists
from random import choice
from time import time
from typing import (
    Callable,
    Self,
)

import requests
from kivy.clock import Clock
from kivy.logger import Logger

from .map import Tile

USER_AGENT = 'kivy-glow.map'


class MapDownloader:
    _instance = None
    MAX_WORKERS = 5
    CAP_TIME = 0.064  # 15 FPS

    @staticmethod
    def instance(cache_dir: str = 'map_cache') -> Self:
        if MapDownloader._instance is None:
            MapDownloader._instance = MapDownloader(cache_dir=cache_dir)
        return MapDownloader._instance

    def __init__(self, max_workers: int | None = None, cap_time: float | None = None, cache_dir: str = 'map_cache') -> None:
        if max_workers is None:
            max_workers = MapDownloader.MAX_WORKERS
        if cap_time is None:
            cap_time = MapDownloader.CAP_TIME

        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.cache_dir = cache_dir
        self.cap_time = cap_time
        self.is_paused = False
        self._futures = []

        Clock.schedule_interval(self._check_executor, 1 / 60.0)
        if not exists(self.cache_dir):
            makedirs(self.cache_dir)

    def submit(self, f: Callable, *args, **kwargs) -> None:
        future = self.executor.submit(f, *args, **kwargs)
        self._futures.append(future)

    def download_tile(self, tile: Tile) -> None:
        Logger.debug(
            f'Downloader: queue(tile) zoom={tile.zoom} x={tile.tile_x} y={tile.tile_y}',
        )
        future = self.executor.submit(self._load_tile, tile)
        self._futures.append(future)

    def download(self, url: str, callback: Callable, **kwargs) -> None:
        Logger.debug(f'Downloader: queue(url) {url}')
        future = self.executor.submit(self._download_url, url, callback, kwargs)
        self._futures.append(future)

    def _download_url(self, url: str, callback: Callable, **kwargs) -> None:
        Logger.debug(f'Downloader: download(url) {url}')
        response = requests.get(url, **kwargs, timeout=100)
        response.raise_for_status()
        return callback, (url, response)

    def _load_tile(self, tile: Tile) -> None:
        if tile.state == 'done':
            return None

        cache_fn = tile.cache_fn
        if exists(cache_fn):
            Logger.debug(f'Downloader: use cache {cache_fn}')
            return tile.set_source, (cache_fn, )

        tile_y = tile.map_source.get_row_count(tile.zoom) - tile.tile_y - 1

        url = tile.map_source.url.format(
            z=tile.zoom,
            x=tile.tile_x,
            y=tile_y,
            sub_domain='{sub_domain}',
            api_key='{api_key}',
        )
        if tile.map_source.sub_domains is not None:
            url = url.format(sub_domain=choice(tile.map_source.sub_domains), api_key='{api_key}')
        if tile.map_source.api_key is not None:
            url = url.format(api_key=tile.map_source.api_key)

        Logger.debug(f'Downloader: download(tile) {url}')
        try:

            response = requests.get(url, headers={'User-agent': USER_AGENT}, timeout=5)
            response.raise_for_status()
            data = response.content

            with open(cache_fn, 'wb') as fd:
                fd.write(data)

            Logger.debug(f'MapDownloaded {len(data)} bytes: {url}')

            return tile.set_source, (cache_fn, )

        except Exception as e:
            Logger.error(f'MapDownloader error: {e!r}')

    def _check_executor(self, *args) -> None:
        start = time()
        try:
            for future in as_completed(self._futures[:], 0):
                self._futures.remove(future)
                try:
                    result = future.result()
                except Exception:
                    traceback.print_exc()
                    continue

                if result is None:
                    continue

                callback, args = result
                callback(*args)

                if time() - start > self.cap_time:
                    break
        except TimeoutError:
            pass
