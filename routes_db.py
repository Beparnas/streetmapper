

class routeDB:
    count:int
    data:dict[str,dict[str:any]]
    def __init__(self,
                db_type:str = "google sheet",
                filteritems:dict[str,list[any]] = None,
                **connectionParams) -> None:
        self.db:dict[str,any] = {}
        
        if db_type == "google sheet":
            try:
                print("Authenticating and connecting to Google Database...")
                self.loadDB_gsheet(sheetName,filteritems)
            except NameError:
                print("google sheet: spreadsheet name required!")
    def loadDB_gsheet(filteritems):
        #mostly from https://developers.google.com/sheets/api/quickstart/python
        from __future__ import print_function

        import glob
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from googleapiclient.errors import HttpError

        SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

        #authenticate with google and connect to database spreadsheet
        #do we have credentials?
        keys = glob.glob("client_secret_*.json")
        if len(keys) == 0:
            print("no api key! deal with this somehow")
            raise RuntimeError("DB: gsheet: no key")
        elif len(keys) > 1:
            print("multiple api keys! deal with this somehow")
            raise RuntimeError("DB: gsheet: too many keys")
        creds = Credentials.from_authorized_user_file(keys[0])
        if not creds or not creds.valid:
            
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