import time

from location_info import states

class G_game:

    def __init__(self, player, location):
        self.player = player
        self.location = location
        self.round_num = 0
        
    def load_states():
        location_list = []
        for state in states:
            location_list.append(Location(state["name"],
                                          state["min_latitude"],
                                          state["max_latitude"],
                                          state["min_longitude"],
                                          state["max_longitude"])
                                )
        return location_list
    
    def start_game(self):
        location_list = self.load_states()
        return
    
    def calc_distance():
        return
    
    def choose_location(location_list):
        return
    
    def get_image():
        return
    
    def get_player_guess():
        return
    
    def get_leaderboard():
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
    


def main():
    print("This is the main function.")
    game = G_game
    game.start_game(game)

if __name__ == "__main__":
    main()

                