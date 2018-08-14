PLEASE NOTICE THAT THIS IS BEING WORKED ON DAILY
BUT ONLY PUSHED TO GITHUB EVERY FEW DAYS

# discord_bot
Discord bot tailored for the book club after dark.

Written for `Python3.6`.

Official Docs for discord.py: http://discordpy.readthedocs.io/en/latest/  
Official Docs for PRAW (reddit): https://praw.readthedocs.io/en/latest/  
Official Docs for wikipedia: https://wikipedia.readthedocs.io/en/latest/  
Official Docs for pytz: https://pythonhosted.org/pytz/  

Official Docs for Discord API: https://discordapp.com/developers/docs/intro


Special thanks to @sharkbound for the help with fetching and pulling apart the data off goodreads.com (their "API" is a joke btw.)
Also special thanks to @ir-3 and @Harrryyyy for helping with getting the second prefix running, testing misc stuff

## Used Libs:

```
import os
import asyncio
import discord
import random
import time
import subprocess
import aiohttp
import async_timeout
import wikipedia
import praw
import json
import pytz
import datetime
import utilities
import memberList
import importLog
import requests
from wiktionaryparser import WiktionaryParser
from datetime import datetime
from datetime import date
from datetime import timedelta
from pytz import timezone 
from xml.etree import ElementTree
from discord.ext import commands
```
## Get started:

You can download the `setup.sh` to install and start the setup up the bot with all you need automatically with:
```
sudo wget https://raw.githubusercontent.com/anonjnr/discord_bot/master/setup.sh ; sudo bash setup.sh
```

Else you can setup everything by manually:
```
sudo apt-get update
sudo apt-get upgrade
cd /opt
sudo wget https://www.python.org/ftp/python/3.6.6/Python-3.6.6.tar.xz
sudo tar xf Python-3.6.6.tar.xz
cd Python-3.6.6/
sudo ./configure
sudo make
sudo make altinstall
sudo apt-get install python-dev
sudo apt-get install python-lxml
sudo python3.6 -m pip install --upgrade pip
sudo python3.6 -m pip install -U discord.py
sudo python3.6 -m pip install requests-xml
sudo python3.6 -m pip install wikipedia
sudo python3.6 -m pip install wiktionaryparser
sudo python3.6 -m pip install praw
sudo python -m pip install pytz
cd ~
sudo mkdir projects
cd projects
sudo wget https://github.com/anonjnr/discord_bot/archive/master.zip
sudo unzip master.zip
sudo chmod 777 credentials.log
sudo chmod 777 members.log
```

Open `setup.py` (`sudo python3.6 setup.py`- will autoomatically be opened if you use the `setup.sh`) and fill in the token for Discord, the role ID's for the administrators/ mods of your server (find out by `\@ROLE_MENTION` into chat on server), reddit api client ID/ client secret/ user agent, ID auf the author (same method as with roles `\@AUTHER_MENTION`) and the goodreads key. The Discord Token is the only thin mandatory, you can leave the rest blank if you'd like. Most funtions will not work properly then.

To start the bot simply use `python3.6 bcad_bot3.6.py`(will automatically start if you use the `setup.sh`).

If you run into any issues, look up the documentation as provided on top of this `readme.md` or file an issue.

XOXOXoxooxo - @anonjnr

## Commands for the Bot:

You can call a command by typing `@Sir Henry Pickles COMMAND` or `!COMMAND`

`help`
Prints this. It's the basic commands you can use the Bot for

`info`
Basic information on the Bot such as name and author

`test`
Tests if the Bot works properly. Has no other purpose

`goodreads`
Let's you look for authors and books on Goodread.com. For this you can use an authors name, book title, ISBN or even all together. Example: `@Sir Henry Pickles goodreads Neil Gaiman Norse Mythology` or `!goodreads Neil Gaiman Norse Mythology`

`reddit`
With this command you can let Henry post the `top 3 hot topics` of a subreddit of your choosing. Simply use `@Sir Henry Pickles reddit SUBREDDIT` or `!reddit SUBREDDIT` with `subreddit` being the subreddit of your choosing. Subreddit
    
`wikipedia`
Let's you search wikipedia for anything. Gives you a short summary and the link to the full article. Use with `@Sir Henry Pickles wikipedia KEYWORD` or `!wikipedia KEYWORD` with KEYWORD being what you're looking for

`roll`
You can `roll` a dice using `2d8` with 2 being the number of dice you want the bot to roll and 8 being the number of sides the dice has. If you just want the bot to throw one dice, just put `d8`. You can add your modifier too! Simply put `2d8 3` with 3 being your modifier. Negative values do work too!")

`time`
Gives you the current time for different timezones. For example use with `!time Berlin` or `!time EST`.

`clear`
With this command a Moderator can clear all messages in a channel if something NSFW or otherwise inapropriate got posted. Other users can use this command aswell - it automatically pings the Moderators for them. For the last 1000 messages purged `clear`, for a certains amount `clear NUMBER` with `NUMBER` being any number between 0 and 1000

`members`
With  this you can save a list of all users of your server

`members_show`
Shows the contains of the saved member list 

`bleach`
Applies eye bleach. Try it! (recommended after and/ or before clear)

`roles`
Shows you what roles you have

`status`
Change the status of the bot. `!status the guitar` to have his status changed to: `@Sir Henry Pickles Playing the guitar`

`votecall`
Calls a simple thumb up/ thumb down vote for the message.

`greeting`
Say Hi to Henry! Or Hello or Morning or something like this

`goodbye`
Same as with greeting. Responds to a variety of goodbyes

`sleep`
Let's the Bot decide if you should go to bed

`shower`
Let's the Bot decide if you should take a shower

`joke`
Let Henry tell you a joke which most certainly is hilarious

`8ball`
Ask the oracle with this all time classic

