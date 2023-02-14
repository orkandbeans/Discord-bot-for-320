import discord
from discord.ext import commands
from dotenv import load_dotenv

import random
import os
from geoguessr import geoguessr_game

#Create bot declaration with intents
bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())

#when bot is logged in
@bot.event
async def on_ready():
    print("Bot is Up and Ready")

    #try to sync all commands that aren't actively in the tree or have been altered
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    #else print exception
    except Exception as e:
        print(e)


#-----------------INSERT BOT COMMANDS HERE--------------------------

@bot.command(name="geoguessr")
async def geoguessr(ctx):
    await geoguessr_game(bot, ctx)
#-------------------------------------------------------------------


#load the key
load_dotenv()
#get the key from the environment
KEY = os.getenv('BOT_TOKEN')
#run the bot with the key
bot.run(KEY)
