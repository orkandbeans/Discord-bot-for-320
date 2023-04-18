#Jake Onkka --Jeopardy Features --CSE320
import json
import random
import discord
import asyncio
import sqlite3
from discord.ui import Button, View
import difflib
intents = discord.Intents.default()
client = discord.Client(intents=intents)
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
        self.database.execute('''DROP TABLE IF EXISTS Multiplayer''')
        self.database.execute('''DROP TABLE IF EXISTS Games''')


        self.conn.commit()

        #Create the table with a primary key, unique constraint, and isInGame column
        createCommand = '''CREATE TABLE IF NOT EXISTS Jeopardy(
                            User_id INTEGER PRIMARY KEY,
                            Server_id INTEGER,
                            isInGame INTEGER,
                            money INTEGER,
                            UNIQUE(User_id, Server_id))'''
        self.database.execute(createCommand)
        self.conn.commit()

        createCommand = '''
                        CREATE TABLE IF NOT EXISTS Multiplayer (
                        User_id INTEGER,
                        Server_id INTEGER,
                        Game_id INTEGER,
                        FOREIGN KEY (User_id, Server_id) REFERENCES Jeopardy(User_id, Server_id),
                        FOREIGN KEY (Game_id) REFERENCES Games(Game_id))
                        '''
        self.database.execute(createCommand)
        self.conn.commit()
        createCommand = '''
                        CREATE TABLE IF NOT EXISTS Games (
                        Game_id INTEGER,
                        Cate_id INTEGER,
                        Quest_id INTEGER,
                        category VARCHAR(255),
                        value INT,
                        question TEXT,
                        answer TEXT,
                        chosen INTEGER)
                        '''
        self.database.execute(createCommand)
        self.conn.commit()

        print("db made")

    def update_money(self, user_id, amount):
        cursor = self.database.execute("SELECT money FROM Jeopardy WHERE User_id=?",(user_id,))
        result = cursor.fetchone()
        if result is not None:
            current_money = result[0]
            new_money = int(current_money) + int(amount)
            self.database.execute("UPDATE Jeopardy SET money=? WHERE User_id=?",(new_money, user_id))
    def multiplayer_insert(self,user_id,server_id,game_id):
        self.database.execute("INSERT INTO Multiplayer (User_id, Server_id, Game_id) VALUES (?, ?, ?)", (user_id,server_id,game_id))
        self.conn.commit
    def insert_questions(self, category, value, question, answer, run, cate_id, quest_id):
        self.database.execute("INSERT INTO Games (Game_id, Cate_id, Quest_id, category, value, question, answer, chosen) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (run, cate_id, quest_id, category, value, question, answer, 1))
        self.conn.commit
    def countrows(self, game_id):
        cursor = self.database.execute("SELECT cate_id, quest_id FROM Games WHERE Game_id = ?", (game_id,))
        rows = cursor.fetchall()
        count = len(rows)
        return count, rows
    def countmultiplayer(self, game_id):
        cursor = self.database.execute("SELECT * FROM Multiplayer WHERE Game_id = ?", (game_id,))
        rows = cursor.fetchall()
        count = len(rows)
        return count
    def gamecheck(self, game_id, user_id):
        cursor = self.database.execute("SELECT * FROM Multiplayer WHERE Game_id = ? AND User_id = ?", (game_id,user_id))
        rows = cursor.fetchall()
        return rows
    def search_questions(self, category, value, game_id):

        cursor = self.database.execute("SELECT * FROM Games WHERE Game_id=? AND category=? AND value=? AND chosen=1", (int(game_id), category, int(value)))
        result = cursor.fetchall()

        if result:
            self.database.execute("UPDATE Games SET chosen = 0 WHERE Game_id=? AND category=? AND value=?", (int(game_id),str(category),int(value)))
            return result
        else:
            return []
    def get_game_categories(self, game_id):
        cursor = self.database.execute("SELECT DISTINCT category FROM Games WHERE Game_id=?", (game_id,))
        result = cursor.fetchall()
        return result
    def get_table_data(self, game_id):

        cursor = self.database.execute("SELECT category, value FROM Games WHERE chosen = 0 AND Game_id=?", (game_id,))
        result = cursor.fetchall()
        #print("RESULTS")
        #print(result)
        return result
    def check_game_state(self, game_id):

        cursor = self.database.execute("SELECT COUNT(*) FROM GAMES WHERE Game_id=? AND chosen = 1", (game_id,))
        result = cursor.fetchone()[0]
        #print("COUNT RESULTS")
        #print(result)
        return(result)


    def get_all_data(self):
        query = "SELECT * FROM Jeopardy"
        cursor = self.conn.execute(query)
        rows = cursor.fetchall()
        print("From Jeopardy:")
        for row in rows:
            print(row)
        query = "SELECT * FROM Games"
        cursor = self.conn.execute(query)
        rows = cursor.fetchall()
        print("From Games:")
        for row in rows:
            print(row)
        query = "SELECT * FROM Multiplayer"
        cursor = self.conn.execute(query)
        rows = cursor.fetchall()
        print("From Multiplayer:")
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
            query = 'INSERT INTO Jeopardy (User_id, Server_id, isInGame, money) VALUES (?, ?, 0, 0)'
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
                                  (int(value), user_id, server_id))
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

    def startgame(command, numberofcategories, myjeopardy, run):
        command = command.lower()
        if command == 'custom':     #Custom Game Solo: In Progress
            category_id=0

        #    print(f"{username} from: ({channel})")
            with open("jeopardydata.json", "w") as file: #empty file first
                myselectcategory = [None] * int(numberofcategories)
                for i in range(int(numberofcategories)):
                    question_id = 0
                    questions = []
                    while(len(questions) < 5):  #guarantees that there are 5 questions per category
                        myrand = random.randint(0, 2000)
                        selectcategory = GameStart.randomcategory(myrand)   #returns a randomly chosen category
                        category_id += 1
                        GameStart.savecategory(selectcategory, myjeopardy, run) #writes to jeopardydata.json
                        print(str(selectcategory) + " " + str(i) + " " + str(myrand) + " " + str(numberofcategories))
                        myselectcategory[i] = str(selectcategory)
                        questions = GameStart.savequestion(selectcategory)  #pulls questions data for the current category
                    for item in questions:
                        category = item['category']
                        value = item['value']
                        question = item['question']
                        answer = item['answer']
                        clean_answer = answer.replace("/", "")
                        question_id += 1
                        #print(category, value, question, answer)
                        myjeopardy.insert_questions(category, value, question, clean_answer, run, category_id, question_id)
            print("MYSELECTCAT")
            print(myselectcategory)
            return (myselectcategory)
    def pullquestion(category, value, game_id, myjeopardy):  #return the question that the user wanted
        #yes=myjeopardy.search_questions(1, value, game_id)
        #print("YES")
        #print(yes)
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
                #value = item["value"]
                question = item["question"]
                answer = item["answer"]
                #round = item["round"]
                #show_number = item["show_number"]
               # air_date = item["air_date"]
                question_data = {
                    "category": category,
                    "value": current_value,
                    "question": question,
                    "answer": answer,
               #     "round": round,
               #     "show_number": show_number,
                #    "air_date": air_date,
                }
                questions.append(question_data)
        return questions[0:5]
    def savecategory(givencategory, myjeopardy, run):    #save the category to a file
        questions = GameStart.savequestion(givencategory)
        try:
            with open("jeopardydata.json", "r") as file:
                data = json.load(file)
        except:
            data = []
        if data == []:
                data = questions[0:5]
        else:
                data.extend(questions[0:5])
        with open("jeopardydata.json", "w") as file:
            #print(data)
            json.dump(data, file, indent=4)




class Input:

    async def playgame(myjeopardy, ctx, arg, bot, run):
        money = 0
        user_id = ctx.author.id
        server_id = ctx.guild.id
        print(user_id)
        print(server_id)

        def checkifquit(m, game_id):
            if m.content == "quit":
                GameBoard.gameover(myjeopardy, m, game_id)
                print("Quitting")
                return True
            else:
                return False

        def check(m):  # only allow the author to answer
            return m.author == ctx.author

        handle = Input.myhandle(arg)  # user assumed to input "custom" to start a game

        if handle == 'custom':

            is_new_game = myjeopardy.start_game(user_id, server_id)
            if not is_new_game:
                print("User already in game")
                await ctx.send("You are already in a game")
                return
            else:
                print("User is not in game, making new one")
            intro = await ctx.send("How many categories would you like to play with? Pick between 1 and 5.")
            usermsg = await bot.wait_for('message', check=check)  # wait for author to type in answer
            if(checkifquit(usermsg, run)):
                await ctx.send("Ending game")
                return

            await usermsg.delete()
            await intro.delete()
            while not Input.checkcategoryamt(usermsg.content):
                await ctx.send("Please enter a valid int between 1 and 5")
                usermsg = await bot.wait_for('message', check=check)
                if (checkifquit(usermsg,run)):
                    await ctx.send("Ending game")
                    return
            # usermsg is how many categories to play with
            botmessage = await ctx.send("``` Choosing categories: ```")
            output = GameStart.startgame(arg, usermsg.content,myjeopardy, run)
            myjeopardy.get_all_data()

            #####   FORMATTING OF "Game"
            botmessageupdate = GameBoard.drawtable(output)
            #GameBoard.initcategories(output)
            #####

            #view = aView(run, myjeopardy, user_id)
            await botmessage.edit(content=botmessageupdate)  # Game table is drawn, categories and values printed
            while (1):
                usermsg = await bot.wait_for('message', check=check)  # wait for author to choose category
                if(checkifquit(usermsg, run)):
                    await ctx.send("Ending game")
                    return
                # categoryusermsg, valueusermsg = usermsg.content.split("# ") #user must type "Category# Value"
                while not Input.pickcategory(usermsg.content, myjeopardy, run):  # loop until category chosen correctly
                    error = await ctx.send("Please enter valid category")
                    await usermsg.delete()
                    await asyncio.sleep(1)
                    usermsg = await bot.wait_for('message', check=check)
                    if (checkifquit(usermsg, run)):
                        await ctx.send("Ending game")
                        return
                    await error.delete()
                await asyncio.sleep(1)
                await usermsg.delete()
                categoryusermsg, valueusermsg = usermsg.content.split("# ")  # user must type "Category# Value"
                botmessageupdate = GameBoard.updatetable(output, myjeopardy, run)
                question = GameStart.pullquestion(categoryusermsg, valueusermsg, run, myjeopardy)
                myquestion = await ctx.send(question["question"])  # SEND QUESTION
                print("Answer: " + question["answer"])
               # print(Input.hint_giver(question["answer"]))
                help = 0
                hint_answer=""
                hint_answer = Input.hint_giver(question["answer"], help, hint_answer)
                hinter = hint_answer
                hinter = hinter.replace('_', r'\_')
                bothint = await ctx.send(hinter)

                while(help < 4):
                   # hint_answer = await ctx.send(Input.hint_giver(question["answer"], help, hint_answer))
                    #print("Hint answer " + str(help) + " : " + hint_answer)
                    if(help > 0):
                        hint_answer = Input.hint_giver(question["answer"], help, hint_answer)
                        hinter = hint_answer
                        hinter = hinter.replace('_', r'\_')
                        #print("Hinter: " + hinter)
                        await bothint.edit(content=hinter)
                    usermsg = await bot.wait_for('message', check=check)
                    if(checkifquit(usermsg, run)):
                        await ctx.send("Ending game")
                        return
                    result = Input.answer(question["answer"], usermsg.content, valueusermsg,myjeopardy,user_id)
                    await botmessage.edit(content=botmessageupdate)  # UPDATE TABLE
                    if int(result) < 0:
                        help += 1
                        sendresult = await ctx.send("Wrong!", delete_after=5)
                        await usermsg.delete()
                        #sendresult = await ctx.send("Wrong, the correct response is: " + question["answer"])
                    else:
                        sendresult = await ctx.send("Correct!", delete_after=5)
                        await usermsg.delete()
                        break

                if int(result) < 0:
                    sendresult = await ctx.send("Wrong, the correct response is: " + question["answer"], delete_after=5)

                money += int(result)
                prize = await ctx.send("You got " + result)
                await asyncio.sleep(5)
                #await usermsg.delete()
                await myquestion.delete()
                await bothint.delete()
                #await sendresult.delete()
                await prize.delete()
                if GameBoard.gameover(myjeopardy, usermsg, run): break
                # if GameBoard.gameover is True: break
            await ctx.send("You earned " + str(money))
            await ctx.send("Thanks for playing!")
            #myjeopardy.end_game(user_id, server_id)

        if handle == 'multi':
            view = MyView(timeout=15)

            button_message = await ctx.send("Click to join the game!", view=view)
            await asyncio.sleep(8)
            print("After waiting here is db")
            myjeopardy.get_all_data()
            await ctx.message.delete()
            await button_message.delete()
            clicked_user_ids = view.get_clicked_user_ids()
            clicked_user_names = view.get_clicked_user_names()
            #await ctx.send(f"The following users clicked the button: {clicked_user_ids}")
           # await ctx.send(f"Players: {clicked_user_names}")
            for user_id in clicked_user_ids:
                is_new_game = myjeopardy.start_game(user_id, server_id)
                if not is_new_game:
                    print("User already in game " + str(user_id))
                    user = await bot.fetch_user(user_id)
                    await ctx.send(str(user.name) + " is being removed because they are already in a game", delete_after=5)
                    clicked_user_ids.remove(user_id)
                    clicked_user_names.remove(user.name)
                else:
                    print("User is not in a previous game, can continue")
                    myjeopardy.multiplayer_insert(user_id, server_id, run)
            await ctx.send(f"Players: {clicked_user_names}")
            if not clicked_user_ids:
                await ctx.send("Nobody joined")
                return
            # usermsg is how many categories to play with
            botmessage = await ctx.send("``` Choosing categories: ```")

            output = GameStart.startgame("custom", 5,myjeopardy, run)
            myjeopardy.get_all_data()

            #####   FORMATTING OF "Game"
            botmessageupdate = GameBoard.drawtable(output)
            #GameBoard.initcategories(output)
            #####
            #First person to pick is the host
            newview = aView(run, myjeopardy, ctx.author.id, ctx, botmessage, bot)
            await botmessage.edit(content=botmessageupdate, view=newview)  # Game table is drawn, categories and values printed
            cat = myjeopardy.get_game_categories(run)
            categories = [r[0] for r in cat]

            while True:
                botmessageupdate = GameBoard.updatetable(categories, myjeopardy, run)
                await botmessage.edit(content=botmessageupdate, view=newview)  # Game table is drawn, categories and values printed
                if GameBoard.gameover(myjeopardy, botmessage,run):
                    break
                #print(newview.is_quit())
                if newview.is_quit():
                    break
            for user_id in clicked_user_ids:
                myjeopardy.update_is_in_game(user_id,server_id,0)
            await ctx.send("Game over")


        myjeopardy.end_game(user_id, server_id)
    def checkcategoryamt(input):    #make sure user wants reasonable amount of categories, it takes substantial time to make one
        try:
            value = int(input)
            if value >= 1 and value <= 5:
                return True
            else:
                return False
        except ValueError:
            return False
    def myhandle(arg):  #lowercase
        arg = arg.lower()
        if arg == 'custom':
            return arg
        if arg == 'multi':
            return arg
        return -1

    def hint_giver(answer, round, previous_results):
        words = answer.split()
        result = ""
        for word in words:
            for i, c in enumerate(word):
                if i == 0 or c in previous_results:
                    result += c
                else:
                    result += "_"
            result += " "
        num_hints = round
        for i in range(num_hints):
            #choose a random word to reveal a character for
            words_with_underscores = [w for w in result.split() if "_" in w]
            if words_with_underscores:
                word_to_reveal = random.choice(words_with_underscores)
                underscore_index = word_to_reveal.index("_")
                correct_char = answer[result.index(word_to_reveal) + underscore_index]
                result = result[:result.index(word_to_reveal) + underscore_index] + correct_char + result[result.index(word_to_reveal) + underscore_index + 1:]
        result = result.strip()
        print("hidden answer: " + result)
        return result

    def answer(answer, arg, value, myjeopardy, user_id):
        answer = answer.lower()
        arg = arg.lower()
        similarity_ratio = difflib.SequenceMatcher(None, answer, arg).ratio()
        if similarity_ratio >= 0.8:
            myjeopardy.update_money(user_id, value)
            return str(value)
        else:
            thisvalue = "-" + str(value)
            myjeopardy.update_money(user_id, int(thisvalue))
            return str("-" + value)
    def pickcategory(input, myjeopardy, game_id):    #verify the user picked a proper category and value, it must exist for it to return true

        categoryusermsg, valueusermsg = input.split("# ")  # user must type "Category# Value"
        result = myjeopardy.search_questions(categoryusermsg,valueusermsg, game_id)
        print(result)
        if result:
        #print(result)
            print("returning true")
            return True
        else:
            print("returning false")
            return False



class aView(View):
    def __init__(self, game_id, myjeopardy, user_id, ctx, botmessage,bot):
        super().__init__()
        self.quit = False
        self.game_id = game_id
        self.user_id = user_id
        self.myjeopardy = myjeopardy
        self.ctx = ctx
        self.bot = bot
        self.botmessage = botmessage
        self.cat = myjeopardy.get_game_categories(game_id)
        self.inround = False
        print(self.cat[0][0])
        print(self.cat[1][0])
        #myjeopardy.search_questions(self.cat[0], 200, game_id)



    #Multiplayer game is hardcoded to have 5 categories, so there must be 25 buttons for each category and question
    async def pick_question(self, category, value):
        self.inround = True
        def check(m):  # only allow the author to answer
            return m.author.id == self.user_id
        def mycheck(m):
            if(self.myjeopardy.gamecheck(self.game_id,m.author.id)):
                return m.author.id

        prompt = self.myjeopardy.search_questions(str(category), int(value), self.game_id)
        question = ", ".join([r[5] for r in prompt])
        answer = ", ".join([r[6] for r in prompt])
        print(question)
        botquestion = await self.ctx.send(question)
        print(answer)
        usermsg = await self.bot.wait_for('message', check=check)
        print(usermsg.content)

        result = Input.answer(answer, usermsg.content, str(value),self.myjeopardy,self.user_id)
        if int(result) < 0:
            playercount = self.myjeopardy.countmultiplayer(self.game_id)
            count=0
            await self.ctx.send(str(usermsg.author) + " got it wrong", delete_after=3)
            await self.ctx.send("First person to give an answer",delete_after=5)
            newuser = await self.bot.wait_for('message', check=mycheck)
            await self.ctx.send(str(newuser.author) + " was first", delete_after=3)
            result = Input.answer(answer, newuser.content, str(value),self.myjeopardy,newuser.author.id)
            if int(result) < 0:
                await self.ctx.send(str(newuser.author) + " got it wrong too",delete_after=3)
            else:   #new person got it right so set them to pick next category
                await self.ctx.send(str(newuser.author) + " got it right!",delete_after=3)
                print(newuser.author.id)
                self.set_user_id(newuser.author.id)
                #self.myjeopardy.get_all_data()
            await newuser.delete()
        else:
            await self.ctx.send(str(usermsg.author) + " got it right!",delete_after=3)
            self.set_user_id(usermsg.author.id)
        await usermsg.delete()
        await botquestion.delete()
        self.inround = False
        await self.ctx.send("Round over", delete_after=3)
    def set_user_id(self, user_id): #setter function to change whose turn it is
        self.user_id = user_id

    @discord.ui.button(label="Cat 1, Quest 1", custom_id="CQ 11")
    async def callback11(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self.inround:
            user_id = interaction.user.id
            if self.user_id != user_id:
                #user is not allowed to select this button
                print("user is not allowed to select this button")
                return
            print(f"Button {button.custom_id} clicked by user {user_id}")
            button.disabled = True
            await self.pick_question(self.cat[0][0], 200)


    @discord.ui.button(label="Cat 1, Quest 2", custom_id="CQ 12")
    async def callback12(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self.inround:
            user_id = interaction.user.id
            if self.user_id != user_id:
                #user is not allowed to select this button
                print("user is not allowed to select this button")
                return
            print(f"Button {button.custom_id} clicked by user {user_id}")
            button.disabled = True
            await self.pick_question(self.cat[0][0], 400)

    @discord.ui.button(label="Cat 1, Quest 3", custom_id="CQ 13")
    async def callback13(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self.inround:
            user_id = interaction.user.id
            if self.user_id != user_id:
                #user is not allowed to select this button
                print("user is not allowed to select this button")
                return
            print(f"Button {button.custom_id} clicked by user {user_id}")
            button.disabled = True
            await self.pick_question(self.cat[0][0], 600)

    @discord.ui.button(label="Cat 1, Quest 4", custom_id="CQ 14")
    async def callback14(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self.inround:
            user_id = interaction.user.id
            if self.user_id != user_id:
                #user is not allowed to select this button
                print("user is not allowed to select this button")
                return
            print(f"Button {button.custom_id} clicked by user {user_id}")
            button.disabled = True
            await self.pick_question(self.cat[0][0], 800)


    @discord.ui.button(label="Cat 1, Quest 5", custom_id="CQ 15")
    async def callback15(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self.inround:
            user_id = interaction.user.id
            if self.user_id != user_id:
                #user is not allowed to select this button
                print("user is not allowed to select this button")
                return
            print(f"Button {button.custom_id} clicked by user {user_id}")
            button.disabled = True
            await self.pick_question(self.cat[0][0], 1000)


    @discord.ui.button(label="Cat 2, Quest 1", custom_id="CQ 21")
    async def callback21(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self.inround:
            user_id = interaction.user.id
            if self.user_id != user_id:
                #user is not allowed to select this button
                print("user is not allowed to select this button")
                return
            print(f"Button {button.custom_id} clicked by user {user_id}")
            button.disabled = True
            await self.pick_question(self.cat[1][0], 200)


    @discord.ui.button(label="Cat 2, Quest 2", custom_id="CQ 22")
    async def callback22(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self.inround:
            user_id = interaction.user.id
            if self.user_id != user_id:
                #user is not allowed to select this button
                print("user is not allowed to select this button")
                return
            print(f"Button {button.custom_id} clicked by user {user_id}")
            button.disabled = True
            await self.pick_question(self.cat[1][0], 400)


    @discord.ui.button(label="Cat 2, Quest 3", custom_id="CQ 23")
    async def callback23(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self.inround:
            user_id = interaction.user.id
            if self.user_id != user_id:
                #user is not allowed to select this button
                print("user is not allowed to select this button")
                return
            print(f"Button {button.custom_id} clicked by user {user_id}")
            button.disabled = True
            await self.pick_question(self.cat[1][0], 600)


    @discord.ui.button(label="Cat 2, Quest 4", custom_id="CQ 24")
    async def callback24(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self.inround:
            user_id = interaction.user.id
            if self.user_id != user_id:
                #user is not allowed to select this button
                print("user is not allowed to select this button")
                return
            print(f"Button {button.custom_id} clicked by user {user_id}")
            button.disabled = True
            await self.pick_question(self.cat[1][0], 800)


    @discord.ui.button(label="Cat 2, Quest 5", custom_id="CQ 25")
    async def callback25(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self.inround:
            user_id = interaction.user.id
            if self.user_id != user_id:
                #user is not allowed to select this button
                print("user is not allowed to select this button")
                return
            print(f"Button {button.custom_id} clicked by user {user_id}")
            button.disabled = True
            await self.pick_question(self.cat[1][0], 1000)
    @discord.ui.button(label="Cat 3, Quest 1", custom_id="CQ 31")
    async def callback31(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self.inround:
            user_id = interaction.user.id
            if self.user_id != user_id:
                #user is not allowed to select this button
                print("user is not allowed to select this button")
                return
            print(f"Button {button.custom_id} clicked by user {user_id}")
            button.disabled = True
            await self.pick_question(self.cat[2][0], 200)

    @discord.ui.button(label="Cat 3, Quest 2", custom_id="CQ 32")
    async def callback32(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self.inround:
            user_id = interaction.user.id
            if self.user_id != user_id:
                #user is not allowed to select this button
                print("user is not allowed to select this button")
                return
            print(f"Button {button.custom_id} clicked by user {user_id}")
            button.disabled = True
            await self.pick_question(self.cat[2][0], 400)

    @discord.ui.button(label="Cat 3, Quest 3", custom_id="CQ 33")
    async def callback33(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self.inround:
            user_id = interaction.user.id
            if self.user_id != user_id:
                #user is not allowed to select this button
                print("user is not allowed to select this button")
                return
            print(f"Button {button.custom_id} clicked by user {user_id}")
            button.disabled = True
            await self.pick_question(self.cat[2][0], 600)

    @discord.ui.button(label="Cat 3, Quest 4", custom_id="CQ 34")
    async def callback34(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self.inround:
            user_id = interaction.user.id
            if self.user_id != user_id:
                #user is not allowed to select this button
                print("user is not allowed to select this button")
                return
            print(f"Button {button.custom_id} clicked by user {user_id}")
            button.disabled = True
            await self.pick_question(self.cat[2][0], 800)

    @discord.ui.button(label="Cat 3, Quest 5", custom_id="CQ 35")
    async def callback35(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self.inround:
            user_id = interaction.user.id
            if self.user_id != user_id:
                #user is not allowed to select this button
                print("user is not allowed to select this button")
                return
            print(f"Button {button.custom_id} clicked by user {user_id}")
            button.disabled = True
            await self.pick_question(self.cat[2][0], 1000)

    @discord.ui.button(label="Cat 4, Quest 1", custom_id="CQ 41")
    async def callback41(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self.inround:
            user_id = interaction.user.id
            if self.user_id != user_id:
                #user is not allowed to select this button
                print("user is not allowed to select this button")
                return
            print(f"Button {button.custom_id} clicked by user {user_id}")
            button.disabled = True
            await self.pick_question(self.cat[3][0], 200)

    @discord.ui.button(label="Cat 4, Quest 2", custom_id="CQ 42")
    async def callback42(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self.inround:
            user_id = interaction.user.id
            if self.user_id != user_id:
                #user is not allowed to select this button
                print("user is not allowed to select this button")
                return
            print(f"Button {button.custom_id} clicked by user {user_id}")
            button.disabled = True
            await self.pick_question(self.cat[3][0], 400)

    @discord.ui.button(label="Cat 4, Quest 3", custom_id="CQ 43")
    async def callback43(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self.inround:
            user_id = interaction.user.id
            if self.user_id != user_id:
                #user is not allowed to select this button
                print("user is not allowed to select this button")
                return
            print(f"Button {button.custom_id} clicked by user {user_id}")
            button.disabled = True
            await self.pick_question(self.cat[3][0], 600)

    @discord.ui.button(label="Cat 4, Quest 4", custom_id="CQ 44")
    async def callback44(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self.inround:
            user_id = interaction.user.id
            if self.user_id != user_id:
                #user is not allowed to select this button
                print("user is not allowed to select this button")
                return
            print(f"Button {button.custom_id} clicked by user {user_id}")
            button.disabled = True
            await self.pick_question(self.cat[3][0], 800)

    @discord.ui.button(label="Cat 4, Quest 5", custom_id="CQ 45")
    async def callback45(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self.inround:
            user_id = interaction.user.id
            if self.user_id != user_id:
                #user is not allowed to select this button
                print("user is not allowed to select this button")
                return
            print(f"Button {button.custom_id} clicked by user {user_id}")
            button.disabled = True
            await self.pick_question(self.cat[3][0], 1000)

    @discord.ui.button(label="Cat 5, Quest 1", custom_id="CQ 51")
    async def callback51(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self.inround:
            user_id = interaction.user.id
            if self.user_id != user_id:
                #user is not allowed to select this button
                print("user is not allowed to select this button")
                return
            print(f"Button {button.custom_id} clicked by user {user_id}")
            button.disabled = True
            await self.pick_question(self.cat[4][0], 200)

    @discord.ui.button(label="Cat 5, Quest 2", custom_id="CQ 52")
    async def callback52(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self.inround:
            user_id = interaction.user.id
            if self.user_id != user_id:
                #user is not allowed to select this button
                print("user is not allowed to select this button")
                return
            print(f"Button {button.custom_id} clicked by user {user_id}")
            button.disabled = True
            await self.pick_question(self.cat[4][0], 400)

    @discord.ui.button(label="Cat 5, Quest 3", custom_id="CQ 53")
    async def callback53(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self.inround:
            user_id = interaction.user.id
            if self.user_id != user_id:
                #user is not allowed to select this button
                print("user is not allowed to select this button")
                return
            print(f"Button {button.custom_id} clicked by user {user_id}")
            button.disabled = True
            await self.pick_question(self.cat[4][0], 600)

    @discord.ui.button(label="Cat 5, Quest 4", custom_id="CQ 54")
    async def callback54(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self.inround:
            user_id = interaction.user.id
            if self.user_id != user_id:
                #user is not allowed to select this button
                print("user is not allowed to select this button")
                return
            print(f"Button {button.custom_id} clicked by user {user_id}")
            button.disabled = True
            await self.pick_question(self.cat[4][0], 800)

    @discord.ui.button(label="Cat 5, Quest 5", custom_id="CQ 55")
    async def callback55(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self.inround:
            user_id = interaction.user.id
            if self.user_id != user_id:
                #user is not allowed to select this button
                print("user is not allowed to select this button")
                return
            print(f"Button {button.custom_id} clicked by user {user_id}")
            button.disabled = True
            await self.pick_question(self.cat[4][0], 1000)


    def is_quit(self):
        if(self.quit):
            return True
        else:
            return False

class MyView(View):
    def __init__(self, timeout):
        super().__init__(timeout=timeout)
        self.clicked_users = []
        self.clicked_users_ids = []
    @discord.ui.button(label="Join", style=discord.ButtonStyle.primary, custom_id="join_button")
    async def button_callback(self, button, interaction):
        user_id = interaction.user.id
        print(interaction.user.name)
        guild_id = interaction.guild.id
        if user_id in self.clicked_users_ids:
            await interaction.response.send_message(f"{interaction.user.mention} has already joined the lobby.", delete_after=5)
        else:
            self.clicked_users.append(interaction.user.name)
            self.clicked_users_ids.append(user_id)

            await interaction.response.send_message(f"{interaction.user.mention} has joined the lobby.", delete_after=5)

    @discord.ui.button(label="Leave", style=discord.ButtonStyle.primary, custom_id="leave_button")
    async def leave_button_callback(self, button, interaction):
        user_id = interaction.user.id
        print(interaction.user.name)
        if user_id in self.clicked_users_ids:
            self.clicked_users.remove(interaction.user.name)
            self.clicked_users_ids.remove(user_id)
            await interaction.response.send_message(f"{interaction.user.mention} has left the lobby.", delete_after=5)
        else:
            await interaction.response.send_message(f"{interaction.user.mention} is not in the lobby.", delete_after=5)

    def get_clicked_user_ids(self):
        return self.clicked_users_ids.copy()
    def get_clicked_user_names(self):
        return self.clicked_users.copy()
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

    def updatetable(categories, myjeopardy, game_id):   #update the table message, save the deletions so game can progress

        rows = myjeopardy.get_table_data(game_id)
        values = [200, 400, 600, 800, 1000]
        game_dict = {}
        for category in categories:
            game_dict[category] = [v if v not in [row[1] for row in rows if row[0] == category] else None for v in
                                   values]
        #print(game_dict)
        message = "```\nCategories:\n"
        longest_category_length = max(len(category) for category in categories)
        for i, category in enumerate(categories):
            message += category + " " * (longest_category_length - len(category)) + "\t\t"
            for value in values:
                if game_dict.get(category, [None, None, None, None, None])[values.index(value)] is None:
                    message += "     \t"
                else:
                    message += str(value) + "\t"
            message += "\n"
        message += "```"
        return message


    def gameover(myjeopardy, user, game_id):        #check to see if all values are null for game over
        count = myjeopardy.check_game_state(game_id)

        if(user.content == "quit"):
            print("Quiting because user said so")

            myjeopardy.end_game(user.author.id, user.guild.id)
            return True
        if count == 0:
            return True
        else:
            return False

