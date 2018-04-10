from pymongo import MongoClient
from pprint import pprint
import re

class Connection():
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client.aruta
        
    def serverStatus(self):
        serverStatusResult=self.db.command("serverStatus")
        pprint(serverStatusResult)
        
    def getall(self):
        return self.db.aruta_export.find({})
    
    def findPrepagata(self,p,s=None):
        if s:
            regex = re.compile("^"+s+"$",re.IGNORECASE);
            return self.db.aruta_export.find({'Prepagata':p,'StorageLevel':regex})
        
        return self.db.aruta_export.find({'Prepagata':p})
        
    
    def findUtente(self,p,s=None):
        if s:
            regex = re.compile("^"+s+"$", re.IGNORECASE);
            return self.db.aruta_export.find({'Utente':p,'StorageLevel':regex})
    
        return self.db.aruta_export.find({'Utente':p})
    
