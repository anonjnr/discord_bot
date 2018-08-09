# discord_bot
Discord bot tailored for the book club after dark.

Written for `Python3.6`.

You'll also need to get the discord.py: https://github.com/Rapptz/discord.py

Official Docs for discord.py: http://discordpy.readthedocs.io/en/latest/migrating.html

Official Docs for Discord API: https://discordapp.com/developers/docs/intro

Special thanks to @sharkbound for the help with fetching and pulling apart the data off goodreads.com (their "API" is a joke btw.)
Also special thanks to @ir-3 for helping with getting the second prefix running and helping with misc stuff

## Used Libs:

```
import asyncio
import discord
import random
import time
import subprocess
import requests
import wikipedia
import praw
import json
from xml.etree import ElementTree
from discord.ext import commands
```
## Get started:

Download all.

Open `data.txt` and fill in the token for Discord, the role ID's for the administrators/ mods of your server (find out by `\@ROLE_MENTION` into chat on server), reddit api client ID/ client secret/ user agent, ID auf the author (same method as with roles `\@AUTHER_MENTION`) and the goodreads key.

If you don't want to use one or more of those, just leave them blank in the `data.txt`. In the `bcad_bot.py` you will have to commend out/ delete everything, you don't want to use.

If you run into any issues, look up the documentation as provided on top of this `readme.md` or file an issue.

@anonjnr

## Commands:

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

`roll`
You can roll a dice using `2d8` with 2 being the number of dice you want the bot to roll and 8 being the number of sides the dice has. If you just want the bot to throw one dice, just put `d8`. You can add your modifier too! Simply put `2d8 3` with 3 being your modifier. Negative values do work too!

`clear`
With this command a Moderator can clear all messages in a channel if something NSFW or otherwise inapropriate got posted. Other users can use this command aswell - it automatically pings the Moderators for them. For the last 1000 messages purged `clear`, for a certains amount `clear NUMBER` with `NUMBER` being any number between 0 and 1000

`GMT`
Gives you the current time for the GMT timezones

`bleach`
Applies eye bleach. Try it! (recommended after and/ or before clear)

`roles`
Shows you what roles you have

`votecall`
Calls a simple thumb up/ thumb down vote for the message.

