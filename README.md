# discord_bot
Discord bot tailored for the book club after dark.

Written for Python3.6.

You'll also need to get the discord.py: https://github.com/Rapptz/discord.py

Official Docs for discord.py: http://discordpy.readthedocs.io/en/latest/migrating.html

Official Docs for Discord API: https://discordapp.com/developers/docs/intro

Used Libs:

import asyncio
import discord
import random
import time
import subprocess
import requests
import wikipedia
from xml.etree import ElementTree
from discord.ext import commands


Commands:

help
Prints this. It's the basic commands you can use the Bot for

info
Basic information on the Bot such as name and author

test
Tests if the Bot works properly. Has no other purpose

goodreads
Let'\s you look for authors and books on Goodread.com. For this you can use an authors name, book title, ISBN or even all together. Example: @Sir Henry Pickles goodreads Neil Gaiman Norse Mythology or !goodreads Neil Gaiman Norse Mythology

greeting
Say Hi to Henry! Or Hello or Morning or something like this

goodbye
Same as with greeting. Responds to a variety of goodbyes

sleep
Let's the Bot decide if you should go to bed

shower
Let's the Bot decide if you should take a shower

joke
Let Henry tell you a joke which most certainly is hilarious

8ball
Ask the oracle with this all time classic

roll
You can roll a dice using 2d8 with 2 being the number of dice you want the bot to roll and 8 being the number of sides the dice has. If you just want the bot to throw one dice, just put d8. You can add your modifier too! Simply put 2d8 3 with 3 being your modifier. Negative values do work too!

clear
With this command a Moderator can clear all messages in a channel if something NSFW or otherwise inapropriate got posted. Other users can use this command aswell - it automatically pings the Moderators for them. For the last 1000 messages purged clear, for a certains amount clear NUMBER with NUMBER being any number between 0 and 1000

GMT
Gives you the current time for the GMT timezones

bleach
Applies eye bleach. Try it! (recommended after and/ or before clear)

roles
Shows you what roles you have

votecall
Calls a simple thumb up/ thumb down vote for the message.

