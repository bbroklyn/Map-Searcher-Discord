"""
    name = "Map Searcher"
    authors = "broklyn & Kassini"
    description = "The Bot, which gives you a download link from the map name and much more"
    version = "3.2"
    url = "https://github.com/heechan194/Map-Searcher-Discord"    
"""
# Importing standart libraries.
import json
import datetime
import time
# importing bot commands.
from commands.mlink import map_link_command
from commands.strack import server_track_command
from commands.help import help_command
from commands.about import about_command
from commands.admin import admin_command
from commands.fastdl import fast_dl_command
from commands.changelog import changelogs
from commands.pack import pack_command
from commands.csite import check_website
from commands.alive_check import send_alive_message
from logger import write_log
# Importing custom libraries.
import disnake
from disnake.ext import commands, tasks

file = open("config.json", "r")
config = json.load(file)

Bot = commands.Bot(config['prefix'], intents=disnake.Intents.all())

list = [
    pack_command,
    changelogs,
    help_command,
    about_command,
    check_website,
    map_link_command,
    fast_dl_command,
    admin_command,
    server_track_command
]

for list in list:
    Bot.add_slash_command(list)

max_attempts = 3
timeout = 5
global startTime
startTime = time.time()

# tasks.
@tasks.loop(minutes=30)
async def update_status():
    end_of_summer = datetime.datetime(datetime.datetime.now().year, 9, 1)
    time_left = end_of_summer - datetime.datetime.now()
    days_left = time_left.days
    status = f"{days_left} day(s) until the end of summer"
    if days_left == 0:
        status = "the summer is over!"
    await Bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.playing, name=status), status=disnake.Status.dnd)

# events.
#@Bot.event
#async def on_slash_command_error(inter: disnake.ApplicationCommandInteraction, error: Exception) -> None:
#   pass

@Bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error

@Bot.event
async def on_ready():
    print("Token verification was successful!")
    update_status.start()
    send_alive_message.start(Bot)
    print("logged in as: " + str(Bot.user)+ "\nStart time: " + str(datetime.datetime.now().strftime("%H:%M:%S [Moscow Time]")))
    write_log("launched, logged in as: " + str(Bot.user), "Bot")

class UTC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(UTC(bot))


for attempt in range(1, max_attempts + 1):
    start_time = time.time()
    try:
        print("Validating the token...")
        Bot.run(config["token"])
        break
    except:
        print("Unconfirmed token, retrying in 5 seconds...")
        elapsed_time = time.time() - start_time
        if elapsed_time < timeout and attempt < max_attempts:
            time.sleep(5)
        else:
            exit("The maximum number of token validation has been exhausted.\nExiting...")