import json

import disnake
from logger import write_log

file = open("config.json", "r")
config = json.load(file)


async def pack(inter: disnake.ApplicationCommandInteraction,
               pack_select):
    await inter.response.defer()
    for pack_info in config['packs']:
        if pack_info['pack'] == pack_select:
            pack_name = pack_info['pack']
            pack_link = pack_info['link']
            embed = disnake.Embed(
                title=f"{pack_name} resource pack, click to download.",
                description=f"[-> {pack_name}]({pack_link})",
                color=0xFFFFFF
            )
            write_log(f"used /pack {pack_name}", inter.author)  
            await inter.edit_original_message(embed=embed)
            return  
    await inter.edit_original_message(content="❗️-> An error has occurred, this pack does not exist!")