from __future__ import annotations
from typing import Optional, Tuple, List, Union
from random import randint


class Color:
    red = None
    green = None
    blue = None
    black = None
    white = None
    transparent = None

    def __init__(self, r: int, g: int, b: int, a: Optional[int] = 255):
        self.r, self.g, self.b, self.a = self.__color = Color.__clamp_color(r, g, b, a)

    @property
    def rgba(self) -> Tuple[int, int, int, int]:
        return self.__color

    @property
    def hex(self) -> str:
        return Color.to_hex(self)

    def __repr__(self):
        return repr(self.__color)

    def __str__(self):
        return str(self.__color)

    def __getitem__(self, item):
        return self.__color[item]

    @staticmethod
    def random(r_range: Optional[Union[Tuple[int, int], List[int, int]]] = (0, 255), 
               g_range: Optional[Union[Tuple[int, int], List[int, int]]] = (0, 255),
               b_range: Optional[Union[Tuple[int, int], List[int, int]]] = (0, 255),
               a_range: Optional[Union[Tuple[int, int], List[int, int]]] = (0, 255)):
        """Return A random RGBA Color clamped between each range"""

        r = randint(*r_range)
        g = randint(*g_range)
        b = randint(*b_range)
        a = randint(*a_range)

        return Color(r, g, b, a)

    @staticmethod
    def to_hex(color: Color) -> str:
        """Return a hex string representation of RGBA"""

        return '#{:02x}{:02x}{:02x}{:.02}'.format(color.r, color.g, color.b, max(min(color.a, 1), 0))

    @staticmethod
    def __clamp_color(r, g, b, a) -> Tuple[int, int, int, int]:
        """Get a new clamped RGBA with RGB between 0, 255 and A between 0, 1"""

        r = max(min(r, 255), 0)
        g = max(min(g, 255), 0)
        b = max(min(b, 255), 0)
        a = max(min(a, 255), 0)
        return r, g, b, a


# Setting up default colors
Color.red = Color(255, 0, 0)
Color.green = Color(0, 255, 0)
Color.blue = Color(0, 0, 255)
Color.black = Color(0, 0, 0)
Color.white = Color(255, 255, 255)
Color.transparent = Color(255, 255, 255, 0)
# TODO: Add more colors as needed!
