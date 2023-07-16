import disnake
from logger import write_log


async def credit(inter: disnake.ApplicationCommandInteraction):
    await inter.response.defer()

    write_log("used /credits.", inter.author)
    embed = disnake.Embed(
        title="Credits",
        description=""
                    "\n"
                    "\n **Thanks to:**"
                    "\n **NiceShot** -> helped us with some things, gave idea about some features."
                    "\n **koen** -> we are using his FastDL."
                    "\n **Killik** -> Hosting for the bot."
                    "\n **Unloze** -> For FastDL.",
        color=0xFFFFFF
    )
    await inter.edit_original_message(embed=embed)