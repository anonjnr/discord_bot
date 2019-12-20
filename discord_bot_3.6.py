#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# bot_bcad_3.6.py

import os
import sys
import re
import ast
import asyncio
import datetime
import json
import random
import time
import logging
from datetime import datetime
from datetime import timedelta
from xml.etree import ElementTree

import aiohttp
import async_timeout
import discord
import praw
import pytz
import wikipedia
import requests
import youtube_dl
from discord.ext import commands
from pytz import timezone
from wiktionaryparser import WiktionaryParser

import memberList
import messages
import utilities

with open('config.json', 'r') as json_file:
    data = json.load(json_file)
    for p in data['TOKEN']:
        TOKEN = p['value']
    for p in data['REDDIT']:
        json_client_id = p['client_id']
        json_client_secret = p['client_secret']
        json_user_agent = p['user_agent']
    for p in data['GOODREADS']:
        goodreads_key = p['goodreads_key']
    for p in data ['PREFIX']:
        prefix_choice = p['prefix']
    for p in data ['COUNTER']:
        reaction_trigger_pull = p['counter_reac']
        cmd_trigger_pull = p['counter_cmd']
    for p in data ['UPTIME']:
        uptime_pull = p['uptime']
    for p in data ['BOT_OWNER_ID']:
        bot_owner_id = p['bot_owner_id']
    for p in data ['STATUS']:
        status_pull = p['status']

description = 'Sir Henry Pickles, the pickly Bot!'
bot = commands.Bot(max_messages=10000, command_prefix=commands.when_mentioned_or(prefix_choice), case_insensitive=True)
reddit = praw.Reddit(client_id=json_client_id, client_secret=json_client_secret, user_agent=json_user_agent)
start_time = time.time()
bot.remove_command('help')
random.seed(a=None)

logger_discord_info = logging.getLogger('discord')
logger_discord_info.setLevel(logging.DEBUG)
log = logging.getLogger()
log.setLevel(logging.DEBUG)
handler_discord_info = logging.FileHandler(filename='./logs/discord_info.log', encoding='utf-8', mode='a+')
handler_discord_info.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger_discord_info.addHandler(handler_discord_info)

async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()

async def create_chan_log():
    for guild in bot.guilds:
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        
        if not discord.utils.get(guild.channels, name='logs'):
            await guild.create_text_channel('logs', overwrites=overwrites, position=1, topic='logs')

async def create_chan_suggestions():
    for guild in bot.guilds:
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }

        if not discord.utils.get(guild.channels, name='suggestions'):
            await guild.create_text_channel('suggestions', overwrites=overwrites, position=2, topic='suggestions')

@bot.event
async def on_connect():
    usage_string = (f'\
    [TIME: {utilities.epoch_to_custom_date(utilities.FMT_TIME)}]\n\
    Connected to discord\n\
------\
    ')
    print(usage_string)

@bot.event
async def on_disconnect():

    total_uptime_save()
    reaction_trigger_save()
    cmd_trigger_save()

    usage_string = (f'\
    [TIME: {utilities.epoch_to_custom_date(utilities.FMT_TIME)}]\n\
    Lost connection to discord\n\
------\
    ')
    print(usage_string)
    try:
        await bot.connect(reconnect=True)
    except Exception as e:
        print(e)
        reloadRaw()

@bot.event
async def on_error(event, *args, **kwargs):

    total_uptime_save()
    reaction_trigger_save()
    cmd_trigger_save()
    
    import traceback
    print(args[0])
    message = args[0]
    print(message)
    
    usage_string = (f'\
    [TIME: {utilities.epoch_to_custom_date(utilities.FMT_TIME)}]\n\
    Author Alias: {message.author.name}\n\
    Author Name: {message.author}\n\
    Author ID: {message.author.id}\n\
    Channel: {message.channel}\n\
    Server: {message.guild}\n\
    Server ID: {message.guild.id}\n\
        \n\
    ON ERROR\n\
        \n\
    ERROR EVENT: {event}\n\
    ERROR ARGS: {args}\n\
    ERROR TRACEBACK: {traceback.format_exc()}\n\
    COMPLETE MESSAGE: {message.content}\n\
------\
    ')
    print(usage_string)
    for channel in message.guild.channels:
        if channel.name == 'logs':
            await channel.send(embed=discord.Embed(title="ERROR", color=0xff0000)
            .add_field(name="EVENT", value=event, inline = False)
            .add_field(name="ARGS", value=args, inline = False)
            .add_field(name="TRACEBACK", value=traceback.format_exc(), inline = False)
            .set_thumbnail(url=message.author.avatar_url))
            return await channel.send("<@!"+bot_owner_id+">")

@bot.event
async def on_ready():
    boot = discord.Game(name="BOOTING")
    boot_fin = discord.Game(name="BOOT FINISHED")
    err = discord.Game(name="EXIT CODE 0")
    stat = discord.Game(name=status_pull)
    print(f'\
    [TIME: {utilities.epoch_to_custom_date(utilities.FMT_TIME)}]\n\
    Logged in as\n\
    Bot Name: {bot.user.name}\n\
    Bot ID: {bot.user.id}\n\
------\
    ')
    await create_chan_log()
    await create_chan_suggestions()
    await bot.change_presence(status=discord.Status.idle, activity=boot)
    await asyncio.sleep(3)
    await bot.change_presence(status=discord.Status.idle, activity=boot_fin)
    await asyncio.sleep(3)
    await bot.change_presence(status=discord.Status.online, activity=err)
    await asyncio.sleep(3)
    await bot.change_presence(status=discord.Status.online, activity=stat)
    
@bot.event
async def on_member_remove(member):
    print("on member remove")

@bot.event
async def on_member_ban(guild, user):
    print("on member ban")

@bot.event
async def on_member_unban(guild, user):
    print("on member unban")

@bot.event
async def on_member_join(member):
    usage_string = (f'\
    [TIME: {utilities.epoch_to_custom_date(utilities.FMT_TIME)}]\n\
    Author Alias: {member.name}\n\
    Author Name: {member}\n\
    Author ID: {member.id}\n\
    Newly joined this server:`\n\
    Server: {member.guild}\n\
    Server ID: {member.guild.id}\n\
------\
    ')
    print(usage_string)
    for channel in member.guild.channels:
        if channel.name == 'general':
            with open('config.json', 'r') as json_file:
                data = json.load(json_file)    
                for p in data ['PREFIX']:
                    prefix_choice = p['prefix']
            welm = (f"Welcome to ")
            delm = (f"`{member.guild}`!")
            desm = (f'Enjoy the guild.')
            vasm = (f'Type `{prefix_choice}help` to learn all my commands.\n Now go and have some fun, {member.mention} <3')
            await channel.send(embed=discord.Embed(title=welm, description=delm, color=0x28e778)
            .add_field(name=desm, value=vasm, inline = False)
            .set_thumbnail(url=member.avatar_url))
    for channel in member.guild.channels:
        if channel.name == 'logs':
            welm = (f"Welcome to `{member.guild}`!")
            desm = (f'ONE OF US!\n A warm welcome to: {member.mention} <3')
            return await channel.send(embed=discord.Embed(title=welm, description=desm, color=0x28e778)
            .set_thumbnail(url=member.avatar_url))

@bot.event
async def on_guild_join(guild):
    usage_string = (f'\
    [TIME: {utilities.epoch_to_custom_date(utilities.FMT_TIME)}]\n\
    HENRY JUST JOINED A NEW SERVER\n\
    Server: {guild}\n\
    Server ID: {guild.id}\n\
------\
    ')
    print(usage_string)
    msg = (f'Sir Henry just joined the Server: `{guild}` `(Server ID: {guild.id})`')
    user = None
    for guild in bot.guilds:
        user = discord.utils.get(guild.members, id = "410406332143763466")
        if user is not None:
            break
    await message.user.send(msg)

@bot.event
async def on_message_delete(message):
    usage_string = (f'\
    [TIME: {utilities.epoch_to_custom_date(utilities.FMT_TIME)}]\n\
    Author Alias: {message.author.name}\n\
    Author Name: {message.author}\n\
    Author ID: {message.author.id}\n\
    Event: Deleted message\n\
    Full Message: {message.content}\n\
    Channel: {message.channel}\n\
    Server: {message.guild}\n\
    Server ID: {message.guild.id}\n\
------\
    ')
    print(usage_string)
    try:
        for channel in message.guild.channels:
            if channel.name == 'logs':
                auth = (f'<@!{message.author.id}> ({message.author})')
                chan = (f'#{message.channel}')
                return await channel.send(embed=discord.Embed(title="Message deleted", color=0xeee657)
                .add_field(name="Channel", value=chan, inline = False)
                .add_field(name="Message Author", value=auth, inline = False)
                .add_field(name="Message Author ID", value=message.author.id, inline = False)
                .add_field(name="Message ID", value=message.id, inline = False)
                .add_field(name="Message", value=message.content, inline = False)
                .set_thumbnail(url=message.author.avatar_url)
                .set_footer(text=bot.user.name, icon_url=bot.user.avatar_url))
    except:
        return

@bot.event
async def on_message_edit(before, after):
    if before.author != bot.user:
        if before.content != after.content:
            usage_string = (f'\
    [TIME: {utilities.epoch_to_custom_date(utilities.FMT_TIME)}]\n\
    Author Alias: {before.author.name}\n\
    Author Name: {before.author}\n\
    Author ID: {before.author.id}\n\
    Edited a message`\n\
    Channel: {before.channel}\n\
    Server: {before.channel.guild}\n\
    Server ID: {before.channel.guild.id}\n\
------\
    ')
            print(usage_string)
            try:
                for channel in before.guild.channels:
                    if channel.name == 'logs':
                        auth = (f'<@!{before.author.id}> ({before.author})')
                        chan = (f'#{before.channel}')
                        return await channel.send(embed=discord.Embed(title="Message edited", color=0xeee657)
                        .add_field(name="Channel", value=chan, inline = False)
                        .add_field(name="Message Author", value=auth, inline = False)
                        .add_field(name="Message Author ID", value=before.author.id, inline = False)
                        .add_field(name="Message ID", value=after.id, inline = False)
                        .add_field(name="Message before", value=before.content, inline = False)
                        .add_field(name="Message after", value=after.content, inline = False)
                        .set_thumbnail(url=after.author.avatar_url)
                        .set_footer(text=bot.user.name, icon_url=bot.user.avatar_url))
            except:
                return

@bot.event
async def on_guild_channel_create(channel):
    usage_string = (f'\
    [TIME: {utilities.epoch_to_custom_date(utilities.FMT_TIME)}]\n\
    A channel was created\n\
    Channel: {channel.name}\n\
    Server: {channel.guild}\n\
    Server ID: {channel.guild.id}\n\
------\
    ')
    print(usage_string)
    for channels in channel.guild.channels:
        if channels.name == 'logs':
            return await channels.send(embed=discord.Embed(title="Channel creation", color=0xeee657)
            .add_field(name="Channel", value=channel.name, inline = False)
            .set_footer(text=bot.user.name, icon_url=bot.user.avatar_url))

@bot.event
async def on_guild_channel_delete(channel):
    usage_string = (f'\
    [TIME: {utilities.epoch_to_custom_date(utilities.FMT_TIME)}]\n\
    A channel was deleted\n\
    Channel: {channel.name}\n\
    Server: {channel.guild}\n\
    Server ID: {channel.guild.id}\n\
------\
    ')
    print(usage_string)
    for channels in channel.guild.channels:
        if channels.name == 'logs':
            return await channels.send(embed=discord.Embed(title="Channel deletion", color=0xeee657)
            .add_field(name="Channel", value=channel.name, inline = False)
            .set_footer(text=bot.user.name, icon_url=bot.user.avatar_url))

@bot.event
async def on_guild_channel_update(before, after):
    print("on guild channel change")

@bot.event
async def on_guild_channel_pins_update(channel, last_pin):
    print("on guild channel pin update")

@bot.event
async def on_command_error(ctx, error):

    total_uptime_save()
    reaction_trigger_save()
    cmd_trigger_save()
    
    usage_string = (f'\
    [TIME: {utilities.epoch_to_custom_date(utilities.FMT_TIME)}]\n\
    Author Alias: {ctx.message.author.name}\n\
    Author Name: {ctx.message.author}\n\
    Author ID: {ctx.message.author.id}\n\
    Channel: {ctx.message.channel}\n\
    Server: {ctx.message.guild}\n\
    Server ID: {ctx.message.guild.id}\n\
        \n\
    ON COMMAND ERROR\n\
    ')
    print(usage_string)
    try:
        error = getattr(error, 'original', error)
        error_message = (f'\
    ERROR MESSAGE: {error}\n\
    COMPLETE MESSAGE: {ctx.message.content}\n\
------\
        ')
        print(error_message)
        list = ["What now, ", "There's no such command, ", "Need help, ", "Thou shalt not speak the language of the peasants, "]
        return await ctx.send(random.choice(list) + ctx.author.mention + "?")
    except RuntimeError as err:
        print(f'\
    ERROR MESSAGE: {err}\n\
------\
        ')

@bot.command()#
async def youtube(ctx, url=""):
    pass

# TODO
# @bot.command()#
# async def youtube(ctx, keyword_raw, url=""):
#     usage_string = (f'[TIME: {utilities.epoch_to_custom_date(utilities.FMT_TIME)}] ID: {ctx.message.author.id} (Name: {ctx.message.author.name}) used `{ctx.command.name}` in channel: {ctx.message.channel} (Server: {ctx.message.guild})')
#     print(usage_string)
#     print('------')
#     cmd_trigger()

#     joining = (f'Okay, I\'m here. What now?')
#     leaving = (f'Okay, okay, I\'ll leave! Jeez, calm down.')
#     stopping = (f'Stopped playing.')
#     pausing = (f'Paused playing.')
#     resuming = (f'Resumed playing.')
#     volume = (f'Changing volume to {url}%.')

#     channel = ctx.message.author.voice.voice_channel
#     voice = bot.join_voice_channel(channel)

#     try:

#         if keyword_raw == "join":
#             await ctx.send(joining)
#             await voice

#         if keyword_raw == "leave":
#             await ctx.send(leaving)
#             for x in bot.voice_clients:
#                 if(x.guild == ctx.message.guild):
#                     return await x.disconnect()

#         # if a song is already playing nothing happens
#         if keyword_raw == "play":
#             if url is "":
#                 return ctx.send("You got to give me a YouTube URL, stupid! `!youtube play URL_HERE`")
#             voice = await bot.join_voice_channel(channel)
#             global player
#             player = await voice.create_ytdl_player(url)
#             player.start()
#             playing = (f'`Now playing {player.title}!`')
#             await ctx.send(playing)
#             return player

#         if keyword_raw == "stop":
#             await ctx.send(stopping)
#             player.stop()

#         if keyword_raw == "pause":
#             await ctx.send(pausing)
#             player.pause()

#         if keyword_raw == "resume":
#             await ctx.send(resuming)
#             player.resume()

#         if keyword_raw == "volume":
#             set_vol = (int(url)/100)
#             if float(set_vol) <= 0:
#                 return await ctx.send("You can\'t do that, silly.")
#             elif float(set_vol) > 1:
#                 return await ctx.send("You can\'t do that, silly.")
#             else:
#                 await ctx.send(volume)
#                 player.volume = set_vol
#     except:
#         return await ctx.send("Whoops, " + ctx.message.author.mention + "! `!" + ctx.command.name + " " + keyword_raw + "` didn\'t work this time.\nI\'m probably already playing something or idk.\nProbably I broke.")

#     if keyword_raw == "info":
#         if player.is_playing():
#             return await ctx.send(embed=discord.Embed(title="Info on Youtube Player", color=0xeee657)
#             .add_field(name="Title", value=player.title, inline = False)
#             .add_field(name="Description", value=player.description, inline = False)
#             .add_field(name="Length", value=player.duration, inline = False)
#             .add_field(name="URL", value=player.url, inline = False)
#             .set_thumbnail(url=ctx.message.author.avatar_url)
#             .set_footer(text=bot.user.name, icon_url=bot.user.avatar_url))
#         else:
#             return await ctx.send("There is nothing playing, silly!")

@bot.command()
async def say(ctx, serv, chan, *mes_raw):
    printCtx(ctx)
    cmd_trigger()

    if ctx.message.author.guild_permissions.administrator:
        if commands.is_owner():
            mes = ' '.join(mes_raw)
            for guild in bot.guilds:
                if guild.name == serv:
                    channel = discord.utils.get(guild.channels, name=chan)
                    return await ctx.message.channel.send(mes)

@bot.command()
async def leave(ctx, ID):
    printCtx(ctx)
    cmd_trigger()

    if ctx.message.author.guild_permissions.administrator:
        try:
            if commands.is_owner():
                serv = bot.get_server(ID)
                msg = (f'Sir Henry just left the Server: `{serv}` `(Server ID: {serv.id})`')
                user = None
                await bot.leave_server(serv)
                for guild in bot.guilds:
                    user = discord.utils.get(guild.members, id = bot_owner_id)
                    if user is not None:
                        break
                await message.user.send(msg)
        except:
            await ctx.send("`Something did go wrong. Please read the log.`")
    else:
        embed = discord.Embed(title="Permission", description=(ctx.message.author.mention + ', you\'re not a mod. You can\'t use `' + ctx.command.name + '`.'),
                            color=0xeee657)
        return await ctx.send(embed=embed)

@bot.command()
async def userinfo(ctx, member : discord.Member = None):
    printCtx(ctx)
    cmd_trigger()

    if member is None: 
        member = ctx.message.author
    return await ctx.send(embed=discord.Embed(title=f"{member.name}'s User Information", color=0xeee657)
    .add_field(name="Name", value="<@!"+str(member.id)+">", inline = False)
    .add_field(name="Discriminator", value=member.discriminator, inline = False)
    .add_field(name="ID", value=member.id, inline = False)
    .add_field(name="This Server's ID", value=ctx.message.guild.id, inline = False)
    .add_field(name="Highest Role", value=member.top_role.name, inline = False)
    .add_field(name="Avatar Url", value=member.avatar_url, inline = False)
    .add_field(name="Joined Discord", value=member.created_at, inline = False)
    .add_field(name="Joined Server", value=member.joined_at, inline = False)
    .add_field(name="Bot", value=member.bot, inline = False)
    .set_thumbnail(url=member.avatar_url)
    .set_footer(text=bot.user.name, icon_url=bot.user.avatar_url))

@bot.command()
async def suggestion(ctx):
    printCtx(ctx)
    cmd_trigger()

    try:
        for channel in ctx.message.guild.channels:
            if channel.name == 'suggestions':
                await channel.send(embed=discord.Embed(title="Suggestion Author", description=ctx.message.author.name, color=0xeee657)
                .add_field(name="Suggestion Message", value=ctx.message.content))
        return await ctx.send(embed=discord.Embed(title="Suggestion received", color=0xeee657))  
    except:
        return

def reloadRaw():
    if os.name is "nt":
        os.execv(sys.executable, ['python3.6'] + sys.argv)
    else:
        import ctypes
        argc = ctypes.c_int()
        argv = ctypes.POINTER(ctypes.c_wchar_p if sys.version_info >= (3, ) else ctypes.c_char_p)()
        ctypes.pythonapi.Py_GetArgcArgv(ctypes.byref(argc), ctypes.byref(argv))
        os.execv(sys.executable, ['python3.6'] + [argv[1]] + sys.argv)

@bot.command()
async def reload(ctx):
    printCtx(ctx)
    cmd_trigger()

    if ctx.message.author.guild_permissions.administrator:
        if commands.is_owner() or ctx.message.author.guild is "The Eclectic Collective":
            await ctx.send("`Reloading modules. Restarting connection.`")
            sd = discord.Game(name="REBOOT")
            bye = discord.Game(name="BYE")
            await bot.change_presence(status=discord.Status.idle, activity=sd)
            await asyncio.sleep(3)
            await bot.change_presence(status=discord.Status.idle, activity=bye)
            await asyncio.sleep(1)
            await bot.change_presence(status=discord.Status.offline)
            total_uptime_save()
            reaction_trigger_save()
            cmd_trigger_save()
            if bot.is_ready():
                await ctx.send("`Values saved`")
                await ctx.send("`Logout`")
                reloadRaw()
        else:
            embed = discord.Embed(title="Notification", description=("<@!"+bot_owner_id+">, " + ctx.message.author.mention + " wants to reload the bot."),
                        color=0xeee657)
            return await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Permission", description=(ctx.message.author.mention + ', you\'re not a mod. You can\'t use this command.'),
                            color=0xeee657)
        return await ctx.send(embed=embed)

@bot.command()
@commands.is_owner()
async def quit(ctx):
    printCtx(ctx)
    cmd_trigger()

    if ctx.message.author.guild_permissions.administrator:
        if commands.is_owner():
            await ctx.send("`Shutdown requested`")
            sd = discord.Game(name="SHUTDOWN")
            bye = discord.Game(name="BYE")
            await bot.change_presence(status=discord.Status.idle, activity=sd)
            await asyncio.sleep(3)
            await bot.change_presence(status=discord.Status.idle, activity=bye)
            total_uptime_save()
            reaction_trigger_save()
            cmd_trigger_save()
            if bot.is_ready():
                await ctx.send("`Values saved`")
                await ctx.send("`Logout`")
                await bot.logout()
                return sys.exit(0)
        else:
            embed = discord.Embed(title="Notification", description=("<@!"+bot_owner_id+">, " + ctx.message.author.mention + " wants to quit the bot."),
                        color=0xeee657)
            return await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Permission", description=(ctx.message.author.mention + ', you\'re not a mod. You can\'t use this command.'),
                            color=0xeee657)
        return await ctx.send(embed=embed)

@bot.command()
async def prefix(ctx, prefix_raw):
    printCtx(ctx)
    cmd_trigger()

    if prefix_raw == "show":
        with open('config.json', 'r') as json_file:
            data = json.load(json_file)    
            for p in data ['PREFIX']:
                prefix_choice = p['prefix']
        embed = discord.Embed(description=("Actual prefix is: " + prefix_choice), color=0xeee657)
        return await ctx.send(embed=embed)
    else:
        if ctx.message.author.guild_permissions.administrator:
            if commands.is_owner():
                with open('config.json', 'r') as json_file:
                    data = json.load(json_file)  
                    data["PREFIX"][0]["prefix"] = prefix_raw
                    with open('config.json', 'w') as outfile:
                        json.dump(data, outfile)
                statusMsg = (f'{prefix_raw}help')
                status_pref = discord.Game(name=statusMsg)
                saveStatus(statusMsg)
                await bot.change_presence(status=discord.Status.online, activity=status_pref)
                bot.command_prefix = commands.when_mentioned_or(prefix_raw)
                return await ctx.send(embed=discord.Embed( description=("Prefix successfully set to: " + prefix_raw), color=0xeee657))
            else:
                return await ctx.send(embed=discord.Embed(
                description=("<@!"+bot_owner_id+">, " + ctx.message.author.mention + " wants to have the prefix changed to " + prefix_raw + "."), 
                color=0xeee657))
        else:
            embed = discord.Embed(description=(ctx.message.author.mention + ', you\'re not a mod. You can\'t use this command.'),
                                color=0xeee657)
            return await ctx.send(embed=embed)

@bot.command()
async def status(ctx, *status_raw):
    printCtx(ctx)
    cmd_trigger()

    if ctx.message.author.guild_permissions.administrator:
        status_arg = ' '.join(status_raw)
        activity_stat = discord.Game(name=status_arg)
        saveStatus(status_arg)
        # data["STATUS"][0]["status"] = status_arg
        # with open('config.json', 'w') as outfile:
        #     json.dump(data, outfile)
        await bot.change_presence(status=discord.Status.online, activity=(activity_stat))
        return await ctx.send(embed=discord.Embed(title="Status changed to: ", description=("@Sir Henry Pickles playing " + status_arg), color=0xeee657))
    else:
        return await ctx.send(ctx.message.author.mention + ', you\'re not a mod. You can\'t use this command.')

def saveStatus(status_arg):
    with open('config.json', 'r') as json_file:
        data = json.load(json_file)  
        data["STATUS"][0]["status"] = status_arg
        with open('config.json', 'w') as outfile:
            json.dump(data, outfile)

@bot.command()
async def members(ctx):
    printCtx(ctx)
    cmd_trigger()

    if ctx.message.author.guild_permissions.administrator:
        log_path = await memberList.membersLog(ctx)
        for channel in ctx.message.guild.channels:
            if channel.name == 'logs':
                await channel.send(file=discord.File(log_path))
        return await ctx.message.author.send(file=discord.File(log_path))
    else:
        return await ctx.send(ctx.message.author.mention + ', you\'re not a mod. You can\'t use this command.')

@bot.command()
async def members_show(ctx):
    printCtx(ctx)
    cmd_trigger()

    if ctx.message.author.guild_permissions.administrator:
        members = await memberList.membersDump(ctx)
        return await ctx.message.author.send(members)
    else:
        return await ctx.send(ctx.message.author.mention + ', you\'re not a mod. You can\'t use this command.')

@bot.command()
async def info(ctx):
    printCtx(ctx)
    cmd_trigger()
    total_uptime_save()
    time_lapsed = (time.time() - start_time)
    total_uptime = time_lapsed + uptime_pull
    link_build = (f'https://discordapp.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=8')
    timeDiff = timedelta(seconds=total_uptime)
    years = int(int(timeDiff.days) / 365)
    days = int(timeDiff.days) - (int(years) * 365)
    uptimeStr = (f'Years: {years}, Days: {days}')

    return await ctx.send(embed = discord.Embed(title="Sir Henry Pickles", description="Pickles are love, pickles are life!", color=0xeee657)
    .set_thumbnail(url=bot.user.avatar_url)
    .add_field(name="System Time:", value=utilities.epoch_to_custom_date(utilities.FMT_TIME), inline=False)
    .add_field(name="Command count: ", value=cmd_trigger.Counter, inline=False)
    .add_field(name="Message count: ", value=reaction_trigger.counter, inline=False)
    .add_field(name="Server count: ", value=len(bot.guilds), inline=False)
    .add_field(name="Uptime", value=timedelta(seconds=time_lapsed), inline=False)
    .add_field(name="Total Uptime", value=uptimeStr, inline=False)
    .add_field(name="GitHub Project Page:", value="https://github.com/x3l51/discord_bot", inline=False)
    .add_field(name="Next features and progress on them:", value="https://github.com/x3l51/discord_bot/projects/1", inline=False)
    .add_field(name="Direct invite to the Developers Discord:", value="https://discordapp.com/invite/5raBJUU", inline=False)
    .add_field(name="Invite the Bot to your Discord Server:", value=link_build, inline=False)
    .add_field(name="Author", value="<@!"+bot_owner_id+">")
    .set_footer(text=bot.user.name, icon_url=bot.user.avatar_url))

@bot.command(name="time", ignore_extras=False)
async def cmd_time(ctx, *tz_keywords):
    printCtx(ctx)
    cmd_trigger()
    tz_keyword = '_'.join(tz_keywords)
    moon = ('Moon', 'moon')
    moon_rep = ('Very funny, ' + ctx.message.author.mention, 'Wow, ' + ctx.message.author.mention,
                'Oi, ' + ctx.message.author.mention + '! Go fork urself m8!',
                'Maan, dude, idk maaan, like ... on the moon? duuuude .... DUUuUuuUuUUuDDDEeeeee. *hits blunt* idk ' + ctx.message.author.mention + ', better call the space tesla guy ..!?')

    if tz_keyword in (moon):
        await ctx.send("...")
        await asyncio.sleep(2)
        return await ctx.send(random.choice(moon_rep))
    if tz_keyword is "":
        tz_keyword = "GMT+0"
        await ctx.send("No keyword given, so I'll give you `GMT+0`. Try `!time GMT+0` or `!time Denver` next time.")
    valid_zones = []
    for zone in pytz.all_timezones:
        zones = zone.split('/')
        region = ''
        region_tz = ''
        region_city = ''
        if len(zones) == 1:
            region = zones[0]
            region_tz = ''
        elif len(zones) == 2:
            region, region_tz = zones[0], zones[1]
        else:
            region, region_tz, region_city = zones[0], zones[1], zones[2]
            found = False
        if region.lower().startswith(tz_keyword.lower()) and not found:
            valid_zones.append('Time Zone: {} is {}'.format(zone, datetime.now(tz=timezone(zone))))
            found = True
        if region_tz.lower().startswith(tz_keyword.lower()) and not found:
            valid_zones.append('Time Zone: {} is {}'.format(zone, datetime.now(tz=timezone(zone))))
            found = True
        if region_city.lower().startswith(tz_keyword.lower()) and not found:
            valid_zones.append('Time Zone: {} is {}'.format(zone, datetime.now(tz=timezone(zone))))
    else:
        if len(valid_zones) == 0:
            return await ctx.send('{} is an invalid timezone'.format(tz_keyword))
        else:
            msg = '\n'.join(valid_zones)
            if len(msg) <= 2000:
                await ctx.send(msg)
            else:
                current_len = 0
                msg = ''
                for idx, _msg in enumerate(valid_zones):
                    msg += '{}\n'.format(valid_zones[idx])
                    current_len = current_len + len(_msg)
                    try:
                        if current_len + len(valid_zones[idx + 1]) > 1950:
                            await ctx.send(msg)
                            msg = ''
                            current_len = 0
                    except IndexError:
                        return await ctx.send(msg)

@bot.command()
async def archive(ctx):
    printCtx(ctx)
    cmd_trigger()

    for channel in ctx.message.guild.channels:
        if channel.name == 'logs':
            msg = (f'{ctx.message.author.mention} just created an archive of {ctx.message.channel.name}!')
            await channel.send(msg)
            return await log_messages(ctx)

async def log_messages(ctx):
    cmd_trigger()

    log_path = ("./logs/archive" + "-server-" + ctx.message.guild.name.replace(' ', '-') + "-channel-" + ctx.message.channel.name + "-" + (utilities.epoch_to_custom_date(utilities.FMT_TIME_FILE)) + ".log")
    if ctx.message.author.guild_permissions.administrator:
        async for m in ctx.message.channel.history(limit=None):
            list_all = (f'Time (CET): {m.created_at}\nID: {m.author.id}\nName: {m.author} ({m.author.name})\nContent: {m.content}\n\n')
            with open(log_path, 'a', encoding='utf-8') as file:
                file.write(list_all)
        for channel in ctx.message.guild.channels:
            if channel.name == 'logs':
                await channel.send(file=discord.File(log_path))
        return await ctx.message.author.send(file=discord.File(log_path))

@bot.command()
async def clear(ctx, cle: int = 1000):
    printCtx(ctx)
    cmd_trigger()

    if ctx.message.author.guild_permissions.administrator:
        for channel in ctx.message.guild.channels:
            if channel.name == 'logs':
                msg = (f'{ctx.message.author.mention} just created an archive of {ctx.message.channel.name} and cleared it!')
                await channel.send(msg)
                await log_messages(ctx)
                if cle == 1000:
                    await ctx.message.channel.purge(bulk=True)
                else:
                    limit=int(cle) + 1
                    await ctx.message.channel.purge(limit=limit, bulk=True)
                cle_num = str(cle)
                if cle == 1000:
                    num_cleared = "up to 1000 messages"
                elif cle <= 0:
                    num_cleared = "your message because why would you want to clear " + cle_num + " messages!?"
                elif cle == 1:
                    num_cleared = "1 message"
                else:
                    num_cleared = str(cle) + " messages"
                embed = discord.Embed(title="Channel has been cleared of " + num_cleared, color=0x00ff00)
                embed.set_image(
                    url="https://media1.giphy.com/media/PAO4KoQ532CRi/giphy.gif")
                await ctx.send(embed=embed)
                return
    else:
        return await ctx.send(
        ctx.message.author.mention + ', you have no permission to use this command.')

@bot.command()
async def test(ctx):
    printCtx(ctx)
    cmd_trigger()

    return await ctx.send("successful")

@bot.command()
async def mod(ctx):
    printCtx(ctx)
    cmd_trigger()

    if ctx.message.author.guild_permissions.administrator:
        return await ctx.send(ctx.message.author.mention + ', you\'re a mod.')
    else:
        return await ctx.send(ctx.message.author.mention + ', you\'re not a mod.')

@bot.command(name='help', )
async def cmd_help(ctx):
    printCtx(ctx)
    cmd_trigger()

    await ctx.message.author.send(
                        "If you are in need of immediate assistance, I kindly suggest you to call the emergency "
                        "services.\n "
                        "\n"
                        "----------\n"
                        "\n"
                        "**Name**: Sir Henry Pickles\n"
                        "**Description:** *Does his best.*\n"
                        )
    for embed in messages.HELP_EMBEDS:
        await ctx.message.author.send(embed=embed)

    return await ctx.message.author.send("If you still have questions, please ping the `@Mods`")

@bot.command()
async def sleep(ctx):
    printCtx(ctx)
    cmd_trigger()

    sleep = ['Yes, you should use the sleep.', 'But mooooom idonwanna!', 'Whatevs, man.', 'JA!']
    return await ctx.send(random.choice(sleep))

@bot.command()
async def shower(ctx):
    printCtx(ctx)
    cmd_trigger()

    shower = [' you reek already!', ' it`s about time...', ' nah, its cool.',
            ' I mean, have you already showered this week?', ' but only a golden shower.']
    return await ctx.send(ctx.message.author.mention + " " + random.choice(shower))

@bot.command()
async def joke(ctx):
    printCtx(ctx)
    cmd_trigger()
    return await ctx.send(embed=discord.Embed(title="Joke", description=random.choice(messages.JOKES), color=0x00ff00))

@bot.command(name='8ball', )
async def cmd_8ball(ctx):
    printCtx(ctx)
    cmd_trigger()

    ball_res = ['It is certain.', 'It is decidedly so.', 'Without a doubt.', 'Yes - definitely.', 'You may rely on it.',
                'As I see it, yes.', 'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.',
                'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.', 'Connot predict now.',
                'Concentrate and ask again.', 'Don`t count on it.', 'My reply is no.', 'My sources say no.',
                'Outlook not so good.']
    return await ctx.send(embed=discord.Embed(title="8Ball", description=random.choice(ball_res), color=0x00ff00))

@bot.command()
async def roll(ctx, dice_string, mod: int = 0):
    printCtx(ctx)
    cmd_trigger()

    try:
        count_raw, num_raw = dice_string.split("d")
        if not count_raw:
            count_raw = 1
        count = int(count_raw)
        num = int(num_raw)
        await ctx.send("Rolling " + str(count) + " d" + str(num) + " ...")
        await asyncio.sleep(2)
        random.seed()
        numbers = []
        for count in range(count):
            number = random.randint(1, num)
            numbers.append(number)
        num_ran_count = (sum(numbers))
        if mod == 0:
            await ctx.send("I rolled a " + str(num_ran_count) + " for you.")
        else:
            num_ran_count_mod = num_ran_count + mod
            await ctx.send("I rolled " + str(num_ran_count) + " for you. That\'s a " + str(
                num_ran_count_mod) + " with your modifier.")
    except:
        await ctx.send(
            f'Error. Something didn\'t work out, <@{ctx.message.author.id}>. Check your formatting. Should it have been `1d{dice_string} {mod}`?')

@bot.command()
async def bleach(ctx):
    printCtx(ctx)
    cmd_trigger()

    await ctx.send(random.choice(messages.BLEACHES))

@bot.command()
async def goodreads(ctx, *keyword_raw):
    printCtx(ctx)
    cmd_trigger()

    keyword = "+".join(keyword_raw)
    async with aiohttp.ClientSession() as session:
        html = await fetch(session,'https://www.goodreads.com/search.xml?key=' + goodreads_key + '&q=' + keyword + '&page=1')
        xml = ElementTree.fromstring(html)
    for i, v in enumerate(xml.find('search/results')):
        book = v.find('best_book')
        author = book.find('author/name').text
        title = book.find('title').text
        book_id = book.find('id').text
        result_list = (f'**{author}**: {title} - https://www.goodreads.com/book/show/{book_id}.It')
        await ctx.send(result_list)
        if i == 2:
            break

@bot.command(name='reddit', )
async def cmd_reddit(ctx, subreddit_raw):
    printCtx(ctx)
    subreddit_input = str(subreddit_raw) 
    cmd_trigger()
    x = int(0)

    try:
        for i, submission in enumerate(reddit.subreddit(subreddit_input).hot(limit=5)):
            if reddit.subreddit(subreddit_input).over18:
                await ctx.send("Please do not request NSFW results.")
                for channel in ctx.message.guild.channels:
                    if channel.name == 'logs':
                        auth = (f'<@!{ctx.message.author.id}> ({ctx.message.author})')
                        chan = (f'#{ctx.message.channel}')
                        await channel.send(embed=discord.Embed(title="Requested NSFW content", color=0xeee657)
                        .add_field(name="Channel", value=chan, inline = False)
                        .add_field(name="Message Author", value=auth, inline = False)
                        .add_field(name="Message Author ID", value=ctx.message.author.id, inline = False)
                        .add_field(name="Message ID", value=ctx.message.id, inline = False)
                        .add_field(name="Message", value=ctx.message.content, inline = False)
                        .set_thumbnail(url=ctx.message.author.avatar_url)
                        .set_footer(text=bot.user.name, icon_url=bot.user.avatar_url))
                        return await channel.send(ctx.message.guild.roles[-1].mention)
                        break
                return
            if submission.over_18:
                continue
            if submission.stickied:
                continue
            result_list = (f'{submission.url}')
            if not submission.over_18 and not submission.stickied:
                await ctx.send(result_list)
                x = int(x + 1)
                if x == 3:
                    break
    except:
        await ctx.send(
            f'Error. Something didn\'t work out. Search for somthing else or some time else, <@{ctx.message.author.id}>')

@bot.command(name='wikipedia', )
async def cmd_wikipedia(ctx, *wiki_keyword_raw):
    printCtx(ctx)
    cmd_trigger()
    wiki_error = "Error. Specify/ check/ rephrase your search query,"

    try:
        wiki_keyword = ' '.join(wiki_keyword_raw)
        wiki_keyword_string = wikipedia.page(wiki_keyword, auto_suggest=True, redirect=True)
        wiki_sum = wikipedia.summary(wiki_keyword_string, sentences=1, chars=100, auto_suggest=True, redirect=True)
        wiki_url = wiki_keyword_string.url
        embed_wiki = discord.Embed(title="Wikipedia", description=wiki_keyword, color=0x00ff00)
        embed_wiki.add_field(name=wiki_sum, value=wiki_url)
        await ctx.send(embed=embed_wiki)
    except:
        await ctx.send(f'{wiki_error} <@{ctx.message.author.id}>!')
        if not wikipedia.search(wiki_keyword, results=3):
            return
        wiki_choice = ', '.join(wikipedia.search(wiki_keyword, results=3))
        await ctx.send(f'Did you mean: {wiki_choice}?')

@bot.command()
async def wiktionary(ctx, *wikti_keyword_list):
    printCtx(ctx)
    wikti_keyword_raw = " ".join(wikti_keyword_list)
    cmd_trigger()
    wiki_error = "Error. Specify/ check/ rephrase your search query,"
    parser = WiktionaryParser()
    parser.set_default_language('english')

    try:
        def wiktionary__dict(the_fetch):
            return ast.literal_eval(str(the_fetch).encode('ascii', 'ignore').decode('ascii'))[0]

        word_to_define = wikti_keyword_raw.title()
        response = wiktionary__dict(parser.fetch(word_to_define))['definitions'][0]
        layout = '**{}** - ({})\n{}\n'.format(word_to_define, response['partOfSpeech'], response['text'])
        word_to_define = wikti_keyword_raw.lower()
        _response = wiktionary__dict(parser.fetch(word_to_define))['definitions'][0]
        layout += '**{}** - ({})\n{}\n'.format(word_to_define, _response['partOfSpeech'], _response['text'])
        embed_wikti = discord.Embed(title="Wiktionary", description=layout, color=0x00ff00)
        await ctx.send(embed=embed_wikti)
    except:
        return await ctx.send(f'{wiki_error} <@{ctx.message.author.id}>!')

@bot.command()
async def python(ctx, *keywords_raw):
    printCtx(ctx)
    keywords_clean = '+'.join(keywords_raw)
    url = ("https://docs.python.org/3.6/search.html?q=" + keywords_clean)
    return await ctx.send("Here you go: " + url)

@bot.command()
async def roles(ctx):
    printCtx(ctx)
    cmd_trigger()

    await ctx.send(ctx.message.author.mention + "\'s roles are:")
    for r in ctx.message.author.roles:
        roles_me = r.name
        await ctx.send("`" + roles_me + "`")

def total_uptime_save():
    time_lapsed = (time.time() - start_time)
    total_uptime = time_lapsed + uptime_pull
    with open('config.json', 'r') as json_file:
        data = json.load(json_file)
        data["UPTIME"][0]["uptime"] = total_uptime
        with open('config.json', 'w') as json_file:
            json.dump(data, json_file)
    return

def reaction_trigger_save():
    with open('config.json', 'r') as json_file:
        data = json.load(json_file)
        data["COUNTER"][0]["counter_reac"] = str(reaction_trigger.counter)
        with open('config.json', 'w') as outfile:
            json.dump(data, outfile)
    return

def reaction_trigger():
    count = int(reaction_trigger.counter)
    count += 1
    reaction_trigger.counter = count
    if reaction_trigger.counter >= int(reaction_trigger_pull) + 100:
        reaction_trigger_save()
    return
reaction_trigger.counter = int(reaction_trigger_pull)

def cmd_trigger_save():
    with open('config.json', 'r') as json_file:
        data = json.load(json_file)
        data["COUNTER"][0]["counter_cmd"] = str(cmd_trigger.Counter)
        with open('config.json', 'w') as outfile:
            json.dump(data, outfile)
    return

def cmd_trigger():
    count = int(cmd_trigger.Counter)
    count += 1
    cmd_trigger.Counter = count
    if cmd_trigger.Counter >= int(cmd_trigger_pull) + 10:
        cmd_trigger_save()
    return
cmd_trigger.Counter = int(cmd_trigger_pull)

def printCtx(ctx):
    usage_string = (f'\
    [TIME: {utilities.epoch_to_custom_date(utilities.FMT_TIME)}]\n\
    Author Alias: {ctx.message.author.name}\n\
    Author Name: {ctx.message.author}\n\
    Author ID: {ctx.message.author.id}\n\
    Command: `{ctx.command.name}`\n\
    Full Message: `{ctx.message.content}`\n\
    Channel: {ctx.message.channel}\n\
    Server: {ctx.message.guild}\n\
    Server ID: {ctx.message.guild.id}\n\
------\
    ')
    print(usage_string)

@bot.event
async def on_message(message):
    reaction_trigger()

    if message.author == bot.user:
        return

    if message.channel.type != discord.ChannelType.private:
        if bot.user.mentioned_in(message) and not message.mention_everyone:
            if any(x in message.content for x in messages.USER_GREETINGS):
                return await message.channel.send(random.choice(messages.BOT_GREETINGS))
            elif any(x in message.content for x in messages.USER_BYES):
                return await message.channel.send(random.choice(messages.BOT_BYES))
            else:
                await message.add_reaction(random.choice(['🤖', '👀', '💾', '🤘']))

        if 'USA' in message.content.upper():
            await message.add_reaction(random.choice(['🇺🇸', '🍔', '🌭', '🔫']))
        if 'NANI' in message.content.upper():
            await message.channel.send('NAAAAANNNIIIIII!?!?!?!11')
        if not message.channel.nsfw:
            offensiveMatch = False
            offensiveMatchList = []
            for y in re.sub("[^\w]", " ",  message.content).split():
                for z in messages.OFFENSIVE_LANGUAGE:
                    if y.lower() == z.lower():
                        offensiveMatchList.append(y)
                        offensiveMatch = True
            if offensiveMatch:
                usage_string = (f'\
    [TIME: {utilities.epoch_to_custom_date(utilities.FMT_TIME)}]\n\
    Author Alias: {message.author.name}\n\
    Author Name: {message.author}\n\
    Author ID: {message.author.id}\n\
    Event: Offensive Language\n\
    Full Message: `{message.content}`\n\
    Channel: {message.channel}\n\
    Server: {message.guild}\n\
    Server ID: {message.guild.id}\n\
------\
                ')
                print(usage_string)
                await message.channel.send(f'{message.author.mention}, please do not use this kind of language in non-NSFW marked channels. There are kids here.')
                for channel in message.guild.channels:
                    if channel.name == 'logs':
                        if len(offensiveMatchList) > 1:
                            singularOrPlural = "Words:" 
                        else:
                            singularOrPlural = "Word:"
                        await channel.send(embed=discord.Embed(title="Offensive Language", color=0xff0000)
                        .add_field(name="Author Alias:", value=message.author, inline = False)
                        .add_field(name="Author Name:", value=message.author.name, inline = False)
                        .add_field(name="Author ID:", value=message.author.id, inline = False)
                        .add_field(name="Server Name:", value=message.guild.name, inline = False)
                        .add_field(name="Server ID:", value=message.guild.id, inline = False)
                        .add_field(name="Channel:", value=message.channel.name, inline = False)
                        .add_field(name="Offensive " + singularOrPlural, value=(', '.join(offensiveMatchList)), inline = False)
                        .add_field(name="Original Message:", value=message.content, inline = False)
                        .add_field(name="State:", value="DELETED", inline = False)
                        .set_thumbnail(url=message.author.avatar_url)
                        .set_footer(text=bot.user.name, icon_url=bot.user.avatar_url))
                        await channel.send(message.guild.roles[-1].mention)
                        break

                messageClean = message.content
                for matchNr in range(0, len(offensiveMatchList)):
                    messageClean = messageClean.replace(offensiveMatchList[matchNr], (len(offensiveMatchList[matchNr]) * "*"))

                await message.channel.send(embed=discord.Embed(title="Offensive Language", color=0xff0000)
                    .add_field(name="Author Alias:", value=message.author, inline = False)
                    .add_field(name="Author Name:", value=message.author.name, inline = False)
                    .add_field(name="Author ID:", value=message.author.id, inline = False)
                    .add_field(name="Server Name:", value=message.guild.name, inline = False)
                    .add_field(name="Server ID:", value=message.guild.id, inline = False)
                    .add_field(name="Channel:", value=message.channel.name, inline = False)
                    .add_field(name="Original Message:", value=discord.utils.escape_markdown(messageClean), inline = False)
                    .add_field(name="State:", value="DELETED", inline = False)
                    .set_thumbnail(url=message.author.avatar_url)
                    .set_footer(text=bot.user.name, icon_url=bot.user.avatar_url))

                await message.author.send(embed=discord.Embed(title="Offensive Language", color=0xff0000)
                        .add_field(name="Author Alias:", value=message.author, inline = False)
                        .add_field(name="Author Name:", value=message.author.name, inline = False)
                        .add_field(name="Author ID:", value=message.author.id, inline = False)
                        .add_field(name="Server Name:", value=message.guild.name, inline = False)
                        .add_field(name="Server ID:", value=message.guild.id, inline = False)
                        .add_field(name="Channel:", value=message.channel.name, inline = False)
                        .add_field(name="Offensive " + singularOrPlural, value=(', '.join(offensiveMatchList)), inline = False)
                        .add_field(name="Original Message:", value=message.content, inline = False)
                        .add_field(name="State:", value="DELETED", inline = False)
                        .add_field(name="Rules", value="Please rephrase your message", inline = False)
                        .set_thumbnail(url=message.author.avatar_url)
                        .set_footer(text=bot.user.name, icon_url=bot.user.avatar_url))
                return await message.delete()

        for t in messages.TRIGGERS:
            if t in message.content.upper() or t in message.content.lower():
                for reaction in messages.TRIGGERS[t]:
                    await message.add_reaction(reaction)

        return await bot.process_commands(message)
    else:
        return await message.channel.send("I can't respond here. Beep boop beep.")

bot.run(TOKEN)