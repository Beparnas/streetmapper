from threading import local
from maps_directions import queryToPath,buildQuery_direct
from routes_db import route_getter,getDestinationm,getOrigin
from kml_tools import routes_to_kml
import json

#database keys 
path_key = "path"

#constants
query_cost = 0.10

def route_mapper(mapfileName,
                 filterData:dict[str,list[any]] = None,
                 dbPath:str = 'streetmapper_db.json'
                ):
    # collect data from route database, filtering if requested. 
    # filters must be equal to the label row text in the database.
    
    routeData_remote:dict[dict[any]] = route_getter()
    #attempt to get the pre-run database, if it exists
    routeData_saved = None
    addRoutes:bool = False
    try:
        localDB = open(dbPath)
        routeData_saved = json.load(localDB)
        #determine how many google maps queries are needed
        count = 0
        for route in routeData_remote:
            if route not in routeData_saved:
                count+=1
        if count > 0: 
            print("{} new routes in remote database, request from google maps API?\n\
                    cost will be {:,.2f}".format(count,query_cost*count))
            addRoutes = input("Y or N:") == "Y"
    except (FileNotFoundError,json.decoder.JSONDecodeError) as e:
        print("no local database found, creating one...")
        routeData_saved:dict[dict[any]] = {}
    
    for route in routeData_remote:
        #get path from local database if it exists
        path:list[tuple] = []
        if route in routeData_saved.keys():
            print("{} in database")
            path = routeData_saved[route][path_key]
        elif addRoutes:    
            
            #get a point array of the route from google maps directions API
            routeQuery = buildQuery_direct( getOrigin(route,", Los Angeles CA"),
                                        getDestinationm(route,", Los Angeles CA"),
                                        "DRIVING")
            #get query from google maps API
            # https://github.com/googlemaps/google-maps-services-python
            # https://developers.google.com/maps/documentation/directions/
            #extract the path  from the query response
            routePath = queryToPath(route,routeQuery)
            #shorten the path so it doesn't take up as much memory
            #store in the local database
        else:
            print("skipping route ")
            continue
        #save route to the local database
    #build a kml file from the local route database 
    # overwrite database
    