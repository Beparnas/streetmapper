from cgitb import handler
from GC_util import GC_util
class routeDB:
    count:int
    data:dict[str,dict[str:any]]
    cred_handler:GC_util
    def __init__(self,
                db_type:str = "google sheet",
                filteritems:dict[str,list[any]] = None,
                **connectionParams) -> None:
        self.db:dict[str,any] = {}
        
        if db_type == "google sheet":
            self.cred_handler = None
            try:                    
                if 'cred_handler' not in connectionParams:      
                    self.cred_handler = GC_util()
                else:
                    self.cred_handler = connectionParams['cred_handler']
                print("Connecting to Google Database...")
                self.loadDB_gsheet( connectionParams['sheetID'],
                                    filteritems)
            except NameError:
                print("google sheet: spreadsheet name required!")
        routes = dict(zip(names,data))
        return routes 
    def loadDB_gsheet(self,sheetID,filteritems):
        from googleapiclient.discovery import build
        from googleapiclient.discovery import Resource
        from googleapiclient.errors import HttpError
        if self.cred_handler is not None:
            try:
                service:Resource = build("sheets","v4",credentials=self.cred_handler.creds)
                # sheet_data = service.spreadsheets().get(spreadsheetId=sheetID).execute()
                # sheetsList = sheet_data.get("sheets","")
                sheet = service.spreadsheets()
                result = sheet.values().get(spreadsheetId=sheetID,range="Main!A1:Z").execute()
            except HttpError as err:
                print(err)
        self.data = result
        return
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