import time
import math
import random
import requests
import discord
import os
import io
import asyncio

from location_info import states

max_rounds = 20
api_key = os.getenv('google_maps_api')


#geoguessr game class
class G_game:

    def __init__(self, rounds, max_time):
        self.cur_location = []
        self.round_num = 0
        self.num_rounds = rounds
        self.max_time = max_time
        
    def load_states(self):
        location_list = []
        
        for state in states:
            location_list.append(Location(state["name"], state["cities"]))
        return location_list
    
    async def start_game(self, bot, message, player_list):
        
        #load state information
        location_list = self.load_states()
        
        await message.channel.send("Starting in...")
        await count_down(message)
        
        #game loop
        while self.round_num < self.num_rounds:
            
            for player in player_list:
                self.choose_location(location_list)
                
                await self.warn_player(player, message)

                image = self.get_image()

                await self.display_image(image, message)

                player_guess, time_taken = await self.get_player_guess(bot, message)

                if_correct = await self.check_player_guess(player_guess, message, player)

                if time_taken < self.max_time:
                    distance = await self.calc_distance(player_guess)                  
                else:
                    distance = 2892
                    
                await self.calc_score(time_taken, distance, player)

                await self.end_round(message, if_correct, distance, player)
            
            self.round_num += 1
        
        for player in player_list:
            await self.display_results(player, message)
            
        return
    
    def choose_location(self, location_list):
        self.cur_location = random.choice(location_list)
        return
    
    async def warn_player(self, player, message):
        await message.channel.send(f'{player.name}\'s turn!')
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
            return new_message.channel == message.channel
    
        start_time = time.time()
        
        guess = "z"
        try:
            guess = await asyncio.wait_for(bot.wait_for('message', check=check_user), timeout=self.max_time)
            end_time = time.time()
            time_taken = end_time - start_time
            input_value = guess.content
            return input_value, time_taken
        except asyncio.TimeoutError:
            end_time = time.time()
            time_taken = end_time - start_time
            await message.channel.send("Times up!")
            time.sleep(1)
            return guess, time_taken
    
    #check the players guess against real location
    async def check_player_guess(self, player_guess, message, player): 
        
        player.rounds += 1
        if player_guess.lower() == self.cur_location.name.lower():
            await message.channel.send("Correct!")
            player.num_correct += 1
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
            
            if len(data["results"]) == 0:
                
                player_lat = 23.6345
                player_lng = 102.5528
            else:
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
        
        return distance
    
    async def calc_score(self, time_to_guess, distance, player):
        
        #first update players average time to guess
        #and average distance
        player.avg_time = (player.total_time + time_to_guess) / player.rounds
        player.avg_distance = (player.total_distance + distance) / player.rounds
        
        player.total_time += time_to_guess
        player.total_distance += distance
        
        #adjustable weights to priortize distance over time taken
        prev_score_weight = 0.7
        distance_weight = 0.225
        time_weight = 0.075
        
        max_distance = 2892
        max_time_to_guess = self.max_time
        
        accuracy = (prev_score_weight * (player.score/100)) + (distance_weight * (1 - (distance/max_distance))) + (time_weight * (1 - (time_to_guess/max_time_to_guess)))

        player.score = 100 * accuracy
        
        return accuracy
    
    async def end_round(self, message, if_correct, distance, player):
        
        formatted_distance = "{:.2f}".format(distance)
        if if_correct:
            if player.avg_time > (self.max_time/2):
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
        await message.channel.send(f'Great job {player.name}! You earned a score of {formatted_score}/100.00')
        await message.channel.send(f'You answered {player.num_correct} correct from playing {player.rounds}')
        await message.channel.send(f'You averaged {formatted_time} seconds per guess,')
        await message.channel.send(f'Along with an average distance from the correct location of {formatted_distance} miles!')
        return

#each player is stored as a Player, holds vars for scoring  
class Player:
    def __init__(self, name, score):
        self.name = name
        self.score = score
        self.num_correct = 0
        self.avg_time = 0
        self.total_time = 0
        self.avg_distance = 0
        self.total_distance = 0
        self.rounds = 0

#each state is stored as a Location, a picture is chosen randomly from 20 cities in the city list
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

#add players to the player list, ensure no duplicates
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
        
        player = message.author.name
    
        joined_flag = False
        for p in player_list:
            if p.name == player:
                await message.channel.send(f'Player "{player}" has already joined')
                joined_flag = True
                
        if not joined_flag:     
            player_list.append(Player(player, 50))
        
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

#creates 4 buttons in the game menu
class menuButtons(discord.ui.View):
    def __init__(self, bot, message):
        super().__init__()
        self.player_list = []
        self.rounds = 5
        self.time = 60
        self.bot = bot
        self.message = message
        self.end = False
    
    @discord.ui.button(label="Single Player",style=discord.ButtonStyle.primary, custom_id="1")
    async def button_callback1(self, x, y):
        player = Player(self.message.author.name, 50)
        self.player_list.append(player)
        self.end = True
        
    @discord.ui.button(label="Multi-Player", style=discord.ButtonStyle.secondary, custom_id="2")
    async def button_callback2(self, x, y):
        num_players = await get_player_num(self.message, self.bot)
        self.player_list = await get_players(num_players, self.message, self.bot)
        self.end = True
        
    @discord.ui.button(label="Settings", style=discord.ButtonStyle.success, custom_id="3")
    async def button_callback3(self, x, y):
        #a couple adjustable settings for the game
        #- time to guess must be > 0 and <= 180
        #- number of rounds must be > 0 and <= 50

        #make sure we are talking to user who issued "Geoguessr" command
        def check_user(new_message):
            return new_message.author == self.message.author and new_message.channel == self.message.channel

        await self.message.channel.send('Which setting would you like to change?')
        await self.message.channel.send('1: Number of rounds')
        await self.message.channel.send('2: Number of seconds to guess')
        await self.message.channel.send('-Message the number that appears before the setting you would like to change-')

        mess = await self.bot.wait_for('message', check=check_user)
        rule_to_change = int(mess.content)

        num_rounds = 5
        time_to_guess = 60

        if rule_to_change == 1:
            await self.message.channel.send('How many rounds would you like to play?')
            await self.message.channel.send('-Please choose between 1 and 50-')

            mess = await self.bot.wait_for('message', check=check_user)
            num_rounds = int(mess.content)
            
            passflag = True
            
            while passflag:
                if 1 > num_rounds or 50 < num_rounds:
                    await self.message.channel.send('-Please choose between 1 and 50 rounds-')
                    mess = await self.bot.wait_for('message', check=check_user)
                    num_rounds = int(mess.content)
                else:
                    passflag = False
            
            self.rounds = num_rounds
            
        elif rule_to_change == 2:
            await self.message.channel.send('How much time would you like to guess?')
            await self.message.channel.send('-Please choose between 1 and 180 seconds-')

            mess = await self.bot.wait_for('message', check=check_user)
            time_to_guess = int(mess.content)
            
            passflag = True
            
            while passflag:
                if 1 > time_to_guess or 180 < time_to_guess:
                    await self.message.channel.send('-Please choose between 1 and 180 seconds-')
                    mess = await self.bot.wait_for('message', check=check_user)
                    time_to_guess = int(mess.content)
                else:
                    passflag = False
                    
            self.time = time_to_guess
        else:
            await self.message.channel.send('That is not a setting you can change')
            
    @discord.ui.button(label="Rules", style=discord.ButtonStyle.danger, custom_id="4")
    async def button_callback4(self, x, y):
        #explain rules to player
        #make sure we are talking to user who issued "Geoguessr" command
        def check_user(new_message):
            return new_message.author == self.message.author and new_message.channel == self.message.channel

        await self.message.channel.send('How it works:')
        time.sleep(0.5)
        await self.message.channel.send('Each round you will be given a picture depicting a random location within the United States.')
        await self.message.channel.send('You will be given 60 seconds to view the image and guess which state the image was taken in.')
        await self.message.channel.send('After guessing, the answer will be revealed.')
        await self.message.channel.send('Your score is 50/100 initially, and will raise or lower depending on how close your guess was,')
        await self.message.channel.send('how quickly you answered, and your previous score')
        await self.message.channel.send('----------------------------------------------------')



async def menu(bot, message):

    buttons = menuButtons(bot, message)
    await message.channel.send('Welcome to Geoguessr!')
    time.sleep(1)
    
    start_game_flag = False
    flag = False
    
    but = await message.channel.send('Options:', view=buttons)
    while not flag:
        
        flag = buttons.end
        #timeout a couple seconds
        try:
            button = await bot.wait_for("button_click", timeout=2)
        except asyncio.TimeoutError:
            pass
        
    await but.delete()
    
    player_list = buttons.player_list
    num_rounds = buttons.rounds
    max_time = buttons.time
    
    return player_list, num_rounds, max_time

async def geoguessr_game(bot, message):
    
    player_list, num_rounds, max_time = await menu(bot, message)
      
    game = G_game(num_rounds, max_time)
    
    await game.start_game(bot, message, player_list)  
    
    return       
       