import datetime

import psutil
import disnake
import time
from logger import write_log

class Paginator(disnake.ui.View):
    def __init__(self, commands: list, items_per_page: int = 5):
        super().__init__()
        self.commands = commands
        self.items_per_page = items_per_page
        self.current_page = 1
        self.total_pages = (len(commands) + items_per_page - 1) // items_per_page
        self.view = None
        self.message = None
        self.command_author_id = None
        
    def get_current_page_commands(self): 
        
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        return self.commands[start_index:end_index]
    
    def get_page_embed(self):
        self.previous_page_button.disabled = (self.current_page == 1)
        self.next_page_button.disabled = (self.current_page == self.total_pages)
        self.page_counter.label = f"Page {self.current_page}/{self.total_pages}"
        current_commands = self.get_current_page_commands()
        content = "\n".join(current_commands)
        return content
    

    async def change_page(self, interaction: disnake.Interaction):
        await interaction.response.defer()
        embed = self.get_page_embed()
        self.view = self
        await interaction.edit_original_response(view=self.view, content=embed)


    async def send_page(self, inter: disnake.ApplicationCommandInteraction):
        embed = self.get_page_embed()
        self.message = await inter.edit_original_message(content=embed, view=self)
        self.view = self
        await inter.edit_original_response()


    @disnake.ui.button(label="Previous", style=disnake.ButtonStyle.primary)
    async def previous_page_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        global command_author_id
        if interaction.user.id != command_author_id:
            return

        if self.current_page > 1:
            self.current_page = self.current_page - 1
            await self.change_page(interaction)

    @disnake.ui.button(label="Page 1/1", style=disnake.ButtonStyle.blurple, disabled=True)
    async def page_counter(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        return

    @disnake.ui.button(label="Next", style=disnake.ButtonStyle.primary)
    async def next_page_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        global command_author_id
        if interaction.user.id != command_author_id:
            return

        if self.current_page < self.total_pages:
            self.current_page = self.current_page + 1
            await self.change_page(interaction)

async def help(inter: disnake.ApplicationCommandInteraction, option, start_Time, command_descriptions):
    uptime = str(datetime.timedelta(seconds=int(round(time.time() - start_Time))))
    await inter.response.defer()
    global command_author_id
    command_author_id = inter.author.id
    help_things = {
        "commands": [
            f"</mlink:1130214840431038484> - {command_descriptions['mlink']}",
            f"</fastdl:1123717659637321749> - {command_descriptions['fastdl']}",
            f"</admin:1125154934904586363> - {command_descriptions['admin']}",
            f"</help:1125453195750166538> - {command_descriptions['help']}",
            f"</about:1125443661547712644> - {command_descriptions['about']}",
            f"</strack:1130221660948140154> - {command_descriptions['strack']}",
            f"</csite:1130920520947351604> - {command_descriptions['csite']}"
        ],
        "run usage": [
            f"Current bot uptime: {uptime}",
            f"RAM Usage: {psutil.virtual_memory().percent} %"
        ]
    }
    if option in help_things:
        write_log(f"used /help {option}.", inter.author)
        if option == "commands":
            paginator = Paginator(help_things[option])
            await paginator.send_page(inter)
        elif option == "run usage":
            embed = disnake.Embed(
                title="Run Usage",
                description="\n".join(help_things[option]),
                color=0xFFFFFF
            )
            await inter.edit_original_message(embed=embed)
