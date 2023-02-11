#Jake Onkka --Jeopardy Features --CSE320
import json



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
                "air_date": air_date,
            }
            questions.append(question_data)
    # Sort the list of questions by value
    sorted_questions = sorted(questions, key=lambda x: int(x["value"].replace("$", "").replace(",", ""))) #comparing by strings give wrong value comparison, convert to int

    # Create a new list that only includes questions with unique values
    ordered_List = []
    seen_values = set()
    for q in sorted_questions:
        if q["value"] not in seen_values:
            ordered_List.append(q)
            seen_values.add(q["value"])

    print(ordered_List[0])  #Testing to make sure lowest value to highest value
    print(ordered_List[1])
    print(ordered_List[2])
    print(ordered_List[3])
    print(ordered_List[4])
    print(ordered_List[5])