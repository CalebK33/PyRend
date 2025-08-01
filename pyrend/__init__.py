from . import overlay
from . import sound
from . import input
from . import files

__version__ = "0.1.0"
__author__  = "Caleb Keenan <caleb.keenan145@gmail.com>"
__license__ = "MIT"

__all__ = [
    "overlay",
    "input",
    "sound",
    "files"
]

def init():
    overlay.init()
def start(update_loop):
    overlay.start(update_loop)
def close():
    overlay.close()

def pixel_to_rel(x=None, y=None):
    rect = overlay._overlay.rect()
    center_x = rect.center().x()
    center_y = rect.center().y()

    if x is not None and y is not None:
        rel_x = (x - center_x) / (rect.width() / 2)
        rel_y = -(y - center_y) / (rect.height() / 2)
        return (rel_x, rel_y)

    elif y is not None:
        rel_y = -(y - center_y) / (rect.height() / 2)
        return rel_y

    elif x is not None:
        rel_x = (x - center_x) / (rect.width() / 2)
        return rel_x

def p2r(x=None, y=None):
    rect = overlay._overlay.rect()
    center_x = rect.center().x()
    center_y = rect.center().y()

    if x is not None and y is not None:
        rel_x = (x - center_x) / (rect.width() / 2)
        rel_y = -(y - center_y) / (rect.height() / 2)
        return (rel_x, rel_y)

    elif y is not None:
        rel_y = -(y - center_y) / (rect.height() / 2)
        return rel_y

    elif x is not None:
        rel_x = (x - center_x) / (rect.width() / 2)
        return rel_x

def rel_to_pixel(rel_x=None, rel_y=None):
    rect = overlay._overlay.rect()
    center_x = rect.center().x()
    center_y = rect.center().y()

    if rel_x is not None and rel_y is not None:
        x = center_x + rel_x * (rect.width() / 2)
        y = center_y - rel_y * (rect.height() / 2)
        return (int(x), int(y))

    elif rel_x is not None:
        x = center_x + rel_x * (rect.width() / 2)
        return int(x)

    elif rel_y is not None:
        y = center_y - rel_y * (rect.height() / 2)
        return int(y)

    return None

def r2p(rel_x=None, rel_y=None):
    rect = overlay._overlay.rect()
    center_x = rect.center().x()
    center_y = rect.center().y()

    if rel_x is not None and rel_y is not None:
        x = center_x + rel_x * (rect.width() / 2)
        y = center_y - rel_y * (rect.height() / 2)
        return (int(x), int(y))

    elif rel_x is not None:
        x = center_x + rel_x * (rect.width() / 2)
        return int(x)

    elif rel_y is not None:
        y = center_y - rel_y * (rect.height() / 2)
        return int(y)

    return None

def hex(hex) -> tuple:
    try:
        h = hex.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    except ValueError:
        print("PyRend error: Couldn't convert hex value to RGB. Please ensure you are giving a colour in the form of '#6E29E5'")
    except TypeError:
        print(f"PyRend error: Expected a string value in format '#FFFFFF' but instead got type {type(hex)}")
    except AttributeError:
        print(f"PyRend error: Expected a string value in format '#FFFFFF' but instead got type {type(hex)}")
