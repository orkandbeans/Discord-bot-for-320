import time
import random
import requests
import sys
import select

from location_info import states

class G_game:

    def __init__(self, player, location):
        self.player = player
        self.cur_location = location
        self.round_num = 0
        
    def load_states(self):
        location_list = []
        for state in states:
            location_list.append(Location(state["name"],
                                          state["min_latitude"],
                                          state["max_latitude"],
                                          state["min_longitude"],
                                          state["max_longitude"])
                                )
        return location_list
    
    def start_game(self, num_rounds, bot, message):
        #load state information
        location_list = self.load_states()
        
        while self.round_num < num_rounds:
            self.choose_location(location_list)

            image = self.get_image()
            
            self.display_image(image, message)

            player_guess = self.get_player_guess(bot, message)
            
            self.check_player_guess(player_guess, message)

            self.calc_distance(player_guess)
            
            self.display_results()
            
            self.round_num += 1
        return
    
    def choose_location(self, location_list):
        self.cur_location = random.choice(location_list)
        return
    
    def get_image(self):
        random.seed(time.time())
        rand_latitude = random.uniform(self.cur_location.min_latitude, self.cur_location.max_latitude)
        rand_longitude = random.uniform(self.cur_location.min_longitude, self.cur_location.max_longitude)
        
        api_key = ""
        location = (rand_latitude,rand_longitude)
        size = "400x400"
        fov = "120"  # in degrees
        heading = random.randint(0, 360)  # in degrees
        pitch = "10"  # in degrees

        url = f"https://maps.googleapis.com/maps/api/streetview?size={size}&location={location}&fov={fov}&heading={heading}&pitch={pitch}&key={api_key}"

        response = requests.get(url)

        if response.status_code == 200:
            print("gotimage", self.cur_location.name)
            return response.content
        else:
            print("Failed to retrieve image. Response status code:", response.status_code)
        return
    
    async def display_image(self, image, message):
        await message.channel.send(image)
        await message.channel.send("Which state was this picture taken in?")
        return
    
    async def get_player_guess(self, bot, message):
        
        def check_user(new_message):
            return new_message.author == message.author and new_message.channel == message.channel
    
        time_to_guess = 10
        start_time = time.time()
        
        guess, _, _ = select.select([await bot.wait_for('message', check=check_user)], [], [], time_to_guess)
        
        if guess:
            input_value = guess.content
            return input_value
        else:
            print("Times up!")
        return
    
    #check the players guess against 
    async def check_player_guess(self, player_guess, message): 
        if player_guess == self.cur_location:
            await message.channel.send("Correct!")
        else:
            await message.channel.send(f"Sorry that is incorrect, it was taken in {self.cur_location}")
        return 
        
    def calc_distance(self, player_guess):
        return
    
    def display_results(self):
        return
    
    def get_leaderboard(self):
        return
    
class Player:
    def __init__(self, name, score, games_played):
        self.name = name
        self.score = score
        self.games_played = games_played

class Location:
    def __init__(self, name, min_latitude, max_latitude, min_longitude, max_longitude):
        self.name = name
        self.min_latitude = min_latitude
        self.max_latitude = max_latitude
        self.min_longitude = min_longitude
        self.max_longitude = max_longitude

async def introduce_user(message):
    await message.channel.send('Welcome to Geoguessr!')
    time.sleep(1)
    await message.channel.send('How it works:')
    time.sleep(0.5)
    await message.channel.send('Each round you will be given a picture depicting a random location within the United States')
    await message.channel.send('You will be given 60 seconds to view the image and guess which state the image was taken in')
    await message.channel.send('After guessing, the answer will be revealed')
    await message.channel.send('Send any message to acknowledge the rules')
    
async def count_down(message):
    await message.channel.send('3...')
    time.sleep(1)
    await message.channel.send('2..')
    time.sleep(1)
    await message.channel.send('1.')
    time.sleep(1)

async def geoguessr_game(bot, message):
    #make sure we are talking to user who issued "Geoguessr" command
    def check_user(new_message):
        return new_message.author == message.author and new_message.channel == message.channel
    
    await introduce_user(message)
    
    player_ack_rules = await bot.wait_for('message', check=check_user)
            
    time.sleep(1)
    await message.channel.send('How many rounds would you like to play?')
    time.sleep(1)
    
    int_flag = True
    while int_flag:
        rounds = await bot.wait_for('message', check=check_user)
    
        try:
            num_rounds = int(rounds)
        except ValueError:
            await message.channel.send(f'{rounds.content} is not a number')
            
    game = G_game(None, None)
    game.start_game(num_rounds, bot, message)
    


def main():
    print("This is the main function.")
    game = G_game(None, None)
    game.start_game(10)

if __name__ == "__main__":
    main()

                