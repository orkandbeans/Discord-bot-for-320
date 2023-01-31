import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
import os

bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is Up and Ready")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

load_dotenv()
KEY = os.getenv('BOT_TOKEN')
bot.run(KEY)
