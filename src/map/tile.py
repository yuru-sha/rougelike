#!/usr/bin/env python3
from dataclasses import dataclass


@dataclass
class Tile:
    """
    A tile on a map. It may or may not be blocked, and may or may not block sight.
    """

    walkable: bool
    transparent: bool

    def __init__(self, walkable: bool, transparent: bool):
        self.walkable = walkable
        self.transparent = transparent


@dataclass
class Rectangle:
    """
    A rectangle on the map, used to characterize a room.
    """

    x: int
    y: int
    w: int
    h: int

    def __init__(self, x: int, y: int, w: int, h: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.x1 = x
        self.x2 = x + w
        self.y1 = y
        self.y2 = y + h

    @property
    def center(self) -> tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y

    def intersects(self, other: "Rectangle") -> bool:
        """Returns true if this rectangle intersects with another one."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )
