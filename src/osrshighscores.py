#Name: John Gregerson --- Course: CS320 --- Assignment: MainProject Feature 2: osrs_highscores

#DESCRIPTION: This feature formats a query for the jagex highscores API, parses the returned information and
# displays the results to the user.
import requests # API call package
import mwparserfromhell # Full Name - Media Wiki Parser from Hell
import unittest

def osrshighscores(player_name: str, search_option: int):
    pass