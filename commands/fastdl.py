import json

import disnake
from disnake.ext import commands
from logger import write_log

file = open("config.json", "r")
config = json.load(file)

Bot = commands.Bot(config['prefix'], intents=disnake.Intents.all())

@Bot.slash_command(name="fastdl", 
                   description="Gives you the link to download the map.")
async def fast_dl_command(inter: disnake.ApplicationCommandInteraction):
    await inter.response.defer()
    if config["fastdl"] and config["fastdl2"] == "":
        await inter.send("❗-> **An error has occurred, fastdl parameter in `config.json` is empty!**")
    else:
        fastdl_embed = disnake.Embed(
            title="FastDL",
            description="Below are links to all FastDL that the bot uses:"
                        "\n"
                        "\n[FASTDL 1](" + config["fastdl"]+")" +
                        "\n[FASTDL 2](" + config["fastdl2"]+")",
            color=0xFFFFFF
        )
        write_log("used /fastdl.", inter.author)
        await inter.edit_original_message(embed=fastdl_embed)