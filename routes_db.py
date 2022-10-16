from cgitb import handler
from copy import deepcopy
import copy
from math import exp
from GC_util import GC_util
from A1fromRC import A1fromRC

from googleapiclient.discovery import build
from googleapiclient.discovery import Resource
from googleapiclient.errors import HttpError

# https://developers.google.com/sheets/api/quickstart/python
class routeDB:
    count:int
    data:dict[str,dict[str:any]]
    cred_handler:GC_util
    sheetName:str
    service: Resource #Google Sheets resource, used to access remote data
    count:int # number of entries
    rawFields:list[str] #the fields of the remote database, in order
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
                self.sheet = self.service.spreadsheets()
                raw_db = self.loadDB_gsheet(self.sheet_ID,
                                            filteritems)['values']
            except NameError:
                print("google sheet: spreadsheet name required!")
        else:
            raise RuntimeError("only google sheet supported currently")


        self.buildDB(prim_key,raw_db)
    
    def buildDB(self,prim_key,raw_data):
        """!
        Creates the structured database, based on the primary key
        and a 2D array of the dataset

        adds fields:
        - row number: the row within the db that the entry existed in
        @param prim_key string of the primary key - must be a header in the DB
        @param raw_data: list of lists, representing [R:[C:""]] data in the DB
        @return true if successful, exceptions otherwise
        """
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
        return True
    
   
    def loadDB_gsheet(self,filteritems):
           
        if self.cred_handler is not None:
            try:

                
                result = self.sheet.values().get(spreadsheetId=self.sheetID,
                                            range=self.sheetName+"!A1:Z",
                                            majorDimension="ROWS")\
                                        .execute()
            except HttpError as err:
                print(err)
        return result
    
    def updatefield_gsheet(self,routes:str|list[str],field):
        """!
        connect to the database, identify the routes to modifiy, and update the given field
        @param routes list of routes to update
        @param filed the field to change - identify it via self.rawFields
        @return True if successful, exceptions otherwise
        """
        if type(routes) == str:
            routes = [routes]
        if field not in self.rawFields:
            raise RuntimeError("requested field {} not in database!".format(field))
        for route in routes:
            cellStr =self.sheetName+"!"+A1fromRC(self.data[route]["row number"]+1,self.rawFields.index(field)+1)
            updateBody = {
                "range": cellStr,
                "majorDimension": "ROWS",
                "values": [[route[field]]]     
            }
            updateData:dict[any] =  self.sheet.values()\
                                    .update(spreasheetId = self.sheet_ID,
                                            range=cellStr,
                                            valueInputOption="RAW",
                                            body=updateBody
                                    )
        
        
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
