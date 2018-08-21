#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# bot_bcad_3.6.py

import os
import sys
import ast
import asyncio
import datetime
import json
import random
import time
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
import youtube_dl # to run this, the installation of ffmpeg is important: sudo apt-get install ffmpeg
from discord.ext import commands
from pytz import timezone
from wiktionaryparser import WiktionaryParser

import memberList
import messages
import utilities

with open('config.json') as json_file:
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


description = 'Sir Henry Pickles, the pickly Bot!'
bot = commands.Bot(max_messages=10000, command_prefix=commands.when_mentioned_or(prefix_choice))
reddit = praw.Reddit(client_id=json_client_id, client_secret=json_client_secret, user_agent=json_user_agent)
start_time = time.time()
bot.remove_command('help')
random.seed(a=None)


async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()


async def create_chan_log():
    for server in bot.servers:
        for channel in server.channels:
            if channel.name == 'logs':
                return
        everyone_perms = discord.PermissionOverwrite(read_messages=False)
        my_perms = discord.PermissionOverwrite(read_messages=True)
        everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)
        mine = discord.ChannelPermissions(target=server.me, overwrite=my_perms)
        await bot.create_channel(server, 'logs', everyone, mine)


async def create_chan_suggestions():
    for server in bot.servers:
        for channel in server.channels:
            if channel.name == 'suggestions':
                return
        everyone_perms = discord.PermissionOverwrite(read_messages=False)
        my_perms = discord.PermissionOverwrite(read_messages=True)
        everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)
        mine = discord.ChannelPermissions(target=server.me, overwrite=my_perms)
        await bot.create_channel(server, 'suggestions', everyone, mine)


@bot.event
async def on_ready():
    activity = discord.Game(name="with pickles.")
    await bot.change_presence(status=discord.Status.online, game=activity)
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await create_chan_log()
    await create_chan_suggestions()
    

@bot.event
async def on_member_join(member):
    for channel in member.server.channels:
        if channel.name == 'general':
            welm = (f"Welcome to `{member.server}`!")
            desm = (
                f'Enjoy the server.\n Type `!help` to learn all my commands.\n Now go and have some fun, {member.mention} <3')
            embed = discord.Embed(title=welm, description=desm, color=0xeee657)
            embed.set_thumbnail(url=member.avatar_url)
            return await bot.send_message(channel, embed=embed)


@bot.event
async def on_server_join(server):
    msg = (f'Sir Henry just joined the Server: `{server}` `(Server ID: {server.id})`')
    user = None
    for guild in bot.servers:
        user = discord.utils.get(guild.members, id = "410406332143763466")
        if user is not None:
            break
    await bot.send_message(user, msg)


@bot.event
async def on_message_delete(message):
    try:
        for channel in message.server.channels:
            if channel.name == 'logs':
                auth = (f'{message.author.name} ({message.author})')
                embed = discord.Embed(title="Message deleted", color=0xeee657)
                embed.add_field(name="Channel", value=message.channel)
                embed.add_field(name="Message Author", value=auth)
                embed.add_field(name="Message Author ID", value=message.author.id)
                embed.add_field(name="Message", value=message.content)
                return await bot.send_message(channel, embed=embed)
    except:
        return


@bot.event
async def on_message_edit(before, after):
    if before.author != bot.user:
        if before.content != after.content:
            try:
                for channel in before.server.channels:
                    if channel.name == 'logs':
                        auth = (f'{before.author.name} ({before.author})')
                        embed = discord.Embed(title="Message edited", color=0xeee657)
                        embed.add_field(name="Channel", value=before.channel)
                        embed.add_field(name="Message Author", value=auth)
                        embed.add_field(name="Message Author ID", value=before.author.id)
                        embed.add_field(name="Message before", value=before.content)
                        embed.add_field(name="Message after", value=after.content)
                        return await bot.send_message(channel, embed=embed)
            except:
                return


@bot.command(pass_context=True)
async def youtube(ctx, keyword_raw, url=""):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `yt`')
    print('------')
    keyword = url

    joining = (f'Okay, I\'m here. What now?')
    playing = (f'Now playing!')
    leaving = (f'Okay, okay, I\'ll leave! Jeez, calm down.')
    stopping = (f'Stopped playing.')
    pausing = (f'Paused playing.')
    resuming = (f'Resumed playing.')
    volume = (f'Changing volume to {keyword}%.')

    channel = ctx.message.author.voice.voice_channel
    voice = bot.join_voice_channel(channel)

    if keyword_raw == "join":
        await ctx.bot.say(joining)
        await voice

    if keyword_raw == "leave":
        await ctx.bot.say(leaving)
        for x in bot.voice_clients:
            if(x.server == ctx.message.server):
                return await x.disconnect()

    if keyword_raw == "play":
        try:
            if url is "":
                return ctx.bot.say("You got to give me a YouTube URL, stupid! `!yt play URL_HERE`")
            await ctx.bot.say(playing)
            voice = await bot.join_voice_channel(channel)
            global player
            player = await voice.create_ytdl_player(url)
            player.start()
            return player

            if keyword_raw == "stop":
                await ctx.bot.say(stopping)
                player.stop()

            if keyword_raw == "pause":
                await ctx.bot.say(pausing)
                player.pause()

            if keyword_raw == "resume":
                await ctx.bot.say(resuming)
                player.resume()

            if keyword_raw == "volume":
                await ctx.bot.say(volume)
                set_vol = (int(keyword)/100)
                if float(set_vol) <= 0:
                    return await ctx.bot.say("You can\'t do that, silly.")
                if float(set_vol) > 100:
                    return await ctx.bot.say("You can\'t do that, silly.")
                else:
                    player.volume = set_vol
        except:
            return await ctx.bot.say(player.error)


@bot.command(pass_context=True)
async def say(ctx, serv_raw, chan, *mes_raw):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `say`')
    print('------')
    if ctx.message.author.server_permissions.administrator:
        if ctx.message.author.id == bot_owner_id:
            serv = serv_raw.replace("-"," ")
            mes = ' '.join(mes_raw)
            for server in bot.servers:
                if server.name == serv:
                    channel = discord.utils.get(server.channels, name=chan)
                    await bot.send_message(channel, mes)
                    all = (f'"{mes}" sent to channel {channel} on server {serv}\n')
                    return print(all)

# todo
@bot.command(pass_context=True)
async def leave(ctx, ID):
    if ctx.message.author.server_permissions.administrator:
        try:
            if ctx.message.author.id == bot_owner_id:
                serv = bot.get_server(ID)
                msg = (f'Sir Henry just left the Server: `{serv}` `(Server ID: {serv.id})`')
                user = None
                await bot.leave_server(serv)
                for guild in bot.servers:
                    user = discord.utils.get(guild.members, id = bot_owner_id)
                    if user is not None:
                        break
                await bot.send_message(user, msg)
        except:
            await ctx.bot.say("`Something did go wrong. Please read the log.`")
    else:
        embed = discord.Embed(title="Permission", description=(ctx.message.author.mention + ', you\'re not a mod. You can\'t use this command.'),
                            color=0xeee657)
        return await ctx.bot.say(embed=embed)


@bot.command(pass_context=True)
async def userinfo(ctx, member : discord.Member = None):
    if member is None: member = ctx.message.author
    await ctx.bot.say(embed=discord.Embed(title=f"{member.name}'s User Information", color=0xeee657)
    .add_field(name="Name", value=member.name, inline = False)
    .add_field(name="Discriminator", value=member.discriminator, inline = False)
    .add_field(name="ID", value=member.id, inline = False)
    .add_field(name="This Server's ID", value=ctx.message.server.id, inline = False)
    .add_field(name="Highest Role", value=member.top_role.name, inline = False)
    .add_field(name="Avatar Url", value=member.avatar_url, inline = False)
    .add_field(name="Joined Discord", value=member.created_at, inline = False)
    .add_field(name="Joined Server", value=member.joined_at, inline = False)
    .add_field(name="Bot", value=member.bot, inline = False)
    .set_thumbnail(url=member.avatar_url)
    .set_footer(text=bot.user.name, icon_url=bot.user.avatar_url))


@bot.command(pass_context=True)
async def reload(ctx):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `reload`')
    print('------')
    cmd_trigger()
    if ctx.message.author.server_permissions.administrator:
        try:
            if ctx.message.author.id == bot_owner_id:
                await ctx.bot.say("`Reloading modules. Restarting connection.`")
                try:
                    total_uptime_save()
                    reaction_trigger_save()
                    cmd_trigger_save()
                    os.execv(sys.executable, ['python3.6'] + sys.argv)
                    # os.execv(sys.executable, ['sudo nohup python3.6'] + sys.argv)
                except:
                    await ctx.bot.say("`Something did go wrong. Please read the log.`")
            else:
                embed = discord.Embed(title="Notification", description=("<@!"+bot_owner_id+">, " + ctx.message.author.mention + " wants to reload the bot."),
                            color=0xeee657)
                return await ctx.bot.say(embed=embed)
        except:
            await ctx.bot.say("`Something did go wrong. Please read the log.`")
    else:
        embed = discord.Embed(title="Permission", description=(ctx.message.author.mention + ', you\'re not a mod. You can\'t use this command.'),
                            color=0xeee657)
        return await ctx.bot.say(embed=embed)


@bot.command(pass_context=True)
async def quit(ctx):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `quit`')
    print('------')
    cmd_trigger()
    if ctx.message.author.server_permissions.administrator:
        try:
            if ctx.message.author.id == bot_owner_id:
                await ctx.bot.say("`Shutdown requested`")
                total_uptime_save()
                reaction_trigger_save()
                cmd_trigger_save()
                await ctx.bot.say("`Values saved`")
                await ctx.bot.say("`Logout`")
                try:
                    await bot.logout()
                    await bot.close()
                    print("Exit script now.")
                    sys.exit()
                except:
                    return ctx.bot.say("Something did not work out. Read log.")

        except:
            embed = discord.Embed(title="Permission", description=(ctx.message.author.mention + "you have no permission to use this command."),
                            color=0xeee657)
            return await ctx.bot.say(embed=embed)


@bot.command(pass_context=True)
async def suggestion(ctx):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `suggestion`')
    print('------')
    cmd_trigger()
    try:
        for channel in ctx.message.server.channels:
            if channel.name == 'suggestions':
                embed = discord.Embed(title="Suggestion Author", description=ctx.message.author.name, color=0xeee657)
                embed.add_field(name="Suggestion Message", value=ctx.message.content)
                await bot.send_message(channel, embed=embed)
        embed = discord.Embed(title="Suggestion received", color=0xeee657)
        return await ctx.bot.say(embed=embed)  
    except:
        return


@bot.command(pass_context=True)
async def prefix(ctx, prefix_raw):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `prefix`') # TODO cmd auto grab
    print('------')
    cmd_trigger()
    if ctx.message.author.server_permissions.administrator:
        try:
            with open('config.json', 'r') as json_file:
                data = json.load(json_file)    
                for p in data ['PREFIX']:
                    prefix_choice = p['prefix']
                    if prefix_raw == "show":
                        embed = discord.Embed(title="Prefix", description=("Actual prefix is: " + prefix_choice), color=0xeee657)
                        return await ctx.bot.say(embed=embed)
                    else:
                        if ctx.message.author.id == bot_owner_id:
                            data["PREFIX"][0]["prefix"] = prefix_raw
                            with open('config.json', 'w') as outfile:
                                json.dump(data, outfile)
                                bot.command_prefix = commands.when_mentioned_or(prefix_raw)
                                embed = discord.Embed(title="Return", description=("Prefix successfully set."),
                            color=0xeee657)
                                return await ctx.bot.say(embed=embed)
                        else:
                            embed = discord.Embed(title="Notification", description=("<@!"+bot_owner_id+">, " + ctx.message.author.mention + " wants to have the prefix changed to " + prefix_raw + "."),
                            color=0xeee657)
                            return await ctx.bot.say(embed=embed)
        except IndexError:
            embed = discord.Embed(title="Error", description=("Index error when grabbing first obj"), color=0xeee657)
            return await ctx.bot.say(embed=embed)
    else:
        embed = discord.Embed(title="Permission", description=(ctx.message.author.mention + ', you\'re not a mod. You can\'t use this command.'),
                            color=0xeee657)
        return await ctx.bot.say(embed=embed)


@bot.command(pass_context=True)
async def status(ctx, *status_raw):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `status`')
    print('------')
    cmd_trigger()
    if ctx.message.author.server_permissions.administrator:
        status_arg = ' '.join(status_raw)
        activity = discord.Game(name=status_arg)
        await bot.change_presence(status=discord.Status.online, game=(activity))
        embed = discord.Embed(title="Status changed to: ", description=("@Sir Henry Pickles playing " + status_arg),
                            color=0xeee657)
        return await ctx.bot.say(embed=embed)
    else:
        return await ctx.bot.say(ctx.message.author.mention + ', you\'re not a mod. You can\'t use this command.')


# # todo
# @bot.event
# async def on_command_error(error):
#     await bot.send_message(error.channel, "What now," + error.author.mention + "?")

# todo converter celsius kelvin farenheit
# todo converter mile kilometer etc
# @bot.command(pass_context = True)
# async def convert(ctx, *keywords_raw):
#     await ctx.bot.say("This is in the making.")

# todo YT?

# # todo
# @bot.command(pass_context = True)
# async def timer(ctx, number, unit):
#     # print(number_unit_raw)
#     # number_unit = number_unit_raw
#     # print(number_unit)
#     # number, unit = number_unit.split(" ")
#     print(number)
#     print(unit)
#     if not unit:
#         unit = minutes
#     if unit == "seconds":
#         unit = seconds
#     if unit == "minutes":
#         unit = minutes
#     if unit == "hours":
#         unit = minutes
#     start_time_now = time.time()
#     print(number)
#     print(unit)
#     print(time.time())
#     timer_to = time.time() + (number * unit)
#     print(timer_to)


# todo 2000 char restriciton (time)
@bot.command(pass_context=True)
async def members(ctx):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `members`')
    print('------')
    cmd_trigger()
    if ctx.message.author.server_permissions.administrator:
        try:
            await memberList.membersLog(ctx)
        except:
            await ctx.bot.say('Whoops, something went wrong ' + ctx.message.author.mention + '.')
        return
    else:
        return await ctx.bot.say(ctx.message.author.mention + ', you\'re not a mod. You can\'t use this command.')


@bot.command(pass_context=True)
async def members_show(ctx):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `members_show`')
    print('------')
    cmd_trigger()
    if ctx.message.author.server_permissions.administrator:
        try:
            await memberList.membersDump(ctx)
        except:
            await ctx.bot.say('Whoops, something went wrong ' + ctx.message.author.mention + '.')
        return
    else:
        return await ctx.bot.say(ctx.message.author.mention + ', you\'re not a mod. You can\'t use this command.')


def total_uptime_save():
    time_lapsed = (time.time() - start_time)
    total_uptime = time_lapsed + uptime_pull
    data["UPTIME"][0]["uptime"] = total_uptime
    with open('config.json', 'w') as outfile:
        json.dump(data, outfile)


@bot.command(pass_context=True)
async def info(ctx):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `info`')
    print('------')
    cmd_trigger()
    total_uptime_save()
    time_lapsed = (time.time() - start_time)
    total_uptime = time_lapsed + uptime_pull
    await ctx.bot.say(embed = discord.Embed(title="Sir Henry Pickles", description="Pickles are love, pickles are life!", color=0xeee657)
    .set_thumbnail(url=bot.user.avatar_url)
    .add_field(name="System Time:", value=utilities.epoch_to_custom_date(utilities.FMT_TIME), inline=False)
    .add_field(name="Command count: ", value=cmd_trigger.Counter, inline=False)
    .add_field(name="Message count: ", value=reaction_trigger.counter, inline=False)
    .add_field(name="Server count: ", value=len(bot.servers), inline=False)
    .add_field(name="Uptime", value=timedelta(seconds=time_lapsed), inline=False)
    .add_field(name="Total Uptime", value=timedelta(seconds=total_uptime), inline=False)
    .add_field(name="GitHub Project Page:", value="https://github.com/x3l51/discord_bot", inline=False)
    .add_field(name="Next features and progress on them:", value="https://github.com/x3l51/discord_bot/projects/1", inline=False)
    .add_field(name="Direct invite to the Developers Discord:", value="https://discordapp.com/invite/5raBJUU", inline=False)
    .add_field(name="Invite the Bot to your Discord Server:", value="https://discordapp.com/oauth2/authorize?client_id=" + bot.user.id + "&scope=bot&permissions=8", inline=False)
    .add_field(name="Author", value="<@!"+bot_owner_id+">")
    .set_footer(text=bot.user.name, icon_url=bot.user.avatar_url))


@bot.command(name="time", pass_context=True, ignore_extras=False)
async def cmd_time(ctx, *tz_keywords):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `time`')
    print('------')
    cmd_trigger()
    tz_keyword = '_'.join(tz_keywords)
    moon = ('Moon', 'moon')
    moon_rep = ('Very funny, ' + ctx.message.author.mention, 'Wow, ' + ctx.message.author.mention,
                'Oi, ' + ctx.message.author.mention + '! Go fork urself m8!',
                'Maan, dude, idk maaan, like ... on the moon? duuuude .... DUUuUuuUuUUuDDDEeeeee. *hits blunt* idk ' + ctx.message.author.mention + ', better call the space tesla guy ..!?')
    if tz_keyword in (moon):
        await ctx.bot.say("...")
        await asyncio.sleep(2)
        return await ctx.bot.say(random.choice(moon_rep))
        sleep()
    if tz_keyword is "":
        tz_keyword = "GMT+0"
        await ctx.bot.say("No keyword given, so I'll give you `GMT+0`. Try `!time GMT+0` or `!time Denver` next time.")
    valid_zones = []
    for i, zone in enumerate(pytz.all_timezones):
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
            return await ctx.bot.say('{} is an invalid timezone'.format(tz_keyword))
        else:
            msg = '\n'.join(valid_zones)
            if len(msg) <= 2000:
                await ctx.bot.say(msg)
            else:
                current_len = 0
                msg = ''
                for idx, _msg in enumerate(valid_zones):
                    msg += '{}\n'.format(valid_zones[idx])
                    current_len = current_len + len(_msg)
                    try:
                        if current_len + len(valid_zones[idx + 1]) > 1950:
                            await ctx.bot.say(msg)
                            msg = ''
                            current_len = 0
                    except IndexError:
                        return await ctx.bot.say(msg)


@bot.command(pass_context=True)
async def archive(ctx):
    print(
        'ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `archive` in channel: ' + ctx.message.channel.name)
    print('------')
    for channel in ctx.message.server.channels:
            if channel.name == 'logs':
                msg = (f'{ctx.message.author.mention} just created an archive of {ctx.message.channel.name}!')
                await ctx.bot.send_message(channel, msg)
                return await log_messages(ctx)

async def log_messages(ctx):
    cmd_trigger()
    log_path = ("./logs/archive" + "-server-" + ctx.message.server.name.replace(' ', '-') + "-channel-" + ctx.message.channel.name + "-" + (utilities.epoch_to_custom_date(utilities.FMT_TIME_FILE)) + ".log")
    if ctx.message.author.server_permissions.administrator:
        async for m in bot.logs_from(ctx.message.channel):
            list_all = (f'Time (CET): {utilities.epoch_to_custom_date(utilities.FMT_TIME)}\nID: {m.author.id}\nName: {m.author} ({m.author.name})\nContent: {m.content}\n\n')
            with open(log_path, 'a') as file:
                file.write(list_all)
        for channel in ctx.message.server.channels:
            if channel.name == 'logs':
                await ctx.bot.send_file(channel, log_path)
        await ctx.bot.send_file(ctx.message.author, log_path)


@bot.command(pass_context=True)
async def clear(ctx, cle: int = 1000):
    print(
        'ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `clear` in channel: ' + ctx.message.channel.name)
    print('------')
    cmd_trigger()
    if ctx.message.author.server_permissions.administrator:
        for channel in ctx.message.server.channels:
            if channel.name == 'logs':
                msg = (f'{ctx.message.author.mention} just created an archive of {ctx.message.channel.name} and cleared it!')
                await ctx.bot.send_message(channel, msg)
                await log_messages(ctx)
                await bot.purge_from(ctx.message.channel, limit=cle + 1)
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
                    url="https://cdn.discordapp.com/attachments/474903005523869715/474903418100645898/FwxbY6j.gif")
                await ctx.bot.say(embed=embed)
                return
    else:
        return await ctx.bot.say(
        ctx.message.author.mention + ', you have no permission to use this command.')


@bot.command(pass_context=True)
async def test(ctx):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `test`')
    print('------')
    cmd_trigger()
    await ctx.bot.say("successful")


@bot.command(pass_context=True)
async def mod(ctx):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `mod`')
    print('------')
    if ctx.message.author.server_permissions.administrator:
        return await ctx.bot.say(ctx.message.author.mention + ', you\'re a mod.')
    else:
        return await ctx.bot.say(ctx.message.author.mention + ', you\'re not a mod.')


@bot.command(name='help', pass_context=True)
async def cmd_help(ctx):
    member = ctx.message.author
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `help`')
    print('------')
    cmd_trigger()

    await bot.send_message(member,
                           "If you are in need of immediate assistance, I kindly suggest you to call the emergency "
                           "services.\n "
                           "\n"
                           "----------\n"
                           "\n"
                           "**Name**: Sir Henry Pickles\n"
                           "**Description:** *Does his best.*\n"
                           )
    for embed in messages.HELP_EMBEDS:
        await bot.send_message(member, embed=embed)

    await bot.send_message(member, "If you still have questions, please ping the `@Mods`")


@bot.command(pass_context=True)
async def sleep(ctx):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `sleep`')
    print('------')
    cmd_trigger()
    sleep = ['Yes, you should use the sleep.', 'But mooooom idonwanna!', 'Whatevs, man.', 'JA!']
    await ctx.bot.say(random.choice(sleep))


@bot.command(pass_context=True)
async def shower(ctx):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `shower`')
    print('------')
    cmd_trigger()
    shower = [' you reek already!', ' it`s about time...', ' nah, its cool.',
              ' I mean, have you already showered this week?', ' but only a golden shower.']
    await ctx.bot.say(ctx.message.author.mention + " " + random.choice(shower))


# todo store jokes in json.log
@bot.command(pass_context=True)
async def joke(ctx):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `joke`')
    print('------')
    cmd_trigger()

    embed = discord.Embed(title="Joke", description=random.choice(messages.JOKES), color=0x00ff00)
    await ctx.bot.say(embed=embed)


@bot.command(name='8ball', pass_context=True)
async def cmd_8ball(ctx):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `8ball`')
    print('------')
    cmd_trigger()
    ball_res = ['It is certain.', 'It is decidedly so.', 'Without a doubt.', 'Yes - definitely.', 'You may rely on it.',
                'As I see it, yes.', 'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.',
                'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.', 'Connot predict now.',
                'Concentrate and ask again.', 'Don`t count on it.', 'My reply is no.', 'My sources say no.',
                'Outlook not so good.']
    embed = discord.Embed(title="8Ball", description=random.choice(ball_res), color=0x00ff00)
    await ctx.bot.say(embed=embed)


@bot.command(pass_context=True)
async def roll(ctx, dice_string, mod: int = 0):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `roll`')
    print('------')
    cmd_trigger()
    try:
        count_raw, num_raw = dice_string.split("d")
        if not count_raw:
            count_raw = 1
        count = int(count_raw)
        num = int(num_raw)
        await ctx.bot.say("Rolling " + str(count) + " d" + str(num) + " ...")
        await asyncio.sleep(2)
        random.seed()
        numbers = []
        for count in range(count):
            number = random.randint(1, num)
            numbers.append(number)
        num_ran_count = (sum(numbers))
        if mod == 0:
            await ctx.bot.say("I rolled a " + str(num_ran_count) + " for you.")
        else:
            num_ran_count_mod = num_ran_count + mod
            await ctx.bot.say("I rolled " + str(num_ran_count) + " for you. That\'s a " + str(
                num_ran_count_mod) + " with your modifier.")
    except:
        await ctx.bot.say(
            f'Error. Something didn\'t work out, <@{ctx.message.author.id}>. Check your formatting. Should it have been `1d{dice_string} {mod}`?')


@bot.command(pass_context=True)
async def bleach(ctx):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `bleach`')
    print('------')
    cmd_trigger()

    await ctx.bot.say(random.choice(messages.BLEACHES))


# todo
# TIP System
# Karma System
# given that karma systems are memory intent can you use the nickname system to hold the karma information. 
# Example USER (0) and I get thanked the bot looks at the nickname takes the int 0 and increments 
# it by one and renames me USER (1). The only caveat to this system  is you would have to restrict 
# nicknames to the bot and build a request to change it. But it would display karma openly and free up 
# memory as it's stored server side.

# todo
# #google calendar
# @bot.command()
# async def cal(ctx):
#     ctx.bot.say()

@bot.command(pass_context=True)
async def goodreads(ctx, *keyword_raw):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `goodreads`')
    print('------')
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
        await ctx.bot.say(result_list)
        if i == 2:
            break


@bot.command(name='reddit', pass_context=True)
async def cmd_reddit(ctx, subreddit_raw):
    subreddit_input = str(subreddit_raw)
    print(
        'ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `reddit`, looking for the subreddit: `' + subreddit_input + '`')
    print('------')
    cmd_trigger()
    x = int(0)
    try:
        for i, submission in enumerate(reddit.subreddit(subreddit_input).hot(limit=5)):
            if reddit.subreddit(subreddit_input).over18:
                await ctx.bot.say("Please do not request NSFW results.")
                break
            if submission.over_18:
                continue
            if submission.stickied:
                continue
            result_list = (f'{submission.url}')
            if not submission.over_18 and not submission.stickied:
                await ctx.bot.say(result_list)
                x = int(x + 1)
                if x == 3:
                    break
    except:
        await ctx.bot.say(
            f'Error. Something didn\'t work out. Search for somthing else or some time else, <@{ctx.message.author.id}>')


@bot.command(name='wikipedia', pass_context=True)
async def cmd_wikipedia(ctx, *wiki_keyword_raw):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `wikipedia`')
    print('------')
    cmd_trigger()
    wiki_error = "Error. Specify/ check/ rephrase your search query,"
    try:
        wiki_keyword = ' '.join(wiki_keyword_raw)
        wiki_keyword_string = wikipedia.page(wiki_keyword, auto_suggest=True, redirect=True)
        wiki_sum = wikipedia.summary(wiki_keyword_string, sentences=1, chars=100, auto_suggest=True, redirect=True)
        wiki_url = wiki_keyword_string.url
        embed_wiki = discord.Embed(title="Wikipedia", description=wiki_keyword, color=0x00ff00)
        embed_wiki.add_field(name=wiki_sum, value=wiki_url)
        await ctx.bot.say(embed=embed_wiki)
    except:
        await ctx.bot.say(f'{wiki_error} <@{ctx.message.author.id}>!')
        if not wikipedia.search(wiki_keyword, results=3):
            return
        wiki_choice = ', '.join(wikipedia.search(wiki_keyword, results=3))
        await ctx.bot.say(f'Did you mean: {wiki_choice}?')


@bot.command(pass_context=True)
async def wiktionary(ctx, *wikti_keyword_list):
    wikti_keyword_raw = " ".join(wikti_keyword_list)
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `wiktionary`')
    print('------')
    cmd_trigger()
    wiki_error = "Error. Specify/ check/ rephrase your search query,"
    parser = WiktionaryParser()
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
        await ctx.bot.say(embed=embed_wikti)
    except:
        await ctx.bot.say(f'{wiki_error} <@{ctx.message.author.id}>!')


@bot.command(pass_context=True)
async def roles(ctx):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `roles`')
    print('------')
    cmd_trigger()
    await ctx.bot.say(ctx.message.author.mention + "\'s roles are:")
    for r in ctx.message.author.roles:
        roles_me = r.name
        await ctx.bot.say("`" + roles_me + "`")


def reaction_trigger_save():
    data["COUNTER"][0]["counter_reac"] = str(reaction_trigger.counter)
    with open('config.json', 'w') as outfile:
        json.dump(data, outfile)
    reaction_trigger.counter = reaction_trigger_pull

def reaction_trigger():
    reaction_trigger.counter += 1
    if reaction_trigger.counter == int(reaction_trigger_pull) + 100:
        return reaction_trigger_save()
reaction_trigger.counter = int(reaction_trigger_pull)


def cmd_trigger_save():
    data["COUNTER"][0]["counter_cmd"] = str(cmd_trigger.Counter)
    with open('config.json', 'w') as outfile:
        json.dump(data, outfile)
    cmd_trigger.Counter = cmd_trigger_pull

def cmd_trigger():
    cmd_trigger.Counter += 1
    if cmd_trigger.Counter == int(cmd_trigger_pull) + 10:
        return cmd_trigger_save()
cmd_trigger.Counter = int(cmd_trigger_pull)


@bot.event
async def on_message(message):

    reaction_trigger()

    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message) and not message.mention_everyone:
        if any(x in message.content for x in messages.USER_GREETINGS):
            await bot.send_message(message.channel, random.choice(messages.BOT_GREETINGS))
        elif any(x in message.content for x in messages.USER_BYES):
            await bot.send_message(message.channel, random.choice(messages.BOT_BYES))
        # else:
        #     await message.add_reaction('👀')

    if 'USA' in message.content:
        await bot.add_reaction(message, random.choice(('🇺🇸', '🍔', '🌭', '🔫')))
    if 'nani' in message.content:
        await bot.send_message(message.channel, 'NAAAAANNNIIIIII!?!?!?!11')

    for t in messages.TRIGGERS:
        if t in message.content:
            for reaction in messages.TRIGGERS[t]:
                await bot.add_reaction(message, reaction)

    # message.content = message.content.lower()
    await bot.process_commands(message)


bot.run(TOKEN)
