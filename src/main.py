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
    def check(m):  # only allow the author to answer
        return m.author == ctx.author
    handle = Input.myhandle(arg)      #user assumed to input "custom" to start a game
    if handle == 'custom':
        await ctx.send("How many categories would you like to play with? Pick between 1 and 5.")
        usermsg = await bot.wait_for('message', check=check)  # wait for author to type in answer

        while not Input.checkcategoryamt(usermsg.content):
            await ctx.send("Please enter a valid int")
            usermsg = await bot.wait_for('message', check=check)
        #usermsg is how many categories to play with
        botmessage = await ctx.send("``` Choosing categories: ```")
        output = GameStart.startgame(arg, usermsg.content)

#####   FORMATTING OF "Game"
        botmessageupdate = GameBoard.drawtable(output)
#####
        await botmessage.edit(content=botmessageupdate) #Game table is drawn, categories and values printed
        #await ctx.send(output['question'])
    usermsg = await bot.wait_for('message', check=check)    #wait for author to choose category
    categoryusermsg, valueusermsg = usermsg.content.split("# ") #user must type "Category# Value"

    botmessageupdate = GameBoard.updatetable(output,categoryusermsg, int(valueusermsg))
    question = GameStart.pullquestion(categoryusermsg,valueusermsg)
    await ctx.send(question["question"])
    await botmessage.edit(content=botmessageupdate)
   # result = answer(output['answer'], usermsg.content, output['value'])
   # await ctx.send("You got " + result)
# -------------------------------------------------------------------


# load the key
load_dotenv()
KEY = os.getenv('BOT_TOKEN')
bot.run(KEY)
