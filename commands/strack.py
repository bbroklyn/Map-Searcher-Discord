import json
import datetime
import socket

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
time_now = datetime.datetime.now().strftime("%H:%M:%S")
command_author_id = None

Bot = commands.Bot(config['prefix'], intents=disnake.Intents.all())

class ServerPlayers(disnake.ui.View):
    
    def __init__(self, players: List[str], times: List[str], player, player_score: List[str], connect_link: str, link: str, server, timeout: Optional[float] = None):
        super().__init__(timeout=timeout)
        self.players_list = players
        self.time = times
        self.players = player
        self.message = None
        self.score = player_score
        self.server_name = server
        self.add_item(disnake.ui.Button(label="Connect", url=connect_link))
        if link != 0:
            self.add_item(disnake.ui.Button(label="Download map", url=link))

    @disnake.ui.button(label="List of players", style=disnake.ButtonStyle.grey, row=2)
    async def button_callback(self, button: disnake.ui.Button, inter: disnake.Interaction):
        global command_author_id
        if inter.user.id != command_author_id:
            return # not a command author.
        player_names_str = ""
        for player, time, score in zip(self.players_list, self.time, self.score):
            player_names_str += f"{player} | {time} | {score}\n"
        if len(player_names_str) == 0:
            await inter.response.send_message(f"**Players ATM {self.players}**:\n```No one is playing on the server ATM!```", ephemeral=True)
        else:
            await inter.response.send_message("sending player list to your PM", ephemeral=True)
            await inter.author.send(f"**Players in ({self.server_name}) at {time_now} {self.players}**:\n```Nickname | Time | Score\n{player_names_str}```")

    @disnake.ui.button(style=disnake.ButtonStyle.red, emoji="🗑️", row=2)
    async def delete_message_button(self, button: disnake.ui.Button, inter: disnake.Interaction):
        await inter.response.defer()
        global command_author_id
        if inter.user.id != command_author_id:
            return        
        await inter.delete_original_response()
        

servers = [server['name'] for server in config['trackers']]
server_tr = commands.option_enum(servers)
@Bot.slash_command(name="strack", 
                   description="Get all server information.")
async def server_track_command(inter: disnake.ApplicationCommandInteraction,
                               server: server_tr = commands.Param(name="option",
                                                                  description="Choose a server.")):
    await inter.response.defer()
    global command_author_id
    command_author_id = inter.author.id
    try:
        for server_info in config['trackers']:
            if server_info['name'] == server:
                server_address = server_info['address']
                server_port = server_info['port']
                if 'url' in server_info:
                    url = server_info['url']
                else:
                    url = 0
                gameid = server_info['ID']
                server_info = a2s.info((server_address,server_port))
                player_list = a2s.players((server_address,server_port))
                platform = server_info.platform
                player_name = []
                times = []
                player_score = []
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
                    player_score.append(player.score)
                server_name = "```"+server_info.server_name+"```"
                curr_map = server_info.map_name.split('/')[-1]
                players = "`"+str(server_info.player_count) + '/' + str(server_info.max_players)+"`"
                embed = disnake.Embed(
                    title=f"**{server} tracker:**",
                    color=0xFFFFFF
                )
                embed.timestamp = datetime.datetime.now()
                connect = f"{server_address}:{server_port}"
                connect_link =f"https://vauff.com/?ip={connect}"
                game_version = server_info.version
                id_game = server_info.app_id
                embed.add_field(name="Server version:", value=game_version, inline=True)
                embed.add_field(name="Platform(W/L/M):", value=platform, inline=True)
                embed.add_field(name="Game ID:", value=id_game, inline=True)
                embed.add_field(name="Server Name:", value=server_name, inline=False)
                link = 0
                if url != 0:
                    response = requests.get(url)
                    html = response.text
                    soup = BS(html, 'html.parser')
                    if gameid == "730":
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
                    elif gameid == "240":
                        table_rows = soup.find_all('a')
                        for row in table_rows:
                            name_text = row.text.strip()
                            if pd.Series(name_text.lower()).str.contains(curr_map.lower()).any():
                                href = row['href']
                                link = url + href
                else:
                    embed.color = 0xFF0000
                    print(f"no url link here: {server}")


                if link == 0:
                    embed.add_field(name="Current Map: ", value=f"```{curr_map} \n[Unable to find map on FastDL]```", inline=False)
                else:
                    embed.add_field(name="Current Map:", value=f"```{curr_map}```", inline=False)

                embed.add_field(name="Players:", value=players, inline=True)
                embed.add_field(name="Connect:", value=f"[{connect}]({connect_link})", inline=True)
                server_players = ServerPlayers(player_name, times, players, player_score, connect_link, link, server)
                write_log(f"used /strack {server}", inter.author)
                await inter.followup.send(embed=embed, view=server_players)
    except socket.timeout as e:
        embed = disnake.Embed(
            title=f"**An error has occurred with {server}**",
            color=0xFF0000,
            description="The server is not responding to the request.")
        embed.add_field(name="Error log:", value=str(e), inline=False)
        await inter.edit_original_message(embed=embed)