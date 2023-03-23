import asyncio

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import Ranking
from openAI import openAI
import SoundBoard
import random
import os
from lorelookup import *
#from osrsinfo import *


#Create bot declaration with intents
bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())
#Create BRIAN declaration for ranking
Brian = Ranking.BRIAN()
AI = openAI()


#when bot is logged in

from jeopardy import *


@bot.event
async def on_ready():
    print("Bot is Up and Ready")

    #get the guild with all users in our specific discord and run an update on the members of the database
    server = discord.utils.get(bot.guilds)
    memberList = bot.get_guild(server.id).members
    roleList = bot.get_guild(server.id).roles
    Brian.initRoles(roleList)
    Brian.updateMembers(memberList)

    #try to sync all commands that aren't actively in the tree or have been altered
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    # else print exception
    except Exception as e:
        print(e)
    

# -----------------INSERT BOT COMMANDS HERE--------------------------
@bot.tree.command(name="osrsinfo")
async def osrs_info_command(interaction: discord.Interaction, entity_name: str, search_option: int = 0):
    command_output = osrsinfo(entity_name, search_option)
    await interaction.response.send_message(command_output[0])
    for i in range(1, len(command_output)):
        await interaction.followup.send(command_output[i])

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
    Brian.deleteMember(member)

@bot.event
async def on_member_join(member):
    Brian.newMember(member)

@bot.tree.command(name="newrole")
async def newrole(ctx: discord.Interaction,role: str,score: int):
    result = Brian.newRole(role,score)
    if result==1:
        await ctx.response.send_message(f"ERROR: {role} was not added to the database.")
    else:
        Brian.updateMembers(ctx.guild.members)
        await ctx.response.send_message(f"{role} has been added to the database.")

@bot.tree.command(name="deleterole")
async def deleterole(ctx: discord.Interaction,role: str):
    result = Brian.deleteRole(role)
    if result==1:
        await ctx.response.send_message(f"ERROR: {role} was not removed from the database.")
    else:
        await ctx.response.send_message(f"{role} has been removed from the database.")

@bot.tree.command(name="addrole")
async def addrole(ctx: discord.Interaction,role: str, member: str):
    result = Brian.addMemberRole(role,member)
    if result==1:
        await ctx.response.send_message(f"ERROR: {role} was not added to {member}.")
    else:
        await ctx.response.send_message(f"{role} has been added to {member}.")

@bot.tree.command(name="removerole")
async def removerole(ctx: discord.Interaction,role: str, member: str):
    result = Brian.removeMemberRole(role,member)
    if result==1:
        await ctx.response.send_message(f"ERROR: {role} was not removed from {member}.")
    else:
        await ctx.response.send_message(f"{role} has been removed from {member}.")

@bot.tree.command(name="getroles")
async def getroles(ctx: discord.Interaction,member: str):
    result = Brian.getMRoles(member)
    
    if result == []:
        await ctx.response.send_message(f"{member} does not have any roles in the database.")
    else:
        sendMessage = f"{member} roles:\n"
        for role in result:
            sendMessage = sendMessage + f"{role}\n"
        await ctx.response.send_message(sendMessage)

@bot.command(name="jeopardy", pass_context=True)
async def jeopardy(ctx, arg):
    money = 0
    def check(m):  # only allow the author to answer
        return m.author == ctx.author
    handle = Input.myhandle(arg)      #user assumed to input "custom" to start a game
    if handle == 'custom':
        intro = await ctx.send("How many categories would you like to play with? Pick between 1 and 5.")
        usermsg = await bot.wait_for('message', check=check)  # wait for author to type in answer
        await usermsg.delete()
        await intro.delete()
        while not Input.checkcategoryamt(usermsg.content):
            await ctx.send("Please enter a valid int")
            usermsg = await bot.wait_for('message', check=check)
        #usermsg is how many categories to play with
        botmessage = await ctx.send("``` Choosing categories: ```")
        output = GameStart.startgame(arg, usermsg.content)

#####   FORMATTING OF "Game"
        botmessageupdate = GameBoard.drawtable(output)
        GameBoard.initcategories(output)
#####
        await botmessage.edit(content=botmessageupdate) #Game table is drawn, categories and values printed
    while(1):
        usermsg = await bot.wait_for('message', check=check)    #wait for author to choose category
        #categoryusermsg, valueusermsg = usermsg.content.split("# ") #user must type "Category# Value"
        while not Input.pickcategory(usermsg.content):   #loop until category chosen correctly
            error = await ctx.send("Please enter valid category")
            await usermsg.delete()
            await asyncio.sleep(1)
            usermsg = await bot.wait_for('message', check=check)
            await error.delete()
        await asyncio.sleep(1)
        await usermsg.delete()
        categoryusermsg, valueusermsg = usermsg.content.split("# ")  # user must type "Category# Value"
        botmessageupdate = GameBoard.updatetable(output, categoryusermsg, int(valueusermsg))
        question = GameStart.pullquestion(categoryusermsg, valueusermsg)
        myquestion = await ctx.send(question["question"])    #SEND QUESTION
        usermsg = await bot.wait_for('message', check=check)
        result = Input.answer(question["answer"], usermsg.content, valueusermsg)
        await botmessage.edit(content=botmessageupdate) #UPDATE TABLE
        if int(result) < 0:
            sendresult = await ctx.send("Wrong, the correct response is: " + question["answer"])
        else:
            sendresult = await ctx.send("Correct!")
        money += int(result)
        prize = await ctx.send("You got " + result)
        await asyncio.sleep(5)
        await usermsg.delete()
        await myquestion.delete()
        await sendresult.delete()
        await prize.delete()
        if GameBoard.gameover("hello"): break
        #if GameBoard.gameover is True: break
    await ctx.send("You earned " + str(money))
    await ctx.send("Thanks for playing!")

@bot.command(name="soundboard", pass_context=True)
async def sound_request(ctx, message):
    speaker = ctx.author
    await SoundBoard.Sound.connect(speaker, message)

@bot.command(name="geoguessr")
async def geoguessr(ctx):
    pass
    #await geoguessr_game(bot,ctx)
    
#-------------------------------------------------------------------

#load the key
load_dotenv()
# get the key from the environment
KEY = os.getenv('BOT_TOKEN')
# run the bot with the key
bot.run(KEY)
