from googlemaps import directions

def queryToDirections(query):
    pathObj:any
    return pathObj
def getPath(pathObj):
    path:any
    return path
def queryToPath(routeName,query):
    pathObj = queryToDirections(query)
    path:list[tuple[any]] = getPath(pathObj)
    return path
def buildQuery_direct(origin,destination,travelMode):
    #build up a maps API query 
    #optimized for a direct path 