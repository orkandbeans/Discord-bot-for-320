import discord
from discord.ext import commands
from dotenv import load_dotenv

import random
import os


from osrsinfo import *

# Create bot declaration with intents
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


# when bot is logged in
@bot.event
async def on_ready():
    print("Bot is Up and Ready")

    # try to sync all commands that aren't actively in the tree or have been altered
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    # else print exception
    except Exception as e:
        print(e)


# -----------------INSERT BOT COMMANDS HERE--------------------------

@bot.tree.command(name="osrsinfo")
async def osrs_info_command(interaction: discord.Interaction, entity_type: str, info_type: str, name: str):
    #need to find a way to forma and present args better to the command view
    # CommandView.__init__(user_args)
    await interaction.response.send_message(output)


# -------------------------------------------------------------------


# load the key
load_dotenv()
# get the key from the environment
KEY = os.getenv('BOT_TOKEN')
# run the bot with the key
bot.run(KEY)
