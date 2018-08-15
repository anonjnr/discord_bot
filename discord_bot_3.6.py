#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# bot_bcad_3.6.py

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

with open('credentials.log') as json_file:
    data = json.load(json_file)
    for p in data['TOKEN']:
        TOKEN = p['value']
    for p in data['MOD_ROLES']:
        mod_role_1 = p['value_1']
        mod_role_2 = p['value_2']
    for p in data['REDDIT']:
        json_client_id = p['client_id']
        json_client_secret = p['client_secret']
        json_user_agent = p['user_agent']
    for p in data['AUTHOR']:
        json_bot_author_id = p['bot_author_id']
    for p in data['GOODREADS']:
        goodreads_key = p['goodreads_key']

description = 'Sir Henry Pickles, the pickly Bot!'
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'))
bot.remove_command('help')
role_mod = [mod_role_1, mod_role_2]
mention_mod = '<@&' + mod_role_1 + '>'
reddit = praw.Reddit(client_id=json_client_id, client_secret=json_client_secret, user_agent=json_user_agent)
bot_author = str("<@!" + json_bot_author_id + ">")
random.seed(a=None)
start_time = time.time()


# temp = (os.popen("vcgencmd measure_temp").readline().replace("temp=","").replace("'C","")) #RASPI

async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()


@bot.event
async def on_ready():
    activity = discord.Game(name="with pickles.")
    await bot.change_presence(status=discord.Status.online, game=activity)
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command(pass_context=True)
async def status(ctx, *status_raw):
    for r in ctx.message.author.roles:
        pulled_roles = r.id
        if pulled_roles in role_mod:
            status_arg = ' '.join(status_raw)
            activity = discord.Game(name=status_arg)
            await bot.change_presence(status=discord.Status.online, game=(activity))
            embed = discord.Embed(title="Status changed to: ", description=("@Sir Henry Pickles playing " + status_arg),
                                  color=0xeee657)
            return await ctx.bot.say(embed=embed)
    return await ctx.bot.say(ctx.message.author.mention + ', you\'re not a mod. You can\'t use this command.')


# todo
# @bot.event
# async def on_command_error(ctx, error):
#     await ctx.bot.say("What now," + ctx.message.author.mention + "?")

# todo
# ###########
# import test
# test.func()
# ##########

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

@bot.event
async def on_member_join(member):
    print("gets called")
    member = ctx.message.author
    welm = (f"Welcome to `{member.server}`!")
    desm = (f'Enjoy the server. Type `!help` so learn all my commands.\n Now go and have some fun, <@!{member.id}> <3')
    if channel.name is "general":
        print("channel is general")
        embed = discord.Embed(title=welm, description=desm, color=0xeee657)
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        await ctx.bot.say(embed=embed)
    else:
        return


# todo 2000 char restriciton (time)
@bot.command(pass_context=True)
async def members(ctx):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `members`')
    print('------')
    info.counter += 1
    for r in ctx.message.author.roles:
        pulled_roles = r.id
        if pulled_roles in role_mod:
            try:
                await memberList.membersLog(ctx)
            except:
                await ctx.bot.say('Whoops, something went wrong ' + ctx.message.author.mention + '.')
            return
    await ctx.bot.say(ctx.message.author.mention + ', you\'re not a mod. You can\'t use this command.')


@bot.command(pass_context=True)
async def members_show(ctx):
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `members_show`')
    print('------')
    info.counter += 1
    for r in ctx.message.author.roles:
        pulled_roles = r.id
        if pulled_roles in role_mod:
            try:
                await memberList.membersDump(ctx)
            except:
                await ctx.bot.say('Whoops, something went wrong ' + ctx.message.author.mention + '.')
            return
    await ctx.bot.say(ctx.message.author.mention + ', you\'re not a mod. You can\'t use this command.')


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
    # embed.add_field(name="Henrys Temperature: ", value=(temp + " °C")) #RASPI
    embed.add_field(name="Command count: ", value=info.counter)
    embed.add_field(name="Message count: ", value=reaction_trigger.counter)
    embed.add_field(name="Server count: ", value=len(bot.servers))
    embed.add_field(name="Author", value=bot_author)
    embed.add_field(name="Next features I'll get and progress:",
                    value="https://github.com/x3l51/discord_bot/projects/1#column-3212654", inline=True)
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
async def clear(ctx, cle: int = 1000):
    print(
        'ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `clear` in channel: ' + ctx.message.channel.name)
    print('------')
    info.counter += 1
    for r in ctx.message.author.roles:
        pulled_roles = r.id
        if pulled_roles in role_mod:
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
    await ctx.bot.say(
        ctx.message.author.mention + ', you\'re not part of ' + mention_mod + '. You can\'t use this command.')


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
    info.counter += 1
    for r in ctx.message.author.roles:
        pulled_roles = r.id
        if pulled_roles in role_mod:
            return await ctx.bot.say(ctx.message.author.mention + ', you\'re a mod.')
    await ctx.bot.say(ctx.message.author.mention + ', you\'re not a mod.')


@bot.command(name='help', pass_context=True)
async def cmd_help(ctx):
    member = ctx.message.author
    print('ID: ' + ctx.message.author.id + ' (Name: ' + ctx.message.author.name + ') used `help`')
    print('------')
    info.counter += 1

    embed_cmd = discord.Embed(title="COMMANDS",
                              description="You can call a command by typing `@Sir Henry Pickles COMMAND` or `!COMMAND`",
                              color=0x00ff00)
    embed_cmd.add_field(name="`help`", value="Sends this per DM. It's the basic commands you can use the Bot for")
    embed_cmd.add_field(name="`info`", value="Basic information on the Bot such as name and author")
    embed_cmd.add_field(name="`test`", value="Tests if the Bot works properly. Has no other purpose")

    embed_use = discord.Embed(title="USEFUL", description="", color=0x00ff00)
    embed_use.add_field(name="`goodreads`",
                        value="Let\'s you look for authors and books on Goodread.com. For this you can use an authors name, book title, ISBN or even all together. Example: `@Sir Henry Pickles goodreads Neil Gaiman Norse Mythology` or `!goodreads Neil Gaiman Norse Mythology`")
    embed_use.add_field(name="`reddit`",
                        value="With this command you can let Henry post the `top 3 hot topics` of a subreddit of your choosing. Simply use `@Sir Henry Pickles reddit SUBREDDIT` or `!reddit SUBREDDIT` with `subreddit` being the subreddit of your choosing. Subreddit")
    embed_use.add_field(name="`wikipedia`",
                        value="Let\'s you search wikipedia for anything. Gives you a short summary and the link to the full article. Use with `@Sir Henry Pickles wikipedia KEYWORD` or `!wikipedia KEYWORD` with KEYWORD being what you\'re looking for")
    embed_use.add_field(name="`wiktionary`",
                        value="Let\'s you search wiktionary for anything. Basicalle the same as `Wikipedia` but only for word definition")
    embed_use.add_field(name="`roll`",
                        value="You can `roll` a dice using `2d8` with 2 being the number of dice you want the bot to roll and 8 being the number of sides the dice has. If you just want the bot to throw one dice, just put `d8`. You can add your modifier too! Simply put `2d8 3` with 3 being your modifier. Negative values do work too!")
    embed_use.add_field(name="`time`",
                        value="Gives you the current time for different timezones. For example use with `!time Berlin` or `!time EST`.")

    embed_mod = discord.Embed(title="MODERATION", description="", color=0x00ff00)
    embed_mod.add_field(name="`clear`",
                        value="With this command a Moderator can clear all messages in a channel if something NSFW or otherwise inapropriate got posted. Other users can use this command aswell - it automatically pings the Moderators for them. For the last 1000 messages purged `clear`, for a certain amount `clear NUMBER` with `NUMBER` being any number between 0 and 1000")
    embed_mod.add_field(name="`bleach`",
                        value="Applies eye bleach. *Try it!* (recommended after and/ or before `clear`)")
    embed_mod.add_field(name="`roles`", value="Shows you what roles you have")
    embed_mod.add_field(name="`status`",
                        value="Change the status of the bot. `!status the guitar` to have his status changed to: `@Sir Henry Pickles Playing the guitar`")

    embed_misc = discord.Embed(title="MISC", description="", color=0x00ff00)
    embed_misc.add_field(name="`votecall`", value="Calls a simple thumb up/ thumb down vote for the message.")
    embed_misc.add_field(name="`greeting`",
                         value="Say `Hi` to Henry! Or `Hello` or `Morning` or something like this. `@Sir Henry Pickles Sup`")
    embed_misc.add_field(name="`goodbye`",
                         value="Same as with greeting. Responds to a variety of goodbyes. `@Sir Henry Pickles Nite`")
    embed_misc.add_field(name="`sleep`", value="Let\'s the Bot decide if you should go to bed")
    embed_misc.add_field(name="`shower`", value="Let\'s the Bot decide if you should take a shower")
    embed_misc.add_field(name="`joke`", value="Let Henry tell you a joke which most certainly is hilarious")
    embed_misc.add_field(name="`8ball`", value="Ask the oracle with this all time classic")
    await bot.send_message(member,
                           "If you are in need of immediate assistance, I kindly suggest you to call the emergency "
                           "services.\n "
                           "\n"
                           "----------\n"
                           "\n"
                           "**Name**: Sir Henry Pickles\n"
                           "**Description:** *Does his best.*\n"
                           )
    await bot.send_message(member, embed=embed_cmd)
    await bot.send_message(member, embed=embed_use)
    await bot.send_message(member, embed=embed_mod)
    await bot.send_message(member, embed=embed_misc)
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
    eye_bleach = [
        'https://imgur.com/gallery/O1busfY',
        'https://i.imgur.com/cQBeAjw.mp4',
        'https://i.imgur.com/p40Hwwi.jpg',
        'https://i.imgur.com/Onyvdgh.mp4',
        'https://i.imgur.com/bGtlZbl.jpg',
        'https://i.imgur.com/kTmRulV.jpg',
        'https://i.imgur.com/lmnpp5K.mp4',
        'https://i.imgur.com/fcRvoJn.jpg',
        'https://i.imgur.com/07lceng.mp4',
        'https://i.imgur.com/J1EPxUk.jpg',
        'https://i.imgur.com/JxO5seE.jpg',
        'https://i.imgur.com/ViNjAKD.mp4',
        'https://i.imgur.com/vpDxduH.jpg',
        'https://i.imgur.com/ngTloKH.jpg',
        'https://i.imgur.com/IiMIW1h.jpg',
        'https://i.imgur.com/aC8xiz5.mp4',
        'https://i.imgur.com/rq56D4o.jpg',
        'https://i.imgur.com/wwOM7kU.mp4',
        'https://i.imgur.com/cXP94NP.mp4',
        'https://i.imgur.com/10b9Y12.mp4',
        "https://i.imgur.com/KnXrY6R.jpg",
        "https://imgur.com/gallery/u61qJad"
    ]
    await ctx.bot.say(random.choice(eye_bleach))


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
                await ctx.bot.say("Please do not request NSFW results. " + mention_mod)
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
        wiki_keyword = str(' '.join(wiki_keyword_raw))
        wiki_sum = wikipedia.summary(wiki_keyword, sentences=1, chars=100, auto_suggest=True, redirect=True)
        wiki_keyword_string = wikipedia.page(wiki_keyword)
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


reaction_trigger.counter = 0


@bot.event
async def on_message(message):
    greeting = ['hello', 'hi', 'hey', 'greetings', 'sup', 'morning']
    greeting_res = ['Quite the *lingo* of the youth, eh? Hi to you too!', 'I bid you pickly greetings!',
                    'Sup brooooooo. Or sis, idc. <3', 'Shama-Lama-Ding-Dong right back at you!', 'hi', 'hey',
                    'greetings', 'sup']
    bye = ['bye', 'see you', 'see ya', 'cya', 'nite', 'good night']
    bye_res = ['Farewell!', 'bye', 'see you', 'see ya', 'cya', 'nite']
    usa_reac = ['🇺🇸', '🍔', '🌭', '🔫']
    str_mcl = message.content.lower()

    if message.author == bot.user:
        return

    if any:
        if bot.user.mentioned_in(message) and not message.mention_everyone:
            if any(x in str_mcl for x in greeting):
                await bot.send_message(message.channel, random.choice(greeting_res))
            elif any(x in str_mcl for x in bye):
                await bot.send_message(message.channel, random.choice(bye_res))
            # else:
            #     await message.add_reaction('👀')
        if 'votecall' in message.clean_content.lower():
            await bot.add_reaction(message, '👍')
            await bot.add_reaction(message, '👎')
        if 'usa' in message.clean_content.lower():
            await bot.add_reaction(message, random.choice(usa_reac))
        if 'australia' in message.clean_content.lower():
            await bot.add_reaction(message, '🇦🇺')
        if 'mexico' in message.clean_content.lower():
            await bot.add_reaction(message, '🌮')
        if 'ireland' in message.clean_content.lower():
            await bot.add_reaction(message, '🇮🇪')
        if 'scotland' in message.clean_content.lower():
            await bot.add_reaction(message, '🏴')
        if 'europe' in message.clean_content.lower():
            await bot.add_reaction(message, '🇪🇺')
        if 'germany' in message.clean_content.lower():
            await bot.add_reaction(message, '🇩🇪')
        if 'united kingdom' in message.clean_content.lower():
            await bot.add_reaction(message, '🇬🇧')
        if 'facepalm' in message.clean_content.lower():
            await bot.add_reaction(message, '🤦')
        if 'canada' in message.clean_content.lower():
            await bot.add_reaction(message, '🇨🇦')
        if 'sweden' in message.clean_content.lower():
            await bot.add_reaction(message, '🇸🇪')
        if 'norway' in message.clean_content.lower():
            await bot.add_reaction(message, '🇳🇴')
        if 'finland' in message.clean_content.lower():
            await bot.add_reaction(message, '🇫🇮')
        if 'sleep' in message.clean_content.lower():
            await bot.add_reaction(message, '💤')
        if 'sushi' in message.clean_content.lower():
            await bot.add_reaction(message, '🍣')
        if 'shower' in message.clean_content.lower():
            await bot.add_reaction(message, '🚿')
        if 'love' in message.clean_content.lower():
            await bot.add_reaction(message, '💓')
        if 'goodest robot' in message.clean_content.lower():
            await bot.add_reaction(message, '🤖')
            await bot.add_reaction(message, '🇮')
            await bot.add_reaction(message, '🇦')
            await bot.add_reaction(message, '🇲')
        if 'nani' in message.clean_content.lower():
            await bot.send_message(message.channel, 'NAAAAANNNIIIIII!?!?!?!11')

    reaction_trigger()

    await bot.process_commands(message)


bot.run('NDc5MzA2ODU5MTY2MTcxMTM2.DlYTLQ.DyLfIkjztb6H2xzXFSqoV71Lf84')
