#Name: John Gregerson --- Course: CS320 --- Assignment: MainProject Feature 2: osrs_highscores

#DESCRIPTION: This feature formats a query for the jagex highscores API, parses the returned information and
# displays the results to the user.
import requests # API call package
import mwparserfromhell # Full Name - Media Wiki Parser from Hell
import unittest

def osrshighscores(player_name: str, second_player_name: str, game_mode: str, activity: int, metric: str):

    #API request URL
    base_url = "https://secure.runescape.com/m=hiscore_oldschool" + game_mode + "/index_lite.ws?"

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
    

    #", construct and send request
        # check game_mode  -- defaults to :normal: other options are Ironman, Ultimate_Ironman, Hardcore_Ironman
        # if player_name == "" (print help message) else send request for and store player 1 scores
        # if second_player_name != "" send request for and store player 2 scores

    # parse text response
        # check for activity specification: defaults to :all: can specify any of 48 activities or 24 skills
        # check for metric specification: defaults to :all: can specify rank, level, or experience
        # parse returned scores into arrays and match up to blueprint array (scores of -1 are unranked)
        # send requested data to smaller array

    # perform calculations
        # if a second player is specified find the difference

    # construct and return output message

    pass



def main():
    my_scores = requests.get('https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player=pvm_gohone').text
                             
    print(type(my_scores))

if __name__ == "__main__":
    main()