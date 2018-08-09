#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# bot_bcad_3.6.py

import asyncio
import discord
import random
import time
import subprocess
import requests
import wikipedia
import praw
import json
import pytz # python -m pip install pytz
from datetime import datetime
from pytz import timezone 
from xml.etree import ElementTree
from discord.ext import commands

#python3 -m pip install -U discord.py
#pip install requests-xml
#pip install wikipedia
#pip install praw

#print(dir(message))
#help(obj)

# data = {}  
# data['TOKEN'] = []  
# data['TOKEN'].append({  
#     'value': 'DISCORD_BOT_TOKEN_HERE'
# })
# data['MOD_ROLES'] = []
# data['MOD_ROLES'].append({  
#     'value_1': 'ADMIN_ROLE_ID_HERE',  
#     'value_2': 'MOD_ROLEID_HERE'
# })
# data['REDDIT'] = []
# data['REDDIT'].append({
#     'client_id': 'REDDIT_CLIENT_ID_HERE',
#     'client_secret': 'REDDIT_CLIENT_SECRET_HERE',
#     'user_agent': 'REDDIT_USER_AGENT_HERE'
# })
# data['AUTHOR'] = []
# data['AUTHOR'].append({
#     'bot_author_id': 'DISCORD_BOT_AUTHER_ID_HERE'
# })
# data['GOODREADS'] = []
# data['GOODREADS'].append({
#     'goodreads_key': 'GOODREADS_KEY_HERE'
# })
# 
# with open('/home/xl4/bcad_bot/bcad_tests/data.txt', 'w') as outfile:  
#     json.dump(data, outfile)

with open('/home/xl4/bcad_bot/bcad_tests/data.txt') as json_file:  
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

TZS = {
    'UTC': timezone('Etc/GMT'),
    'GMT': timezone('Etc/GMT'),
    'ECT': timezone('Etc/GMT+5'),
    'CEST': timezone('Etc/GMT-2'),
    'BST': timezone('Etc/GMT-1'),
    'CET': timezone('Etc/GMT-1'),
    'EET': timezone('Etc/GMT-2'),
    'EEST': timezone('Etc/GMT-3'),
    'CT': timezone('Etc/GMT-3'),
    'DT': timezone('Etc/GMT-4'),
    'WST': timezone('Etc/GMT-8'),
    'WSST': timezone('Etc/GMT-9'),
    'HAST': timezone('Etc/GMT+10'),
    'SST': timezone('Etc/GMT+11'),
    'ADT': timezone('Etc/GMT+2'),
    'AST': timezone('Etc/GMT+4'),
    'EDT': timezone('Etc/GMT+4'),
    'EST': timezone('Etc/GMT+5'),
    'CDT': timezone('Etc/GMT+5'),
    'CST': timezone('Etc/GMT+6'),
    'MDT': timezone('Etc/GMT+6'),
    'MST': timezone('Etc/GMT+7'),
    'PDT': timezone('Etc/GMT+7'),
    'PST': timezone('Etc/GMT+8'),
    'ADT': timezone('Etc/GMT+8'),
    'AST': timezone('Etc/GMT+9'),
}

# ###########
# import test
# test.func()
# ##########

@bot.event
async def on_ready():
    activity = discord.Game(name="with pickles.")
    await bot.change_presence(status=discord.Status.online, game=activity)
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

# @bot.event
# async def on_member_join(ctx, member):
#     welcome = ['Welcome to my kingdom, ']
# 	string = random.choice(welcome) + str(member)
# 	await ctx.bot.say(string)
    
@bot.command(pass_context = True)
async def members(ctx):
    print('ID: '+ctx.message.author.id+' (Name: '+ctx.message.author.name+') used `members`')
    print('------')
    for r in ctx.message.author.roles:
        pulled_roles = r.id
        if pulled_roles in role_mod:
            for server in bot.servers:
                for member in server.members:
                    print(f'ID: {member.id} Name: {member} ({member.name})')
            await ctx.bot.say('List saved into logs.')
            return
    await ctx.bot.say(ctx.message.author.mention+', you\'re not a mod. You can\'t use this command.')
    print('\n')
    
@bot.command(pass_context = True)
async def info(ctx):
    print('ID: '+ctx.message.author.id+' (Name: '+ctx.message.author.name+') used `info`')
    print('------')
    embed = discord.Embed(title="Sir Henry Pickles", description="Pickles are love, pickles are life!", color=0xeee657)
    embed.add_field(name="Author", value=bot_author)
    await ctx.bot.say(embed=embed)

@bot.command(name="time", pass_context = True, ignore_extras = False)
async def cmd_time(ctx, *tz_keywords):
    tz_keyword = '_'.join(tz_keywords)
    if tz_keyword is None:
        return await ctx.bot.say("No keyword given, so here/'s UTC/GMT: " + datetime.now())
    valid_zones = []
    for zone in pytz.all_timezones:

        zones = zone.split('/')
        region = ''
        region_tz = ''
        region_city = ''
        # print(len(zones))
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
                msg =''
                for idx, _msg in enumerate(valid_zones):       
                    msg += '{}\n'.format(valid_zones[idx])
                    current_len = current_len + len(_msg)
                    try:
                        if current_len + len(valid_zones[idx + 1]) > 1950:
                            print(current_len, current_len + len(valid_zones[idx + 1]))
                            await ctx.bot.say(msg)
                            msg = ''
                            current_len = 0
                    except IndexError:
                        print("INDEX ERROR")
                        return await ctx.bot.say(msg)

                    
@bot.command(pass_context = True)
async def clear(ctx, cle: int = 1000):
    print('ID: '+ctx.message.author.id+' (Name: '+ctx.message.author.name+') used `clear` in channel: '+ctx.message.channel.name)
    print('------')
    for r in ctx.message.author.roles:
        pulled_roles = r.id
        if pulled_roles in role_mod:
            await bot.purge_from(ctx.message.channel, limit=cle+1)
            cle_num = str(cle)
            if cle == 1000:
                num_cleared = "up to 1000 messages"
            elif cle <= 0:
                num_cleared = "your message because why would you want to clear " + cle_num + " messages!?"
            elif cle == 1:
                num_cleared = "1 message"
            else:
                num_cleared = str(cle) + " messages"
            embed=discord.Embed(title="Channel has been cleared of " + num_cleared, color=0x00ff00)
            embed.set_image(url="https://cdn.discordapp.com/attachments/474903005523869715/474903418100645898/FwxbY6j.gif")
            await ctx.bot.say(embed=embed)
            return
    await ctx.bot.say(ctx.message.author.mention+', you\'re not part of ' + mention_mod + '. You can\'t use this command.')

@bot.command(pass_context = True)
async def test(ctx):
    print('ID: '+ctx.message.author.id+' (Name: '+ctx.message.author.name+') used `test`')
    print('------')
    await ctx.bot.say("successful")

@bot.command(pass_context = True)
async def mod(ctx):
    print('ID: '+ctx.message.author.id+' (Name: '+ctx.message.author.name+') used `mod`')
    print('------')
    for r in ctx.message.author.roles:
        pulled_roles = r.id
        if pulled_roles in role_mod:
            return await ctx.bot.say(ctx.message.author.mention+', you\'re a mod.')
    await ctx.bot.say(ctx.message.author.mention+', you\'re not a mod.')

@bot.command(name='help', pass_context=True)
async def cmd_help(ctx):
    member = ctx.message.author
    print('ID: '+ctx.message.author.id+' (Name: '+ctx.message.author.name+') used `help`')
    print('------')
    
    embed_cmd=discord.Embed(title="COMMANDS", description="You can call a command by typing `@Sir Henry Pickles COMMAND` or `!COMMAND`", color=0x00ff00)
    embed_cmd.add_field(name="`help`", value="Sends this per DM. It's the basic commands you can use the Bot for")
    embed_cmd.add_field(name="`info`", value="Basic information on the Bot such as name and author")
    embed_cmd.add_field(name="`test`", value="Tests if the Bot works properly. Has no other purpose")

    embed_use=discord.Embed(title="USEFUL", description="", color=0x00ff00)
    embed_use.add_field(name="`goodreads`", value="Let\'s you look for authors and books on Goodread.com. For this you can use an authors name, book title, ISBN or even all together. Example: `@Sir Henry Pickles goodreads Neil Gaiman Norse Mythology` or `!goodreads Neil Gaiman Norse Mythology`")
    embed_use.add_field(name="`reddit`", value="With this command you can let Henry post the `top 3 hot topics` of a subreddit of your choosing. Simply use `@Sir Henry Pickles reddit SUBREDDIT` or `!reddit SUBREDDIT` with `subreddit` being the subreddit of your choosing. Subreddit")
    embed_use.add_field(name="`wikipedia`", value="Let\s you search wikipedia for anything. Gives you a short summary and the link to the full article. Use with `@Sir Henry Pickles wikipedia KEYWORD` or `!wikipedia KEYWORD` with KEYWORD being what you\'re looking for")
    embed_use.add_field(name="`roll`", value="You can `roll` a dice using `2d8` with 2 being the number of dice you want the bot to roll and 8 being the number of sides the dice has. If you just want the bot to throw one dice, just put `d8`. You can add your modifier too! Simply put `2d8 3` with 3 being your modifier. Negative values do work too!")
    embed_use.add_field(name="`time`", value="Gives you the current time for different timezones. These are the possibilities: UTC, BST, CET, CEST, EET, EST, CT, DT, WST, WSST, HAST, SST, ADT, AST, EDT, EST, CDT, CST, MDT, MST, PDT, PST, ADT, AST, GMT")

    embed_mod=discord.Embed(title="MODERATION", description="", color=0x00ff00)
    embed_mod.add_field(name="`clear`", value="With this command a Moderator can clear all messages in a channel if something NSFW or otherwise inapropriate got posted. Other users can use this command aswell - it automatically pings the Moderators for them. For the last 1000 messages purged `clear`, for a certain amount `clear NUMBER` with `NUMBER` being any number between 0 and 1000")
    embed_mod.add_field(name="`bleach`", value="Applies eye bleach. *Try it!* (recommended after and/ or before `clear`)")
    embed_mod.add_field(name="`roles`", value="Shows you what roles you have")

    embed_misc=discord.Embed(title="MISC", description="", color=0x00ff00)
    embed_misc.add_field(name="`votecall`", value="Calls a simple thumb up/ thumb down vote for the message.")
    embed_misc.add_field(name="`greeting`", value="Say `Hi` to Henry! Or `Hello` or `Morning` or something like this")
    embed_misc.add_field(name="`goodbye`", value="Same as with greeting. Responds to a variety of goodbyes")
    embed_misc.add_field(name="`sleep`", value="Let\'s the Bot decide if you should go to bed")
    embed_misc.add_field(name="`shower`", value="Let\'s the Bot decide if you should take a shower")
    embed_misc.add_field(name="`joke`", value="Let Henry tell you a joke which most certainly is hilarious")
    embed_misc.add_field(name="`8ball`", value="Ask the oracle with this all time classic")
    await bot.send_message(member, 
        "If you are in need of immediate assistance, I kindly suggest you to call the emergency services.\n"
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

@bot.command(pass_context = True)
async def sleep(ctx):
    print('ID: '+ctx.message.author.id+' (Name: '+ctx.message.author.name+') used `sleep`')
    print('------')
    sleep = ['Yes, you should use the sleep.', 'But mooooom idonwanna!', 'Whatevs, man.', 'JA!']
    await ctx.bot.say(random.choice(sleep))

@bot.command(pass_context = True)
async def shower(ctx):
    print('ID: '+ctx.message.author.id+' (Name: '+ctx.message.author.name+') used `shower`')
    print('------')
    shower = [' you reek already!', ' it`s about time...', ' nah, its cool.', ' I mean, have you already showered this week?',' but only a golden shower.']
    await ctx.bot.say(ctx.message.author.mention+ " " + random.choice(shower))

@bot.command(pass_context = True)
async def joke(ctx):
    print('ID: '+ctx.message.author.id+' (Name: '+ctx.message.author.name+') used `joke`')
    print('------')
    joke = [
        'I always get pickle and chutney mixed up.\n'
        'It makes me chuckle.',

        'What do you call a lazy dill?\n'
        'A shirkin\' gherkin.',

        'Why don\'t pickles laugh at Hebrew jokes?\n'
        'It\'s not kosher.',

        'When the giant cannibals started to soak me in vinegar, I\'d had enough.\n'
        '"Why don\'t you pickle someone your own size?" I shouted.',

        'What\'s green and sour and swims in an aquarium?\n'
        'A tro-pickle fish.',

        'What\'s green and got two wheels?\n'
        'A motorpickle.',

        'I walked into the kitchen today to find my blonde wife looking very confused while holding a jar of pickle.\n'
        '"What\'s wrong?" I asked her.\n'
        'She replied "This jar of pickle says to store it in a cool, dark location."\n'
        'I said, "Okay, how about in the fridge?"\n'
        'She said "No, silly, there\'s a little light inside."',

        'What do you call a pickle lullaby?\n'
        'A cucumber slumber number.',

        'Why are pickles in sandwiches always so polite?\n'
        'They\'re well-bread.',

        'This guy had devoted his whole working life to his job in a pickle factory.\n'
        'Then one day he got home from work and told his wife he\'d been fired from his job.\n'
        'She was very upset at this and angry at the company he\'d worked for, shouting, "You\'ve given that firm twenty years of devoted service. Why the hell did they fire you?"\n'
        'The guy explained, "For the whole twenty years I worked there I\'ve been tempted to stick my John Thomas in the pickle slicer and today I finally did it!"\n'
        'The wife screamed in horror and ran over to her husband. Then she pulled his pants down to see what damage had been done.\n'
        'She let out a big sigh of relief. "You look okay" she said, "So what happened to the pickle slicer?"\n'
        'The guy said, "They fired her, too."',

        'What\'s a baby gherkin\'s favorite TV channel?\n'
        'Pickleodeon.',

        'What do you call a pickle you got at a cheap price?\n'
        'A sweet dill.',

        'I recently got a new job as a golf caddy, but I was fired after less than an hour.\n'
        'The guy asked me for a sand wedge.\n'
        'I don\'t think he likes pickle.',

        'Why shouldn\'t you shoot pool using a pickle?\n'
        'Because you\'ll find the cue cumbersome.',

        'What do you get when you cross a pickle with an alligator?\n'
        'A crocodill.',

        'On what radio station would you hear Bob Dill-on?\n'
        'Vlasic rock.',

        'I\'ve been feeling really down recently so I thought I\'d cheer myself up by making a nice cheese and pickle sandwich.\n'
        'But when I picked up the pickle jar, it said "reject if depressed", so now I\'m off to take an overdose.',

        'What do you call a pickle doctor?\n'
        'A dill pusher.',

        'I\'ve just got my hand stuck in a jar of gherkins and I can\'t get it out.\n'
        'I\'m in a right pickle!',

        'Why do gherkins giggle when you touch them?\n'
        'They\'re pickle-ish.',

        'What did the pickle say when he was told he was going in to a salad?\n'
        'I relish the thought.',

        'If Santa had sex with a pickle, what would they call their baby?\n'
        'Claussen.',

        'What\'s green and pecks on trees?\n'
        'Woody Wood Pickle.',

        'What do you do when a pickle wants to play cards?\n'
        'Dill\'em in.',

        'This guy makes a small math error on a report he\'s written. His boss is mad and tries to belittle him in front of his peers.\n'
        'She shouts angrily, "If you had 4 pickles and I asked for one, how many would you have left?"\n'
        'The guy replies, "If it was you who asked, I\'d still have 4 pickles."',

        'What\'s green and swims in the sea?\n'
        'Moby Pickle.',

        'What\'s the difference between a pickle and a psychiatrist?\n'
        'If you don\'t know, you ought to stop talking to your pickle!',

        'What do you call a pickle that got run over on the road?\n'
        'Road dill.',

        'Who\'s a pickle\'s favorite artist?\n'
        'Salvador Dilli.',

        'What\'s green and wears a cape?\n'
        'Super Pickle.',

        'What did the arrogant pickle say?\n'
        'I\'m kind of a big dill.',

        'What\'s a pickle\'s favorite book?\n'
        'To Dill A Mockingbird.',

        'Why is the pickle container always open?\n'
        'Because it\'s ajar.',
        
        'Where\'s a pickle\'s favorite place to go in London?\n'
        'Pickle-dilly Square.',

        'What do you call a pickle from the southern backwoods.\n'
        'A hill-dilly.',

        'What\'s a pickle\'s life philosophy?\n'
        'Never a dill moment.',

        'What did the pickle say to the cat?\n'
        'Nothing, pickles can\'t talk.',

        ]
    await ctx.bot.say(random.choice(joke))

@bot.command(name='8ball', pass_context = True)
async def cmd_8ball(ctx):
    print('ID: '+ctx.message.author.id+' (Name: '+ctx.message.author.name+') used `8ball`')
    print('------')
    ball_res = ['It is certain.', 'It is decidedly so.', 'Without a doubt.', 'Yes - definitely.', 'You may rely on it.', 'As I see it, yes.', 'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.', 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.', 'Connot predict now.', 'Concentrate and ask again.', 'Don`t count on it.', 'My reply is no.', 'My sources say no.', 'Outlook not so good.']
    await ctx.bot.say(random.choice(ball_res))

@bot.command(pass_context = True)
async def roll(ctx, dice_string, mod: int = 0):
    print('ID: '+ctx.message.author.id+' (Name: '+ctx.message.author.name+') used `roll`')
    print('------')
    try:
        count_raw, num_raw = dice_string.split("d")
        if not count_raw:
            count_raw = 1
        count = int(count_raw)
        num = int(num_raw)
        await ctx.bot.say("Rolling "+ str(count) +" d"+ str(num) +" ...")
        await asyncio.sleep( 2 )
        random.seed()
        numbers = []
        for count in range(count):
            number = random.randint(1,num)
            numbers.append(number)
        num_ran_count = (sum(numbers))
        if mod == 0:
            await ctx.bot.say("I rolled a "+ str(num_ran_count) + " for you.")
        else:
            num_ran_count_mod = num_ran_count+mod
            await ctx.bot.say("I rolled "+ str(num_ran_count) + " for you. That\'s a " + str(num_ran_count_mod) + " with your modifier.")
    except:
        await ctx.bot.say(f'Error. Something didn\'t work out, <@{ctx.message.author.id}>. Check your formatting. Was it: `4d12 3`?')

@bot.command(pass_context = True)
async def bleach(ctx):
    print('ID: '+ctx.message.author.id+' (Name: '+ctx.message.author.name+') used `bleach`')
    print('------')
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

# TIP System
# Karma System

# #google calendar
# @bot.command()
# async def cal(ctx):
#     ctx.bot.say()

@bot.command(pass_context = True)
async def goodreads(ctx, *keyword_raw):
    print('ID: '+ctx.message.author.id+' (Name: '+ctx.message.author.name+') used `goodreads`')
    print('------')
    keyword = str(keyword_raw)
    xml = ElementTree.fromstring(
        requests.get('https://www.goodreads.com/search.xml?key=' + goodreads_key + '&q=' + keyword + '&page=1').text)

    for i,v in enumerate(xml.find('search/results')):
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
    print('ID: '+ctx.message.author.id+' (Name: '+ctx.message.author.name+') used `reddit`, looking for the subreddit: `'+subreddit_input+'`')
    print('------')
    x = int(0)
    try:
        for i, submission in enumerate(reddit.subreddit(subreddit_input).hot(limit=5)):
            if submission.over_18:
                await ctx.bot.say("Please do not request NSFW results. "+mention_mod)
                break
            if submission.stickied:
                continue  
            result_list = (f'{submission.url}')
            if not submission.over_18 and not submission.stickied:
                await ctx.bot.say(result_list)
                x = int(x + 1 )
                if x == 3:
                    break
    except:
       await ctx.bot.say(f'Error. Something didn\'t work out. Search for somthing else or some time else, <@{ctx.message.author.id}>')

@bot.command(name='wikipedia', pass_context = True)
async def cmd_wikipedia(ctx, *wiki_keyword_raw):
    wiki_error = "Error. Specify/ check/ rephrase your search query"
    try:
        wiki_keyword = str(wiki_keyword_raw)
        wiki_keyword_clean = str(*wiki_keyword_raw)
        wiki_sum = wikipedia.summary(wiki_keyword, sentences=1, chars=100,auto_suggest=True, redirect=True)
        wiki_keyword_string = wikipedia.page(wiki_keyword)
        wiki_url = wiki_keyword_string.url
        embed_wiki=discord.Embed(title="Wikipedia", description=wiki_keyword_clean, color=0x00ff00)
        embed_wiki.add_field(name=wiki_sum, value=wiki_url)    
        await ctx.bot.say(embed=embed_wiki)
    #except wikipedia.exceptions.DisambiguationError:
    except:
        await ctx.bot.say(f'{wiki_error} <@{ctx.message.author.id}>')
    except wikipedia.exceptions.PageError:
        await ctx.bot.say(f'{wiki_error} <@{ctx.message.author.id}>')
    except wikipedia.exceptions.HTTPTimeoutError:
        await ctx.bot.say(f'{wiki_error} <@{ctx.message.author.id}>')
    except wikipedia.exceptions.RedirectError:
        await ctx.bot.say(f'{wiki_error} <@{ctx.message.author.id}>')
    except wikipedia.exceptions.WikipediaException:
        await ctx.bot.say(f'{wiki_error} <@{ctx.message.author.id}>')

##Movie Knights
# https://i.imgur.com/QNiL6SP.gif
# https://i.imgur.com/GDNyuPn.mp4
# https://i.imgur.com/DKJhx9l.gif

@bot.command(pass_context = True)
async def roles(ctx):
    print('ID: '+ctx.message.author.id+' (Name: '+ctx.message.author.name+') used `roles`')
    print('------')
    await ctx.bot.say(ctx.message.author.mention + "\'s roles are:")
    for r in ctx.message.author.roles:
        roles_me = r.name
        await ctx.bot.say("`"+roles_me+"`")

@bot.event
async def on_message(message):
    greeting = ['hello', 'hi', 'hey', 'greetings', 'sup', 'morning']
    greeting_res = ['Quite the *lingo* of the youth, eh? Hi to you too!','I bid you pickly greetings!', 'Sup brooooooo. Or sis, idc. <3', 'Shama-Lama-Ding-Dong right back at you!', 'hi', 'hey', 'greetings', 'sup']
    bye = ['bye', 'see you', 'see ya', 'cya', 'nite', 'good night']
    bye_res = ['Farewell!', 'bye', 'see you', 'see ya', 'cya', 'nite']
    usa_reac = ['🇺🇸', '🍔', '🌭', '🔫']
    str_mcl = message.content.lower()

    if message.author == bot.user:
        return

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
    if 'facepalm'  in message.clean_content.lower():
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

    await bot.process_commands(message)

bot.run(TOKEN)
