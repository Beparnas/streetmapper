

def route_getter(filteritems:dict[str,list[any]]):
    names:any # assigned key 'x&y to x&z'
    data:dict[str,any]
    routes = dict(zip(names,data))
    return routes 
def getOrigin(route,clarifyingSuffix:str):
    street:str
    cross:str
    origin = getAddrFromCrossSts(street,cross,clarifyingSuffix)
    return origin
def getDestination(route,clarifyingSuffix:str):
    street:str
    cross:str
    dest = getAddrFromCrossSts(street,cross,clarifyingSuffix)
    return dest

def getAddrFromCrossSts(street,cross,suffix=None):
    #generates an address string given the route data from the database. 
    # takes in a suffix to clarify the location 
    AddrStr:str

    return AddrStr