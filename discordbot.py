"""
    The Bot, which gives you a download link from the map name
            Bot by HeeChan  & Kassini    |       Version: 1.0
                    https://github.com/heechan194

"""
import discord
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd

from time import sleep
from typing import Optional, List
import disnake
from disnake.ext import commands

file = open("config.json", "r")
config = json.load(file)

intents = discord.Intents.all()
intents.message_content = True

Bot = commands.Bot(config['prefix'], intents=disnake.Intents.all())
activity = discord.Game(name="Searching for the links...")
status = discord.Status.do_not_disturb

Version = "1.2"

@Bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return


@Bot.event
async def on_ready():
    sleep(0.5)
    await Bot.change_presence(activity=disnake.Game(name="searching for the links..."), status=status)
    print("Game activity loaded. (1/3)")
    print("Bot status loaded! (2/3)")
    print("Bot enabled! (3/3)")


helpopt = commands.option_enum(["information", "commands"])


@Bot.slash_command(name="helpme", description="Gives you every information about this bot/owners")
async def helpme(inter: disnake.ApplicationCommandInteraction, choice: helpopt):
    help_things = {
        "information": "This Bot gives you a **link** to download the map by its name and much more!"
                       "\n"
                       "\n Bot owners: [HeeChan](https://steamcommunity.com/id/6561198326716239/) & [Kassini](https://steamcommunity.com/id/I_God_Sigma/)"
                       "\n You can contract us, **heechan194** or **.kassini**"
                       "\n",
        "commands": "\n **Bot Commands:**"
                    "\n"
                    "\n </maplink:1123674597494100119> - Gives you the link to download the map from name."
                    "\n </fastdl:1123717659637321749> - Link to FastDL"
                    "\n </shutdown:1123709315887403078> - Shutdowns the bot. Only for Admins!"
                    "\n </credits:1123702310837686292> - Credits to people, who helped in writing this bot"
                    "\n </helpme:1123680440662904933> - Information/commands about this bot",
    }
    if choice in help_things:
        embed = disnake.Embed(
            title="",
            description=f"{help_things[choice]}",
            color=0xFFFFFF
        )
        embed.add_field(name="", value="\n")
        embed.add_field(name="Current Version:", value=Version)
        await inter.send(embed=embed)


@Bot.slash_command(name="shutdown", description="Kills the bot")
async def shutdown(inter: disnake.ApplicationCommandInteraction):
    if inter.user.id in [1041292965483651102, 390221466689339392]:
        await inter.send("Successfully shut down!")
        print(Bot.user.name)
        sleep(1)
        exit("Bot has been killed by an Admin!")
    else:
        await inter.send("You don't have permissions to use this command!")


@Bot.slash_command(name="fastdl", description="Gives you the link to download the map!")
async def fastdl(inter: disnake.ApplicationCommandInteraction):
    if config["url"] == "":
        await inter.send("FastDL links is empty at the moment!")
    else:
        fastdl_embed = disnake.Embed(
            title="FastDL",
            description="Below are links to all FastDL that the bot uses:"
                        "\n"
                        "\n" + config["url"],
            color=0xFFFFFF
        )
        await inter.send(embed=fastdl_embed)


ITEMS_PER_PAGE = 20


class Paginator(disnake.ui.View):
    def __init__(self, items: List[str], link: List[str], name, timeout: Optional[float] = None):
        super().__init__(timeout=timeout)
        self.items = items
        self.link = link
        self.name = name
        self.view = None
        self.current_page = 1
        self.message = None

    async def show_page(self, page: int):
        pages = [self.items[i:i + ITEMS_PER_PAGE] for i in range(0, len(self.items), ITEMS_PER_PAGE)]
        if not pages:
            embed = disnake.Embed(title=f"No results found for `{self.name}`", color=0xFF0000)
            return embed

        page_items = pages[page - 1]
        embed = disnake.Embed(title=f"Input `{self.name}` has results: **{len(self.items)}**", color=0xFFFFFF)
        embed.add_field(name="", value="Click the map name to download it!")
        for i, item in enumerate(page_items):
            embed.add_field(name="",
                            value=f"> ㅤ{(page - 1) * 20 + i + 1}. [{item}]({self.link[(page - 1) * 20 + i]})",
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
        embed = await self.show_page(self.current_page)
        self.message = await inter.edit_original_message(embed=embed, view=self)
        self.view = self  # Добавляем ссылку на текущий объект view
        await inter.edit_original_response()


@Bot.slash_command(name="maplink", description="Gives you the link to download the map!")
async def maplink(inter: disnake.ApplicationCommandInteraction, name: str):
    await inter.response.defer(ephemeral=True)
    url = 'https://www.notkoen.xyz/fastdl/csgo/maps/'
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    a_tags = soup.find_all('a')
    link = []
    namemap = []
    for a_tag in a_tags:
        href = a_tag['href']
        if pd.Series(href.lower()).str.contains(name.lower()).any():
            link.append("https://www.notkoen.xyz" + href)
            namemap.append('https://www.notkoen.xyz' + href)
        for i in range(len(namemap)):
            namemap[i] = namemap[i].replace('https://www.notkoen.xyz/fastdl/csgo/maps/', '')
            namemap[i] = namemap[i].replace('.bsp.bz2', '')
            namemap[i] = namemap[i].replace('.bsp', '')
    paginator = Paginator(namemap, link, name)
    await paginator.start(inter)


@Bot.slash_command(name="credits", description="Credits to people, who helped in writing this bot")
async def credits(inter: disnake.ApplicationCommandInteraction):
    embed = disnake.Embed(
        title="Credits",
        description=""
                    "\n"
                    "\n **Thanks to:**"
                    "\n **NiceShot** - helped us with some things, gave idea about some features "
                    "\n **koen** - we're using his FastDL."
                    "\n **Killik** -Hosting for the bot.",
        color=0xFFFFFF
    )
    await inter.send(embed=embed)


packvote = commands.option_enum(["Zeddy", "GFL", "Mapeadores"])


@Bot.slash_command(name="pack", description="Download resource packs of various servers!")
async def pack(inter: disnake.ApplicationCommandInteraction, pack: packvote):
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
        await inter.send(embed=embed)
    else:
        await inter.send("You wrote something wrong, please check it!")


try:
    print("Starting the bot...")
    Bot.run(config["token"])
except discord.errors.LoginFailure:
    exit("TOKEN IS INVALID")
