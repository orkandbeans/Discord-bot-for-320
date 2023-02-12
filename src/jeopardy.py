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
def startgame(command):#, username, channel):
    command = command.lower()
    if command == 'custom':     #Custom Game Solo: In Progress
    #    print(f"{username} from: ({channel})")
        openfile("HISTORY")
 #       openfile("3-LETTER WORDS")
    questions = savequestion("HISTORY")
    return (questions[random.randint(0,5)])

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
def openfile(givencategory):
    questions = savequestion(givencategory)
    # Sort the list of questions by value
    sorted_questions = sorted(questions, key=lambda x: int(x["value"].replace("$", "").replace(",", ""))) #comparing by strings give wrong value comparison, convert to int
    ordered_List = []   #order the list by value, least -> greatest
    seen_values = set()
    for q in sorted_questions:
        if q["value"] not in seen_values:
            ordered_List.append(q)
            seen_values.add(q["value"])
    with open("jeopardydata.txt", "w") as file:     #save the dict into a temp file, this temp file will be used to play the game
        for x in range(6):
            file.write(str(ordered_List[x]))
