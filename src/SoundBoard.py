import discord  # discord API
from discord.ui import Button, View
import yt_dlp as youtube_dl
import ffmpeg
#intercation with youtube 
async def play_youtube_audio(video_url, voice_channel):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(id)s.%(ext)s',
        'nocheckcertificate': True,
        'quiet': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0'
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            audio_file_path = ydl.prepare_filename(info_dict)
    except Exception as e:
        print(f"Error extracting information from {video_url}: {e}")
        return
    try:
        voice_client = await voice_channel.connect()
    except discord.errors.ClientException:
        # If the bot is already in a voice channel, don't try to connect again
        voice_client = voice_channel.guild.voice_client
    source = discord.FFmpegPCMAudio(audio_file_path, pipe=False)
    voice_client.play(source)
#soundboard object
class Board():
    def __init__(self, ctx):
        #init default menu buttons
        self.bark =Button(
            style=discord.ButtonStyle.green,
            emoji="🐶")
        self.meow =Button(
            style=discord.ButtonStyle.green,
            emoji="😺")
        self.running =Button(
            style=discord.ButtonStyle.green,
            emoji="🏃‍♂️")
        self.trombone =Button(
            style=discord.ButtonStyle.green,
            emoji="🎺")
        self.cricket =Button(
            style=discord.ButtonStyle.green,
            emoji="🦗")
        self.sad =Button(
            style=discord.ButtonStyle.green,
            emoji="😔")
        self.mushroom =Button(
            style=discord.ButtonStyle.green,
            emoji="🍄")
        self.roar =Button(
            style=discord.ButtonStyle.green,
            emoji="🐯")
        self.scream =Button(
            style=discord.ButtonStyle.green,
            emoji="🤕")
        self.coin =Button(
            style=discord.ButtonStyle.green,
            emoji="🪙")
        self.harp =Button(
            style=discord.ButtonStyle.green,
            emoji="😇")
        self.bonk =Button(
            style=discord.ButtonStyle.green,
            emoji="💥")
        self.snore =Button(
            style=discord.ButtonStyle.green,
            emoji="😪")
        self.boom =Button(
            style=discord.ButtonStyle.green,
            emoji="💣")
        self.detective =Button(
            style=discord.ButtonStyle.green,
            emoji="🕵️")
        self.technologist =Button(
            style=discord.ButtonStyle.green,
            emoji="🧑‍💻")
        self.cowboy =Button(
            style=discord.ButtonStyle.green,
            emoji="🤠")
        self.clown =Button(
            style=discord.ButtonStyle.green,
            emoji="🤡")
        self.robot =Button(
            style=discord.ButtonStyle.green,
            emoji="🤖")
        self.sus =Button(
            style=discord.ButtonStyle.green,
            emoji="👀")
        self.fire =Button(
            style=discord.ButtonStyle.green,
            emoji="🔥")
        self.frost =Button(
            style=discord.ButtonStyle.green,
            emoji="❄️")
        self.popo =Button(
            style=discord.ButtonStyle.green,
            emoji="🚓")
        self.car =Button(
            style=discord.ButtonStyle.green,
            emoji="🚗")
        self.default_exit =Button(
            style=discord.ButtonStyle.red,
            emoji="✖️")
        #init custom menu buttons
        self.add1 =Button(
            label="1",
            style=discord.ButtonStyle.green)
        self.add2 =Button(
            label="2",
            style=discord.ButtonStyle.green)
        self.add3 =Button(
            label="3",
            style=discord.ButtonStyle.green)
        self.add4 =Button(
            label="4",
            style=discord.ButtonStyle.green)
        self.add5 =Button(
            label="5",
            style=discord.ButtonStyle.green)
        self.add6 =Button(
            label="6",
            style=discord.ButtonStyle.green)
        self.add7 =Button(
            label="7",
            style=discord.ButtonStyle.green)
        self.add8 =Button(
            label="8",
            style=discord.ButtonStyle.green)
        self.add9 =Button(
            label="9",
            style=discord.ButtonStyle.green)
        self.add10 =Button(
            label="10",
            style=discord.ButtonStyle.green)
        self.add11 =Button(
            label="11",
            style=discord.ButtonStyle.green)
        self.add12 =Button(
            label="12",
            style=discord.ButtonStyle.green)
        self.add13 =Button(
            label="13",
            style=discord.ButtonStyle.green)
        self.add14 =Button(
            label="14",
            style=discord.ButtonStyle.green)
        self.add15 =Button(
            label="15",
            style=discord.ButtonStyle.green)
        self.add16 =Button(
            label="16",
            style=discord.ButtonStyle.green)
        self.add17 =Button(
            label="17",
            style=discord.ButtonStyle.green)
        self.add18 =Button(
            label="18",
            style=discord.ButtonStyle.green)
        self.add19 =Button(
            label="19",
            style=discord.ButtonStyle.green)
        self.add20 =Button(
            label="20",
            style=discord.ButtonStyle.green)
        self.add21 =Button(
            label="21",
            style=discord.ButtonStyle.green)
        self.add22 =Button(
            label="22",
            style=discord.ButtonStyle.green)
        self.add23 =Button(
            label="23",
            style=discord.ButtonStyle.green)
        self.add24 =Button(
            label="24",
            style=discord.ButtonStyle.green)
        self.custom_exit =Button(
            style=discord.ButtonStyle.red,
            emoji="✖️")
        #init main menut buttons
        self.default_button = Button(
            label = "default",
            style = discord.ButtonStyle.green)
        self.custom_button = Button(
            label = "custom",
            style = discord.ButtonStyle.blurple)
        self.menu_exit = Button(
            style = discord.ButtonStyle.red,
            emoji="✖️")
        #init views
        self.default = View()
        self.custom = View()
        self.menu = View()
        #adding buttons to default menu
        self.default.add_item(self.bark)
        self.default.add_item(self.meow)
        self.default.add_item(self.running)
        self.default.add_item(self.trombone)
        self.default.add_item(self.cricket)
        self.default.add_item(self.sad)
        self.default.add_item(self.mushroom)
        self.default.add_item(self.roar)
        self.default.add_item(self.scream)
        self.default.add_item(self.coin)
        self.default.add_item(self.harp)
        self.default.add_item(self.bonk)
        self.default.add_item(self.snore)
        self.default.add_item(self.boom)
        self.default.add_item(self.detective)
        self.default.add_item(self.technologist)
        self.default.add_item(self.cowboy)
        self.default.add_item(self.clown)
        self.default.add_item(self.robot)
        self.default.add_item(self.sus)
        self.default.add_item(self.fire)
        self.default.add_item(self.frost)
        self.default.add_item(self.popo)
        self.default.add_item(self.car)
        self.default.add_item(self.default_exit)
        #adding buttons to custom menu
        self.custom.add_item(self.add1)
        self.custom.add_item(self.add2)
        self.custom.add_item(self.add3)
        self.custom.add_item(self.add4)
        self.custom.add_item(self.add5)
        self.custom.add_item(self.add6)
        self.custom.add_item(self.add7)
        self.custom.add_item(self.add8)
        self.custom.add_item(self.add9)
        self.custom.add_item(self.add10)
        self.custom.add_item(self.add11)
        self.custom.add_item(self.add12)
        self.custom.add_item(self.add13)
        self.custom.add_item(self.add14)
        self.custom.add_item(self.add15)
        self.custom.add_item(self.add16)
        self.custom.add_item(self.add17)
        self.custom.add_item(self.add18)
        self.custom.add_item(self.add19)
        self.custom.add_item(self.add20)
        self.custom.add_item(self.add21)
        self.custom.add_item(self.add22)
        self.custom.add_item(self.add23)
        self.custom.add_item(self.add24)
        self.custom.add_item(self.custom_exit)
        #adding the buttons to the main menu
        self.menu.add_item(self.default_button)
        self.menu.add_item(self.custom_button)
        self.menu.add_item(self.menu_exit)
        #urls submitted
        self.video_url1 = ''
        self.video_ur2 = ''
        self.video_ur3 = ''
        self.video_ur4 = ''
        self.video_ur5 = ''
        self.video_ur6 = ''
        self.video_ur7 = ''
        self.video_ur8 = ''
        self.video_ur9 = ''
        self.video_url0 = ''
        self.video_url11 = ''
        self.video_url2 = ''
        self.video_url3 = ''
        self.video_url4 = ''
        self.video_url5 = ''
        self.video_url6 = ''
        self.video_url7 = ''
        self.video_url8 = ''
        self.video_url9 = ''
        self.video_ur20 = ''
        self.video_ur21 = ''
        self.video_ur22 = ''
        self.video_ur23 = ''
        self.video_ur24 = ''
#--------------------------------interaction-------------------------------------------#
    #----------------------------main_menu---------------------------------------------#
        #---------------------------defualt--------------------------------------------#
        async def default_button_callback(interaction):
            await interaction.response.send_message(view=self.default)
        self.default_button.callback = default_button_callback
        #---------------------------custom---------------------------------------------#
        async def custom_button_callback(interaction):
            await interaction.response.send_message(view=self.custom)
        self.custom_button.callback = custom_button_callback
        #---------------------------exit-----------------------------------------------#
        async def menu_exit_callback(interaction):
            await interaction.response.edit_message(content="Bye", view = None)
        self.menu_exit.callback = menu_exit_callback
    #----------------------------default_menu------------------------------------------#
        #---------------------------bark-----------------------------------------------#
        async def bark_callback(interaction):
            voice_channel = ctx.author.voice.channel
            video_url = 'https://www.youtube.com/watch?v=b-fX44-tJHI'
            await play_youtube_audio(video_url, voice_channel)
            await interaction.response.defer()  
        self.bark.callback = bark_callback
        #---------------------------meow-----------------------------------------------#
        async def meow_callback(interaction):
            voice_channel = ctx.author.voice.channel
            video_url = 'https://www.youtube.com/watch?v=acusg9X_opQ'
            await play_youtube_audio(video_url, voice_channel)
            await interaction.response.defer() 
        self.meow.callback = meow_callback
        #---------------------------running--------------------------------------------#
        async def running_callback(interaction):
            voice_channel = ctx.author.voice.channel
            video_url = 'https://youtu.be/NcWwiv0HJow'
            await play_youtube_audio(video_url, voice_channel)
            await interaction.response.defer()
        self.running.callback = running_callback
        #---------------------------trombone-------------------------------------------#
        async def trombone_callback(interaction):
            voice_channel = ctx.author.voice.channel
            video_url = 'https://youtu.be/LukyMYp2noo'
            await play_youtube_audio(video_url, voice_channel)
            await interaction.response.defer()
        self.trombone.callback = trombone_callback
        #---------------------------cricket--------------------------------------------#
        async def cricket_callback(interaction):
            voice_channel = ctx.author.voice.channel
            video_url = 'https://www.youtube.com/watch?v=RktX4lbe_g4'
            await play_youtube_audio(video_url, voice_channel)
            await interaction.response.defer()
        self.cricket.callback = cricket_callback
        #---------------------------sad------------------------------------------------#
        async def sad_callback(interaction):
            voice_channel = ctx.author.voice.channel
            video_url = 'https://www.youtube.com/watch?v=vMv6O9IDdUQ'
            await play_youtube_audio(video_url, voice_channel)
            await interaction.response.defer()
        self.sad.callback = sad_callback
        #---------------------------mushroom-------------------------------------------#
        async def mushroom_callback(interaction):
            voice_channel = ctx.author.voice.channel
            video_url = 'https://youtu.be/6G-k4zxou7Y'
            await play_youtube_audio(video_url, voice_channel)
            await interaction.response.defer()
        self.mushroom.callback = mushroom_callback
        #---------------------------roar-----------------------------------------------#
        async def roar_callback(interaction):
            voice_channel = ctx.author.voice.channel
            video_url = 'https://youtu.be/nwq249Me9Yk'
            await play_youtube_audio(video_url, voice_channel)
            await interaction.response.defer()
        self.roar.callback = roar_callback
        #---------------------------scream---------------------------------------------#
        async def scream_callback(interaction):
            voice_channel = ctx.author.voice.channel
            video_url = 'https://youtu.be/5ynslUS4vvM'
            await play_youtube_audio(video_url, voice_channel)
            await interaction.response.defer()
        self.scream.callback = scream_callback
        #---------------------------coin-----------------------------------------------#
        async def coin_callback(interaction):
            voice_channel = ctx.author.voice.channel
            video_url = 'https://www.youtube.com/watch?v=mQSmVZU5EL4'
            await play_youtube_audio(video_url, voice_channel)
            await interaction.response.defer()
        self.coin.callback = coin_callback
        #---------------------------harp-----------------------------------------------#
        async def harp_callback(interaction):
            voice_channel = ctx.author.voice.channel
            video_url = 'https://youtu.be/SPUpsb_L6Z4'
            await play_youtube_audio(video_url, voice_channel)
            await interaction.response.defer()
        self.harp.callback = harp_callback
        #---------------------------bonk-----------------------------------------------#
        async def bonk_callback(interaction):
            voice_channel = ctx.author.voice.channel
            video_url = 'https://youtu.be/gwxTZaa3NgI'
            await play_youtube_audio(video_url, voice_channel)
            await interaction.response.defer()
        self.bonk.callback = bonk_callback
        #---------------------------snore----------------------------------------------#
        async def snore_callback(interaction):
            voice_channel = ctx.author.voice.channel
            video_url = 'https://youtu.be/dNr7nXvntO8'
            await play_youtube_audio(video_url, voice_channel)
            await interaction.response.defer()
        self.snore.callback = snore_callback
        #---------------------------boom-----------------------------------------------#
        async def boom_callback(interaction): 
            voice_channel = ctx.author.voice.channel
            video_url = 'https://www.youtube.com/watch?v=TApmI8YtYhc'
            await play_youtube_audio(video_url, voice_channel)
            await interaction.response.defer()
        self.boom.callback = boom_callback
        #---------------------------detective------------------------------------------#
        async def detective_callback(interaction):
            voice_channel = ctx.author.voice.channel
            video_url = 'https://www.youtube.com/watch?v=qgEx3LqfIHM'
            await play_youtube_audio(video_url, voice_channel)
            await interaction.response.defer()
        self.detective.callback = detective_callback
        #---------------------------technologist---------------------------------------#
        async def technologist_callback(interaction):
            voice_channel = ctx.author.voice.channel
            video_url = 'https://www.youtube.com/watch?v=bXC__vhmi6s'
            await play_youtube_audio(video_url, voice_channel)
            await interaction.response.defer()
        self.technologist.callback = technologist_callback
        #---------------------------cowboy---------------------------------------------#
        async def cowboy_callback(interaction):
            voice_channel = ctx.author.voice.channel
            video_url = 'https://www.youtube.com/watch?v=7_eEug_ysmw'
            await play_youtube_audio(video_url, voice_channel)
            await interaction.response.defer()
        self.cowboy.callback = cowboy_callback
        #---------------------------clown----------------------------------------------#
        async def clown_callback(interaction):
            voice_channel = ctx.author.voice.channel
            video_url = 'https://www.youtube.com/watch?v=Z0mrOFZuNJo'
            await play_youtube_audio(video_url, voice_channel)
            await interaction.response.defer()
        self.clown.callback = clown_callback
        #---------------------------robot----------------------------------------------#
        async def robot_callback(interaction):
            voice_channel = ctx.author.voice.channel
            video_url = 'https://www.youtube.com/watch?v=-Vkz9z_epSc'
            await play_youtube_audio(video_url, voice_channel)
            await interaction.response.defer()
        self.robot.callback = robot_callback
        #---------------------------sus------------------------------------------------#
        async def sus_callback(interaction):
            voice_channel = ctx.author.voice.channel
            video_url = 'https://www.youtube.com/watch?v=Regpv0xU3ZQ'
            await play_youtube_audio(video_url, voice_channel)
            await interaction.response.defer()
        self.sus.callback = sus_callback
        #---------------------------fire-----------------------------------------------#
        async def fire_callback(interaction): 
            voice_channel = ctx.author.voice.channel
            video_url = 'https://www.youtube.com/watch?v=Qj3n7iPzhvE'
            await play_youtube_audio(video_url, voice_channel)
            await interaction.response.defer()
        self.fire.callback = fire_callback
        #---------------------------frost----------------------------------------------#
        async def frost_callback(interaction):
            voice_channel = ctx.author.voice.channel
            video_url = 'https://www.youtube.com/watch?v=HVAmnzWPam0'
            await play_youtube_audio(video_url, voice_channel)
            await interaction.response.defer()
        self.frost.callback = frost_callback
        #---------------------------popo-----------------------------------------------#
        async def popo_callback(interaction):
            voice_channel = ctx.author.voice.channel
            video_url = 'https://www.youtube.com/watch?v=pwWqrrd-iTs'
            await play_youtube_audio(video_url, voice_channel)
            await interaction.response.defer()
        self.popo.callback = popo_callback
        #---------------------------car------------------------------------------------#
        async def car_callback(interaction):
            voice_channel = ctx.author.voice.channel
            video_url = 'https://www.youtube.com/watch?v=HjpBzQ_oWwU'
            await play_youtube_audio(video_url, voice_channel)
            await interaction.response.defer()
        self.car.callback = car_callback
        #------------------------default_exit------------------------------------------#
        async def default_exit_callback(interaction):
            await interaction.response.edit_message(content="Bye", view = None)
        self.default_exit.callback = default_exit_callback
    #----------------------------custom_menu-------------------------------------------#
        #------------------------add1-------------------------------------------#
        async def add1_callback(interaction):
            voice_channel = ctx.author.voice.channel
            if self.video_url1 == '':
                await interaction.response.send_message("submit a link")
                self.video_url1 = await self.bot.wait_for('message')
            else:
                await play_youtube_audio(self.video_url1, voice_channel)
                await interaction.response.defer()
        self.add1.callback = add1_callback
        #------------------------add2-------------------------------------------#
        #------------------------add3-------------------------------------------#
        #------------------------add4-------------------------------------------#
        #------------------------add5-------------------------------------------#
        #------------------------add6-------------------------------------------#
        #------------------------add7-------------------------------------------#
        #------------------------add8-------------------------------------------#
        #------------------------add9-------------------------------------------#
        #------------------------add10------------------------------------------#
        #------------------------add11------------------------------------------#
        #------------------------add12------------------------------------------#
        #------------------------add13------------------------------------------#
        #------------------------add14------------------------------------------#
        #------------------------add15------------------------------------------#
        #------------------------add16------------------------------------------#
        #------------------------add17------------------------------------------#
        #------------------------add18------------------------------------------#
        #------------------------add19------------------------------------------#
        #------------------------add20------------------------------------------#
        #------------------------add21------------------------------------------#
        #------------------------add22------------------------------------------#
        #------------------------add23------------------------------------------#
        #------------------------add24------------------------------------------#
        
        #------------------------custom_exit-------------------------------------------#
        async def custom_exit_callback(interaction):
            await interaction.response.edit_message(content="Bye", view = None)
        self.custom_exit.callback = custom_exit_callback
#--------------------------------------------------------------------------------------#