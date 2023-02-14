#import jason   # for database
import discord  # discord API
import asyncio  # for concurrent code using the async or await syntax.


class Soundboard:
    async def constructor(self, message):
        # store the command and file in instance variables
        self.message = message
        #self.file = file

        # initialize instance of the classes and pass them the required variables
        self.audio = Sound(message)
        await self.audio.play()
        #self.secure = Security(command)
        #self.manage = Uploader(command, secure)
        

class Sound:
    def constructor(self, message):
        self.message = message
        # from the command argument derive the file name
        self.audio_file = message.content.split(" ")[1] + ".mp3"
        self.audio_file = "./Audio_files/" + self.audio_file
        self.sound = None
        self.channel = None
    
    # def embed

    async def connect(self):
        # Join voice channel that the message came from
        channel = self.message.author.voice.channel
        # get the sound object
        self.sound = await channel.connect()

    async def play(self):
        # Play the sound file
        self.sound.play(discord.FFmpegPCMAudio(self.audio_file))
        while self.sound.is_playing():
            # finish playing the sound
            await asyncio.sleep(1)
        self.sound.stop()
        # Disconnect from voice channel
        await self.sound.disconnect()
    
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

"""main roughdraft
# Check for the soundboard slash command
    #if message.content.startswith('!soundboard upload'):
"""

"""
@
if .content.startswith('!soundboard'):
    activate = Soundboard()
    await activate.audio.connect()

"""