import time
import math
import random
import requests
import discord
from discord.ext import commands
from discord.components import DiscordComponents, Button, ButtonStyle, ComponentContext
import os
import io
import asyncio
from geopy.distance import great_circle

from location_info import states

max_rounds = 20
api_key = ''
#api_key = os.getenv('google_maps_api')

class G_game:

    def __init__(self):
        self.cur_location = []
        self.round_num = 0
        
    def load_states(self):
        location_list = []
        for state in states:
            location_list.append(Location(state["name"], state["cities"]))
        return location_list
    
    async def start_game(self, num_rounds, bot, message):
        #load state information
        location_list = self.load_states()
        
        player = Player(message.author.name, 50)
        
        #await message.channel.send("Starting in...")
        #await count_down(message)
        
        while self.round_num < num_rounds:
            
            self.choose_location(location_list)
            
            image = self.get_image()
            
            #await self.display_image(image, message)
            
            player_guess, time_taken = await self.get_player_guess(bot, message)
            
            if_correct = await self.check_player_guess(player_guess, message, player)
            
            distance = await self.calc_distance(player_guess)
            
            time_to_guess = 0
            
            await self.calc_score(time_taken, distance, player)
            
            await self.end_round(message, if_correct, distance, player)
            
            self.round_num += 1
            
        await self.display_results(player, message)
        return
    
    def choose_location(self, location_list):
        self.cur_location = random.choice(location_list)
        return
    
    def get_image(self):
        random.seed(time.time())
        
        rand_city = random.choice(self.cur_location.city_list)
        
        location = f"{rand_city},{self.cur_location.name}"
        size = "800x800"
        fov = "120"  # in degrees
        heading = random.randint(0, 360)  # in degrees
        pitch = "10"  # in degrees

        url = f"https://maps.googleapis.com/maps/api/streetview?size={size}&location={location}&fov={fov}&heading={heading}&pitch={pitch}&key={api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            print("state:", self.cur_location.name, "city:", rand_city)
            return response
        else:
            print("Failed to retrieve image. Response status code:", response.status_code)
            return
    
    async def display_image(self, response, message):
        with io.BytesIO(response.content) as image:
            await message.channel.send(file=discord.File(image, filename="image.jpg"))
        await message.channel.send("Which state was this picture taken in?")
        return
    
    async def get_player_guess(self, bot, message):
        
        def check_user(new_message):
            return new_message.author == message.author and new_message.channel == message.channel
    
        time_to_guess = 60.0
        start_time = time.time()
        
        guess = "z"
        try:
            guess = await asyncio.wait_for(bot.wait_for('message', check=check_user), timeout=time_to_guess)
            end_time = time.time()
            time_taken = end_time - start_time
            input_value = guess.content
            return input_value, time_taken
        except asyncio.TimeoutError:
            await message.channel.send("Times up!")
            time.sleep(1)
            return guess
    
    #check the players guess against real location
    async def check_player_guess(self, player_guess, message, player): 
        
        player.rounds += 1
        if player_guess.lower() == self.cur_location.name.lower():
            await message.channel.send("Correct!")
            time.sleep(1)
            return True
        else:
            await message.channel.send(f"Sorry that is incorrect, it was taken in {self.cur_location.name}")
            time.sleep(1)
            return False
    
    async def calc_distance(self, player_guess):
        #get the coordinates of the players guess
        address = player_guess
        
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
        response = requests.get(url)

        
        if response.status_code == 200:
            data = response.json()
            player_lat = data["results"][0]["geometry"]["location"]["lat"]
            player_lng = data["results"][0]["geometry"]["location"]["lng"]
            print(f"Player guess - Latitude: {player_lat}, Longitude: {player_lng}")
            
        else:
            print(f"Error: {response.status_code}")
            
        #get the coordinates of the real location
        address = self.cur_location.name
        
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
        response = requests.get(url)
        
        
        if response.status_code == 200:
            data = response.json()
            real_lat = data["results"][0]["geometry"]["location"]["lat"]
            real_lng = data["results"][0]["geometry"]["location"]["lng"]
            print(f"Real location - Latitude: {real_lat}, Longitude: {real_lng}")
            
        else:
            print(f"Error: {response.status_code}")
            
        #calculate the distance between pairs of coordinates - haversine formula
        radius = 3959
        rad_p_lat = math.radians(player_lat)
        rad_r_lat = math.radians(real_lat)
        rad_lat = math.radians(real_lat - player_lat)
        rad_lng = math.radians(real_lng - player_lng)
        
        a = math.sin(rad_lat/2) ** 2 + math.cos(rad_p_lat) * math.cos(rad_r_lat) * math.sin(rad_lng/2) ** 2
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt( 1 - a))
        
        distance = radius * c
        print(distance)
        
        return distance
    
    async def calc_score(self, time_to_guess, distance, player):
        
        #first update players average time to guess
        #and average distance
        player.avg_time = (player.total_time + time_to_guess) / player.rounds
        player.avg_distance = (player.total_distance + distance) / player.rounds
        
        player.total_time += time_to_guess
        player.total_distance += distance
        
        #adjustable weights to priortize distance over time taken
        prev_score_weight = 0.5
        distance_weight = 0.4
        time_weight = 0.1
        
        max_distance = 5859
        max_time_to_guess = 60
        
        accuracy = (prev_score_weight * (player.score/100)) + (distance_weight * (1 - (distance/max_distance))) + (time_weight * (1 - (time_to_guess/max_time_to_guess)))
        print(accuracy)
        player.score = 100 * accuracy
        
        return accuracy
    
    async def end_round(self, message, if_correct, distance, player):
        
        formatted_distance = "{:.2f}".format(distance)
        if if_correct:
            if player.avg_time > 30:
                await message.channel.send(f'Remember answering quickly leads to a higher score!')
            else:
                await message.channel.send(f'Good speed!')
        else:
            await message.channel.send(f'You were {formatted_distance} miles off from the correct state.')
        return
    
    async def display_results(self, player, message):
        formatted_score = "{:.2f}".format(player.score)
        formatted_time = "{:.2f}".format(player.avg_time)
        formatted_distance = "{:.2f}".format(player.avg_distance)
        await message.channel.send(f'Great job {player.name}! You earned a score of {formatted_score}/100.00 from playing {player.rounds} rounds')
        await message.channel.send(f'You averaged {formatted_time} seconds per guess,')
        await message.channel.send(f'Along with an average distance from the correct location of {formatted_distance} miles!')
        return
    
class Player:
    def __init__(self, name, score):
        self.name = name
        self.score = score
        self.avg_time = 0
        self.total_time = 0
        self.avg_distance = 0
        self.total_distance = 0
        self.rounds = 0

class Location:
    def __init__(self, name, city_list):
        self.name = name
        self.city_list = city_list
    
async def get_num_rounds(message, bot):
    #make sure we are talking to user who issued "Geoguessr" command
    def check_user(new_message):
        return new_message.author == message.author and new_message.channel == message.channel
    
    time.sleep(1)
    await message.channel.send('How many rounds would you like to play?')
    
    num_rounds = 0
    int_flag = True
    while int_flag:
        rounds = await bot.wait_for('message', check=check_user)
    
        try:
            num_rounds = int(rounds.content)
            if num_rounds == 0 or num_rounds > max_rounds:
                await message.channel.send(f'Please pick between 1 and {max_rounds} rounds')
                continue
            int_flag = False
        except ValueError:
            await message.channel.send(f'{rounds.content} is not a number')
            await message.channel.send('How many rounds would you like to play?')
            
    return num_rounds
    
async def get_player_num(message, bot):
    #make sure we are talking to user who issued "Geoguessr" command
    def check_user(new_message):
        return new_message.author == message.author and new_message.channel == message.channel
    
    time.sleep(1)
    await message.channel.send('How many people would like to play?')
    
    int_flag = True
    while int_flag:
        players = await bot.wait_for('message', check=check_user)
    
        try:
            num_players = int(players.content)
            if num_players <= 1 or num_players > 5:
                await message.channel.send(f'Please pick between 2 and 5 players')
                continue
            int_flag = False
        except ValueError:
            await message.channel.send(f'{players.content} is not a number')
            await message.channel.send('How many people would like to play?')
    return num_players

async def get_players(num_players, message, bot):
    #make sure we are talking to user who issued "Geoguessr" command
    def check_user(new_message):
        return new_message.channel == message.channel
    
    time.sleep(1)
    await message.channel.send(f'The next {num_players} that message this channel will be included in the game')
    
    numjoined = 0
    player_list = []

    while numjoined < num_players:
        
        message = await bot.wait_for('message', check=check_user)
        
        player = message.author
    
        player_list.append(Player(player, 1, 0))
        
        await message.channel.send(f'Player "{player}" has joined the game')
        
        numjoined += 1
        
    return player_list
    
async def count_down(message):
    await message.channel.send('3...')
    time.sleep(1)
    await message.channel.send('2..')
    time.sleep(1)
    await message.channel.send('1.')
    time.sleep(1)
    return

async def menu(bot, message):
    DiscordComponents(bot)
    row = [
        Button(style=ButtonStyle.blue, label="Single player", custom_id="single-player"),
        Button(style=ButtonStyle.blue, label="Multi player", custom_id="multi-player"),
        Button(style=ButtonStyle.grey, label="Settings", custom_id="settings"),
        Button(style=ButtonStyle.grey, label="Rules", custom_id="rules")
    ]

    await message.channel.send('Welcome to Geoguessr!')
    time.sleep(1)
    
    start_game_flag = False
    
    while not start_game_flag:
        message = await message.channel.send(content="---------------------", components=[row])

        # Wait for a button to be pressed
        button: ComponentContext = await bot.wait_for("button_click")

        # Call the appropriate function based on the custom_id of the button that was pressed
        if button.custom_id == "single-player":
            player_list = await handle_single_player(message)
            start_game_flag = True
        elif button.custom_id == "multi-player":
            num_players = await get_player_num(message, bot)
            player_list = await get_players(num_players, message, bot)
            start_game_flag = True
        elif button.custom_id == "settings":
            num_rounds, max_time = await handle_settings(message, bot)
        elif button.custom_id == "rules":
            await handle_rules(message, bot)

    return player_list, num_rounds, max_time

async def handle_single_player(message):
    #single player game
    player_list = []
    player = Player(message.author.name, 50)
    player_list.append(player)
    return player_list

async def handle_settings(message, bot):
    #a couple adjustable settings for the game
    #- time to guess must be > 0 and <= 180
    #- number of rounds must be > 0 and <= 50
    
    #make sure we are talking to user who issued "Geoguessr" command
    def check_user(new_message):
        return new_message.author == message.author and new_message.channel == message.channel
    
    await message.channel.send('Which setting would you like to change?')
    await message.channel.send('-Message the number that appears before the setting you would like to change-')
    
    message = await bot.wait_for('message', check=check_user)
    rule_to_change = int(message.content)
    
    num_rounds = 5
    time_to_guess = 60
    
    if rule_to_change == 0:
        await message.channel.send('How many rounds would you like to play?')
        await message.channel.send('-Please choose between 1 and 50-')
        
        message = await bot.wait_for('message', check=check_user)
        num_rounds = int(message.content)
    elif rule_to_change == 1:
        await message.channel.send('How much time would you like to guess?')
        await message.channel.send('-Please choose between 1 and 180 seconds-')
        
        message = await bot.wait_for('message', check=check_user)
        time_to_guess = int(message.content)
    else:
        await message.channel.send('That is not a setting you can change')
    
    return num_rounds, time_to_guess

async def handle_rules(message, bot):
    #explain rules to player
    #make sure we are talking to user who issued "Geoguessr" command
    def check_user(new_message):
        return new_message.author == message.author and new_message.channel == message.channel
    
    await message.channel.send('How it works:')
    time.sleep(0.5)
    await message.channel.send('Each round you will be given a picture depicting a random location within the United States.')
    await message.channel.send('You will be given 60 seconds to view the image and guess which state the image was taken in.')
    await message.channel.send('After guessing, the answer will be revealed.')
    await message.channel.send('Your score is 50/100 initially, and will raise or lower depending on how close your guess was,')
    await message.channel.send('how quickly you answered, and your previous score')
    await message.channel.send('-Send any message to acknowledge the rules-')
    
    player_ack_rules = await bot.wait_for('message', check=check_user)
    
    return

async def geoguessr_game(bot, message):
    
    #await introduce_user(message, bot)
            
    #num_rounds = await get_num_rounds(message, bot)
    num_rounds = 3
            
    #num_players = await get_player_num(message, bot)
    
    #players = await get_players(num_players, message, bot)
      
    game = G_game()
    await game.start_game(num_rounds, bot, message)  
    
    return       
       