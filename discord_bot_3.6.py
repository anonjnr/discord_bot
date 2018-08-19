#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# bot_bcad_3.6.py

import os
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
            welm = (f"Welcome to `{server}`!")
            desm = (
                f'Enjoy the server. Type `!help` so learn all my commands.\n Now go and have some fun, {member.mention} <3')
            embed = discord.Embed(title=welm, description=desm, color=0xeee657)
            embed.set_thumbnail(url=member.avatar_url)
            return await bot.send_message(channel, embed=embed)


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
async def suggestion(ctx):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `suggestion`')
    print('------')
    try:
        for channel in ctx.message.server.channels:
            if channel.name == 'suggestions':
                embed = discord.Embed(title="Suggestion Author", description=ctx.message.author.name, color=0xeee657)
                embed.add_field(name="Suggestion Message", value=ctx.message.content)
                return await bot.send_message(channel, embed=embed)
    except:
        return


@bot.command(pass_context=True)
async def prefix(ctx, prefix_raw):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `prefix`') # TODO cmd auto grab
    print('------')
    if ctx.message.author.server_permissions.administrator:
        try:
            with open('config.json', 'r') as json_file:
                data = json.load(json_file)    
                for p in data ['PREFIX']:
                    prefix_choice = p['prefix']
                    if prefix_raw == "show":
                        return await ctx.bot.say("Actual prefix is: " + prefix_choice)
                    else:
                        data["PREFIX"][0]["prefix"] = prefix_raw
                        with open('config.json', 'w') as outfile:
                            json.dump(data, outfile)
                            bot.command_prefix = commands.when_mentioned_or(prefix_raw)
                            return await ctx.bot.say("Prefix successfully set.")
        except IndexError:
            return await ctx.bot.say("Index error when grabbing first obj")
    else:
        return await ctx.bot.say(ctx.message.author.mention + ', you\'re not a mod. You can\'t use this command.')


@bot.command(pass_context=True)
async def status(ctx, *status_raw):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `status`')
    print('------')
    if ctx.message.author.server_permissions.administrator:
        status_arg = ' '.join(status_raw)
        activity = discord.Game(name=status_arg)
        await bot.change_presence(status=discord.Status.online, game=(activity))
        embed = discord.Embed(title="Status changed to: ", description=("@Sir Henry Pickles playing " + status_arg),
                            color=0xeee657)
        return await ctx.bot.say(embed=embed)
    else:
        return await ctx.bot.say(ctx.message.author.mention + ', you\'re not a mod. You can\'t use this command.')


# todo
# @bot.event
# async def on_command_error(ctx, error):
#     await ctx.bot.say("What now," + ctx.message.author.mention + "?")

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
    info.counter += 1
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
    info.counter += 1
    if ctx.message.author.server_permissions.administrator:
        try:
            await memberList.membersDump(ctx)
        except:
            await ctx.bot.say('Whoops, something went wrong ' + ctx.message.author.mention + '.')
        return
    else:
        return await ctx.bot.say(ctx.message.author.mention + ', you\'re not a mod. You can\'t use this command.')


@bot.command(pass_context=True)
async def info(ctx):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `info`')
    print('------')
    info.counter += 1
    time_lapsed = (time.time() - start_time)
    embed = discord.Embed(title="Sir Henry Pickles", description="Pickles are love, pickles are life!", color=0xeee657)
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.add_field(name="System Time:", value=utilities.epoch_to_custom_date(utilities.FMT_TIME))
    embed.add_field(name="Uptime", value=timedelta(seconds=time_lapsed))
    # embed.add_field(name="Henrys Temperature: ", value=(os.popen("vcgencmd measure_temp").readline().replace("temp=","").replace("'C",""))) #RASPI
    embed.add_field(name="Command count: ", value=info.counter)
    embed.add_field(name="Message count: ", value=reaction_trigger.counter)
    embed.add_field(name="Server count: ", value=len(bot.servers))
    embed.add_field(name="Author", value="<@!410406332143763466>")
    embed.add_field(name="GitHub:", value="https://github.com/x3l51/discord_bot", inline=True)
    embed.add_field(name="Next features I'll get and progress on me:",
                    value="https://github.com/x3l51/discord_bot/projects/1", inline=True)
    embed.add_field(name="Direct invite to the Developers Discord:", value="https://discordapp.com/invite/5raBJUU",
                    inline=True)
    await ctx.bot.say(embed=embed)


info.counter = 0


@bot.command(name="time", pass_context=True, ignore_extras=False)
async def cmd_time(ctx, *tz_keywords):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `time`')
    print('------')
    info.counter += 1
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
    info.counter += 1
    log_path = ("./logs/archive" + "-server-" + ctx.message.server.name + "-channel-" + ctx.message.channel.name + "-" + (utilities.epoch_to_custom_date(utilities.FMT_TIME_FILE)) + ".log")
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
    info.counter += 1
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
    info.counter += 1
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
    info.counter += 1

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
    info.counter += 1
    sleep = ['Yes, you should use the sleep.', 'But mooooom idonwanna!', 'Whatevs, man.', 'JA!']
    await ctx.bot.say(random.choice(sleep))


@bot.command(pass_context=True)
async def shower(ctx):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `shower`')
    print('------')
    info.counter += 1
    shower = [' you reek already!', ' it`s about time...', ' nah, its cool.',
              ' I mean, have you already showered this week?', ' but only a golden shower.']
    await ctx.bot.say(ctx.message.author.mention + " " + random.choice(shower))


# todo store jokes in json.log
@bot.command(pass_context=True)
async def joke(ctx):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `joke`')
    print('------')
    info.counter += 1

    embed = discord.Embed(title="Joke", description=random.choice(messages.JOKES), color=0x00ff00)
    await ctx.bot.say(embed=embed)


@bot.command(name='8ball', pass_context=True)
async def cmd_8ball(ctx):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `8ball`')
    print('------')
    info.counter += 1
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
    info.counter += 1
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
    info.counter += 1

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
    info.counter += 1
    keyword = str(keyword_raw)
    async with aiohttp.ClientSession() as session:
        html = await fetch(session,
                           'https://www.goodreads.com/search.xml?key=' + goodreads_key + '&q=' + keyword + '&page=1')
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
    info.counter += 1
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
    info.counter += 1
    wiki_error = "Error. Specify/ check/ rephrase your search query,"
    try:
        print(wiki_keyword_raw)
        wiki_keyword = ' '.join(wiki_keyword_raw)
        print(wiki_keyword)
        wiki_sum = wikipedia.summary(wiki_keyword, sentences=1, chars=100, auto_suggest=True, redirect=True)
        wiki_keyword_string = wikipedia.page(wiki_keyword)
        print(wiki_keyword_string)
        wiki_url = wiki_keyword_string.url
        embed_wiki = discord.Embed(title="Wikipedia", description=wiki_keyword, color=0x00ff00)
        embed_wiki.add_field(name=wiki_sum, value=wiki_url)
        await ctx.bot.say(embed=embed_wiki)
    except:
        await ctx.bot.say(f'{wiki_error} <@{ctx.message.author.id}>!')
        if not wikipedia.search(wiki_keyword, results=3):
            return
        await ctx.bot.say(f'Did you mean: {wikipedia.search(wiki_keyword, results=3)}?')


@bot.command(pass_context=True)
async def wiktionary(ctx, *wikti_keyword_list):
    wikti_keyword_raw = " ".join(wikti_keyword_list)
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `wiktionary`')
    print('------')
    info.counter += 1
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
    info.counter += 1
    await ctx.bot.say(ctx.message.author.mention + "\'s roles are:")
    for r in ctx.message.author.roles:
        roles_me = r.name
        await ctx.bot.say("`" + roles_me + "`")


# todo get rid of all these and somehow call them somehow else
# reaction is triggered on EVERY message :S
def reaction_trigger():
    reaction_trigger.counter += 1
    # if reaction_trigger.counter == 100:
    #     open json
    #     save


reaction_trigger.counter = 0


@bot.event
async def on_message(message):
    content_lower = message.content.lower()

    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message) and not message.mention_everyone:
        if any(x in content_lower for x in messages.USER_GREETINGS):
            await bot.send_message(message.channel, random.choice(messages.BOT_GREETINGS))
        elif any(x in content_lower for x in messages.USER_BYES):
            await bot.send_message(message.channel, random.choice(messages.BOT_BYES))
        # else:
        #     await message.add_reaction('👀')

    if 'usa' in content_lower:
        await bot.add_reaction(message, random.choice(('🇺🇸', '🍔', '🌭', '🔫')))
    if 'nani' in content_lower:
        await bot.send_message(message.channel, 'NAAAAANNNIIIIII!?!?!?!11')

    for t in messages.TRIGGERS:
        if t in content_lower:
            for reaction in messages.TRIGGERS[t]:
                await bot.add_reaction(message, reaction)

    reaction_trigger()

    await bot.process_commands(message)


bot.run(TOKEN)
