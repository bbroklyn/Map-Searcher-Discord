import sys
import os

import disnake
from logger import write_log


async def admin(inter: disnake.ApplicationCommandInteraction, action):
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