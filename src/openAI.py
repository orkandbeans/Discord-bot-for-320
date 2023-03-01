from db import db as database
from dalle import Dalle
from dotenv import load_dotenv
from chatGPT import chatGPT
import os



class openAI:
    def __init__(self):
        #self.APIkey = self.fetchAPI(serverID)
        load_dotenv()
        APIKEY = os.getenv('API_TOKEN')
        self.APIkey = APIKEY
        self.dalle = Dalle(self.APIkey)
        self.chatGPT = chatGPT(self.APIkey)

    #def fetchAPI(self, serverID):

    #def insertKey(self, APIkey, serverID):

    #def deleteKey(self, APIkey):
