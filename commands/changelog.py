import re

import disnake
from logger import write_log

changelogs_content = ""
dates = re.findall(r"\d{1,2}\.\d{2}\.\d{2}", changelogs_content)

intents = disnake.Intents(messages=True, guilds=True)


async def change_log(inter: disnake.ApplicationCommandInteraction,
                     requested_date):
    await inter.response.defer()
    with open("changelog.txt", "r") as file:
        change_logs_content = file.read()
    changelog_cont = {}
    date_s = re.findall(r"\d{1,2}\.\d{2}\.\d{2}", change_logs_content)
    for date in date_s:
        matches = re.findall(fr"{date}->(.+?);", change_logs_content)
        changelog_cont[date] = matches
    if requested_date in changelog_cont:
        changelog_embed = disnake.Embed(
            color=0xFFFFFF
        )
        changelog_embed.title = f"Bot changes for {requested_date}"
        changelog_embed.description = "\n".join(changelog_cont[requested_date])
    else:
        changelog_embed = disnake.Embed(
            title="An error has occurred",
            description="Invalid date! You can check everything here: [Press](https://github.com/heechan194/Map-Searcher-Bot/blob/main/changelog.txt)",
            color=0xFF0000
        )
    write_log(f"used /changelog {requested_date}.", inter.author)
    await inter.edit_original_message(embed=changelog_embed)