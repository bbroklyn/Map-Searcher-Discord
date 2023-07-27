import json
import sys
import datetime

from logger import write_log
import psutil
import disnake
import time
from disnake.ui import Button
from disnake.ext import commands

file = open("config.json", "r")
config = json.load(file)
buildtime = datetime.date.today()
pversion = ".".join(map(str, sys.version_info[:3]))
Bot = commands.Bot(config['prefix'], intents=disnake.Intents.all())

global start_Time
start_Time = time.time()
command_author_id = None

class ResourcePackView(disnake.ui.View):
    def __init__(self):
        super().__init__()

    @disnake.ui.button(label="Kassini", style=disnake.ButtonStyle.url, url="https://github.com/KassiniGit")
    async def Kassini():
        return
    @disnake.ui.button(label="HeeChan", style=disnake.ButtonStyle.url, url="https://github.com/heechan194")
    async def HeeChan():
        return
    @disnake.ui.button(label="Code", style=disnake.ButtonStyle.url, url="https://github.com/heechan194/Map-Searcher-Bot")
    async def Source():
        return
    @disnake.ui.button(label="Invite Link", style=disnake.ButtonStyle.url, url="https://discord.com/api/oauth2/authorize?client_id=1122605455194193931&permissions=277025396736&scope=applications.commands%20bot")
    async def Invite():
        return
    @disnake.ui.button(style=disnake.ButtonStyle.red, emoji="🗑️")
    async def delete_message_button(self, button: disnake.ui.Button, inter: disnake.Interaction):
        await inter.response.defer()
        global command_author_id
        if inter.user.id != command_author_id:
            return        
        await inter.delete_original_response()

@Bot.slash_command(name="about", 
                   description="Information about this bot.")
async def about_command(inter: disnake.ApplicationCommandInteraction):
    await inter.response.defer()
    global command_author_id
    command_author_id = inter.author.id
    uptime = str(datetime.timedelta(seconds=int(round(time.time() - start_Time))))
    embed = disnake.Embed(
        description="\n Bot owners: [HeeChan](https://steamcommunity.com/id/6561198326716239/) & [Kassini](https://steamcommunity.com/id/I_God_Sigma/)"
                    "\n"
                    "\n Map Searcher is a **multifunctional** bot written in **Python** using the disnake. If you want to see commands, you can type </help:1125453195750166538>."
                    "\n",
        color=0xFFFFFF
    )
    embed.set_thumbnail(url="https://i.pinimg.com/564x/a6/ce/74/a6ce746599c3834a587af159d448978c.jpg")

    embed.set_author(
        name="Map Searcher",
        url="https://github.com/heechan194/Map-Searcher-Bot"
    )
    ram: float = psutil.virtual_memory().used/1048/1048
    ram_formatted = round(ram)
    embed.add_field(name="Version", value=config["version"])
    embed.add_field(name="Up Time", value=f"`{uptime}`")
    embed.add_field(name='RAM', value=f"`{ram_formatted} MB`")
    embed.add_field(name='Build Date', value=f"`{buildtime}`")
    embed.add_field(name='Python Version', value=f"`{pversion}`")
    embed.add_field(name="Disnake Version", value="`"+disnake.__version__+"`")
    write_log("used /about.", inter.author)
    view = ResourcePackView()
    await inter.edit_original_message(embed=embed, view=view)