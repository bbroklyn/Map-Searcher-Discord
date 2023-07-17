import json

import a2s
import requests
import disnake
import pandas as pd
from bs4 import BeautifulSoup as BS
from typing import Optional, List
from disnake.ext import commands
from logger import write_log

file = open("config.json", "r")
config = json.load(file)

Bot = commands.Bot(config['prefix'], intents=disnake.Intents.all())


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

        if len(player_names_str) == 0:
            await inter.response.send_message(f"**Players {self.players}**:\n```No one is playing on the server at the moment!```", ephemeral=True)
        else:
            await inter.response.send_message(f"**Players {self.players}**:\n```{player_names_str}```", ephemeral=True)


async def server_track(inter: disnake.ApplicationCommandInteraction, server):
    await inter.response.defer()
    for server_info in config['trackers']:
        if server_info['name'] == server:
            server_address = server_info['address']
            server_port = server_info['port']
            url = server_info['url']
            server_info = a2s.info((server_address,server_port))
            player_list = a2s.players((server_address,server_port))
            player_name = []
            times = []
            for player in player_list:
                player_duration = player.duration
                minutes, seconds = divmod(player_duration, 60)
                hours, minutes = divmod(minutes, 60)
                if hours < 1:
                    duration_formatted = f"{int(minutes):02d}:{int(seconds):02d}"
                else:
                    duration_formatted = f"{int(hours)}:{int(minutes):02d}:{int(seconds):02d}"
                player_name.append(player.name)
                times.append(duration_formatted)
            server_name = server_info.server_name
            curr_map = server_info.map_name.split('/')[-1]
            players = "`"+str(server_info.player_count) + '/' + str(server_info.max_players)+"`"
            embed = disnake.Embed(
                title=f"**{server} tracker:**",
                color=0xFFFFFF
            )
            connect = f"{server_address}:{server_port}"
            connect_link =f"https://vauff.com/?ip={connect}"
            game_version = "`"+server_info.version+"`"
            id_game = "`%s`" % server_info.app_id
            link = 0
            response = requests.get(url)
            html = response.text
            soup = BS(html, 'html.parser')
            if server in ["ZeddY^s", "RSS", "Mapeadores", "GFL CS:GO"]:
                table_rows = soup.find_all('tr')
                for row in table_rows:
                    name_cell = row.find('td', class_='fb-n')
                    if name_cell:
                        name_text = name_cell.text.strip()
                        if pd.Series(name_text.lower()).str.contains(curr_map.lower()).any():
                            link_cell = row.find('a')
                            if link_cell:
                                href = link_cell['href']
                                link = 'https://www.notkoen.xyz' + href
            elif server in ["NIDE.GG", "UNLOZE", "GFL CS:S"]:
                table_rows = soup.find_all('a')
                for row in table_rows:
                    name_text = row.text.strip()
                    if pd.Series(name_text.lower()).str.contains(curr_map.lower()).any():
                        href = row['href']
                        link = url + href
            embed.add_field(name="Server version:", value=game_version, inline=True)
            embed.add_field(name="Game ID:", value=id_game, inline=True)
            embed.add_field(name="Server Name:", value="`"+server_name+"`", inline=False)
            if link == 0:
                embed.add_field(name="Current Map:", value="`"+curr_map+"`", inline=False)
            else:
                embed.add_field(name="Current Map:", value=f"[{curr_map}]({link})", inline=False)

            embed.add_field(name="Players:", value=players, inline=True)
            embed.add_field(name="Connect:", value=f"[{connect}]({connect_link})", inline=True)
            server_players = ServerPlayers(player_name, times, players)
            write_log(f"used /strack {server}", inter.author)
            await inter.followup.send(embed=embed, view=server_players)