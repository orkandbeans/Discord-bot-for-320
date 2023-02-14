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
# -------------------------------------------------------------------


# load the key
load_dotenv()
# get the key from the environment
KEY = os.getenv('BOT_TOKEN')
# run the bot with the key
bot.run(KEY)
