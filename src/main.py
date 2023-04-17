import asyncio
import discord
import datetime as dt
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv
import Ranking
from openAI import openAI
from discord.ui import Button, view
from SoundBoard import Board
import wavelink
import youtube_dl
import random
import os
from osrsinfo import *
from osrshighscores import *
from geoguessr import geoguessr_game
import giveaway as giveaway


#Create bot declaration with intents
bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())
#Create BRIAN declaration for ranking
#Brian = Ranking.BRIAN()
#AI = openAI()


#when bot is logged in

from jeopardy import *


@bot.event
async def on_ready():
    print("Bot is Up and Ready")
    if not daily_giveaway.is_running():
        daily_giveaway.start()

    #get the guild with all users in our specific discord and run an update on the members of the database
    server = discord.utils.get(bot.guilds)
    guild = bot.get_guild(server.id)
    memberList = guild.members
    roleList = []
    for role in bot.get_guild(server.id).roles:
        if role.is_bot_managed():
            continue
        roleList.append(role)

    Brian.initRoles(roleList)
    Brian.updateMembers(memberList)

    if Brian.shouldSearch():
        print("Running background scoring...")
        for channel in guild.text_channels:
            await searchMessages(channel)
        Brian.historyUpdate()
        print("Done with background scoring.")
    #try to sync all commands that aren't actively in the tree or have been altered
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    # else print exception
    except Exception as e:
        print(e)

@tasks.loop(hours=24)
async def daily_giveaway():
    giveaways = await giveaway.getGiveaways()
    channels = giveaway.fetchAll()
    msg = discord.Embed(title='Giveaways')
    msg.description = giveaways[0]
    for channel in channels:
        await bot.get_channel(int(str(channel)[2:len(channel)-4])).send(embed=msg)


# -----------------INSERT BOT COMMANDS HERE--------------------------
# -----John's Commands-----
# osrsinfo pulls and returns information from the osrs wiki
# returning a list of output messages to accomodate discords 2000 character limit.
@bot.tree.command(name="osrsinfo")
async def osrs_info_command(interaction: discord.Interaction, entity_name: str, search_option: int = 0):
    command_output = osrsinfo(entity_name, search_option)
    await interaction.response.send_message(command_output[0])
    for i in range(1, len(command_output)):
        await interaction.followup.send(command_output[i])

# osrshighscores pulls player information from the osrs highscores api
# returning a list of output messages to accomodate discords 2000 character limit.
@bot.tree.command(name="osrshighscores")
async def osrs_highscores_command(interaction: discord.Interaction, player_name: str, second_player_name: str = "", game_mode: str = ""):
    command_output = osrshighscores(player_name, second_player_name, game_mode)
    await interaction.response.send_message(command_output[0])
    for i in range(1, len(command_output)):
        await interaction.followup.send(command_output[i])
#--------------------------

# -----Aaron's Commands-----
#set up api key for server
@bot.tree.command(name="aisetup", description = "Start setup process of openAI API for arnold bot for the server")
async def aisetup(ctx: discord.Interaction):
    author = ctx.user
    server = ctx.guild.name
    if (AI.fetchAPI(server) != None):
        await ctx.response.send_message("This server already has an API key associated with it! if you wish to use another, please use \"remove\" or \"sudoremove\" followed by this command in order to use a different API")
        return
    await ctx.response.send_message("Okay! Creating a DM!")
    dm = await ctx.user.create_dm()
    await dm.send(f"Hello {author}! You just used the setup command for openAI on the server {server}! Please provide the openAI API key to your wallet in order to make openAI commands available. you must provide the"
     + " API key in its entirety in this message. It will then be linked to this server.")
    APIkey = await bot.wait_for('message')
    AI.insertKey(APIkey.content, ctx.guild.id)
    await dm.send("Your key has been added to the database! You should now be able to use the Dalle and ChatGPT commands")

#run the dalle command to generate an image
@bot.tree.command(name = "dalle", description = "Give a prompt and let openAI generate an image")
@app_commands.describe(prompt = "What prompt would you like to generate?")
@app_commands.describe(download = "Specify if you want this image sent and kept via download (specify True for yes, False for no)")
async def dalle(ctx: discord.Interaction, prompt: str, download: bool):
    await ctx.response.send_message("Give us a few seconds to generate your image.")
    user = ctx.user.id
    server = ctx.guild.id
    if (AI.fetchAPI(server) == None):
        await ctx.channel.send("This server does not have an API key associated with it. Please use \"aisetup\" command in order to save an API key to this server")
        return
    api = str(AI.fetchAPI(server))
    api = api[2:len(api)-3]
    data = AI.dalle.generate(prompt, api, download)
    if (data == "ERROR CODE 1"):
        await ctx.channel.send(f"""
        <@{user}> your API key for this server is invalid.
        We removed it from our database.
        Please reuse \"aisetup\" with the correct API key.
        Make sure the submission is exactly like the one provided in openAI
        """)
        return
    if (data == "ERROR CODE 2"):
        await ctx.channel.send(f"""
        <@{user}> Your being rate limited for too many requests or you have hit your soft or hard limit for your API key.
        In order to fix the latter, you must increase your limit for this month.
        You can do so by following this link: https://platform.openai.com/account/billing/limits
        """)
        return
    if (data == "ERROR CODE 3"):
        await ctx.channel.send(f"""
        <@{user}> The OpenAI site is having issues at the moment!
        Please come back later!
        """)
        return
    if (data == "ERROR CODE 4"):
        await ctx.channel.send(f"""
        <@{user}> The prompt given is against OpenAI terms of service and was rejected.
        Please stay within openAI terms of service
        """)
        return
    if (not download):
        embed = discord.Embed()
        embed.set_image(url=data)
        await ctx.channel.send(f"""
        <@{user}> here's your image for prompt: {prompt}
        """, embed=embed)
        return
    else:
        with open("temp/dalle.png", 'rb') as image_file:
            await ctx.channel.send(f"""
            <@{user}> here's your image for prompt: {prompt}
            """, file=discord.File(image_file, filename='dalle.png'))
    os.remove("temp/dalle.png")

#remove the api key from the database
@bot.tree.command(name = "remove", description = "Remove the current API key from this server for OpenAI")
async def remove(ctx: discord.Interaction):
    server = ctx.guild.id
    if ctx.permissions.administrator:
        if AI.fetchAPI(server) == None:
            await ctx.response.send_message("""
            There is no API key associated with this server.
            Remove rejected
            """)
        else:
            AI.removeKey(server)
            await ctx.response.send_message("""
            API key successfully removed!
            """)
    else:
        await ctx.response.send_message("""
        You are not an admin of this server.
        If you own the API Key, you must use superRemove
        """)

#superremove all api keys and server links
@bot.tree.command(name = "sudoremove", description = "Remove an API key from all servers")
async def sudoremove(ctx: discord.Interaction):
    await ctx.response.send_message("""
    Okay!
    Creating a DM!
    """)
    dm = await ctx.user.create_dm()
    author = ctx.user
    server = ctx.guild.id
    await dm.send(f"""
    Hello {author}!
    You just used the superRemove command for openAI on the server {server}!
    Please provide the openAI API key to your wallet in order to remove your API key from the database.
    you must provide the API key in its entirety in this message.
    It will then be removed from any linked servers.
    """)
    APIkey = await bot.wait_for('message')
    AI.superRemoveKey(APIkey)
    await dm.send("""
    Your key has been removed from the database.
    No servers should be able to use your key now
    """)

#generate text from chatgpt from a prompt
@bot.tree.command(name = "chat", description = "Give a prompt and let openAI generate text")
@app_commands.describe(prompt = "What prompt would you like to generate?")
@app_commands.describe(size = "What size do you want your prompt to return")
async def dalle(ctx: discord.Interaction, prompt: str, size: int):
    await ctx.response.send_message("Give us a few seconds to generate your text.")
    user = ctx.user.id
    server = ctx.guild.id
    if (AI.fetchAPI(server) == None):
        await ctx.channel.send(f"""
        <@{user}> Your being rate limited for too many requests or you have hit your soft or hard limit for your API key.
        In order to fix the latter, you must increase your limit for this month.
        You can do so by following this link: https://platform.openai.com/account/billing/limits
        """)
        return
    api = str(AI.fetchAPI(server))
    api = api[2:len(api)-3]
    data = AI.chatGPT.generate(prompt, size, api)
    if (data == "ERROR CODE 1"):
        await ctx.channel.send(f"""
        <@{user}> Your being rate limited for too many requests or you have hit your soft or hard limit for your API key.
        In order to fix the latter, you must increase your limit for this month.
        You can do so by following this link: https://platform.openai.com/account/billing/limits
        """)
        return
    if (data == "ERROR CODE 2"):
        await ctx.channel.send(f"<@{user}> Your being rate limited for too many requests or you have hit your soft or hard limit for your API key. In order to fix the latter, you must increase your limit for this month. You can do so by following this link: https://platform.openai.com/account/billing/limits")
        return
    if (data == "ERROR CODE 3"):
        await ctx.channel.send(f"""
        <@{user}> The OpenAI site is having issues at the moment!
        Please come back later!
        """)
        return
    if (data == "ERROR CODE 4"):
        await ctx.channel.send(f"""
        <@{user}> The prompt given is against OpenAI terms of service and was rejected.
        Please stay within openAI terms of service
        """)
    await ctx.channel.send(f"""
    <@{user}> here's your text for prompt: {prompt} : {data}
    """)

#set up channel for daily giveaways
@bot.tree.command(name = "setupgiveaway", description = "Give a channel to receive news about giveaways")
@app_commands.describe(channel = "What channel would you like to use for your giveaways?")
async def setupgiveaway(ctx: discord.Interaction, channel: discord.TextChannel):
    author = ctx.user
    server = ctx.guild.id
    if ctx.permissions.administrator != True:
        await ctx.response.send_message("You are not an admin of this server and can not set up a giveaway channel")
        return
    if (giveaway.fetchGiveaway(server) != None):
        await ctx.response.send_message("This server already has a channel set up for giveaways. In order to set up a new one, please use the \"removegive\" followed by this command in order to use a different channel")
        return
    else:
        giveaway.setGiveaway(server, channel.id)
        await ctx.response.send_message("This server now has a giveaway channel that will be updated every day at 12:00PM Pacific Standard")

#remove channel for daily giveaways
@bot.tree.command(name = "removegiveaway", description = "remove the giveaway channel for this server")
async def removegiveaway(ctx: discord.Interaction):
    author = ctx.user
    server = ctx.guild.id
    if ctx.permissions.administrator != True:
        await ctx.response.send_message("You are not an admin of this server and can not remove a giveaway channel")
        return
    if (giveaway.fetchGiveaway(server) == None):
        await ctx.response.send_message("This server does not have a giveaway channel associated with it already")
        return
    else:
        giveaway.removeGiveaway(server)
        await ctx.response.send_message("Giveaway channel has successfully been deleted. No more updates will be given")
# -------------------------

@bot.event
async def on_message(message):
    member = message.author
    if not member.bot:
        Brian.updateScore(member,message.content)
        await updateRoles(member)

@bot.event
async def on_message_delete(message):
    member = message.author
    if not member.bot:
        Brian.reduceScore(member,message.content)
        await updateRoles(member)

@bot.event
async def on_message_edit(before,after):
    member = before.author
    if not member.bot:
        Brian.reduceScore(member,before.content)
        Brian.updateScore(member,after.content)
        await updateRoles(member)

async def searchMessages(channel):
    async for message in channel.history(limit=None):
        if message.author.bot:
            continue
        result = Brian.historyCheck(message.author)

        if result == 1:
            continue
        Brian.updateScore(message.author,message.content)
        await updateRoles(message.author)

async def updateRoles(member):
    result = Brian.getMRoles(member)
    hasRoles = []

    for role in member.roles:
        hasRoles.append(role.name)

    for role in result:
        if role not in hasRoles:
            #add role to member in discord
            this = discord.utils.get(member.guild.roles, name=str(role))
            if this is not None:
                await member.add_roles(this)
            else:
                print(role + " role does not exist.")


@bot.event
async def on_member_ban(guild, member):
    Brian.deleteMember(member)

@bot.event
async def on_member_join(member):
    if not member.bot:
        Brian.newMember(member)

@bot.tree.command(name="listranks")
async def listranks(ctx: discord.Interaction):
    result = Brian.getMemberRankList()
    if result==1:
        await ctx.response.send_message(f"ERROR: The database did not access any members.")
    else:
        i=1
        message = ""
        for member in result:
            message = message + f"{i}. {member[1]} with a score of {member[0]}\n"
            i+=1
        await ctx.response.send_message(message)


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


#load the key
load_dotenv()
# get the key from the environment
KEY = os.getenv('BOT_TOKEN')
# run the bot with the key
bot.run(KEY)
