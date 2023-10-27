from html.parser import HTMLParser
from KomootTypes import Coordinate, Route, WayPoint
from typing import List
import re, json, ast

class ParserException(Exception):
    pass

class KomootParser(HTMLParser):
    _last_starttag = ""
    route = None

    def handle_starttag(self, tag, attrs):
        self._last_starttag = tag

    def handle_endtag(self, tag):
        self._last_endtag = tag

    def handle_data(self, data):
        if self._last_starttag != "script":
            return

        x = re.search(r"kmtBoot\.setProps\(.{1,}\)", data)

        if x == None:
            return
        
        route = re.findall(r"\{.{1,}\}", data)

        if len(route) == 0:
            return
        
        t = f'{{"route": "{route[0]}" }}'
        t = json.loads(t)
        routeData = json.loads(t["route"])

        self.route = self.__map_route(routeData)            


    def __map_route(self, routeData) -> Route:
        coordinates = self.__map_coordinates(routeData)      
        wayPoints = self.__map_way_points(routeData)

        creator = "unknown"
        creatorLink = ""
        if "creator" in routeData["page"]["_embedded"]["tour"]["_embedded"]:
            if "display_name" in routeData["page"]["_embedded"]["tour"]["_embedded"]["creator"]:
                creator = routeData["page"]["_embedded"]["tour"]["_embedded"]["creator"]["display_name"]
            
            if "_links" in routeData["page"]["_embedded"]["tour"]["_embedded"]["creator"]:
                creatorLink = routeData["page"]["_embedded"]["tour"]["_embedded"]["creator"]["_links"]["self"]["href"]

        sport = "unknown"
        if "sport" in routeData["page"]["_embedded"]["tour"]:
            sport = routeData["page"]["_embedded"]["tour"]["sport"]
        
        name = "unknown"
        if "name" in routeData["page"]["_embedded"]["tour"]:
            name = routeData["page"]["_embedded"]["tour"]["name"]

        return Route(coordinates, creator, creatorLink, wayPoints, name, sport)
    
    def __map_coordinates(self, routeData) -> List[Coordinate]:
        coordinates = []
        for coordinate in routeData["page"]["_embedded"]["tour"]["_embedded"]["coordinates"]["items"]:
            coordinates.append(Coordinate(coordinate["lat"], coordinate["lng"], coordinate["alt"], coordinate["t"]))
        
        return coordinates


    def __map_way_points(self, routeData) -> List[WayPoint]:
        wayPoints = []
        for wayPoint in routeData["page"]["_embedded"]["tour"]["_embedded"]["way_points"]["_embedded"]["items"]:
            if "name" in wayPoint["_embedded"]["reference"]:
                name = wayPoint["_embedded"]["reference"]["name"]
            else:
                name = None

            if "alt" in wayPoint["_embedded"]["reference"]["location"]:
                alt = wayPoint["_embedded"]["reference"]["location"]["alt"]
            else:
                alt = None

            wayPoints.append(
                WayPoint(
                    wayPoint["type"],
                    wayPoint["index"],
                    name,
                    Coordinate(
                        wayPoint["_embedded"]["reference"]["location"]["lat"],
                        wayPoint["_embedded"]["reference"]["location"]["lng"],
                        alt
                    ),
                )
            )
        
        return wayPoints
