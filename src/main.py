import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
import os


bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())

from jeopardy import *

# Create bot declaration with intents
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())



@bot.event
async def on_ready():
    print("Bot is Up and Ready")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)



# -----------------INSERT BOT COMMANDS HERE--------------------------

@bot.command(name="npclookup")
async def npclookup(ctx, npc, infotype):
    output = npcquery(npc, infotype)
    await ctx.send(output)

@bot.command(name="jeopardy", pass_context=True)
async def jeopardy(ctx, arg):
    print(f"{arg.author} ({arg.channel})")
    #output = startgame(arg, arg.author, arg.channel)

   # await ctx.send(output)

# -------------------------------------------------------------------


# load the key
load_dotenv()
KEY = os.getenv('BOT_TOKEN')
bot.run(KEY)
