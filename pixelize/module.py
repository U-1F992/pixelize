import numpy as np
from PIL import Image
from PIL.Image import Image as PIL_Image


def _is_even(num: int):
    return num % 2 == 0


def _is_odd(num: int):
    return not _is_even(num)


_RGBA = tuple[int, int, int, int]

_BOTH = " "
_UPPER = "\u2580"
_LOWER = "\u2584"

_ESC = "\033"
_RESET_COLOR = f"{_ESC}[0m"


def _COLOR(r: int, g: int, b: int, a: int):
    return f"{_ESC}[38;2;{r};{g};{b}m"


def _BACKGROUND_COLOR(r: int, g: int, b: int, a: int):
    return f"{_ESC}[48;2;{r};{g};{b}m"


def _is_transparent(rgba: _RGBA):
    return rgba[3] == 0


def _convert_to_ascii(upper: _RGBA, lower: _RGBA):
    if _is_transparent(upper):
        buf = _COLOR(*lower) + _LOWER
    elif _is_transparent(lower):
        buf = _COLOR(*upper) + _UPPER
    else:
        buf = _BACKGROUND_COLOR(*lower) + _COLOR(*upper) + _UPPER

    buf += _RESET_COLOR
    return buf


def _convert_to_even_height_rgba(image: PIL_Image):
    """
    Change height to even if odd, and align color to RGBA.
    """
    if _is_odd(image.height):
        rgba = Image.new("RGBA", (image.width, image.height + 1))
        rgba.alpha_composite(image)
    else:
        rgba = image.convert("RGBA")
    return rgba


def _combine_rows(image: PIL_Image):
    """
    Combine two rows into one line.
    """
    tmp: list[list[_RGBA]] = np.array(image).tolist()
    return [
        zip(row, tmp[index + 1])
        for index, row in enumerate(tmp)
        if _is_even(index)
    ]


def pixelize(image: PIL_Image):
    combined = _combine_rows(_convert_to_even_height_rgba(image))

    return "".join([
        "".join([
            _convert_to_ascii(*pixel_x2)
            for pixel_x2 in row
        ]) + "\n"
        for row in combined
    ])[:-1]
