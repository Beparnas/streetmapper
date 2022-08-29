from maps_directions import queryToPath,buildQuery_direct
from routes_db import route_getter,getDestinationm,getOrigin
from kml_tools import routes_to_kml

def route_mapper(mapfileName,filterData:dict[str,list[any]] = None):
    # collect data from route database, filtering if requested. 
    # filters must be equal to the label row text in the database.
    routeData = route_getter()
    for route in routeData:
        #get a point array of the route from google maps directions API
        routeQuery = buildQuery_direct( getOrigin(route,", Los Angeles CA"),
                                        getDestinationm(route,", Los Angeles CA"),
                                        "DRIVING")
        routePath = queryToPath(route,routeQuery)
        #shorten the path so it doesn't take up as much memory
        routepath_short = 
    # check that the map file name exists, and if it does, confirm overwritten