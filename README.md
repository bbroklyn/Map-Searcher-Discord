[![changelogs](https://img.shields.io/badge/changelogs%20-76c22f)](https://github.com/heechan194/Map-Searcher-Bot/blob/main/changelog.txt) [![invite](https://img.shields.io/badge/Add_bot_to-Discord-blue)](https://discord.com/api/oauth2/authorize?client_id=1122605455194193931&permissions=277025396736&scope=applications.commands%20bot) 

# Map Searcher Bot for Discord

Bot version : **3.2**

A Python bot for Discord, the main function of which is to give people a link to the map that they entered in the search with the `/mlink` command. If you want to see all bot commands, you can type `/help`.

At the moment the bot is still being implemented to the end, being updated or we are trying to add some new features. If you find any bugs, want to suggest new features or any optimization, you can write in the discord: **heechan194** or **.kassini**.


# Commands:

- You can see every commands bellow or type `/help`.

# For everyone:

`/about` - About this bot. Shows uptime, RAM usage and etc.

`/help <commands/run usage>` - Navigation help command, some information

`/fastdl` - Gives you the link to download the map.

`/mlink <CS:S/CS:GO/CS2> <mapname>` - Gives you the link to download the map.

`/pack <Zeddy/GFL/High Contract Zombies/Mapeadores/ZombieDen/MoeUB/ExG>` - Download resource packs of various servers.

`/changelog <DD.MM.YY>` - Bot changelogs.

`/strack <server>` - Get all server information.

`/csite <URL>` - Checks if the site is running. Also gives information about him.

# For Owners:

`/admin <shutdown/restart>` - Admin commands.


# How to install this bot for your server?

- I strongly **do not** recommend starting the bot yourself, because this may not be the last code to be trusted, because this repository is used only in order not to lose the code!

- Click to [this](https://discord.com/api/oauth2/authorize?client_id=1122605455194193931&permissions=277025396736&scope=applications.commands%20) button and then choose your server. The bot will work 24/7 as long as the hosting is working.


# How to add new servers/pack to the bot?
  ```json 
     {
        
        "ID":"730 OR 240 (CSGO - 730, CSS - 240)",
        "name":"Server Name",
        "address":"IP ADRESS",
        "port":SERVER_PORT,
        "url":"FASTDL-URL"
     }
```
   ```json 
    {
       "pack":"pack name",
       "link":"download-link"
    }
```

# How to use this bot?

1. install all libraries with `pip install -r requirements.txt`;
2. Edit `config.json` file;
3. Run the bot.


# Any issues?

- Press an **issues** button here, if you want to submit an issue.


# Future updates:
- Make better code optimization;
- Add more choice in games besides **CS:GO**, **CS:S** and **CS2**;


# Credits
**NiceShot** - Coding help.

**koen** - [FastDL](https://www.notkoen.xyz/fastdl/).

**Killik** - Linux server.
