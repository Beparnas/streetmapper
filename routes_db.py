from cgitb import handler
from copy import deepcopy
from GC_util import GC_util
class routeDB:
    count:int
    data:dict[str,dict[str:any]]
    cred_handler:GC_util
    def __init__(self,
                prim_key:str,
                db_type:str = "google sheet",
                filteritems:dict[str,list[any]] = None,
                **connectionParams) -> None:
        self.db:dict[str,any] = {}
        #acquire full dataset
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
        
        #confirm primary key exists
        p_idx = 0 #index
        if prim_key not in self.data['values'][0]:
            raise RuntimeError(" in Database: primary key {} not found.".format(prim_key)) 
        else:
            p_idx = self.data['values'][0].index(prim_key)
        
        #create data entries
        fields:list = self.data['values'][0]
        fields.remove(prim_key)
        #TODO: pare down options based on any filters
        keys:list = []
        data:list[dict[str:any]] = []
        temp_data:dict[str:any] = {}
        for row in self.data['values'][1:]:
            
            key = row[p_idx]
            row.pop(p_idx)
            temp_data = {}
            for i in range(0,len(row)):
                temp_data[fields[i]] = row[i]
            data.append(temp_data)
            keys.append(key)
            self.count+=1

        self.data = dict(zip(keys,data))
        
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
                result = sheet.values().get(spreadsheetId=sheetID,range="Main!A1:Z",majorDimension="ROWS"	
).execute()
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