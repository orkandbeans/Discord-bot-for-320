import requests
from datetime import datetime
from db import db as database

createCommand = "CREATE TABLE IF NOT EXISTS giveaway(serverID INTEGER PRIMARY KEY, channelID TEXT)"
database.execute(createCommand)
database.commit()

def setGiveaway(serverID, channelID):
    insertCommand = f"INSERT OR IGNORE INTO giveaway VALUES ({serverID}, {channelID})"
    database.execute(insertCommand)
    database.commit()

def fetchGiveaway(serverID):
    return database.record('SELECT channelID FROM giveaway WHERE serverID=?', str(serverID))

def fetchAll():
    return database.records('SELECT channelID FROM giveaway')

def removeGiveaway(serverID):
    deleteCommand = f"DELETE FROM giveaway WHERE serverID={serverID}"
    database.execute(deleteCommand)
    database.commit()

async def getGiveaways():
    giveaways = []
    date = datetime.now()
    msg = f'Game Giveaways:\n\n'

    response = requests.get('https://www.gamerpower.com/api/filter?platform=steam.epic-games-store.ubisoft.origin.switch.vr&sort-by=popularity&type=game')
    json = response.json()
    for game in json:
        msg += f"[{game['title']}]({game['gamerpower_url']})\n"
    giveaways.append(msg)
    return giveaways
