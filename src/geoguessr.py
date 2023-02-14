import time
import random
import requests
import discord
import os
import io
import asyncio

from location_info import states

max_rounds = 20

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
        
        player = Player(message.author.name, 0, 0)
        
        await message.channel.send("Starting in...")
        await count_down(message)
        
        while self.round_num < num_rounds:
            self.choose_location(location_list)
            
            image = self.get_image()
            
            await self.display_image(image, message)
            
            player_guess = await self.get_player_guess(bot, message)
            
            await self.check_player_guess(player_guess, message, player)
            
            self.round_num += 1
            
        await self.display_results(player, message)
        return
    
    def choose_location(self, location_list):
        self.cur_location = random.choice(location_list)
        return
    
    def get_image(self):
        random.seed(time.time())
        
        rand_city = random.choice(self.cur_location.city_list)
        
        api_key = os.getenv('google_maps_api')
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
    
        time_to_guess = 10
        start_time = time.time()
        
        guess = "z"
        try:
            guess = await asyncio.wait_for(bot.wait_for('message', check=check_user), timeout=60.0)
            input_value = guess.content
            return input_value
        except asyncio.TimeoutError:
            await message.channel.send("Times up!")
            time.sleep(1)
            return guess
    
    #check the players guess against 
    async def check_player_guess(self, player_guess, message, player): 
        if player_guess.lower() == self.cur_location.name.lower():
            await message.channel.send("Correct!")
            player.num_correct += 1
        else:
            await message.channel.send(f"Sorry that is incorrect, it was taken in {self.cur_location.name}")
        time.sleep(1)
        player.rounds += 1
        return 
    
    async def display_results(self, player, message):
        await message.channel.send(f'Great job {player.name}! You were correct on {player.num_correct} out of {player.rounds} rounds')
        return
    
class Player:
    def __init__(self, name, num_correct, rounds):
        self.name = name
        self.num_correct = num_correct
        self.rounds = rounds

class Location:
    def __init__(self, name, city_list):
        self.name = name
        self.city_list = city_list

async def introduce_user(message):
    await message.channel.send('Welcome to Geoguessr!')
    time.sleep(1)
    await message.channel.send('How it works:')
    time.sleep(0.5)
    await message.channel.send('Each round you will be given a picture depicting a random location within the United States.')
    await message.channel.send('You will be given 60 seconds to view the image and guess which state the image was taken in.')
    await message.channel.send('After guessing, the answer will be revealed.')
    await message.channel.send('-Send any message to acknowledge the rules-')
    
async def count_down(message):
    await message.channel.send('3...')
    time.sleep(1)
    await message.channel.send('2..')
    time.sleep(1)
    await message.channel.send('1.')
    time.sleep(1)
    return

async def geoguessr_game(bot, message):
    #make sure we are talking to user who issued "Geoguessr" command
    def check_user(new_message):
        return new_message.author == message.author and new_message.channel == message.channel
    
    await introduce_user(message)
    
    player_ack_rules = await bot.wait_for('message', check=check_user)
            
    time.sleep(1)
    await message.channel.send('How many rounds would you like to play?')
    time.sleep(1)
    
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
      
    game = G_game()
    await game.start_game(num_rounds, bot, message)  
    
    return              