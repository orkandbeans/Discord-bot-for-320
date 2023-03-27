#Jake Onkka --Jeopardy Features --CSE320
import json
import random
import asyncio
import sqlite3

class JeopardyData:
    def __init__(self):
        #Create a connection to the database file
        self.conn = sqlite3.connect('jeopardydatabase.db')
        self.database = self.conn.cursor()

        #Create the Jeopardy table if it doesn't exist
        self.create()

    def create(self):
        #Drop the Jeopardy table if it exists
        self.database.execute('''DROP TABLE IF EXISTS Jeopardy''')
        self.conn.commit()

        #Create the table with a primary key, unique constraint, and isInGame column
        createCommand = '''CREATE TABLE IF NOT EXISTS Jeopardy(
                            User_id INTEGER PRIMARY KEY,
                            Server_id INTEGER,
                            isInGame INTEGER,
                            UNIQUE(User_id, Server_id))'''
        self.database.execute(createCommand)
        self.conn.commit()
        print("db made")

    def get_all_data(self):
        query = "SELECT * FROM Jeopardy"
        cursor = self.conn.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    def user_exists(self, user_id, server_id):
        try:
            self.database.execute("SELECT * FROM Jeopardy WHERE User_id = ? AND Server_id = ?", (user_id, server_id))
            row = self.database.fetchone()
            if row is not None:
                return True
            else:
                return False
        except sqlite3.Error as error:
            print("Error verifying if user exists in Jeopardy table:", error)
    def start_game(self, user_id, server_id):
        #Check if the user exists in the database
        rows = self.conn.execute("SELECT User_id, Server_id, isInGame FROM Jeopardy").fetchall()
        print(rows)
        if not self.user_exists(user_id, server_id):
            #If the user does not exist, add them to the database
            self.add_user(user_id, server_id)
            self.update_is_in_game(user_id, server_id, 1)
            rows = self.conn.execute("SELECT User_id, Server_id, isInGame FROM Jeopardy").fetchall()
            print(rows)
            return True
        else:
            #If the user does exist, check if isInGame is set to 1
            if self.is_in_game(user_id, server_id):
                print("User is already in a game.")
                return False
            else:
                self.update_is_in_game(user_id, server_id, 1)
                return True

    def add_user(self, user_id, server_id):
        #Check if the user already exists in the Jeopardy table
        query = 'SELECT * FROM Jeopardy WHERE User_id = ?'
        self.database.execute(query, (user_id,))
        row = self.database.fetchone()
        if row is not None:
            #User already exists, update Server_id if necessary
            if row[1] != server_id:
                query = 'UPDATE Jeopardy SET Server_id = ? WHERE User_id = ?'
                self.database.execute(query, (server_id, user_id))
                self.conn.commit()
        else:
            #User does not exist, add a new row to the Jeopardy table
            query = 'INSERT INTO Jeopardy (User_id, Server_id, isInGame) VALUES (?, ?, 0)'
            self.database.execute(query, (user_id, server_id))
            self.conn.commit()

    def is_in_game(self, user_id, server_id):
        try:
            self.database.execute("SELECT isInGame FROM Jeopardy WHERE User_id = ? AND Server_id = ?", (user_id, server_id))
            row = self.database.fetchone()
            if row is not None and row[0] == 1:
                return True
            else:
                return False
        except sqlite3.Error as error:
            print("Error checking isInGame value for user in Jeopardy table:", error)

    def update_is_in_game(self, user_id, server_id, value):
        try:
            self.database.execute("UPDATE Jeopardy SET isInGame = ? WHERE User_id = ? AND Server_id = ?",
                                  (value, user_id, server_id))
            self.conn.commit()
            print("isInGame value updated in Jeopardy table.")
        except sqlite3.Error as error:
            print("Error updating isInGame value for user in Jeopardy table:", error)
    def end_game(self, user_id: int, server_id: int):
        update_command = '''
            UPDATE Jeopardy
            SET isInGame = 0
            WHERE User_id = ? AND Server_id = ?
        '''
        self.database.execute(update_command, (user_id, server_id))
        self.conn.commit()

class GameStart:
    def gameexist(ctx): #checks to see if game exists in file
        user_id = ctx.author.id
        guild_id = int(ctx.guild.id)
        channel_id = int(ctx.channel.id)
        with open("games.json","r") as file:
            data = json.load(file)
 #           for i in range(len(data)):
 #               print(data(i)["user_id"])
 #               if user_id == data(i)["user_id"]:
 #                   return False
            for item in data:
                print(item[user_id])
         #       if user_id == data[item]["user_id"]:# or channel_id == int(item["channel_id"]) or guild_id == int(item["guild_id"]):
         #           return False
        return False
        return True
    def gamemake(ctx):
        user_id = str(ctx.author.id)
        guild_id = int(ctx.guild.id)
        channel_id = int(ctx.channel.id)
        data = {
            "user_id": user_id,
            "guild_id": guild_id,
            "channel_id": channel_id
        }
        with open("games.json","a") as file:
            json.dump(data,file)
    def startgame(command, numberofcategories):#, username, channel):

        command = command.lower()
        if command == 'custom':     #Custom Game Solo: In Progress
        #    print(f"{username} from: ({channel})")
            with open("jeopardydata.json", "w") as file: #empty file first
                myselectcategory = [None] * int(numberofcategories)
                for i in range(int(numberofcategories)):
                    myrand = random.randint(0, 1000)
                    selectcategory = GameStart.randomcategory(myrand)
                    GameStart.savecategory(selectcategory)
                    print(str(selectcategory) + " " + str(i) + " " + str(myrand) + " " + str(numberofcategories))
                    myselectcategory[i] = str(selectcategory)
                    questions = GameStart.savequestion(selectcategory)
            return (myselectcategory)
    def pullquestion(category, value):  #return the question that the user wanted
        with open("jeopardydata.json", "r") as file:
            data = json.load(file)
            #print(data)
            #print(value)
            #print(category)
            for i in range(len(data)):
                #print(data[i]["category"])
                if data[i]["category"] == category and data[i]["value"] == int(value):
                    return data[i]
    def randomcategory(myrand): #randomly choose categories to pick from, KNOWN PROBLEM: VERY SMALL CHANCE BUT CAN PICK THE SAME CATEGORY TWICE, NEEDS ATTENTION
        with open("JEOPARDY_QUESTIONS1.json", "r") as file:
            data = json.load(file)
            return (data[myrand]['category'])
    def savequestion(givencategory):    #save all the details pertaining to the question
        with open("JEOPARDY_QUESTIONS1.json", "r") as file:  # THIS IS A LOCAL FILE, IT IS VERY BIG :)
            data = json.load(file)
        questions = []  # save questions in here
        #    category = "HISTORY"    #select a category
        current_value = 0
        for item in data:
            if item["category"] == givencategory:  # check through every item and match based on category and save it's information
                current_value += 200
                category = item["category"]
                value = item["value"]
                question = item["question"]
                answer = item["answer"]
                round = item["round"]
                show_number = item["show_number"]
                air_date = item["air_date"]
                question_data = {
                    "category": category,
                    "value": current_value,
                    "question": question,
                    "answer": answer,
                    "round": round,
                    "show_number": show_number,
                    "air_date": air_date,
                }
                questions.append(question_data)
        return questions
    def savecategory(givencategory):    #save the category to a file
        questions = GameStart.savequestion(givencategory)
        try:
            with open("jeopardydata.json", "r") as file:
                data = json.load(file)
        except:
            data = []
        if data == []:
                data = questions[0:5]
        else:
                data.extend(questions)
        with open("jeopardydata.json", "w") as file:
            print(data)
            json.dump(data, file, indent=4)

class Input:

    async def playgame(myjeopardy, ctx, arg, bot):
        money = 0
        user_id = ctx.author.id
        server_id = ctx.guild.id
        print(user_id)
        print(server_id)
        is_new_game = myjeopardy.start_game(user_id, server_id)
        if not is_new_game:
         print("User already in game")
         await ctx.send("Hol up wait a minute, you is in a game fool")
         return
        else:
            print("User is not in game, making new one")
        def checkifquit(m):
            if m.content == "quit":
                GameBoard.gameover(myjeopardy, m)
                print("It happened")
                return True
            else:
                return False

        def check(m):  # only allow the author to answer
            return m.author == ctx.author

        handle = Input.myhandle(arg)  # user assumed to input "custom" to start a game
        if handle == 'custom':



           # doesGameExist = GameStart.gameexist(ctx)
           # if (doesGameExist):
            #    await ctx.send("Error, user already playing")
            #    return
            GameStart.gamemake(ctx)

            intro = await ctx.send("How many categories would you like to play with? Pick between 1 and 5.")
            usermsg = await bot.wait_for('message', check=check)  # wait for author to type in answer
            if(checkifquit(usermsg)):
                await ctx.send("Ending game")
                return

            await usermsg.delete()
            await intro.delete()
            while not Input.checkcategoryamt(usermsg.content):
                await ctx.send("Please enter a valid int")
                usermsg = await bot.wait_for('message', check=check)
                if (checkifquit(usermsg)):
                    await ctx.send("Ending game")
                    return
            # usermsg is how many categories to play with
            botmessage = await ctx.send("``` Choosing categories: ```")
            output = GameStart.startgame(arg, usermsg.content)

            #####   FORMATTING OF "Game"
            botmessageupdate = GameBoard.drawtable(output)
            GameBoard.initcategories(output)
            #####
            await botmessage.edit(content=botmessageupdate)  # Game table is drawn, categories and values printed
        while (1):
            usermsg = await bot.wait_for('message', check=check)  # wait for author to choose category
            if(checkifquit(usermsg)):
                await ctx.send("Ending game")
                return
            # categoryusermsg, valueusermsg = usermsg.content.split("# ") #user must type "Category# Value"
            while not Input.pickcategory(usermsg.content):  # loop until category chosen correctly
                error = await ctx.send("Please enter valid category")
                await usermsg.delete()
                await asyncio.sleep(1)
                usermsg = await bot.wait_for('message', check=check)
                if (checkifquit(usermsg)):
                    await ctx.send("Ending game")
                    return
                await error.delete()
            await asyncio.sleep(1)
            await usermsg.delete()
            categoryusermsg, valueusermsg = usermsg.content.split("# ")  # user must type "Category# Value"
            botmessageupdate = GameBoard.updatetable(output, categoryusermsg, int(valueusermsg))
            question = GameStart.pullquestion(categoryusermsg, valueusermsg)
            myquestion = await ctx.send(question["question"])  # SEND QUESTION
            usermsg = await bot.wait_for('message', check=check)
            if(checkifquit(usermsg)):
                await ctx.send("Ending game")
                return
            result = Input.answer(question["answer"], usermsg.content, valueusermsg)
            await botmessage.edit(content=botmessageupdate)  # UPDATE TABLE
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
            if GameBoard.gameover(myjeopardy, ctx): break
            # if GameBoard.gameover is True: break
        await ctx.send("You earned " + str(money))
        await ctx.send("Thanks for playing!")
        myjeopardy.end_game(user_id, server_id)

    def checkcategoryamt(input):    #make sure user wants reasonable amount of categories, it takes substantial time to make one
        try:
            value = int(input)
            if value >= 0 and value <= 6:
                return True
            else:
                return False
        except ValueError:
            return False
    def myhandle(arg):  #lowercase
        arg = arg.lower()
        if arg == 'custom':
            return arg
        return -1

    def answer(answer, arg, value): #simple answer check, user must type answer perfectly in accordance to the JSON file, this will be updated for major milestone
        answer = answer.lower()
        arg = arg.lower()
        if arg == answer:
            return str(value)
        if arg != answer:
            return str("-" + value)
    def pickcategory(input):    #verify the user picked a proper category and value, it must exist for it to return true
        try:
            categoryusermsg, valueusermsg = input.split("# ")  # user must type "Category# Value"
          #  print(categoryusermsg)
          #  print(valueusermsg)
            with open("categorystate.json","r") as file:
                current_categories = json.load(file)
               # print("categories found")
                #print(current_categories)
                values = [200, 400, 600, 800, 1000]
                value_index = values.index(int(valueusermsg))
                if current_categories[categoryusermsg][value_index] is None:    #make sure user picks unique categories and not a previously selected one
                    return False
                else:
                    return True
        except:
            return False

class GameBoard:
    def drawtable(categories):  #initial create the table
        values = [[200, 400, 600, 800, 1000] for i in range(len(categories))]

        message = "```\nCategories:\n"
        longest_category_length = max(len(category) for category in categories)

        for category_index, category in enumerate(categories):  #FORMATTING THE TABLE PLS DONT TOUCH
            message += category + " " * (longest_category_length - len(category)) + "\t\t"
            for value in values[category_index]:
                if value is not None:
                    message += str(value) + "\t"
                else:
                    message += " " * len(str(value)) + "\t"
            message += "\n"

        message += "```"
        return message

    def initcategories(categories): #initialize all categories with their values in an "array"
        with open("categorystate.json", "w") as file:
            file.close()
        try:
            with open("categorystate.json", "r") as f:
                categories_values = json.load(f)
        except:
            categories_values = {category: [200, 400, 600, 800, 1000] for category in categories}
        with open("categorystate.json", "w") as f:
            json.dump(categories_values, f)

    def updatetable(categories, category_to_remove, value_to_delete):   #update the table message, save the deletions so game can progress
        values = [200, 400, 600, 800, 1000]
        value_index = values.index(value_to_delete)

        with open("categorystate.json", "r") as f:
            current_categories = json.load(f)
        current_categories[category_to_remove][value_index] = None

        with open("categorystate.json", "w") as f:
            json.dump(current_categories, f)

        message = "```\nCategories:\n"
        longest_category_length = max(len(category) for category in categories)
        for i, category in enumerate(categories):
            message += category + " " * (longest_category_length - len(category)) + "\t\t"
            for value in values:
                if current_categories.get(category, [None, None, None, None, None])[values.index(value)] is None:
                    message += "     \t"
                else:
                    message += str(value) + "\t"
            message += "\n"
        message += "```"
        return message

    #NEEDS ADDING: CHECK IF USER HAS Content attribute before checking user.content k thx bye
    def gameover(myjeopardy, user):        #check to see if all values are null for game over
        if(user.content == "quit"):
            print("Quiting because user said so")
            myjeopardy.end_game(user.author.id, user.guild.id)
            return True
        with open("categorystate.json", "r") as f:
            current_categories = json.load(f)
            game_over = True
            for category_values in current_categories.values():
                if any(value is not None for value in category_values):
                    game_over = False
                    break
            if game_over:
                return True
            else:
                return False