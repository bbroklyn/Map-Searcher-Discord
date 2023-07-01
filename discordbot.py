"""
    The Bot, which gives you a download link from the map name
            Bot by HeeChan  & Kassini    |       Version: 1.6
            https://github.com/heechan194/Map-Searcher-Bot
                    https://github.com/heechan194
                    https://github.com/KassiniGit

"""
import discord
import json
import sys
import os

import requests
import disnake
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from typing import Optional, List
from disnake.ext import commands
from disnake.ui import Button

file = open("config.json", "r")
config = json.load(file)

intents = discord.Intents.all()
intents.message_content = True

Bot = commands.Bot(config['prefix'], intents=disnake.Intents.all())
activity = disnake.Game(name="searching for the links...")
status = discord.Status.do_not_disturb

Version = "The latest one is `1.6`"

@Bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return


@Bot.event
async def on_ready():
    sleep(0.5)
    await Bot.change_presence(activity=activity, status=status)
    print("+ Game activity. [1/2]")
    print("+ Bot status [2/2]")
    print("logged in as: "+str(Bot.user))


helpopt = commands.option_enum(["information", "commands"])


@Bot.slash_command(name="helpme", description="Gives you every information about this bot/owners")
async def helpme(inter: disnake.ApplicationCommandInteraction, choice: helpopt):
    await inter.response.defer()
    help_things = {
        "information": "**information about Map Searcher:**"
                       "\n"
                       "\n Bot owners: [HeeChan](https://steamcommunity.com/id/6561198326716239/) & [Kassini](https://steamcommunity.com/id/I_God_Sigma/)"
                       "\n You can contract us, **heechan194** or **.kassini**"
                       "\n"
                       "\n A **Python** bot for **Discord**, the main function of which is to give people a link to the map that they entered in the search with the </maplink:1123674597494100119> command. If you want to see all bot commands, you can type </helpme:1123680440662904933>."
                       "\n"
                       "\n At the moment the bot is still being implemented to the end, being updated or we are trying to add some new features. If you find any bugs, want to suggest new features or any optimization, you can write in the discord: **heechan194** or **.kassini**."
                       "\n"
                       "\n Version: " + Version,
        "commands": "\n **Bot Commands:**"
                    "\n"
                    "\n </maplink:1123674597494100119> - Gives you the link to download the map from name."
                    "\n </fastdl:1123717659637321749> - Link to FastDL"
                    "\n </admin:1124782641581916200> - Shutdowns the bot. Only for Admins!"
                    "\n </credits:1123702310837686292> - Credits to people, who helped in writing this bot"
                    "\n </helpme:1123680440662904933> - Information/commands about this bot",
    }
    if choice in help_things:
        embed = disnake.Embed(
            title="",
            description=f"{help_things[choice]}",
            color=0xFFFFFF
        )
        Gitbuttonheechan = Button(label="HeeChan", style=disnake.ButtonStyle.url,
                        url="https://github.com/heechan194")
        Gitbuttonkassini = Button(label="Kassini", style=disnake.ButtonStyle.url,
                        url="https://github.com/KassiniGit")
        Gitbutton = Button(label="Bot Open Code", style=disnake.ButtonStyle.url,
                        url="https://github.com/heechan194/Map-Searcher-Bot")
        Invitebutton = Button(label="Bot invite", style=disnake.ButtonStyle.url,
                           url="https://discord.com/api/oauth2/authorize?client_id=1122605455194193931&permissions=277025396736&scope=applications.commands%20bot")

        await inter.edit_original_message(embed=embed, components=[Gitbuttonheechan, Gitbuttonkassini, Gitbutton, Invitebutton])




adminoption = commands.option_enum(["shutdown", "restart"])

@Bot.slash_command(name="admin", description="Admin commands.")
async def admin(inter: disnake.ApplicationCommandInteraction, choice: adminoption):
    await inter.response.defer()
    allowed_users = [1041292965483651102, 390221466689339392]
    if inter.user.id in allowed_users:
        if choice == "shutdown":
            await inter.edit_original_message(content="Successfully shut down by " + inter.author.mention)
            print("Bot has been killed by\n ", inter.author)
            #raise exit("Bot has been killed by an Admin!")
            raise SystemExit("Bot has been killed by\n", inter.author)
        elif choice == "restart":
            await inter.edit_original_message(content="the bot is restarting by " + inter.author.mention)
            print("Bot has been restarted by:", inter.author)
            python = sys.executable
            os.execl(python, python, * sys.argv)
    else:
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
    def __init__(self, items: List[str], link: List[str], name, choice, timeout: Optional[float] = None):
        super().__init__(timeout=timeout)
        self.items = items
        self.link = link
        self.name = name
        self.choice = choice
        self.view = None
        self.current_page = 1
        self.message = None

    async def show_page(self, page: int):
        self.first_page_button.disabled = self.previous_page_button.disabled = (page == 1)
        self.next_page_button.disabled = self.last_page_button.disabled = (page == self.get_max_pages())
        pages = [self.items[i:i + ITEMS_PER_PAGE] for i in range(0, len(self.items), ITEMS_PER_PAGE)]
        if not pages:
            embed = disnake.Embed(title=f"❗ No results found for `{self.name}`", color=0xFF0000)
            return embed

        page_items = pages[page - 1]
        embed = disnake.Embed(title=f"Input `{self.name}` has results: **{len(self.items)}**", color=0xFFFFFF)
        embed.add_field(name="", value="Click the map name to download it!")
        for i, item in enumerate(page_items):
            embed.add_field(name="",
                            value=f"> ㅤ{(page - 1) * 20 + i + 1}. [{item}]({self.link[(page - 1) * 20 + i]}) [{self.choice}]",
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


fastdllnik = commands.option_enum(["CS:GO", "CS:S"])

@Bot.slash_command(name="maplink", description="Gives you the link to download the map!")
async def maplink(inter: disnake.ApplicationCommandInteraction, choice: fastdllnik, mapname: str):
    await inter.response.defer(ephemeral=True)
    name = mapname
    url = 0
    urlreplace = 0
    if choice == "CS:GO":
        url = 'https://www.notkoen.xyz/fastdl/csgo/maps/'
        urlreplace = "https://www.notkoen.xyz"
    elif choice == "CS:S":
        url = 'https://fastdl.unloze.com/css_ze/maps/'
        urlreplace = "https://fastdl.unloze.com/css_ze/maps/"

    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    a_tags = soup.find_all('a')
    link = []
    namemap = []
    for a_tag in a_tags:
        href = a_tag['href']
        if pd.Series(href.lower()).str.contains(name.lower()).any():
            link.append(urlreplace + href)
            namemap.append(urlreplace + href)
        for i in range(len(namemap)):
            namemap[i] = namemap[i].replace(url, '')
            namemap[i] = namemap[i].replace('.bsp.bz2', '')
            namemap[i] = namemap[i].replace('.bsp', '')
    paginator = Paginator(namemap, link, name, choice)
    await paginator.start(inter)


@Bot.slash_command(name="credits", description="Credits to people, who helped in writing this bot")
async def credits(inter: disnake.ApplicationCommandInteraction):
    await inter.response.defer()
    embed = disnake.Embed(
        title="Credits",
        description=""
                    "\n"
                    "\n **Thanks to:**"
                    "\n **NiceShot** -> helped us with some things, gave idea about some features "
                    "\n **koen** -> we are using his FastDL."
                    "\n **Killik** -> Hosting for the bot.",
        color=0xFFFFFF
    )
    await inter.edit_original_message(embed=embed)


packvote = commands.option_enum(["Zeddy", "GFL", "Mapeadores"])


@Bot.slash_command(name="pack", description="Download resource packs of various servers!")
async def pack(inter: disnake.ApplicationCommandInteraction, pack: packvote):
    await inter.response.defer()
    packs = {
        "Zeddy": "https://www.notkoen.xyz/fastdl/public/packs/Zeddy%20Resource%20Pack.7z",
        "GFL": "https://www.notkoen.xyz/fastdl/public/packs/GFL%20Resource%20Pack.7z",
        "Mapeadores": "https://www.notkoen.xyz/fastdl/public/packs/Mapeadores%20Resource%20Pack.7z"
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
    print("Starting the bot...")
    Bot.run(config["token"])
except discord.errors.LoginFailure:
    exit("TOKEN IS INVALID")