import json

import disnake
from logger import write_log
from disnake.ext import commands

file = open("config.json", "r")
config = json.load(file)
intents = disnake.Intents(messages=True, guilds=True)
Bot = commands.Bot(config['prefix'], intents=disnake.Intents.all())

all_packs = [r_pack['pack'] for r_pack in config['ResourcePack']]
pack_option = commands.option_enum(all_packs)

@Bot.slash_command(name="pack", 
                   description="Download resource packs of various servers.")
async def pack_command(inter: disnake.ApplicationCommandInteraction,
                       pack_select: pack_option = commands.Param(name="packs",
                                                                 description="Enter the pack name.")):
    await inter.response.defer()
    for pack_info in config['ResourcePack']:
        if pack_info['pack'] == pack_select:
            pack_name = pack_info['pack']
            pack_link = pack_info['link']
            embed = disnake.Embed(
                title=f"**{pack_name}** resource pack, click to download.",
                description=f"Your link: [{pack_name}]({pack_link})",
                color=0xFFFFFF
            )
            embed.set_footer(text="* If the link is outdated or you have a newer version - contact the owners of this bot")
            write_log(f"used /pack {pack_name}", inter.author)  
            await inter.edit_original_message(embed=embed)
            return  
    await inter.edit_original_message(content="❗️-> An error has occurred, this pack does not exist!")