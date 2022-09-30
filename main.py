
from maps_directions import MapsAsker
from routes_db import routeDB
from GC_util import GC_util
from kml_tools import routes_to_kml
import json

#database keys 
route_key = "auto-generated google maps link"
path_key = "path data compressed"
pathData_key = "path data decoded"
#constants
query_cost = 0.10

def main(filterData = None):
    #get google credentials
    cred_handler = GC_util()
    #TODO: log properly
    #TODO: handle filters
    #TODO: set file name
    #run route mapper
    route_mapper(cred_handler)

def route_mapper(cred_handler,
                 filterData:dict[str,list[any]] = None,
                 dbPath:str = 'streetmapper_db.json',
                ):
    
    #TODO: handle .csv Database
    print("collecting from database...")
    # collect data from route database, filtering if requested. 
    # filters must be equal to the label row text in the database.
    db = routeDB(   route_key,
                    sheetID="1AtQY7oARVJT0JUjudXbc8jFvdIySWZUbK1LTWyAmIfY",
                    cred_handler=cred_handler)
    #TODO: print info if filtered
    print("got {} route(s)".format(db.count))
    # collect all routes to be queried to get the path.
    # routes with pre-queried paths are skipped
    runQueries:bool = False
    query_list = []
    for route in db.data:
        if len(db.data[route][path_key])==0:
            query_list.append(route)
    count = len(query_list)
    print("Alert! {} new routes found in database, request from google maps API?\n\
                    cost will be ${:,.2f}".format(count,query_cost*count))
    map_asker = None
    if input("Y or N:") == "Y":
        runQueries = True
        map_asker = MapsAsker(cred_handler.creds)
    
    # go through all routes
    # and either pull their path, or generate one (if doing so) 

    for route in db.data:
        #get path from local database if it exists
        path:list[tuple] = []
        if route in query_list and runQueries:            
            #get path from google maps API
            path = map_asker.queryToPath(qFrom= db.getOrigin(route,", Los Angeles CA"),
                                                             qTo=db.getDestination(route,", Los Angeles CA"),
                                    )
            db.data[route][path_key] = path
            print("queried {}".format(route))
        else:
            print("skipped {}".format(route))
        # expand out the path and store it 
        db.data[route][]
    #build a kml file from the local route database 
    # overwrite database

if __name__ == "__main__":
    main()