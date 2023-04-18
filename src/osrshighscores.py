#Name: John Gregerson --- Course: CS320 --- Assignment: MainProject Feature 2: osrs_highscores

#DESCRIPTION: This feature formats a query for the jagex highscores API, parses the returned information and
# displays the results to the user.
# users may specify one or two players to lookup as well as a game mode to pull scores from.

import requests # API call package
import mwparserfromhell # Full Name - Media Wiki Parser from Hell
import unittest

#main command function called by main.py
def osrshighscores(player_name: str, second_player_name: str, game_mode: str):

    mode = game_mode.lower()
    player_one = player_name.lower().replace(" ", "_")
    player_two = second_player_name.lower().replace(" ", "_")
   
    if player_name == "":
        output = errormessage()
        return output
    else:
    #send request for and store player 1 scores
        player_one_url = constructrequest(player_one, mode)
        if (player_one_url == "error"):
            output = errormessage()
            return output
        else:
            player_one_scores = requests.get(player_one_url)
            if player_one_scores.ok:
                parsed_player_one = parsetextresponse(player_one_scores.text)
            else:
                output = errormessage()
                return output
            

    if second_player_name != "":
    #send request for and store player 2 scores
        player_two_url = constructrequest(player_two, mode)
        if (player_two_url == "error"):
            output = errormessage()
            return output
        else:
            player_two_scores = requests.get(player_two_url)
            if player_two_scores.ok:
                parsed_player_two = parsetextresponse(player_two_scores.text)
                isCompareRequest = True
            else:
                output = errormessage()
                return output
    else:
        isCompareRequest = False

    if isCompareRequest == True:
        output = constructcomparisonoutput(parsed_player_one, parsed_player_two, player_one, player_two)
    else:
        output = constructsingleoutput(parsed_player_one, player_one)

    return output
    

# constructs correct api url from user specified player name and game mode
# accepted game modes contain the substrings 'hard, 'ult, or 'iron
# or are common abbreviations of the three modes.
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


# parses returned cvs data into a list of lists with
# either a skill or activity as the first member of each inner list
# where skill members are [skill, rank, level, experience]
# and activity members are [activity, rank, killcount]
def parsetextresponse(api_response: str):

    #list of keys for pairing player scores to skills
    skill_list = ["Overall", "Attack", "Defence",
                  "Strength", "Hitpoints", "Ranged",
                  "Prayer", "Magic", "Cooking",
                  "Woodcutting", "Fletching", "Fishing",
                  "Firemaking", "Crafting", "Smithing", 
                  "Mining", "Herblore", "Agility",
                  "Thieving", "Slayer", "Farming",
                  "Runecrafting", "Hunter", "Construction"]
     
     #list of keys for pairing player scores to activities and bosses
    activity_list = ["League Points", "Bounty Hunter - Hunter", "Bounty Hunter - Rogue",
                     "Clue Scrolls (all)", "Clue Scrolls (beginner)", "Clue Scrolls (easy)",
                     "Clue Scrolls (medium)", "Clue Scrolls (hard)", "Clue Scrolls (elite)",
                     "Clue Scrolls (master)", "LMS - Rank", "PvP, Arena - Rank",
                     "Soul Wars Zeal", "Rifts closed", "Abyssal Sire",
                     "Alchemical Hydra", "Artio", "Barrows Chests",
                     "Bryophyta", "Callisto", "Cal'varion",
                     "Cerberus", "Chambers of Xeric", "Chambers of Xeric: Challenge Mode",
                     "Chaos Elemental", "Chaos Fanatic", "Commander Zilyana",
                     "Corporeal Beast", "Crazy Archaeologist", "Dagannoth Prime",
                     "Dagannoth Rex", "Dagannoth Supreme", "Deranged Archaeologist",
                     "General Graardor", "Giant Mole", "Grotesque Guardians",
                     "Hespori", "Kalphite Queen", "King Black Dragon",
                     "Kraken", "Kree'Arra", "K\'ril Tsutsaroth",
                     "Mimic", "Nex", "Nightmare",
                     "Phosani\'s Nightmare", "Obor", "Phantom Muspah",
                     "Sarachnis", "Scorpia", "Skotizo",
                     "Spindel", "Tempoross", "The Gauntlet",
                     "The Corrupted Gauntlet", "Theatre of Blood", "Theatre of Blood: Hard Mode",
                     "Thermonuclear Smoke Devil", "Tombs of Amascut", "Tombs of Amascut: Expert Mode",
                     "TzKal-Zuk", "TzTok-Jad", "Venenatis",
                     "Vet\'ion", "Vorkath", "Wintertodt",
                     "Zalcano", "Zulrah",]
    
    api_response = api_response.replace('\n', ',').replace('-1', 'unranked')
    
    raw_player_scores = api_response.split(",")

    formatted_player_scores = []
    
    i = 0

    # each list has 4 members [skill, rank, level, experience]
    for x in skill_list:
        skill = [x, raw_player_scores[i], raw_player_scores[i+1], raw_player_scores[i+2]]
        formatted_player_scores.append(skill)
        i+= 3
    
    # each list has 3 members [activity, rank, killcount]
    for x in activity_list:
        activity = [x, raw_player_scores[i], raw_player_scores[i+1]]
        formatted_player_scores.append(activity)
        i+=2

    return formatted_player_scores


# a single player was specified construct normal output
def constructsingleoutput(player_one_scores_list: list, player_one: str):
    output_list = []

    j = 0
    output_list.append("Scores:  " + player_one + "\n")
    activity_index = 0
    for i in player_one_scores_list:
        if activity_index < 24:
            output_list[j] += i[0] + ":   (" + player_one.upper() + ":   RANK:  " + i[1] + ",   LEVEL:  " + i[2] + ",   XP:  " + i[3] + ")\n" 
        else:
            output_list[j] += i[0] + ":   (" + player_one.upper() + ":   RANK:  " + i[1] + ",   KC:  " + i[2] + ")\n"
        activity_index += 1
        if(len(output_list[j]) > 1800):
            j += 1
            output_list.append("")
    output_list[j] += "\n"
    return output_list

# more than one player specified, construct outputs side by side
# this function should have a difference between scores output added later
def constructcomparisonoutput(player_one_scores_list: list, player_two_scores_list: list, player_one: str, player_two: str):
    output_list = []

    j = 0
    output_list.append("Scores:  " + player_one + "\n")
    activity_index = 0
    for i in player_one_scores_list:
        if activity_index < 24:
            output_list[j] += i[0] + ":   (" + player_one.upper() + ":   RANK:  " + i[1] + ",   LEVEL:  " + i[2] + ",   XP:  " + i[3] + "):  " 
            output_list[j] += "   (" + player_two.upper() + ":   RANK:  " + player_two_scores_list[activity_index][1] + ",   LEVEL:  " + player_two_scores_list[activity_index][2] + ",   XP:  " + player_two_scores_list[activity_index][3] + ")\n"
        else:
            output_list[j] += i[0] + ":   (" + player_one.upper() + ":   RANK:  " + i[1] + ",   KC:  " + i[2] + "): "
            output_list[j] += "   (" + player_two.upper() + ":   RANK:  " + player_two_scores_list[activity_index][1] + ",   KC:  " + player_two_scores_list[activity_index][2] + ")\n"
        activity_index += 1
        if(len(output_list[j]) > 1800):
            j += 1
            output_list.append("")
    output_list[j] += "\n"
    return output_list

# generic something went wrong. doesn't currently specify what error occured
def errormessage():
    output_list = []
    output_list.append("")
    output_list[0] += "Either player name not found, api is currently unreachable, or command arguements were enetered incorrectly.\n"
    output_list[0] += "Please check inputs. Accepted modes are:  \n"
    output_list[0] += "\"hcim\", \"hc\", or anything containing the substring \"hard\" for the hardcore ironman mode.\n"
    output_list[0] += "\"uim\" or anything containing the substring \"ult\" for the ultimate ironman mode."
    output_list[0] += "\"im\" or anything containing the substring \"iron\" for the ironman mode."
    return output_list


def main():
    #if running command on it's own edit osrshighscores values below to test
    my_scores = osrshighscores("pvm_gohone", "", "iron", "", "")
                             
    print(type(my_scores))
    print(my_scores)

if __name__ == "__main__":
    #allows the command to be run on it's own
    main()