#Jake Onkka --Jeopardy Features --CSE320
import json

import lamda as lamda


def startgame(command):#, username, channel):
    command = command.lower()
    if command == 'custom':     #Custom Game Solo: In Progress
    #    print(f"{username} from: ({channel})")
        openfile()
        #return str("Hello " + username + " what category do you want?")
        return "Hello"
    if command == 'start':      #Multiplayer Feature: TO-DO
        return 'TBA'

    return 'Invalid'

def openfile():
    with open("JEOPARDY_QUESTIONS1.json", "r") as file:     #THIS IS A LOCAL FILE, IT IS VERY BIG :)
        data = json.load(file)
    questions = []          #save questions in here
    category = "HISTORY"    #select a category
    for item in data:
        if item["category"] == category:    #check through every item and match based on category and save it's information
            value = item["value"]
            question = item["question"]
            answer = item["answer"]
            round = item["round"]
            show_number = item["show_number"]
            air_date = item["air_date"]
        question_data = {
            "value": value,
            "question": question,
            "answer": answer,
            "round": round,
            "show_number": show_number,
            "air_date": air_date
        }
        questions.append(question_data)
    print(questions[0])     #testing