from datetime import datetime
import json
import googlemaps
from googlemaps.client import Client
from googlemaps.convert import decode_polyline,encode_polyline
# https://github.com/googlemaps/google-maps-services-python
# https://developers.google.com/maps/documentation/directions/
class MapsAsker():
    gmaps:Client
    queries:list[str]
    querycount:int
    def __init__(self,creds) -> None:
        #load api key from file
        key:str
        service:str = "googleMaps"
        try:
            with open("keys.json","r") as f:
                key = json.load(f)[service]
        except KeyError:
            raise RuntimeError("MapsAsker: keys file is missing API key for '{}', or has the wrong name").format(service)
        except FileNotFoundError:
            raise RuntimeError("you must create an API key to run this! see the ReadMe for details")
        self.gmaps = Client(key=key)

    def queryToDirections(self,qFrom:str,qTo:str,mode:str,departureTime = None):
        if departureTime is None:
            departureTime = datetime.now()
        return self.gmaps.directions(qFrom,
                                     qTo,
                                     mode=mode,
                                     departure_time=departureTime)
    #Path tools
    #algorithm defined https://developers.google.com/maps/documentation/utilities/polylinealgorithm
    def encodePath(self,points:list[tuple]):
        return encode_polyline(points=points)
    def decodePath(self,path_encoded):
        return decode_polyline(path_encoded)
    def queryToPath(self,qFrom,qTo,dt=None):
        dirObj = self.queryToDirections(qFrom,qTo,dt)
        #save the query
        self.queries.append(dirObj[0])
        self.querycount+=1
        path = dirObj[0]['overview_polyline']['points']
        return path
   