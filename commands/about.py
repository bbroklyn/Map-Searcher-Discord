import json
import sys
import datetime

from logger import write_log
import psutil
import disnake
import time
from disnake.ui import Button

file = open("config.json", "r")
config = json.load(file)
buildtime = datetime.date.today()
pversion = ".".join(map(str, sys.version_info[:3]))

async def about(inter, start_Time):
    await inter.response.defer()
    uptime = str(datetime.timedelta(seconds=int(round(time.time() - start_Time))))
    embed = disnake.Embed(
        description="\n Bot owners: [HeeChan](https://steamcommunity.com/id/6561198326716239/) & [Kassini](https://steamcommunity.com/id/I_God_Sigma/)"
                    "\n"
                    "\n Map Searcher is a **multifunctional** bot written in **Python** using the disnake. If you want to see commands, you can type </help:1125453195750166538>."
                    "\n",
        color=0xFFFFFF
    )
    embed.set_thumbnail(url="https://i.pinimg.com/564x/a6/ce/74/a6ce746599c3834a587af159d448978c.jpg")

    git_button_heechan = Button(label="HeeChan", style=disnake.ButtonStyle.url, url="https://github.com/heechan194")
    git_button_kassini = Button(label="Kassini", style=disnake.ButtonStyle.url, url="https://github.com/KassiniGit")
    git_button = Button(label="Source Code", style=disnake.ButtonStyle.url, url="https://github.com/heechan194/Map-Searcher-Bot")
    invite_button = Button(label="Invite Link", style=disnake.ButtonStyle.url, url="https://discord.com/api/oauth2/authorize?client_id=1122605455194193931&permissions=277025396736&scope=applications.commands%20bot")
    embed.set_author(
        name="Map Searcher",
        url="https://github.com/heechan194/Map-Searcher-Bot"
    )
    embed.add_field(name="Version", value=config["version"])
    embed.add_field(name="Up Time", value=f"`{uptime}`")
    embed.add_field(name='RAM', value=f"`{psutil.virtual_memory().percent} %`")
    embed.add_field(name='Build Date', value=f"`{buildtime}`")
    embed.add_field(name='Python Version', value=f"`{pversion}`")
    embed.add_field(name="Disnake Version", value="`"+disnake.__version__+"`")
    write_log("used /about.", inter.author)
    await inter.edit_original_message(embed=embed, components=[git_button_heechan, git_button_kassini, git_button, invite_button])