import json
import psutil
import datetime
import time

import disnake
from disnake.ext import tasks, commands

file = open("config.json", "r")
config = json.load(file)

global startTime
startTime = time.time()
uptime = str(datetime.timedelta(seconds=int(round(time.time() - startTime))))

Bot = commands.Bot(config['prefix'], intents=disnake.Intents.all())

class ResourcePackView(disnake.ui.View):
    def __init__(self):
        super().__init__()

    @disnake.ui.button(style=disnake.ButtonStyle.red, emoji="🗑️")
    async def delete_message_button(self, button: disnake.ui.Button, inter: disnake.Interaction):
        await inter.response.defer()
        await inter.delete_original_response()     
@tasks.loop(hours=12)
async def send_alive_message(Bot):
    try:
        uptime = str(datetime.timedelta(seconds=int(round(time.time() - startTime))))
        channel_id = 1133046102074069002
        channel = Bot.get_channel(channel_id)
        ram: float = psutil.virtual_memory().used/1048/1048
        ram_formatted = round(ram)
        
        if channel is None:
            print("Channel not found, entered channel ID:", channel_id)
            return

        embed = disnake.Embed(description="Current Time: " + str(datetime.datetime.now().strftime("`%H:%M:%S`"))
                              +"\nDate: " + str(datetime.datetime.now().strftime("`%d.%m.%Y`")),
                              color=disnake.Color.green())
        embed.add_field(name="Up Time", value=f"`{uptime}`")
        embed.add_field(name='RAM', value=f"`{ram_formatted} MB`")
        if uptime <= "0:00:10":
            embed.title = "Bot has been enabled:"
            embed.color = disnake.Color.green()
        else:
            embed.title = "Bot is still running!"
            embed.color = disnake.Color.yellow()
        
        embed.timestamp = datetime.datetime.now()

    except disnake.HTTPException as e:
        embed = disnake.Embed(title="An error has occurred:",
                              description="Current Time: " + str(datetime.datetime.now().strftime("`%H:%M:%S`")),
                              color=disnake.Color.red())      
        embed.add_field(name="Error log:", value=str(e))
        embed.timestamp = datetime.datetime.now()
        print("[send_alive_messages] An error has occurred:", e)
    view = ResourcePackView()
    await channel.send(embed=embed, view=view)
