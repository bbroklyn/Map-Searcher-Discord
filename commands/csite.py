import requests
import json


import disnake
from bs4 import BeautifulSoup
from logger import write_log

file = open("config.json", "r")
config = json.load(file)
Bot = disnake.Client()

async def check_website(inter: disnake.ApplicationCommandInteraction, website):
    await inter.response.defer()
    if not website.startswith("https://"):
        website = "https://" + website
    await inter.send(f"Getting information about `{website}`")
    write_log(f"used /csite {website}", inter.author)
    
    try:
        response = requests.get(website, timeout=5)
        response.raise_for_status()
        headers = response.headers
        content_type = headers.get("Content-Type")
        content_length = headers.get("Content-Length")
        status_code = response.status_code
        status_text = response.reason
        server = headers.get("Server")
        
        
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string if soup.title else "N/A"
        meta_tags = soup.find_all("meta")
        meta_description = ""
        for tag in meta_tags:
            if tag.get("name") == "description":
                meta_description = tag.get("content")
                break
        
        embed = disnake.Embed(title=f"Website information:", description=f"{website}", color=disnake.Color.blue())
        embed.add_field(name="Title:", value=title, inline=False)   
        embed.add_field(name="Meta Description:", value=meta_description, inline=False)     
        embed.add_field(name="Status:", value=f"{status_code} {status_text}", inline=False)
        embed.add_field(name="Content Type:", value=content_type, inline=False)
        embed.add_field(name="Content Length:", value=content_length, inline=False)
        embed.add_field(name="Server:", value=server, inline=False)
        await inter.edit_original_message(embed=embed)
        
        
    except requests.exceptions.Timeout:
        error_message = "Timeout occurred while getting information."
        embed = disnake.Embed(title="Error:", description=error_message, color=disnake.Color.red())
        await inter.edit_original_message(embed=embed)
    except requests.exceptions.RequestException as e:
        error_message = f"{str(e)}"
        embed = disnake.Embed(title="An error occurred:", color=disnake.Color.red())
        embed.set_footer(text=error_message)
        await inter.edit_original_message(embed=embed)
    except UnicodeError as e:
        error_message = f"UnicodeError: {e}"
        embed = disnake.Embed(title="Error log:", color=disnake.Color.red())
        embed.set_footer(text=error_message)
        await inter.edit_original_message(embed=embed)