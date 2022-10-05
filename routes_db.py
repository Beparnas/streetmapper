from cgitb import handler
from copy import deepcopy
import copy
from math import exp
from GC_util import GC_util

from googleapiclient.discovery import build
from googleapiclient.discovery import Resource
from googleapiclient.errors import HttpError
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
        self.count = 0
        #acquire full dataset
        raw_db = {}
        if db_type == "google sheet":
            
            self.sheetName = "Testing"
            self.cred_handler = None
            self.service:Resource = build("sheets","v4",credentials=self.cred_handler.creds)

            try:                    
                self.sheet_ID = connectionParams['sheetID']
                if 'cred_handler' not in connectionParams:      
                    self.cred_handler = GC_util()
                else:
                    self.cred_handler = connectionParams['cred_handler']
                print("Connecting to Google Database...")
                raw_db = self.loadDB_gsheet(self.sheet_ID,
                                            filteritems)['values']
            except NameError:
                print("google sheet: spreadsheet name required!")
        else:
            raise RuntimeError("only google sheet supported currently")


        self.buildDB(prim_key,raw_db)
    
    def buildDB(self,prim_key,raw_data):
        #confirm primary key exists
        p_idx = 0 
        if prim_key not in raw_data[0]:
            raise RuntimeError(" in Database: primary key {} not found.".format(prim_key)) 
        else:
            p_idx = raw_data[0].index(prim_key)
        
        #create data entries
        self.rawFields:list = raw_data[0]
        fields = copy(self.rawFields)
        fields.remove(prim_key)
        #track the db entry row
        fields.append("row number")
        #TODO: pare down options based on any filters
        keys:list = []
        data:list[dict[str:any]] = []
        temp_data:dict[str:any] = {}
        for row in raw_data[1:]:
            
            key = row[p_idx]
            if key == "":# empty row
                continue
            row.pop(p_idx)
            row.append(copy(self.count)+1) #row number
            temp_data = {}
            #pad  rows to length of headers with emptry strings
            for i in range(0,len(fields)):
                try:
                    temp_data[fields[i]] = row[i]
                except IndexError:
                    temp_data[fields[i]] = ""
            
            data.append(temp_data)
            keys.append(key)
            self.count+=1

        self.data = dict(zip(keys,data))
    
   
    def loadDB_gsheet(self,filteritems):
           
        if self.cred_handler is not None:
            try:

                sheet = self.service.spreadsheets()
                result = sheet.values().get(spreadsheetId=self.sheetID,
                                            range=self.sheetName+"!A1:Z",
                                            majorDimension="ROWS")\
                                        .execute()
            except HttpError as err:
                print(err)
        return result
    def updatefield(self,routes,field):
        pass
        
    def getOrigin(self,route,clarifyingSuffix:str):
        street:str = self.data[route]["Street"]
        cross:str = self.data[route]["From"]
        origin = getAddrFromCrossSts(street,cross,clarifyingSuffix)
        return origin
    def getDestination(self,route,clarifyingSuffix:str):
        street:str = self.data[route]["Street"]
        cross:str = self.data[route]["To"]
        dest = getAddrFromCrossSts(street,cross,clarifyingSuffix)
        return dest

def getAddrFromCrossSts(street,cross,suffix=None):
    #generates an address string given the route data from the database. 
    # takes in a suffix to clarify the location 
    AddrStr:str = street + " & " + cross + suffix

    return AddrStr
def A1fromRC(r,c,r_end = None,c_end = None):
    start:str
    end:str
    iterable:list = [c]
    if r_end is not None and c_end is not None:
        iterable.append(c_end)
    for c in iterable:    
        result:str = ''
        while c > 0:
            
            n = 1
            #find the highest letter needed
            while c // pow(26,n) > 0:
                n +=1
            if n >1:
                partial = c // pow(26,n-1)+1
            else:
                partial = c // pow(26,n-1)

            result += chr(ord("@")+partial)
            c -= partial*pow(26,n-1)
        result += str(r)
    return result