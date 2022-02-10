from typing import List, Optional, Dict, Any
from pydantic import BaseModel, validator


class Point:
    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon

    def __str__(self) -> str:
        return '({}, {})'.format(self.lat, self.lon)

class Area:
    def __init__(self, sw: Point, ne: Point):
        self.southwest_lat = sw.lat
        self.southwest_lon = sw.lon
        self.northeast_lat = ne.lat
        self.northeast_lon = ne.lon

    def __str__(self) -> str:
        """Allows to unpack data this way: *area"""
        return '{}, {}, {}, {}'.format(self.southwest_lat, self.southwest_lon,
                                       self.northeast_lat, self.northeast_lon)

    def __iter__(self):
        return (coord for coord in (self.southwest_lat, self.southwest_lon,
                                    self.northeast_lat, self.northeast_lon))