import re

import disnake
from logger import write_log

changelogs_content = ""
dates = re.findall(r"\d{1,2}\.\d{2}\.\d{2}", changelogs_content)

intents = disnake.Intents(messages=True, guilds=True)

    
async def changelog(inter: disnake.ApplicationCommandInteraction, requested_date):
    await inter.response.defer()
    with open("changelog.txt", "r") as file:
        change_logs_content = file.read()
    changelog_cont = {
        date: re.findall(fr"{date}->(.+?);", change_logs_content)
        for date in re.findall(r"\d{1,2}\.\d{2}\.\d{2}", change_logs_content)
    }
    changelog_embed = disnake.Embed()
    if requested_date in changelog_cont:
        changelog_embed.title = f"Bot changes for {requested_date}:"
        changelog_embed.description = "\n".join(changelog_cont[requested_date])
        changelog_embed.color = 0xFFFFFF
    else:
        changelog_embed.title = "An error has occurred"
        changelog_embed.description = f"Invalid date! You can check everything here: [Press](https://github.com/heechan194/Map-Searcher-Discord/blob/main/changelog.txt)"
        changelog_embed.color = 0xFF0000
        if changelog_cont:
            changelog_embed.add_field(name="Possible Dates:", value="\n".join(changelog_cont.keys()), inline=True)
    write_log(f"used /changelog {requested_date}.", inter.author)
    await inter.edit_original_message(embed=changelog_embed)