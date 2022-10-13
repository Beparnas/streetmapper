from simplekml import Kml
from routes_db import routeDB
from streetmapper_utils import *
from datetime import datetime

# reference:
# https://simplekml.readthedocs.io/en/latest/


def routes_to_kml(routeNames:list[str],db:routeDB):
    docName = "streetmapper_" + datetime.now().strftime("%m-%d-%Y_%H_%M_%S")+".kml"
    root:Kml = Kml()
    root.document.name = docName
    for name in routeNames:
        root.newlinestring(name=name,coords=db.data[name][pathData_key])
    root.save(docName)
    return docName


def trimRoute(routeData):
    #remove unnecessary data from a route
    routeData_trimmed:any
    return routeData_trimmed