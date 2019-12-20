PLEASE NOTICE THAT THIS IS BEING WORKED ON DAILY
BUT ONLY PUSHED TO GITHUB EVERY NOW AND THEN

# discord_bot
Discord bot tailored for book clubs.

Written for `Python3.*`.

Official Docs for discord.py: http://discordpy.readthedocs.io/en/latest/  
Official Docs for PRAW (reddit): https://praw.readthedocs.io/en/latest/  
Official Docs for wikipedia: https://wikipedia.readthedocs.io/en/latest/  
Official Docs for pytz: https://pythonhosted.org/pytz/  

Official Docs for Discord API: https://discordapp.com/developers/docs/intro


Special thanks to @sharkbound for the help with fetching and pulling apart the data off goodreads.com (their "API" is a joke btw.)
Also special thanks to @vasiliykovalev (thanks so much!), @ir-3 and @Harrryyyy for helping with getting the second prefix running, testing misc stuff

## Used External Libs:

```
import aiohttp
import async_timeout
import discord
import praw
import pytz
import wikipedia
import requests
import youtube_dl
import pytz
import wiktionaryparser
```
## Get started:

You can download the `setup.sh` to install and start the setup up the bot with all you need automatically with:
```
sudo wget https://raw.githubusercontent.com/x3l51/discord_bot/master/setup.sh ; sudo bash setup.sh
```

Else you can setup everything manually:
```
sudo apt-get update
sudo apt-get upgrade
sudo ./configure
sudo make
sudo make altinstall
sudo apt-get install python-dev
sudo apt-get install python-lxml
sudo python3 -m pip install --upgrade pip
sudo python3 -m pip install -U discord.py
sudo python3 -m pip install requests-xml
sudo python3 -m pip install wikipedia
sudo python3 -m pip install wiktionaryparser
sudo python3 -m pip install praw
sudo python3 -m pip install pytz
cd ~
sudo mkdir projects
cd projects
sudo mkdir logs
sudo wget https://github.com/x3l51/discord_bot/archive/master.zip
sudo unzip master.zip
sudo chmod 777 config.json
sudo python3.6 setup.py
```

Open `setup.py` (`sudo python3 setup.py`- will autoomatically be opened if you use the `setup.sh`) and fill in the token for Discord, the role ID's for the administrators/ mods of your server (find out by `\@ROLE_MENTION` into chat on server), reddit api client ID/ client secret/ user agent, ID auf the author (same method as with roles `\@AUTHER_MENTION`) and the goodreads key. The Discord Token is the only thin mandatory, you can leave the rest blank if you'd like. Most funtions will not work properly then.

To start the bot simply use `python3 bcad_bot3.6.py`(will automatically start if you use the `setup.sh`).

If you run into any issues, look up the documentation as provided on top of this `readme.md` or file an issue.

XOXOXoxooxo - @x3l51

## Commands for the Bot:

You can call a command by typing `@Sir Henry Pickles COMMAND` or `!COMMAND`

`help`

Prints this. It's the basic commands you can use the Bot for

`info`

Basic information on the Bot such as name and author

`userinfo`

Let's you look up basic info about another user. Example: `!userinfo @OTHERUSER`

`test`

Tests if the Bot works properly. Has no other purpose

`suggestion`

Lets everyone suggest stuff for the bot/ server. Example: `!suggestion The bot should stay as it is for it is already awesome`

`goodreads`

Let's you look for authors and books on Goodread.com. For this you can use an authors name, book title, ISBN or even all together. Example: `@Sir Henry Pickles goodreads Neil Gaiman Norse Mythology` or `!goodreads Neil Gaiman Norse Mythology`

`reddit`

With this command you can let Henry post the `top 3 hot topics` of a subreddit of your choosing. Simply use `@Sir Henry Pickles reddit SUBREDDIT` or `!reddit SUBREDDIT` with `subreddit` being the subreddit of your choosing. Subreddit
    
`wikipedia`

Let's you search wikipedia for anything. Gives you a short summary and the link to the full article. Use with `@Sir Henry Pickles wikipedia KEYWORD` or `!wikipedia KEYWORD` with KEYWORD being what you're looking for

`wiktionary`

Let's you search wiktionary for anything. Gives you a short summary and stuff. Use with `@Sir Henry Pickles wiktionary KEYWORD` or `!wiktionary KEYWORD` with KEYWORD being what you're looking for

`roll`

You can `roll` a dice using `2d8` with 2 being the number of dice you want the bot to roll and 8 being the number of sides the dice has. If you just want the bot to throw one dice, just put `d8`. You can add your modifier too! Simply put `2d8 3` with 3 being your modifier. Negative values do work too!")

`time`

Gives you the current time for different timezones. For example use with `!time Berlin` or `!time EST`.

`bleach`

Applies eye bleach. Try it! (recommended after and/ or before clear)

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

`python`

Gives you a link to the official python docs: `!python recursion`

## This section is commands for mods/ owners only

`archive`

Archives alll messages of the channel it is called from. A log will be send to the caller of the commmand via PM and another copy goes into #logs

`clear`

With this command a Moderator can clear all messages in a channel if something NSFW or otherwise inapropriate got posted. Other users can use this command aswell - it automatically pings the Moderators for them. For the last 1000 messages purged `clear`, for a certains amount `clear NUMBER` with `NUMBER` being any number between 0 and 1000

`members`

With  this you can save a list of all users of your server

`members_show`

Shows the contains of the saved member list 

`mod`

Shows if you're a mod

`roles`

Shows you what roles you have

`status`

Change the status of the bot. `!status the guitar` to have his status changed to: `@Sir Henry Pickles Playing the guitar`

`prefix`

With `!prefix show` the bot will say what prefix is currently used. With `!prefix ?` you can change it to `?` with `?` being whatever you want

`reload`

Shuts down the bot and let's it start up anew

`quit`

Shuts down the bot. It needs to be restarted manually after

`leave`

Leaves the server the command is called from