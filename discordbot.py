"""
    The Bot, which gives you a download link from the map name
            Bot by HeeChan  & Kassini    |       Version: 2.3
            https://github.com/heechan194/Map-Searcher-Bot
                    https://github.com/heechan194
                    https://github.com/KassiniGit

"""
import discord
import json
import sys
import os
import datetime

import psutil
import requests
import disnake
import pandas as pd
from bs4 import BeautifulSoup as BS
import time
from typing import Optional, List
from disnake.ext import commands
from disnake.ui import Button

file = open("config.json", "r")
config = json.load(file)

intents = discord.Intents.all()
intents.message_content = True

Bot = commands.Bot(config['prefix'], intents=disnake.Intents.all())
activity = disnake.Game(name="/about <- all information")
status = discord.Status.do_not_disturb

Version = "`2.3`"


class UTC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


global startTime
startTime = time.time()

@Bot.event
async def on_slash_command_error(inter: disnake.ApplicationCommandInteraction, error: Exception) -> None:
    return


@Bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error


@Bot.event
async def on_ready():
    await Bot.change_presence(activity=activity, status=status)
    global startTime
    startTime = time.time()
    time.sleep(0.50)
    print("Loading bot data...")
    time.sleep(1.00)
    print("+ Game activity. [1/3]")
    time.sleep(1.00)
    print("+ Bot status. [2/3]")
    time.sleep(1.00)
    print("+ UpTime. [3/3]")
    time.sleep(1.00)
    print("logged in as: " + str(Bot.user))


@Bot.slash_command(name="about", description="Information about this bot.")
async def about(inter: disnake.ApplicationCommandInteraction):
    await inter.response.defer()
    uptime = str(datetime.timedelta(seconds=int(round(time.time() - startTime))))
    embed = disnake.Embed(
        description="\n Bot owners: [HeeChan](https://steamcommunity.com/id/6561198326716239/) & [Kassini](https://steamcommunity.com/id/I_God_Sigma/)"
                    "\n You can contract us in discord, **heechan194** or **.kassini**"
                    "\n"
                    "\n A **Python** bot for **Discord**, the main function of which is to give people a link to the map that they entered in the search with the </maplink:1123674597494100119> command. If you want to see all bot commands, you can type </help:1125453195750166538>."
                    "\n"
                    "\n At the moment the bot is still being implemented to the end, being updated or we are trying to add some new features. If you find any bugs, want to suggest new features or any optimization, you can write in the discord: **heechan194** or **.kassini**."
                    "\n",
        color=0xFFFFFF
    )
    embed.set_thumbnail(url="https://i.pinimg.com/564x/a6/ce/74/a6ce746599c3834a587af159d448978c.jpg")
    Gitbuttonheechan = Button(label="HeeChan", style=disnake.ButtonStyle.url,
                              url="https://github.com/heechan194")
    Gitbuttonkassini = Button(label="Kassini", style=disnake.ButtonStyle.url,
                              url="https://github.com/KassiniGit")
    Gitbutton = Button(label="Source Code", style=disnake.ButtonStyle.url,
                       url="https://github.com/heechan194/Map-Searcher-Bot")
    Invitebutton = Button(label="Bot invite", style=disnake.ButtonStyle.url,
                          url="https://discord.com/api/oauth2/authorize?client_id=1122605455194193931&permissions=277025396736&scope=applications.commands%20bot")

    embed.set_author(
        name="Map Searcher:",
        url="https://github.com/heechan194/Map-Searcher-Bot",
        icon_url="https://e7.pngegg.com/pngimages/94/403/png-clipart-beautiful-black-arrow-black-arrow-pretty-arrow.png",
    )
    embed.add_field(name="Version:", value=Version)
    embed.add_field(name="UpTime:", value="`" + uptime + "`")
    embed.add_field(name='RAM:', value="`" + str(psutil.virtual_memory().percent) + " %`")
    await inter.edit_original_message(embed=embed,
                                      components=[Gitbuttonheechan, Gitbuttonkassini, Gitbutton, Invitebutton])


def setup(bot):
    bot.add_cog(UTC(bot))


helpopt = commands.option_enum(["commands", "run usage"])


@Bot.slash_command(name="help", description="Navigation help command, some information")
async def help(inter: disnake.ApplicationCommandInteraction, choice: helpopt):
    uptime = str(datetime.timedelta(seconds=int(round(time.time() - startTime))))
    await inter.response.defer()
    help_things = {
        "commands": "\n **Bot Commands:**"
                    "\n"
                    "\n </maplink:1123674597494100119> - Gives you the link to download the map from name."
                    "\n </fastdl:1123717659637321749> - Link to FastDL."
                    "\n </admin:1125154934904586363> - Admin commands. Can restart/shutdown bot."
                    "\n </credits:1123702310837686292> - Credits to people, who helped in writing this bot"
                    "\n </help:1125453195750166538> - Navigation help command."
                    "\n </about:1125443661547712644> - About this bot.",

        "run usage": "\n **Current** bot uptime: `" + uptime + "`"
                                                               "\n **RAM** Usage: `" + str(
            psutil.virtual_memory().percent) + " %`"
    }
    if choice in help_things:
        embed = disnake.Embed(
            title="",
            description=f"{help_things[choice]}",
            color=0xFFFFFF
        )
        await inter.edit_original_message(embed=embed)


adminoption = commands.option_enum(["shutdown", "restart"])


@Bot.slash_command(name="admin", description="Admin commands.")
async def admin(inter: disnake.ApplicationCommandInteraction, choice: adminoption):
    await inter.response.defer()
    allowed_users = [1041292965483651102, 390221466689339392]
    if inter.user.id in allowed_users:
        if choice == "shutdown":
            await inter.edit_original_message(content="✔️ -> **Successfully shut down by** " + inter.author.mention)
            print("[DEBUG] Bot has been killed by\n ", inter.author)
            # raise exit("Bot has been killed by an Admin!")
            raise SystemExit("Bot has been killed by\n", inter.author, "in", inter.channel)
        elif choice == "restart":
            await inter.edit_original_message(content="✔️ -> **The bot is restarting by** " + inter.author.mention)
            print("Bot has been restarted by:", inter.author, "in", inter.channel)
            python = sys.executable
            os.execl(python, python, *sys.argv)
    else:
        print("[DEBUG]", inter.author, "<- tried to use the admin command without permissions!")
        await inter.edit_original_message(content="❗ -> **You don't have permissions to use this command!**")


@Bot.slash_command(name="fastdl", description="Gives you the link to download the map!")
async def fastdl(inter: disnake.ApplicationCommandInteraction):
    await inter.response.defer()
    if config["url"] and config["unloze_url"] == "":
        await inter.send("❗ -> FastDL links is empty at the moment!")
    else:
        fastdl_embed = disnake.Embed(
            title="FastDL",
            description="Below are links to all FastDL that the bot uses:"
                        "\n"
                        "\n" + config["url"] +
                        "\n" + config["unloze_url"],
            color=0xFFFFFF
        )
        await inter.edit_original_message(embed=fastdl_embed)


ITEMS_PER_PAGE = 20


class Paginator(disnake.ui.View):
    def __init__(self, items: List[str], link: List[str], name, choice, size: List[str], date: List[str],
                 timeout: Optional[float] = None):
        super().__init__(timeout=timeout)
        self.items = items
        self.link = link
        self.name = name
        self.choice = choice
        self.size = size
        self.date = date
        self.view = None
        self.current_page = 1
        self.message = None

    async def show_page(self, page: int):
        self.first_page_button.disabled = self.previous_page_button.disabled = (page == 1)
        self.next_page_button.disabled = self.last_page_button.disabled = (page == self.get_max_pages())
        pages = [self.items[i:i + ITEMS_PER_PAGE] for i in range(0, len(self.items), ITEMS_PER_PAGE)]
        if not pages:
            embed = disnake.Embed(title=f"❗ No results found for `{self.name}` in `{self.choice}` option.", color=0xFF0000)
            return embed

        page_items = pages[page - 1]
        embed = disnake.Embed(title=f"Input `{self.name}` has results: **{len(self.items)}**", color=0xFFFFFF)
        embed.add_field(name="", value="Click the map name to download it!")
        for i, item in enumerate(page_items):
            embed.add_field(name="",
                            value=f"> ㅤ{(page - 1) * 20 + i + 1}. [{item}]({self.link[(page - 1) * 20 + i]})"
                                  f" [{self.date[(page - 1) * 20 + i]}, {self.size[(page - 1) * 20 + i]} - {self.choice}]", 
                            inline=False)
        self.next_page.label = f"Page {self.current_page}/{self.get_max_pages()}"
        return embed

    @disnake.ui.button(label="◀◀ First", style=disnake.ButtonStyle.grey)
    async def first_page_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await self.change_page(1, interaction)

    @disnake.ui.button(label="◀ Previous", style=disnake.ButtonStyle.grey)
    async def previous_page_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await self.change_page(self.current_page - 1, interaction)

    @disnake.ui.button(label="Page 1/1", style=disnake.ButtonStyle.grey, disabled=True)
    async def next_page(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        return

    @disnake.ui.button(label="Next ▶", style=disnake.ButtonStyle.grey)
    async def next_page_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await self.change_page(self.current_page + 1, interaction)

    @disnake.ui.button(label="Last ▶▶", style=disnake.ButtonStyle.grey)
    async def last_page_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await self.change_page(self.get_max_pages(), interaction)

    async def change_page(self, page: int, interaction: disnake.Interaction):
        await interaction.response.defer()
        if page < 1 or page > self.get_max_pages():
            return
        self.current_page = page
        embed = await self.show_page(self.current_page)
        self.view = self
        await interaction.edit_original_response(view=self.view, embed=embed)

    def get_max_pages(self):
        return (len(self.items) - 1) // ITEMS_PER_PAGE + 1

    async def start(self, inter: disnake.ApplicationCommandInteraction):
        if self.get_max_pages() <= 1:
            self.clear_items()
        elif self.get_max_pages() == 2:
            self.remove_item(self.first_page_button)
            self.remove_item(self.last_page_button)
        embed = await self.show_page(self.current_page)
        self.message = await inter.edit_original_message(embed=embed, view=self)
        self.view = self  # Добавляем ссылку на текущий объект view
        await inter.edit_original_response()


fastdllnik = commands.option_enum(["CS:GO", "CS2", "CS:S"])


@Bot.slash_command(name="maplink", description="Gives you the link to download the map!")
async def maplink(inter: disnake.ApplicationCommandInteraction, choice: fastdllnik, mapname: str):
    await inter.response.defer(ephemeral=True)
    name = mapname
    url = 0
    if choice == "CS:GO":
        url = 'https://www.notkoen.xyz/fastdl/csgo/maps/'
    elif choice == "CS2":
        url = 'https://www.notkoen.xyz/fastdl/cs2/maps/'
    elif choice == "CS:S":
        url = 'https://fastdl.unloze.com/css_ze/maps/'

    response = requests.get(url)
    html = response.text
    soup = BS(html, 'html.parser')

    link = []
    namemap = []
    size = []
    date = []

    if choice == "CS:GO" or choice == "CS2":
        table_rows = soup.find_all('tr')
        for row in table_rows:
            name_cell = row.find('td', class_='fb-n')
            if name_cell:
                name_text = name_cell.text.strip()
                if pd.Series(name_text.lower()).str.contains(name.lower()).any():
                    link_cell = row.find('a')
                    if link_cell:
                        href = link_cell['href']
                        link.append('https://www.notkoen.xyz' + href)
                        namemap.append(name_text)
                        size_cell = row.find('td', class_='fb-s')
                        if size_cell:
                            size_text = size_cell.text.strip()
                            size_text = size_text.replace(' KB', '')
                            size_mb = float(size_text) / 1048
                            size.append(f"{size_mb:.2f} MB")
                        date_cell = row.find('td', class_='fb-d')
                        if date_cell:
                            date_text = date_cell.text.strip()
                            date_value = date_text.split()[0]
                            date.append(date_value)

    elif choice == "CS:S":
        table_rows = soup.find_all('a')
        for row in table_rows:
            name_text = row.text.strip()
            if pd.Series(name_text.lower()).str.contains(name.lower()).any():
                href = row['href']
                link.append(url + href)
                namemap.append(name_text)
                size_text = row.next_sibling.strip()
                size_value = size_text.split()[-1]
                dateyear = size_text.split()[0]
                size_mb = float(size_value) / 1024 / 1024
                size.append(f"{size_mb:.2f} MB")
                date.append(dateyear)
    for i in range(len(namemap)):
        namemap[i] = namemap[i].replace('.bsp.bz2', '')
        namemap[i] = namemap[i].replace('.bsp', '')
        namemap[i] = namemap[i].replace('.vpk', '')
    paginator = Paginator(namemap, link, name, choice, size, date)
    await paginator.start(inter)
    print("[DEBUG]", inter.author, "<- used maplink command!")


@Bot.slash_command(name="credits", description="Credits to people, who helped in writing this bot")
async def credits(inter: disnake.ApplicationCommandInteraction):
    await inter.response.defer()
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


packvote = commands.option_enum(["Zeddy", "GFL", "High Contract Zombies", "Mapeadores", "ZombieDen", "MoeUB", "ExG"])


@Bot.slash_command(name="pack", description="Download resource packs of various servers!")
async def pack(inter: disnake.ApplicationCommandInteraction, pack: packvote):
    await inter.response.defer()
    packs = {
        "Zeddy": "https://www.notkoen.xyz/fastdl/public/packs/Zeddy%20Resource%20Pack.7z",
        "GFL": "https://www.notkoen.xyz/fastdl/public/packs/GFL%20Resource%20Pack.7z",
        "High Contract Zombies": "https://www.notkoen.xyz/fastdl/public/packs/GFL%20High%20Contrast%20Zombies.7z",
        "Mapeadores": "https://www.notkoen.xyz/fastdl/public/packs/Mapeadores%20Resource%20Pack.7z",
        "ZombieDen": "https://www.notkoen.xyz/fastdl/public/packs/ZombieDen%20Resource%20Pack.7z",
        "MoeUB": "https://www.notkoen.xyz/fastdl/public/packs/MoeUB%20Resource%20Pack.7z",
        "ExG": "https://www.notkoen.xyz/fastdl/public/packs/ExG%20Resource%20Pack.7z"
    }
    if pack in packs:
        embed = disnake.Embed(
            title="Click to download the Resource Pack!",
            description=f"[{pack} Resource Pack]({packs[pack]})",
            color=0xFFFFFF
        )
        await inter.edit_original_message(embed=embed)
    else:
        await inter.edit_original_message("❗ -> **You wrote something wrong, please check it!**")


try:
    print("The bot is running!")
    Bot.run(config["token"])
except discord.errors.LoginFailure:
    exit("TOKEN IS INVALID")