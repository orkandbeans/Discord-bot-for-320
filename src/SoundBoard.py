import discord  # discord API
import jason    # for database

class Soundboard:
    def constructor(self, command, file):
        # store the command and file in instance variables
        self.command = command
        self.file = file

        # initialize instance of the classes and pass them the required variables
        self.get Standby(command)
        self.play = Sound(command)
        self.secure = Security(file)
        self.manage = Uploader(command, secure)
        


class Standby:
    def constructor(command):
    # store the command in instance variables
    self.command = command

    def command_list(self):
        print(f"")


class Sound:
    def constructor(self, command):
        self.command = command

    def audio_name(self):
        # swap code to retrieve an audio from database and play it
        await message.channel.send(f"playing silly sound")



class Security:
    def constructor(self, file):
        #store the file in instance variables
        self.file = file

    def check_file_type(self):

    def is_it_safe(self):



class Uploader:
    def constructor(self, file):
    #store the command and file in instance variables
    self.file = file
    self.command = command








"""
main

#Initialize an instance of Soundboard
    go = Soundboard(command)
if message.content.startswith (':joy:'): #recieve Command
    await message.channel
    go.play.audioname()
    
"""