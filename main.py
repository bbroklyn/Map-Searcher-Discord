"""
    name = "Map Searcher"
    author = "HeeChan & Kassini"
    description = "The Bot, which gives you a download link from the map name and much more"
    version = "3.0"
    url = "https://github.com/heechan194/Map-Searcher-Discord"    
"""
import json
import re
import psutil

from commands.mlink import map_link
from commands.strack import server_track
from commands.help import help
from commands.about import about
from commands.admin import admin
from commands.fastdl import fast_dl
from commands.changelog import changelog
#from commands.credits import credit
from commands.pack import pack
from commands.csite import check_website
from logger import write_log

import disnake
from disnake.ext import commands, tasks

import datetime
import time

# json
file = open("config.json", "r")
config = json.load(file)
# changelogs
changelogs_content = ""
dates = re.findall(r"\d{1,2}\.\d{2}\.\d{2}", changelogs_content)

intents = disnake.Intents(messages=True, guilds=True)
Bot = commands.Bot(config['prefix'], intents=disnake.Intents.all())

# bot start
max_attempts = 3
timeout = 5

@tasks.loop(minutes=30)
async def update_status():
    end_of_summer = datetime.datetime(datetime.datetime.now().year, 9, 1)
    time_left = end_of_summer - datetime.datetime.now()
    days_left = time_left.days
    status = f"{days_left} day(s) until the end of summer"
    await Bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.playing, name=status), status=disnake.Status.dnd)

@tasks.loop(hours=12)
async def send_alive_message():
    start_Time = time.time()
    uptime = str(datetime.timedelta(seconds=int(round(time.time() - start_Time))))
    channel = Bot.get_channel(1132109859375034480)
    try:
        embed = disnake.Embed(title="Bot check:",
                              description="Current Time: " + str(datetime.datetime.now().strftime("`%H:%M:%S`")),
                              color=disnake.Color.green())
        embed.add_field(name="Up Time", value=f"`{uptime}`")
        embed.add_field(name='RAM', value=f"`{psutil.virtual_memory().percent} %`")
        await channel.send(embed=embed)
    except disnake.HTTPException as e:
        embed = disnake.Embed(title="An error has occurred:",
                              color=disnake.Color.dark_red())
        embed.add_field(name="Log:", value=f"{e}")
        await channel.send(embed=embed)

@send_alive_message.before_loop
async def before_send_alive_message():
    await Bot.wait_until_ready()

send_alive_message.start()

# error slash event
@Bot.event
async def on_slash_command_error(inter: disnake.ApplicationCommandInteraction, error: Exception) -> None:
    pass

# invalid command event
@Bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error

@Bot.event
async def on_ready():
    print("Token verification was successful!")
    global startTime
    startTime = time.time()
    time.sleep(1.00)
    await update_status()
    update_status.start()
    print("logged in as: " + str(Bot.user))
    write_log("launched, logged in as: " + str(Bot.user), "Bot")

class UTC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


@Bot.slash_command(name="about", 
                   description="Information about this bot.")
async def about_command(inter: disnake.ApplicationCommandInteraction):
    await about(inter, startTime)


command_descriptions = {
    "mlink": "Gives you the link to download the map from name.",
    "fastdl": "Link to FastDL.",
    "admin": "Admin commands. Can restart/shutdown bot.",
    "help": "Navigation help command.",
    "about": "About this bot.",
    "strack": "Get all server information.",
    "csite": "Checks website and all information about him."
}
help_opt = commands.option_enum(["commands", "run usage"])
@Bot.slash_command(name="help",
                  description="Navigation help command, some information.")

async def help_command(inter: disnake.ApplicationCommandInteraction,
                       option: help_opt = commands.Param(name="option",
                                                         description="Choose an option.")):
    await help(inter, option, startTime, command_descriptions)


def setup(bot):
    bot.add_cog(UTC(bot))


servers = [server['name'] for server in config['trackers']]
server_tr = commands.option_enum(servers)
@Bot.slash_command(name="strack", 
                   description="Get all server information.")
async def server_track_command(inter: disnake.ApplicationCommandInteraction,
                               server: server_tr = commands.Param(name="option",
                                                                  description="Choose a server.")):
    await server_track(inter, server)


admin_option = commands.option_enum(["shutdown", "restart"])
@Bot.slash_command(name="admin", 
                   description="Admin commands.")
async def admin_command(inter: disnake.ApplicationCommandInteraction,
                action: admin_option = commands.Param(name="action",
                                                      description="Select admin command actions.")):
    await admin(inter, action)


@Bot.slash_command(name="fastdl", 
                   description="Gives you the link to download the map.")
async def fast_dl_command(inter: disnake.ApplicationCommandInteraction):
    await fast_dl(inter)


fast_dl_link = commands.option_enum(["CS:GO", "CS2", "CS:S"]) 
@Bot.slash_command(name="mlink", 
                   description="Gives you the link to download the map!")
async def map_link_command(inter: disnake.ApplicationCommandInteraction,
                  game: fast_dl_link = commands.Param(name="game",
                                                      description="Enter the game name."),
                  map_name: str = commands.Param(name="mapname",
                                                 description="Enter the map name")):
    await map_link(inter, game, map_name)

'''
@Bot.slash_command(name="credits", description="Credits to people, who helped in writing this bot.")
async def credits_command(inter: disnake.ApplicationCommandInteraction):
    await credit(inter)
'''

all_packs = [r_pack['pack'] for r_pack in config['ResourcePack']]
pack_option = commands.option_enum(all_packs)
@Bot.slash_command(name="pack", 
                   description="Download resource packs of various servers.")
async def pack_command(inter: disnake.ApplicationCommandInteraction,
                       pack_select: pack_option = commands.Param(name="packs",
                                                                 description="Enter the pack name.")):
    await pack(inter, pack_select)


@Bot.slash_command(name="changelog", 
                   description="Gives you the bot changelogs.")
async def changelogs(inter: disnake.ApplicationCommandInteraction,
                    requested_date: str = commands.Param(name="date",
                                                         description="Enter the date in DD.MM.YY format.")):
    await changelog(inter, requested_date)


@Bot.slash_command(name="csite", 
                   description="Checks if the site is running. Also gives information about him.")
async def csite(inter: disnake.ApplicationCommandInteraction,
                    website: str = commands.Param(name="website",
                                                         description="Enter the website URL. you can use https:// at your discretion.")):
    await check_website(inter, website)


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