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


@bot.command(name="jeopardy", pass_context=True)
async def jeopardy(ctx, arg):
    handle = myhandle(arg)      #user assumed to input "custom" to start a game
    if handle == 'custom':
        output = startgame(arg)
        await ctx.send(output['question'])
        def check(m):       #only allow the author to answer
            return m.author == ctx.author
    msg = await bot.wait_for('message', check=check)    #wait for author to type in answer

    result = answer(output['answer'], msg.content, output['value'])
    await ctx.send("You got " + result)
# -------------------------------------------------------------------


# load the key
load_dotenv()
KEY = os.getenv('BOT_TOKEN')
bot.run(KEY)
