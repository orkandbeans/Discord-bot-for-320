#Name: John Gregerson --- Course: CS320 --- Assignment: MainProject Feature 2: osrs_highscores

#DESCRIPTION: This feature formats a query for the jagex highscores API, parses the returned information and
# displays the results to the user.
import requests # API call package
import mwparserfromhell # Full Name - Media Wiki Parser from Hell
import unittest

def osrshighscores(player_name: str, second_player_name: str, game_mode: str, activity: int, metric: str):

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
        # parse text response

    if second_player_name != "":
        #send request for and store player 2 scores
        player_two_url = constructrequest(player_two, mode)
        player_two_scores = requests.get(player_two_url)
        isCompareRequest = True
        #check api response code
        # parse text response
    else:
        isCompareRequest = False

    if isCompareRequest == True:
        # perform calculations
        # construct and return comparison output message
        pass
    # construct and return single output message
    return
    

    # construct and send request
def constructrequest(player_name: str, game_mode: str):
    
    if game_mode == "":
        #normal highscores
        mode = ""
    elif (game_mode.find('hard') != -1 | game_mode == "hcim" | game_mode == "hc"):
        mode = "_hardcore_ironman"
    elif (game_mode.find('ult') != -1 | game_mode == "uim"):
        mode = "_ultimate"
    elif (game_mode.find('iron') != -1 | game_mode == "im"):
        mode = "_ironman"
    else:
        return("error")

    return("https://secure.runescape.com/m=hiscore_oldschool" + mode + "/index_lite.ws?" + player_name)

def parsetextresponse(api_response: str):

    #list of keys for pairing player scores to activities
    activity_list = ["Overall", "Attack", "Defence", "Strength", "Hitpoints",
                    "Ranged", "Prayer", "Magic", "Cooking", "Woodcutting",
                    "Fletching", "Fishing", "Firemaking", "Crafting", "Smithing"
                    "Mining", "Herblore", "Agility", "Thieving", "Slayer", 
                    "Farming", "Runecrafting", "Hunter", "Construction", 
                    "League Points", "Bounty Hunter - Hunter", "Bounty Hunter - Rogue", "Clue Scrolls (all)", "Clue Scrolls (beginner)",
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
    
        # check for activity specification: defaults to :all: can specify any of 48 activities or 24 skills
        # check for metric specification: defaults to :all: can specify rank, level, or experience
        # parse returned scores into arrays and match up to blueprint array (scores of -1 are unranked)
        # send requested data to smaller array
    pass

def comparescores():
    # if a second player is specified find the difference
    pass

def constructsingleoutput():
    #one player specified
    pass

def constructcomparisonoutput():
    #two players specified
    pass

def errormessage():
    #improper arguments or api response
    pass

def main():
    my_scores = requests.get('https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player=pvm_gohone').text
                             
    print(type(my_scores))

if __name__ == "__main__":
    main()