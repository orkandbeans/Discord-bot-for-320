from db import db as database
from dalle import Dalle
from dotenv import load_dotenv
from chatGPT import chatGPT
import os

class openAI:
    def __init__(self):
        load_dotenv()
        self.dalle = Dalle()
        self.chatGPT = chatGPT()

        createCommand = "CREATE TABLE IF NOT EXISTS api(serverID INTEGER PRIMARY KEY, apiKey TEXT)"
        database.execute(createCommand)
        database.commit()

    def fetchAPI(self, serverID):
        return database.record('SELECT apiKey FROM api WHERE serverID=?', str(serverID))

    def insertKey(self, APIkey, serverID):
        insertCommand = f"INSERT INTO api VALUES ({serverID}, \"{APIkey}\")"
        database.execute(insertCommand)
        database.commit()

    def removeKey(self, serverID):
        deleteCommand = f"DELETE FROM api WHERE serverID={serverID}"
        database.execute(deleteCommand)
        database.commit()

    def superRemoveKey(self, APIkey):
        deleteCommand = f"DELETE FROM api WHERE apiKey={APIkey}"
        database.execute(deleteCommand)
        database.commit()
