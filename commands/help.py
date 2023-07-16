import datetime

import psutil
import disnake
import time
from logger import write_log

async def help(inter: disnake.ApplicationCommandInteraction, option, start_Time):
    uptime = str(datetime.timedelta(seconds=int(round(time.time() - start_Time))))
    await inter.response.defer()
    help_things = {
        "commands": "\n **Bot Commands:**"
                    "\n"
                    "\n </mlink:1130214840431038484> - Gives you the link to download the map from name."
                    "\n </fastdl:1123717659637321749> - Link to FastDL."
                    "\n </admin:1125154934904586363> - Admin commands. Can restart/shutdown bot."
                    "\n </credits:1123702310837686292> - Credits to people, who helped in writing this bot."
                    "\n </help:1125453195750166538> - Navigation help command."
                    "\n </about:1125443661547712644> - About this bot."
                    "\n </strack:1130221660948140154> - Get all server information.",

        "run usage": "\n **Current** bot uptime: `" + uptime + "`""\n **RAM** Usage: `" + str(psutil.virtual_memory().percent) + " %`"
    }
    if option in help_things:
        embed = disnake.Embed(
            title="",
            description=f"{help_things[option]}",
            color=0xFFFFFF
        )
        write_log(f"used /help {option}.", inter.author)
        await inter.edit_original_message(embed=embed)
