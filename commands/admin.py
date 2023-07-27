import json
import sys
import os

import disnake
from logger import write_log
from disnake.ext import commands

file = open("config.json", "r")
config = json.load(file)

Bot = commands.Bot(config['prefix'], intents=disnake.Intents.all())

admin_option = commands.option_enum(["shutdown", "restart"])
@Bot.slash_command(name="admin", 
                   description="Admin commands.")
async def admin_command(inter: disnake.ApplicationCommandInteraction,
                action: admin_option = commands.Param(name="action",
                                                      description="Select admin command actions.")):

    await inter.response.defer()
    allowed_users = [1041292965483651102, 390221466689339392]
    if inter.user.id in allowed_users:
        if action == "shutdown":
            await inter.edit_original_message(content="**Successfully shut down by** " + inter.author.mention)
            write_log("Disabled the bot.", inter.author)
            raise SystemExit("Bot has been killed by\n", inter.author, "in", inter.channel)
        elif action == "restart":
            write_log("Restarted the bot.", inter.author)
            await inter.edit_original_message(content="**The bot is restarting by** " + inter.author.mention)
            python = sys.executable
            os.execl(python, python, *sys.argv)
    else:
        write_log("Tried to use admin command.", inter.author)
        await inter.edit_original_message(content="**You don't have permissions to use this command!**")