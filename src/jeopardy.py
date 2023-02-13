#Jake Onkka --Jeopardy Features --CSE320
import json
import random

class GameStart:
    def startgame(command, numberofcategories):#, username, channel):
        ##########

        ##########
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
                #print(myselectcategory)
            return (myselectcategory)
            #return (questions[0])

    """
                data = json.load(file)
                chosencategories = []
                chosencategories[0] = data[0]['category']
                for x in range(len(data)):
                    if data[x]['category'] != chosencategories[x]:
                        chosencategories[x] = data[x]['category']
    """
            #print(chosencategories)
            #return (questions[0])
    def pullquestion(category, value):
        with open("jeopardydata.json", "r") as file:
            data = json.load(file)
            myvalue = "$"
            myvalue += value
            #print(data)
            for i in range(len(data)):
                #print(data[i])
                if data[i]["category"] == category and data[i]["value"] == myvalue:
                    print(data[i])
                    return data[i]
    def randomcategory(myrand):
        with open("JEOPARDY_QUESTIONS1.json", "r") as file:
            data = json.load(file)
            return (data[myrand]['category'])
    def savequestion(givencategory):
        with open("JEOPARDY_QUESTIONS1.json", "r") as file:  # THIS IS A LOCAL FILE, IT IS VERY BIG :)
            data = json.load(file)
        questions = []  # save questions in here
        #    category = "HISTORY"    #select a category
        for item in data:
            if item["category"] == givencategory:  # check through every item and match based on category and save it's information
                category = item["category"]
                value = item["value"]
                question = item["question"]
                answer = item["answer"]
                round = item["round"]
                show_number = item["show_number"]
                air_date = item["air_date"]
                question_data = {
                    "category": category,
                    "value": value,
                    "question": question,
                    "answer": answer,
                    "round": round,
                    "show_number": show_number,
                    "air_date": air_date,
                }
                questions.append(question_data)
        return questions
    def savecategory(givencategory):
        questions = GameStart.savequestion(givencategory)
        # Sort the list of questions by value
        sorted_questions = sorted(questions, key=lambda x: int(x["value"].replace("$", "").replace(",", "")) if x["value"] is not None else 0) #comparing by strings give wrong value comparison, convert to int
        ordered_List = []   #order the list by value, least -> greatest
        seen_values = set()
        for q in sorted_questions:
            if q["value"] is not None and int(q["value"].replace("$", "").replace(",", "")) != 0:
                if q["value"] not in seen_values:
                    ordered_List.append(q)
                    seen_values.add(q["value"])
        #with open("jeopardydata.json", "r") as files:     #save the dict into a temp file, this temp file will be used to play the game
        try:
            with open("jeopardydata.json", "r") as file:
                data = json.load(file)
        except:
            data = []
        if data == []:
                data = ordered_List
        else:
                #print(data)
                data.extend(ordered_List)
        with open("jeopardydata.json", "w") as file:
            json.dump(data, file, indent=4)

class Input:
    def checkcategoryamt(input):
        try:
            value = int(input)
            if value >= 0 and value <= 6:
                return True
            else:
                return False
        except ValueError:
            return False
    def myhandle(arg):
        arg = arg.lower()
        if arg == 'custom':
            return arg
        return -1

    def answer(answer, arg, value):
        answer = answer.lower()
        arg = arg.lower()
        if arg == answer:
            return str(value)
        if arg != answer:
            return str("-" + value)
class GameBoard:
    def drawtable(categories):
        values = [[200, 400, 600, 800, 1000] for i in range(len(categories))]

        message = "```\nCategories:\n"

        # Find the length of the longest category
        longest_category_length = max(len(category) for category in categories)

        for category_index, category in enumerate(categories):
            message += category + " " * (longest_category_length - len(category)) + "\t\t"
            for value in values[category_index]:
                if value is not None:
                    message += str(value) + "\t"
                else:
                    message += " " * len(str(value)) + "\t"
            message += "\n"

        message += "```"
        return message
    def updatetable(categories, category, value):
        values = [[200, 400, 600, 800, 1000] for i in range(len(categories))]
        myvalues = [200, 400, 600, 800, 1000]
        value_index = myvalues.index(value)
        category_index = categories.index(category)
        values[category_index][value_index] = None      #delete the value of a specified category
        message = "```\nCategories:\n"
        longest_category_length = max(len(category) for category in categories)     #reformatting same as drawtable

        for category_index, category in enumerate(categories):
            message += category + " " * (longest_category_length - len(category)) + "\t\t"
            for value in values[category_index]:
                if value is not None:
                    message += str(value) + "\t"
                else:
                    message += " " * len(str(value)) + "\t"
            message += "\n"

        message += "```"
        return message