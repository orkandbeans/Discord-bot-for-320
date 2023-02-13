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
    handle = myhandle(arg)      #user assumed to input "custom" to start a game
    if handle == 'custom':
        await ctx.send("How many categories would you like to play with? Pick between 1 and 5.")
        usermsg = await bot.wait_for('message', check=check)  # wait for author to type in answer
        while not isinstance(usermsg.content, int) and 0 > int(usermsg.content) > 6:
            await ctx.send("Please enter a valid int")
            usermsg = await bot.wait_for('message', check=check)  # wait for author to type in answer
            if not isinstance(usermsg.content, int) and 0 < int(usermsg.content) < 6: break
        #usermsg is how many categories to play with
        botmessage = await ctx.send("``` Choosing categories: ```")
        output = startgame(arg, usermsg.content)

#####   FORMATTING OF "Game"
        botmessageupdate = "```\nCategories:\n"
        # Find the length of the longest category
        longest_category_length = max(len(category) for category in output)

        for category in output:
            botmessageupdate += category + " " * (longest_category_length - len(category)) + "\t\t"
            for i in range(200, 1100, 200):
                botmessageupdate += str(i) + "\t"
            botmessageupdate += "\n"

        botmessageupdate += "```"
#####
        await botmessage.edit(content=botmessageupdate)
        #await ctx.send(output['question'])


    #usermsg = await bot.wait_for('message', check=check)    #wait for author to type in answer

   # result = answer(output['answer'], usermsg.content, output['value'])
   # await ctx.send("You got " + result)
# -------------------------------------------------------------------


# load the key
load_dotenv()
KEY = os.getenv('BOT_TOKEN')
bot.run(KEY)
