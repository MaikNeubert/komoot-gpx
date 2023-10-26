from html.parser import HTMLParser
from KomootTypes import Coordinate, Route, WayPoint
from typing import List
import re, json, ast

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
        
        unescapedRoute = ast.literal_eval(f"'{route[0]}'")
        routeData = json.loads(unescapedRoute)
        self.route = self.__map_route(routeData)            


    def __map_route(self, routeData) -> Route:
        coordinates = self.__map_coordinates(routeData)      
        wayPoints = self.__map_way_points(routeData)
        creator = routeData["page"]["_embedded"]["tour"]["_embedded"]["creator"]["display_name"]
        creatorLink = routeData["page"]["_embedded"]["tour"]["_embedded"]["creator"]["_links"]["self"]["href"]

        return Route(coordinates, creator, creatorLink, wayPoints)
    
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
                alt = wayPoint["_embedded"]["reference"]["location"]
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
