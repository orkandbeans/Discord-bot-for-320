import discord
from discord.ext import commands
from dotenv import load_dotenv
import Ranking

import random
import os

#Create bot declaration with intents
bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())
Brian = Ranking.BRIAN()

#when bot is logged in
@bot.event
async def on_ready():
    print("Bot is Up and Ready")

    memberList = bot.get_guild(1065019755628613682).members
    Brian.botCommand("updateMembers",memberList,"")

    #try to sync all commands that aren't actively in the tree or have been altered
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    #else print exception
    except Exception as e:
        print(e)

#-----------------INSERT BOT COMMANDS HERE--------------------------



#-------------------------------------------------------------------


#load the key
load_dotenv()
#get the key from the environment
KEY = os.getenv('BOT_TOKEN')
#run the bot with the key
bot.run(KEY)
