import asyncio

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

import os




bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())



#when bot is logged in

from jeopardy import *

# Create bot declaration with intents
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
myjeopardy = JeopardyData()


@bot.event
async def on_ready():
    print("Bot is Up and Ready")

    #try to sync all commands that aren't actively in the tree or have been altered
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    # else print exception
    except Exception as e:
        print(e)


# -----------------INSERT BOT COMMANDS HERE--------------------------
@bot.command(name="jeopardy", pass_context=True)
async def jeopardy(ctx, arg):
    myjeopardy.get_all_data()
    await Input.playgame(myjeopardy, ctx, arg, bot)
    print("Game has ended and back in main")
    myjeopardy.get_all_data()
# -------------------------------------------------------------------


# load the key
load_dotenv()
# get the key from the environment
KEY = os.getenv('BOT_TOKEN')
# run the bot with the key
bot.run(KEY)
