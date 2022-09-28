from __future__ import print_function
import glob
from datetime import date
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


class GC_util:
    _SCOPES:str
    creds:Credentials
    def __init__(self) -> None:
        self._SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        self.getCreds()
   
    def getCreds(self):
        #mostly from https://developers.google.com/sheets/api/quickstart/python
        

        #authenticate with google and connect to database spreadsheet
        #do we have credentials?
        cs = glob.glob("client_secret_*.json")
        token_file = glob.glob("token.json")
        creds = None
        if len(cs) == 0:
            print("no api key! you should make one")
            raise RuntimeError("DB: gsheet: no key")
        elif len(cs) > 1:
            print("multiple api keys! deal with this somehow")
            raise RuntimeError("DB: gsheet: too many keys")
        else:
            cs = cs[0]
        if len(token_file) > 0 :
            token_file = token_file[0]
            creds = Credentials.from_authorized_user_file(token_file)
        if not creds or not creds.valid:
            if creds and (creds.expired or creds.refresh_token):
                creds.refresh(Request())
            else:
                print("generating token from api key...")
                flow = InstalledAppFlow.from_client_secrets_file(cs,self._SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json','w') as token:
                token.write(creds.to_json())
        self.creds = creds