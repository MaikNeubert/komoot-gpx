import requests
import gpxpy
from html.parser import HTMLParser
from KomootParser import KomootParser
from KomootTypes import Coordinate, Route, WayPoint

class Komoot:

    def get_route(self, route_url):
        html = self.__request_route(route_url)
        parser = KomootParser()
        parser.feed(html)
        return parser.route

    
    def route_to_gpx(self, route: Route):
        gpx = gpxpy.gpx.GPX()

        track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(track)

        segment = gpxpy.gpx.GPXTrackSegment()
        track.segments.append(segment)

        for track_point in route.coordinates:
            segment.points.append(gpxpy.gpx.GPXTrackPoint(track_point.lat, track_point.lng, track_point.alt))
        
        return gpx.to_xml()


    def __request_route(self, route_url: str) -> str:
        r = requests.get(route_url)
        return r.text
    

if __name__ == "__main__":
    test = Komoot("https://www.komoot.de/tour/1337546037?ref=itd&share_token=ab4RrjzHVzsEGADQne9wr3dykdERCcSwsQ4iAhJCdat2sBm85i&ref=its")
