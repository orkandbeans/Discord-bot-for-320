#Jake Onkka --Jeopardy Features --CSE320
import json
import random
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
def startgame(command, numberofcategories):#, username, channel):

    command = command.lower()
    if command == 'custom':     #Custom Game Solo: In Progress
    #    print(f"{username} from: ({channel})")
        with open("jeopardydata.txt", "w") as file: #empty file first
            myselectcategory = [None] * int(numberofcategories)
            for i in range(int(numberofcategories)):
                myrand = random.randint(0, 1000)
                selectcategory = randomcategory(myrand)
                savecategory(selectcategory)
                print(str(selectcategory) + " " + str(i) + " " + str(myrand) + " " + str(numberofcategories))
                myselectcategory[i] = str(selectcategory)
                questions = savequestion(selectcategory)
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
        if item[
            "category"] == givencategory:  # check through every item and match based on category and save it's information
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
    questions = savequestion(givencategory)
    # Sort the list of questions by value
    sorted_questions = sorted(questions, key=lambda x: int(x["value"].replace("$", "").replace(",", "")) if x["value"] is not None else 0) #comparing by strings give wrong value comparison, convert to int
    ordered_List = []   #order the list by value, least -> greatest
    seen_values = set()
    for q in sorted_questions:
        if q["value"] is not None and int(q["value"].replace("$", "").replace(",", "")) != 0:
            if q["value"] not in seen_values:
                ordered_List.append(q)
                seen_values.add(q["value"])
    with open("jeopardydata.txt", "a") as file:     #save the dict into a temp file, this temp file will be used to play the game
        for x in range(len(ordered_List)):
            file.write(str(ordered_List[x]))
