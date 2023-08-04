import json
import requests
import disnake
import pandas as pd
from rapidfuzz import fuzz
from bs4 import BeautifulSoup as BS
from typing import Optional, List
from logger import write_log
from disnake.ext import commands, tasks


file = open("config.json", "r")
config = json.load(file)

Bot = commands.Bot(config['prefix'], intents=disnake.Intents.all())
ITEMS_PER_PAGE = 20
command_author_id = None

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

        def create_embed(embed):
            for i, item in enumerate(page_items):
                embed.add_field(name="",
                                value=f"> ㅤ{(page - 1) * 20 + i + 1}. [{item}]({self.link[(page - 1) * 20 + i]}) "
                                      f"[{self.date[(page - 1) * 20 + i]}, {self.size[(page - 1) * 20 + i]} - {self.game}]",
                                inline=False)
            self.next_page.label = f"Page {self.current_page}/{self.get_max_pages()}"

        if self.search == True:
            embed = disnake.Embed(title=f"Input `{self.name}` has results: **{len(self.items)}**", color=0xFFFFFF)
            create_embed(embed)
            return embed
        else:
            embed = disnake.Embed(title=f"Input `{self.name}` has no results.\n\nMaybe you mean:", color=0xFFA500)
            create_embed(embed)
            return embed

    @disnake.ui.button(label="◀◀", style=disnake.ButtonStyle.grey)
    async def first_page_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        global command_author_id
        if interaction.user.id != command_author_id:
            return
        await self.change_page(1, interaction)

    @disnake.ui.button(label="◀", style=disnake.ButtonStyle.grey)
    async def previous_page_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        global command_author_id
        if interaction.user.id != command_author_id:
            return
        await self.change_page(self.current_page - 1, interaction)

    @disnake.ui.button(label="Page 1/1", style=disnake.ButtonStyle.blurple, disabled=True)
    async def next_page(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        return

    @disnake.ui.button(label="▶", style=disnake.ButtonStyle.grey)
    async def next_page_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        global command_author_id
        if interaction.user.id != command_author_id:
            return
        await self.change_page(self.current_page + 1, interaction)

    @disnake.ui.button(label="▶▶", style=disnake.ButtonStyle.grey)
    async def last_page_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        global command_author_id
        if interaction.user.id != command_author_id:
            return
        await self.change_page(self.get_max_pages(), interaction)
        
    @disnake.ui.button(style=disnake.ButtonStyle.red, emoji="🗑️")
    async def delete_message_button(self, button: disnake.ui.Button, inter: disnake.Interaction):
        global command_author_id
        if inter.user.id != command_author_id:
            return        
        await inter.response.defer()
        await inter.delete_original_response()       

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





fast_dl_link = commands.option_enum(["CS:GO", "CS2", "CS:S"]) 
@Bot.slash_command(name="mlink", 
                   description="Gives you the link to download the map!")
async def map_link_command(inter: disnake.ApplicationCommandInteraction,
                  game: fast_dl_link = commands.Param(name="game",
                                                      description="Enter the game name."),
                  map_name: str = commands.Param(name="mapname",
                                                 description="Enter the map name")):
    await inter.response.defer()
    global command_author_id
    command_author_id = inter.author.id
    name = map_name
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
    name_map = []
    size = []
    date = []
    search = True

    if game == "CS:GO" or game == "CS2":
        search = parser_link_csgo_cs2(soup, search, name, link, name_map, size, date)
    elif game == "CS:S":
        search = parser_link_css(soup, search, url, name, link, name_map, size, date)
    for i in range(len(name_map)):
        name_map[i] = name_map[i].replace('.bsp.bz2', '')
        name_map[i] = name_map[i].replace('.bsp', '')
        name_map[i] = name_map[i].replace('.vpk', '')
    paginator = Paginator(name_map, link, name, game, size, date, search)
    write_log("used /mlink.", inter.author)
    await paginator.start(inter)

def parser_link_csgo_cs2(soup, search, name, link: List[str], name_map: List[str], size: List[str], date: List[str]):
    table_rows = soup.find_all('tr')
    found_match = False 
    for row in table_rows:
        name_cell = row.find('td', class_='fb-n')
        if name_cell:
            name_text = name_cell.text.strip()
            if pd.Series(name_text.lower()).str.contains(name.lower()).any():
                append_link_csgo_cs2(row, name_text, link, name_map, size, date)
                found_match = True
    if not found_match:
        for row in table_rows:
            name_cell = row.find('td', class_='fb-n')
            if name_cell:
                name_text = name_cell.text.strip()
                if fuzz.WRatio(name_text.lower(), name.lower()) >= 75:
                    search = False
                    append_link_csgo_cs2(row, name_text, link, name_map, size, date)
    return search

def append_link_csgo_cs2(row, name_text, link: List[str], name_map: List[str], size: List[str], date: List[str]):
    link_cell = row.find('a')
    if link_cell:
        href = link_cell['href']
        link.append('https://www.notkoen.xyz' + href)
        name_map.append(name_text)
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

def parser_link_css(soup, search, url, name, link: List[str], name_map: List[str], size: List[str], date: List[str]):
    table_rows = soup.find_all('a')
    found_match = False
    for row in table_rows:
        name_text = row.text.strip()
        if pd.Series(name_text.lower()).str.contains(name.lower()).any():
            append_link_css(row, url, name_text, link, name_map, size, date)
            found_match = True
    if not found_match:
        for row in table_rows:
            name_text = row.text.strip()
            if fuzz.WRatio(name_text.lower(), name.lower()) >= 75:
                search = False
                append_link_css(row, url, name_text, link, name_map, size, date)  
    return search

def append_link_css(row, url, name_text, link: List[str], name_map: List[str], size: List[str], date: List[str]):
    href = row['href']
    link.append(url + href)
    name_map.append(name_text)
    size_text = row.next_sibling.strip()
    size_value = size_text.split()[-1]
    date_year = size_text.split()[0]
    size_mb = float(size_value) / 1024 / 1024
    size.append(f"{size_mb:.2f} MB")
    date.append(date_year)