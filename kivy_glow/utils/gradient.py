__all__ = ('LinearGradient', 'RadialGradient')

from kivy.graphics.texture import Texture
from kivy.utils import get_color_from_hex
import math


def _compute_max_distance(size, angle):
    rad = math.radians(angle % 360)

    size -= 1

    x1, y1 = size / 2, (size / 2) * math.tan(rad)
    x2, y2 = -size / 2, -(size / 2) * math.tan(rad)

    if abs(y1) > size / 2:
        y1 = size / 2 if y1 > 0 else -size / 2
        x1 = y1 / math.tan(rad)
    if abs(y2) > size / 2:
        y2 = size / 2 if y2 > 0 else -size / 2
        x2 = y2 / math.tan(rad)

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def _format_colors(colors):
    formatted_colors = []
    for color in colors:
        if isinstance(color, str):
            formatted_colors.append(get_color_from_hex(color))
        elif isinstance(color, (tuple, list)):
            if len(color) == 3:
                formatted_colors.append((color[0], color[1], color[2], 1))
            elif len(color) == 4:
                formatted_colors.append(tuple(color))

    return formatted_colors


def LinearGradient(colors: list, angle: int = 0, stops: dict = {}, size: tuple = (100, 100), crop_factor: float = 8.0):
    cropped_size = max(int(size[0] // crop_factor), int(size[1] // crop_factor))
    max_dist = _compute_max_distance(cropped_size, angle)
    texture = Texture.create(size=(cropped_size, cropped_size), colorfmt='rgba')
    buf = []

    angle = angle % 360
    rad = math.radians(angle)
    cos_angle = math.cos(rad)
    sin_angle = math.sin(rad)

    if not len(colors):
        return texture

    colors = _format_colors(colors)
    formatted_stops = {}
    for key in range(len(colors)):
        if key in stops.keys():
            formatted_stops[key] = stops[key]
        else:
            formatted_stops[key] = key / (len(colors) - 1)

    for y in range(cropped_size):
        for x in range(cropped_size):
            u = (x * cos_angle + y * sin_angle) / max_dist

            if 90 < angle < 180:
                u += .5
            elif 180 <= angle <= 270:
                u += 1
            elif 270 < angle < 360:
                u += .5

            stop_index = int(u * (len(colors) - 1))
            next_stop_index = min(stop_index + 1, len(colors) - 1)

            stop_value = formatted_stops[stop_index]
            next_stop_value = formatted_stops[next_stop_index]

            if stop_value == next_stop_value:
                color = colors[stop_index]
            else:
                t = (u - stop_value) / (next_stop_value - stop_value)
                color1 = colors[stop_index]
                color2 = colors[next_stop_index]
                color = [max(0, min(1, color1[j] * (1 - t) + color2[j] * t)) for j in range(4)]
            buf.extend(int(c * 255) for c in color)

    buf = bytes(buf)
    texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
    return texture


def RadialGradient(colors: list, center: tuple = (.5, .5), stops: dict = {}, size: tuple = (100, 100), crop_factor: float = 8.0):
    cropped_size = max(int(size[0] // crop_factor), int(size[1] // crop_factor))
    texture = Texture.create(size=(cropped_size, cropped_size), colorfmt='rgba')
    center_x, center_y = center[0] * size, center[1] * size
    max_radius = max(
        cropped_size - center_x,
        cropped_size - center_y,
        center_x,
        center_y,
    )
    buf = []

    if not len(colors):
        return texture

    colors = _format_colors(colors)
    formatted_stops = {}
    for key in range(len(colors)):
        if key in stops.keys():
            formatted_stops[key] = stops[key]
        else:
            formatted_stops[key] = key / (len(colors) - 1)

    for y in range(cropped_size):
        for x in range(cropped_size):
            u = math.hypot((x - center_x), (y - center_y)) / max_radius

            stop_index = int(u * (len(colors) - 1))
            next_stop_index = min(stop_index + 1, len(colors) - 1)

            stop_value = formatted_stops[stop_index]
            next_stop_value = formatted_stops[next_stop_index]

            if stop_value == next_stop_value:
                color = colors[stop_index]
            else:
                t = (u - stop_value) / (next_stop_value - stop_value)
                color1 = colors[stop_index]
                color2 = colors[next_stop_index]
                color = [max(0, min(1, color1[j] * (1 - t) + color2[j] * t)) for j in range(4)]
            buf.extend(int(c * 255) for c in color)

    buf = bytes(buf)
    texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
    return texture
