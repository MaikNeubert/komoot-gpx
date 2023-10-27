import requests
import gpxpy
from gpxpy.gpx import GPXWaypoint
from html.parser import HTMLParser
from KomootParser import KomootParser
from KomootTypes import Coordinate, Route, WayPoint

class Forbidden(Exception):
    pass

class ServerError(Exception):
    pass


class Komoot:

    def get_route(self, route_url):
        html = self.__request_route(route_url)
        parser = KomootParser()
        parser.feed(html)
        return parser.route


    def route_to_gpx(self, route: Route):
        gpx = gpxpy.gpx.GPX()

        gpx.creator = route.creator
        gpx.name = route.name

        for waypoint in route.wayPoints:
            gpx.waypoints.append(
                GPXWaypoint(
                    waypoint.location.lat,
                    waypoint.location.lng,
                    waypoint.location.alt,
                    name=waypoint.name,
                    type=waypoint.type
                )
            )


        track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(track)

        segment = gpxpy.gpx.GPXTrackSegment()
        track.segments.append(segment)

        for track_point in route.coordinates:
            segment.points.append(gpxpy.gpx.GPXTrackPoint(track_point.lat, track_point.lng, track_point.alt))
        
        return gpx.to_xml()


    def __request_route(self, route_url: str) -> str:
        r = requests.get(route_url)
        if r.status_code == 403:
            raise Forbidden()
        if r.status_code != 200:
            raise ServerError(r.status_code, r.reason)
        return r.text
