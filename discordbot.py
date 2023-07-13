"""
    The Bot, which gives you a download link from the map name and much more
                Bot by HeeChan  & Kassini    |       Version: 2.6
                https://github.com/heechan194/Map-Searcher-Bot
                        https://github.com/heechan194
                        https://github.com/KassiniGit

"""
import json
import sys
import os
import datetime

import a2s
import psutil
import requests
import disnake
import pandas as pd
from rapidfuzz import fuzz
from bs4 import BeautifulSoup as BS
import time
from typing import Optional, List
from disnake.ext import commands
from disnake.ui import Button

Version = "`2.6`"


file = open("config.json", "r")
config = json.load(file)

changelogs=open("changelog.txt","r")
changelogs_content = changelogs.read()

intents = disnake.Intents(messages=True, guilds=True)

Bot = commands.Bot(config['prefix'], intents=disnake.Intents.all())
activity = disnake.Game(name="/about <- about me :)")
status = disnake.Status.do_not_disturb



class UTC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


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
    print("Token verification was successful!")
    await Bot.change_presence(activity=activity, status=status)
    global startTime
    startTime = time.time()
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
                    "\n If you want to add server, just do pull request and edit config.json."
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
    embed.set_footer(text="*if something does not work, then refer to .kassini or heechan194.")
    embed.add_field(name="Version:", value=Version)
    embed.add_field(name="UpTime:", value="`" + uptime + "`")
    embed.add_field(name='RAM:', value="`" + str(psutil.virtual_memory().percent) + " %`")
    await inter.edit_original_message(embed=embed,
                                      components=[Gitbuttonheechan, Gitbuttonkassini, Gitbutton, Invitebutton])


def setup(bot):
    bot.add_cog(UTC(bot))


class ServerPlayers(disnake.ui.View):
    def __init__(self, players: List[str], times: List[str], player, timeout: Optional[float] = None):
        super().__init__(timeout=timeout)
        self.players_list = players
        self.time = times
        self.players = player
        self.message = None
    @disnake.ui.button(label="List of players", style=disnake.ButtonStyle.grey)
    async def button_callback(self, button: disnake.ui.Button, inter: disnake.Interaction):
        player_names_str = ""
        for player, time in zip(self.players_list, self.time):
            player_names_str += f"{player} -> {time}\n"

        await inter.response.send_message(f"**Players {self.players}**:\n```{player_names_str}```", ephemeral=True)


# Получение списка серверов из файла JSON
servers = [server['name'] for server in config['trackers']]
# Определение параметра команды с использованием списка серверов
servertr = commands.option_enum(servers)
@Bot.slash_command(name="servertrack", description="Get all server information.")
async def servertrack(inter: disnake.ApplicationCommandInteraction, server: servertr = commands.Param(name="option", description="Choose a server.")):
    await inter.response.defer()
    for server_info in config['trackers']:
        if server_info['name'] == server:
            server_address = server_info['address']
            server_port = server_info['port']
            server_info = a2s.info((server_address,server_port))
            player_list = a2s.players((server_address,server_port))

            playername = []
            times = []
            for player in player_list:

                player_duration = player.duration
                minutes, seconds = divmod(player_duration, 60)
                hours, minutes = divmod(minutes, 60)

                if hours < 1:
                    duration_formatted = f"{int(minutes):02d}:{int(seconds):02d}"
                else:
                    duration_formatted = f"{int(hours)}:{int(minutes):02d}:{int(seconds):02d}"
                playername.append(player.name)
                times.append(duration_formatted)
            server_name = server_info.server_name
            curr_map = server_info.map_name.split('/')[-1]
            players = str(server_info.player_count) + '/' + str(server_info.max_players)
            embed = disnake.Embed(
                title=f"**{server} tracker:**",
                color=0xFFFFFF
            )
            connect = f"{server_address}:{server_port}"
            connectlink =f"https://vauff.com/?ip={connect}"
            embed.add_field(name="Server Name:", value=server_name, inline=False)
            embed.add_field(name="Current Map:", value=curr_map, inline=False)
            embed.add_field(name="Players:", value=players, inline=False)
            embed.add_field(name="Connect:", value=f"[{connect}]({connectlink}) <- Press to join", inline=False)
            serverplayers = ServerPlayers(playername, times, players)
            await inter.followup.send(embed=embed, view=serverplayers)


helpopt = commands.option_enum(["commands", "run usage"])
@Bot.slash_command(name="help", description="Navigation help command, some information.",)

async def help(inter: disnake.ApplicationCommandInteraction, option: helpopt = commands.Param(name= "option", description="Choose an option.")):
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
                    "\n </about:1125443661547712644> - About this bot."
                    "\n </servertrack:1128787852612882432> - Get all server information.",

        "run usage": "\n **Current** bot uptime: `" + uptime + "`"
                                                               "\n **RAM** Usage: `" + str(
            psutil.virtual_memory().percent) + " %`"
    }
    if option in help_things:
        embed = disnake.Embed(
            title="",
            description=f"{help_things[option]}",
            color=0xFFFFFF
        )
        await inter.edit_original_message(embed=embed)


adminoption = commands.option_enum(["shutdown", "restart"])
@Bot.slash_command(name="admin", description="Admin commands.")
async def admin(inter: disnake.ApplicationCommandInteraction, action: adminoption = commands.Param(name= "action", description="Select admin command actions.")):
    await inter.response.defer()
    allowed_users = [1041292965483651102, 390221466689339392]
    if inter.user.id in allowed_users:
        if action == "shutdown":
            await inter.edit_original_message(content="✔️ -> **Successfully shut down by** " + inter.author.mention)
            print("Bot has been killed by\n ", inter.author)
            # raise exit("Bot has been killed by an Admin!")
            raise SystemExit("Bot has been killed by\n", inter.author, "in", inter.channel)
        elif action == "restart":
            await inter.edit_original_message(content="✔️ -> **The bot is restarting by** " + inter.author.mention)
            print("Bot has been restarted by:", inter.author, "in", inter.channel)
            python = sys.executable
            os.execl(python, python, *sys.argv)
    else:
        print("[DEBUG]", inter.author, "<- tried to use the admin command without permissions!")
        await inter.edit_original_message(content="❗-> **You don't have permissions to use this command!**")


@Bot.slash_command(name="fastdl", description="Gives you the link to download the map.")
async def fastdl(inter: disnake.ApplicationCommandInteraction):
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
        await inter.edit_original_message(embed=fastdl_embed)


ITEMS_PER_PAGE = 20

class Paginator(disnake.ui.View):
    def __init__(self, items: List[str], link: List[str], name, game, size: List[str], date: List[str], search,
                 timeout: Optional[float] = None):
        super().__init__(timeout=timeout)
        self.items = items
        self.link = link
        self.name = name
        self.game = game
        self.size = size
        self.date = date
        self.search = search
        self.view = None
        self.current_page = 1
        self.message = None

    async def show_page(self, page: int):
        self.first_page_button.disabled = self.previous_page_button.disabled = (page == 1)
        self.next_page_button.disabled = self.last_page_button.disabled = (page == self.get_max_pages())
        pages = [self.items[i:i + ITEMS_PER_PAGE] for i in range(0, len(self.items), ITEMS_PER_PAGE)]
        if not pages:
            embed = disnake.Embed(title=f"❗-> **No results found for** `{self.name}`", color=0xFF0000)
            return embed

        page_items = pages[page - 1]
        def createembed(embed):
            for i, item in enumerate(page_items):
                embed.add_field(name="",
                                value=f"> ㅤ{(page - 1) * 20 + i + 1}. [{item}]({self.link[(page - 1) * 20 + i]}) "
                                      f"[{self.date[(page - 1) * 20 + i]}, {self.size[(page - 1) * 20 + i]} - {self.game}]",
                                inline=False)
            self.next_page.label = f"Page {self.current_page}/{self.get_max_pages()}"

        if self.search == True:

            embed = disnake.Embed(title=f"Input `{self.name}` has results: **{len(self.items)}**", color=0xFFFFFF)
            createembed(embed)
            return embed
        else:
            embed = disnake.Embed(title=f"Input `{self.name}` has no results.\n\nMaybe you mean:", color=0xFFA500)
            createembed(embed)
            return embed

    @disnake.ui.button(label="◀◀", style=disnake.ButtonStyle.grey)
    async def first_page_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await self.change_page(1, interaction)

    @disnake.ui.button(label="◀", style=disnake.ButtonStyle.grey)
    async def previous_page_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await self.change_page(self.current_page - 1, interaction)

    @disnake.ui.button(label="Page 1/1", style=disnake.ButtonStyle.blurple, disabled=True)
    async def next_page(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        return

    @disnake.ui.button(label="▶", style=disnake.ButtonStyle.grey)
    async def next_page_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await self.change_page(self.current_page + 1, interaction)

    @disnake.ui.button(label="▶▶", style=disnake.ButtonStyle.grey)
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
        self.view = self
        await inter.edit_original_response()



fastdllnik = commands.option_enum(["CS:GO", "CS2", "CS:S"])
@Bot.slash_command(name="maplink", description="Gives you the link to download the map!")
async def maplink(inter: disnake.ApplicationCommandInteraction, game: fastdllnik = commands.Param(name= "game", description="Enter the game name."), mapname: str = commands.Param(name= "mapname", description="Enter the map name")):
    await inter.response.defer(ephemeral=True)
    name = mapname
    url = 0
    if game == "CS:GO":
        url = 'https://www.notkoen.xyz/fastdl/csgo/maps/'
    elif game == "CS2":
        url = 'https://www.notkoen.xyz/fastdl/cs2/maps/'
    elif game == "CS:S":
        url = 'https://fastdl.unloze.com/css_ze/maps/'
    response = requests.get(url)
    html = response.text
    soup = BS(html, 'html.parser')
    link = []
    namemap = []
    size = []
    date = []
    search = True
    if game == "CS:GO" or game == "CS2":
        table_rows = soup.find_all('tr')
        found_match = False
        def process_row(row):
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
        for row in table_rows:
            name_cell = row.find('td', class_='fb-n')
            if name_cell:
                name_text = name_cell.text.strip()
                if pd.Series(name_text.lower()).str.contains(name.lower()).any():
                    process_row(row)
                    found_match = True
        if not found_match:
            for row in table_rows:
                name_cell = row.find('td', class_='fb-n')
                if name_cell:
                    name_text = name_cell.text.strip()
                    if fuzz.WRatio(name_text.lower(), name.lower()) >= 75:
                        search = False
                        process_row(row)
                        found_match = True

    elif game == "CS:S":
        def process_row(row):
            href = row['href']
            link.append(url + href)
            namemap.append(name_text)
            size_text = row.next_sibling.strip()
            size_value = size_text.split()[-1]
            dateyear = size_text.split()[0]
            size_mb = float(size_value) / 1024 / 1024
            size.append(f"{size_mb:.2f} MB")
            date.append(dateyear)

        table_rows = soup.find_all('a')
        found_match = False
        for row in table_rows:
            name_text = row.text.strip()
            if pd.Series(name_text.lower()).str.contains(name.lower()).any():
                process_row(row)
                found_match = True
        if not found_match:
            for row in table_rows:
                name_text = row.text.strip()
                if fuzz.WRatio(name_text.lower(), name.lower()) >= 75:
                    search = False
                    process_row(row)


    for i in range(len(namemap)):
        namemap[i] = namemap[i].replace('.bsp.bz2', '')
        namemap[i] = namemap[i].replace('.bsp', '')
        namemap[i] = namemap[i].replace('.vpk', '')
    paginator = Paginator(namemap, link, name, game, size, date, search)
    await paginator.start(inter)
    print("[DEBUG]", inter.author, "<- used /maplink")


@Bot.slash_command(name="credits", description="Credits to people, who helped in writing this bot.")
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
@Bot.slash_command(name="pack", description="Download resource packs of various servers.")
async def pack(inter: disnake.ApplicationCommandInteraction,pack: packvote = commands.Param(name= "packs", description="Enter the pack name.")):
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
        await inter.edit_original_message("❗-> **An error has occurred, this pack does not exist!**")


@Bot.slash_command(name="changelog", description="Gives you the bot changelogs.")
async def changelog(inter: disnake.ApplicationCommandInteraction):
    await inter.response.defer()
    changelog_cont = {
        "haslens": changelogs_content,
        "empty": "\n ❗-> **An error has occurred, `changelog.txt` is empty!**"
    }
    changelog_embed = disnake.Embed(
    title="All bot changes:",
    description=changelog_cont["haslens"] if len(changelogs_content) > 0 else changelog_cont["empty"],
    color=0xFFFFFF
    )
    await inter.edit_original_message(embed=changelog_embed)
changelogs.close()

try:
    print("Validating the token...")
    Bot.run(config["token"])
    time.sleep(1)
except:
    exit("TOKEN IS INVALID")    