"""
    name = "Map Searcher"
    author = "HeeChan & Kassini"
    description = "The Bot, which gives you a download link from the map name and much more"
    version = "2.9"
    url = "https://github.com/heechan194/Map-Searcher-Bot"    
"""
import json
import re

from commands.mlink import map_link
from commands.strack import server_track
from commands.help import help
from commands.about import about
from commands.admin import admin
from commands.fastdl import fast_dl
from commands.changelog import change_log
from commands.credits import credit
from commands.pack import pack
from logger import write_log

import disnake
from disnake.ext import commands

import time

file = open("config.json", "r")
config = json.load(file)
changelogs_content = ""
dates = re.findall(r"\d{1,2}\.\d{2}\.\d{2}", changelogs_content)

intents = disnake.Intents(messages=True, guilds=True)

Bot = commands.Bot(config['prefix'], intents=disnake.Intents.all())
activity = disnake.Game(name="/about <- about me :)")
status = disnake.Status.do_not_disturb


class UTC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


@Bot.event
async def on_slash_command_error(inter: disnake.ApplicationCommandInteraction, error: Exception) -> None:
    return


@Bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error


@Bot.event
async def on_ready():
    print("Token verification was successful!")
    await Bot.change_presence(activity=activity, status=status)
    global startTime
    startTime = time.time()
    time.sleep(1.00)
    print("logged in as: " + str(Bot.user))
    write_log("launched!", "Bot")



@Bot.slash_command(name="about", description="Information about this bot.")
async def about_command(inter: disnake.ApplicationCommandInteraction):
    await about(inter, startTime)


help_opt = commands.option_enum(["commands", "run usage"])
@Bot.slash_command(name="help", description="Navigation help command, some information.")
async def help_command(inter: disnake.ApplicationCommandInteraction,
                       option: help_opt = commands.Param(name="option",
                                                         description="Choose an option.")):
    await help(inter, option, startTime)


def setup(bot):
    bot.add_cog(UTC(bot))


servers = [server['name'] for server in config['trackers']]
server_tr = commands.option_enum(servers)
@Bot.slash_command(name="strack", description="Get all server information.")
async def server_track_command(inter: disnake.ApplicationCommandInteraction,
                               server: server_tr = commands.Param(name="option",
                                                                  description="Choose a server.")):
    await server_track(inter, server)


admin_option = commands.option_enum(["shutdown", "restart"])
@Bot.slash_command(name="admin", description="Admin commands.")
async def admin_command(inter: disnake.ApplicationCommandInteraction,
                action: admin_option = commands.Param(name="action",
                                                      description="Select admin command actions.")):
    await admin(inter, action)


@Bot.slash_command(name="fastdl", description="Gives you the link to download the map.")
async def fast_dl_command(inter: disnake.ApplicationCommandInteraction):
    await fast_dl(inter)


fast_dl_link = commands.option_enum(["CS:GO", "CS2", "CS:S"])
@Bot.slash_command(name="mlink", description="Gives you the link to download the map!")
async def map_link_command(inter: disnake.ApplicationCommandInteraction,
                  game: fast_dl_link = commands.Param(name="game",
                                                      description="Enter the game name."),
                  map_name: str = commands.Param(name="mapname",
                                                 description="Enter the map name")):
    await map_link(inter, game, map_name)


@Bot.slash_command(name="credits", description="Credits to people, who helped in writing this bot.")
async def credits_command(inter: disnake.ApplicationCommandInteraction):
    await credit(inter)


all_packs = [r_pack['pack'] for r_pack in config['packs']]
pack_option = commands.option_enum(all_packs)
@Bot.slash_command(name="pack", description="Download resource packs of various servers.")
async def pack_command(inter: disnake.ApplicationCommandInteraction,
                       pack_select: pack_option = commands.Param(name="packs",
                                                                 description="Enter the pack name.")):
    await pack(inter, pack_select)


@Bot.slash_command(name="changelog", description="Gives you the bot changelogs.")
async def changelog(inter: disnake.ApplicationCommandInteraction,
                    requested_date: str = commands.Param(name="date",
                                                         description="Enter the date in DD.MM.YY format.")):
    await change_log(inter, requested_date)




try:
    print("Validating the token...")
    Bot.run(config["token"])
    time.sleep(1)
except:
    exit("TOKEN IS INVALID")