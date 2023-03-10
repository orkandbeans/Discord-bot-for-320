#Jake Onkka --Jeopardy Features --CSE320
import json
import random
class GameStart:
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
            print(value)
            print(category)
            for i in range(len(data)):
                print(data[i]["category"])
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
            json.dump(data, file, indent=4)

class Input:
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
            print(categoryusermsg)
            print(valueusermsg)
            with open("categorystate.json","r") as file:
                current_categories = json.load(file)
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
    def gameover(hello):        #check to see if all values are null for game over
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