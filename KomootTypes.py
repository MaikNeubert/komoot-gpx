from typing import List


class Coordinate:
    def __init__(self, lat, lng, alt, t = None):
        self.lat = lat
        self.lng = lng
        self.alt = alt
        self.t = t


class WayPoint:
    def __init__(self, type: str, index: int, name: str, location: List[Coordinate]):
        self.type = type
        self.index = index
        self.name = name
        self.location = location


class Route:
    def __init__(self, coordinates: List[Coordinate], creator: str, creatorLink: str, wayPoints: List[WayPoint]):
        self.coordinates = coordinates
        self.creator = creator
        self.creatorLink = creatorLink
        self.wayPoints = wayPoints
