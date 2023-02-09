#Jake Onkka --Jeopardy Features --CSE320

def startgame(command, username, channel):
    command = command.lower()
    if command == 'custom':     #Custom Game Solo: In Progress
        print(f"{username} from: ({channel})")
        #return str("Hello " + username + " what category do you want?")
        return "Hello"
    if command == 'start':      #Multiplayer Feature: TO-DO
        return 'TBA'

    return 'Invalid'