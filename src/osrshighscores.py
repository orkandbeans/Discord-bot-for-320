#Name: John Gregerson --- Course: CS320 --- Assignment: MainProject Feature 2: osrs_highscores

#DESCRIPTION: This feature formats a query for the jagex highscores API, parses the returned information and
# displays the results to the user.
import requests # API call package
import mwparserfromhell # Full Name - Media Wiki Parser from Hell
import unittest

def osrshighscores(player_name: str, second_player_name: str, game_mode: str, activity: str, metric: str):

    mode = game_mode.lower()
    player_one = player_name.lower().replace(" ", "_")
    player_two = second_player_name.lower().replace(" ", "_")
   
    if player_name == "":
        #(print help message)
        pass 
    else:
    #send request for and store player 1 scores
        player_one_url = constructrequest(player_one, mode)
        player_one_scores = requests.get(player_one_url)
        # check api response code
        parsed_player_one = parsetextresponse(player_one_scores.text)

    if second_player_name != "":
    #send request for and store player 2 scores
        player_two_url = constructrequest(player_two, mode)
        player_two_scores = requests.get(player_two_url)
        isCompareRequest = True
        #check api response code
        parsed_player_two = parsetextresponse(player_two_scores.text)
    else:
        isCompareRequest = False

    if isCompareRequest == True:
        compared_scores = comparescores(parsed_player_one, parsed_player_two)
        output = constructcomparisonoutput(parsed_player_one, parsed_player_two, compared_scores)
    else:
        output = constructsingleoutput(parsed_player_one)

    return output
    

    # construct and send request
def constructrequest(player_name: str, game_mode: str):
    
    if game_mode == "":
        #normal highscores
        mode = ""
    elif ((game_mode.find('hard') != -1) | (game_mode == "hcim") | (game_mode == "hc")):
        mode = "_hardcore_ironman"
    elif ((game_mode.find('ult') != -1) | (game_mode == "uim")):
        mode = "_ultimate"
    elif ((game_mode.find('iron') != -1) | (game_mode == "im")):
        mode = "_ironman"
    else:
        return("error")

    return("https://secure.runescape.com/m=hiscore_oldschool" + mode + "/index_lite.ws?player=" + player_name)

def parsetextresponse(api_response: str):

    #list of keys for pairing player scores to activities
    skill_list = ["Overall", "Attack", "Defence", "Strength", "Hitpoints",
                    "Ranged", "Prayer", "Magic", "Cooking", "Woodcutting",
                    "Fletching", "Fishing", "Firemaking", "Crafting", "Smithing", 
                    "Mining", "Herblore", "Agility", "Thieving", "Slayer", 
                    "Farming", "Runecrafting", "Hunter", "Construction"]
     
    activity_list = ["League Points", "Bounty Hunter - Hunter", "Bounty Hunter - Rogue", "Clue Scrolls (all)", "Clue Scrolls (beginner)",
                    "Clue Scrolls (easy)", "Clue Scrolls (medium)", "Clue Scrolls (hard)", "Clue Scrolls (elite)", "Clue Scrolls (master)",
                    "LMS - Rank", "PvP, Arena - Rank", "Soul Wars Zeal", "Rifts closed", "Abyssal Sire",
                    "Alchemical Hydra", "Artio", "Barrows Chests", "Bryophyta", "Callisto",
                    "Cal'varion", "Cerberus", "Chambers of Xeric", "Chambers of Xeric: Challenge Mode", "Chaos Elemental",
                    "Chaos Fanatic", "Commander Zilyana", "Corporeal Beast", "Crazy Archaeologist", "Dagannoth Prime",
                    "Dagannoth Rex", "Dagannoth Supreme", "Deranged Archaeologist", "General Graardor", "Giant Mole",
                    "Grotesque Guardians", "Hespori", "Kalphite Queen", "King Black Dragon", "Kraken",
                    "Kree'Arra", "K\'ril Tsutsaroth", "Mimic", "Nex", "Nightmare", 
                    "Phosani\'s Nightmare", "Obor", "Phantom Muspah", "Sarachnis", "Scorpia",
                    "Skotizo", "Spindel", "Tempoross", "The Gauntlet", "The Corrupted Gauntlet",
                    "Theatre of Blood", "Theatre of Blood: Hard Mode", "Thermonuclear Smoke Devil", "Tombs of Amascut", "Tombs of Amascut: Expert Mode",
                    "TzKal-Zuk", "TzTok-Jad", "Venenatis", "Vet\'ion", "Vorkath",
                    "Wintertodt", "Zalcano", "Zulrah",]
    
    api_response = api_response.replace('\n', ',').replace('-1', 'unranked')
    raw_player_scores = api_response.split(",")

    formatted_player_scores = []
    
    i = 0

    for x in skill_list:
        skill = [x, raw_player_scores[i], raw_player_scores[i+1], raw_player_scores[i+2]]
        formatted_player_scores.append(skill)
        i+= 3
    
    for x in activity_list:
        activity = [x, raw_player_scores[i], raw_player_scores[i+1]]
        formatted_player_scores.append(activity)
        i+=2

    return formatted_player_scores

def comparescores(player_one_scores_list: list, player_two_scores_list: list):
    # if a second player is specified find the difference
    pass

def constructsingleoutput(player_one_scores_list: list):
    output_list = []

    j = 0
    output_list.append("-----------------------------------------------------------------------------------------------------\n")
    activity_index = 0
    for i in player_one_scores_list:
        if activity_index < 24:
            output_list[j] += i[0] + ": " + i[1] + ", " + i[2] + ", " + i[3] + "\n" 
        else:
            output_list[j] += i[0] + ": " + i[1] + ", " + i[2] + "\n"
        activity_index += 1
        if(len(output_list[j]) > 1500):
            j += 1
            output_list.append("")
    output_list[j] += "-----------------------------------------------------------------------------------------------------\n"
    return output_list

def constructcomparisonoutput(player_one_scores: list, player_two_scores_list: list, score_difference_list: list):
    #two players specified
    pass

def errormessage():
    #improper arguments or api response
    pass

def main():
    my_scores = osrshighscores("pvm_gohone", "", "iron", "", "")
                             
    print(type(my_scores))
    print(my_scores)

if __name__ == "__main__":
    main()