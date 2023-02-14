import discord
from discord.ext import commands
from dotenv import load_dotenv

import SoundBoard

import random
import os

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

@bot.command(name="soundboard", pass_context=True)
async def sound_request(ctx, message):
    speaker = ctx.author
    await SoundBoard.Sound.connect(speaker, message)
    
#-------------------------------------------------------------------


#load the key
load_dotenv()
#get the key from the environment
KEY = os.getenv('BOT_TOKEN')
#run the bot with the key
bot.run(KEY)
