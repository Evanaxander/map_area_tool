"""
geometry.py - Area, perimeter, bounding box calculations
All pixel-space math lives here. Unit conversion is separate.
"""

import math
from typing import List, Tuple


Point = Tuple[float, float]


def polygon_area_pixels(points: List[Point]) -> float:
    """Shoelace formula. Returns area in px²."""
    n = len(points)
    if n < 3:
        return 0.0
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += points[i][0] * points[j][1]
        area -= points[j][0] * points[i][1]
    return abs(area) / 2.0


def perimeter_pixels(points: List[Point]) -> float:
    """Total perimeter of a closed polygon in px."""
    n = len(points)
    if n < 2:
        return 0.0
    total = 0.0
    for i in range(n):
        j = (i + 1) % n
        dx = points[j][0] - points[i][0]
        dy = points[j][1] - points[i][1]
        total += math.sqrt(dx * dx + dy * dy)
    return total


def bounding_box_pixels(points: List[Point]) -> Tuple[float, float, float, float]:
    """Returns (min_x, min_y, width_px, height_px)."""
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)


def distance_pixels(p1: Point, p2: Point) -> float:
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return math.sqrt(dx * dx + dy * dy)


# ── Unit conversions ──────────────────────────────────────────

def pixels_to_meters(px: float, scale_px_per_m: float) -> float:
    return px / scale_px_per_m


def area_px_to_unit(area_px2: float, scale_px_per_m: float, unit: str) -> float:
    area_m2 = area_px2 / (scale_px_per_m ** 2)
    conversions = {
        "m²":   1.0,
        "ft²":  10.7639,
        "yd²":  1.19599,
        "km²":  1e-6,
        "acre": 0.000247105,
    }
    return area_m2 * conversions.get(unit, 1.0)


def length_px_to_unit(length_px: float, scale_px_per_m: float, unit: str) -> float:
    length_m = length_px / scale_px_per_m
    # Use appropriate length unit for each area unit
    length_conversions = {
        "m²":   ("m",  1.0),
        "ft²":  ("ft", 3.28084),
        "yd²":  ("yd", 1.09361),
        "km²":  ("km", 0.001),
        "acre": ("m",  1.0),
    }
    factor = length_conversions.get(unit, ("m", 1.0))[1]
    return length_m * factor


def length_unit_label(unit: str) -> str:
    mapping = {
        "m²":   "m",
        "ft²":  "ft",
        "yd²":  "yd",
        "km²":  "km",
        "acre": "m",
    }
    return mapping.get(unit, "m")
