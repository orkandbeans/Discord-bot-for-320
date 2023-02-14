import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import Ranking
from openAI import openAI
import random
import os
from lorelookup import *
from osrsinfo import *

#Create bot declaration with intents
bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())
#Create BRIAN declaration for ranking
Brian = Ranking.BRIAN()
AI = openAI()

#when bot is logged in
@bot.event
async def on_ready():
    print("Bot is Up and Ready")

    #get the guild with all users in our specific discord and run an update on the members of the database
    memberList = bot.get_guild(1065019755628613682).members
    Brian.botCommand("updateMembers",memberList,"")

    #try to sync all commands that aren't actively in the tree or have been altered
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    # else print exception
    except Exception as e:
        print(e)

# -----------------INSERT BOT COMMANDS HERE--------------------------

@bot.tree.command(name="osrsinfo")
async def osrs_info_command(interaction: discord.Interaction, entity_name: str):
    output = osrsinfo(entity_name)
    await interaction.response.send_message(output)

@bot.tree.command(name="aisetup", description = "Start setup process of openAI API for arnold bot for the server")
async def aisetup(ctx: discord.Interaction):
    await ctx.response.send_message("Okay! Creating a DM!")
    dm = await ctx.user.create_dm()
    author = ctx.user
    server = ctx.guild.name
    await dm.send(f"Hello {author}! You just used the setup command for openAI on the server {server}! Please provide the openAI API key to your wallet in order to make openAI commands available. you must provide the"
     + " API key in its entirety in this message. It will then be linked to this server.")
    APIkey = await bot.wait_for('message')
    # AI.insertKey(APIkey.content, ctx.guild.id)
    await dm.send("GOOD WE GOT THE KEY :)")

@bot.tree.command(name = "dalle", description = "Give a prompt and let openAI generate an image")
@app_commands.describe(prompt = "What prompt would you like to generate?")
async def dalle(ctx: discord.Interaction, prompt: str):
    await ctx.response.send_message("Give us a few seconds to generate your image.")
    user = ctx.user.id
    data = AI.dalle.generate(prompt)
    embed = discord.Embed()
    embed.set_image(url=data)
    await ctx.channel.send(f"<@{user}> here's your image for prompt: {prompt}", embed=embed)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    Brian.updateScore(message.author,message.content)

@bot.event
async def on_member_ban(guild, member):
    print(member,guild)#member name without number?????
    Brian.addRemoveMember(member,False)

@bot.event
async def on_member_join(member):
    print(member)
    Brian.addRemoveMember(member,True)
# -------------------------------------------------------------------

# load the key
load_dotenv()
# get the key from the environment
KEY = os.getenv('BOT_TOKEN')
# run the bot with the key
bot.run(KEY)
