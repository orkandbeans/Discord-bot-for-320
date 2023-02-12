import discord  # discord API
import jason    # for database


class Soundboard:
    def constructor(self, message):
        # store the command and file in instance variables
        self.message = message
        #self.file = file

        # initialize instance of the classes and pass them the required variables
        self.audio = Sound(message)
        #self.secure = Security(command)
        #self.manage = Uploader(command, secure)
        

class Sound:
    def constructor(self, message):
        self.message = message
        # from the command argument derive the file name
        self.audio_file = message.content.split(" ")[1] + ".mp3"
        self.sound = None
        self.channel = None


    async def connect(self):
        # Join voice channel that the message came from
        channel = message.author.voice.channel
        # get the sound object
        sound = await channel.connect()

    async def play(self):
        # Play the sound file
        sound.play(discord.FFmpegPCMAudio(audio_file))
        while sound.is_playing():
            # finish playing the sound
            await asyncio.sleep(1)
        sound.stop()
        # Disconnect from voice channel
        await sound.disconnect()
    
"""
class Security:
    def constructor(self, file):
        # store the file in instance variables
        self.file = file

    def check_file_type(self):

    def is_it_safe(self):
"""

"""
class Uploader:
    def constructor(self, message, file):
    # store the command and file in instance variables
    self.file = file
    self.message = message
"""

"""main
# Check for the soundboard slash command
    #if message.content.startswith('!soundboard upload'):
    if message.content.startswith('!soundboard'):
        activate = Soundboard()
        await activate.audio.connect()
        await activate.audio.play()
"""