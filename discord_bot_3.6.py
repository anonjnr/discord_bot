#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import asyncio
import discord
import random
import time
import subprocess
import urllib.request
import requests
from xml.etree import ElementTree
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot

#python3 -m pip install -U discord.py
#pip install requests-xml

#print(dir(message))
#help(obj)

TOKEN = 'TOKENGOESHERE'

description = '''Sir Henry Pickles, the pickly Bot!'''
bot = commands.Bot(command_prefix=commands.when_mentioned)
bot.remove_command('help')
role_mod = ['468826620648620042', '475322910635065345']
mention_mod = '<@&475322910635065345>'

@bot.event
async def on_ready():
    activity = discord.Game(name="with pickles.")
    await bot.change_presence(status=discord.Status.online, game=activity)
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(pass_context=True)
async def members(ctx):
    for r in ctx.message.author.roles:
        pulled_roles = r.id
        if pulled_roles in role_mod:
            for server in bot.servers:
                for member in server.members:
                    await ctx.bot.say(member)
            return
    await ctx.bot.say(ctx.message.author.mention+', you\'re not a mod. You can\'t use this command.')

@bot.command(pass_context=True)
async def info(ctx):
    embed = discord.Embed(title="Sir Henry Pickles", description="Pickles are love, pickles are life!", color=0xeee657)
    embed.add_field(name="Author", value='<@!410406332143763466>')
    await ctx.bot.say(embed=embed)

@bot.command(pass_context=True)
async def gmt(ctx):
    t = time.gmtime()
    await ctx.bot.say("Actual time GMT: " + time.asctime(t))

@bot.command(pass_context = True)
async def clear(ctx, cle: int = 1000):
    for r in ctx.message.author.roles:
        pulled_roles = r.id
        if pulled_roles in role_mod:
            #await ctx.channel.purge(limit=cle+1)
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
    await ctx.bot.say(ctx.message.author.mention+', you\'re part of ' + mention_mod + '. You can\'t use this command.')

@bot.command(pass_context=True)
async def test(ctx):
    await ctx.bot.say("successful")
    print(ctx.message.author.mention+" used *test*.")
    print('------')

@bot.command(pass_context=True)
async def mod(ctx):
    for r in ctx.message.author.roles:
        pulled_roles = r.id
        if pulled_roles in role_mod:
            return await ctx.bot.say(ctx.message.author.mention+', you\'re a mod.')
    await ctx.bot.say(ctx.message.author.mention+', you\'re not a mod.')

@bot.command(name='help', pass_context=True)
async def cmd_help(ctx):
    await ctx.bot.say(
        "If you are in need of immediate assistance, I kindly suggest you to call the emergency services.\n"
        "\n"
        "----------\n"
        "\n"
        "**Name**: Sir Henry Pickles\n"
        "**Description:** *Does his best.*\n"
    )
    embed=discord.Embed(title="COMMANDS", description="You can call a command by typing `@Sir Henry Pickles COMMAND`", color=0x00ff00)
    embed.add_field(name="`help`", value="Prints this. It's the basic commands you can use the Bot for")
    embed.add_field(name="`info`", value="Basic information on the Bot such as name and author")
    embed.add_field(name="`test`", value="Tests if the Bot works properly. Has no other purpose")
    embed.add_field(name="`goodreads`", value="Let'\s you look for authors and books on Goodread.com. For this you can use an authors name, book title, ISBN or even all together. Example: `@Sir Henry Pickles goodreads Neil Gaiman Norse Mythology`")
    embed.add_field(name="`greeting`", value="Say `Hi` to Henry! Or `Hello` or `Morning` or something like this")
    embed.add_field(name="`goodbye`", value="Same as with greeting. Responds to a variety of goodbyes")
    embed.add_field(name="`sleep`", value="Let\'s the Bot decide if you should go to bed")
    embed.add_field(name="`shower`", value="Let\'s the Bot decide if you should take a shower")
    embed.add_field(name="`joke`", value="Let Henry tell you a joke which most certainly is hilarious")
    embed.add_field(name="`8ball`", value="Ask the oracle with this all time classic")
    embed.add_field(name="`roll`", value="You can `roll` a dice using `2d8` with 2 being the number of dice you want the bot to roll and 8 being the number of sides the dice has. If you just want the bot to throw one dice, just put `d8`. You can add your modifier too! Simply put `2d8 3` with 3 being your modifier. Negative values do work too!")
    embed.add_field(name="`clear`", value="With this command a Moderator can clear all messages in a channel if something NSFW or otherwise inapropriate got posted. Other users can use this command aswell - it automatically pings the Moderators for them. For the last 1000 messages purged `clear`, for a certains amount `clear NUMBER` with `NUMBER` being any number between 0 and 1000")
    embed.add_field(name="`GMT`", value="Gives you the current time for the GMT timezones")
    embed.add_field(name="`bleach`", value="Applies eye bleach. *Try it!* (recommended after and/ or before `clear`)")
    embed.add_field(name="`roles`", value="Shows you what roles you have")
    embed.add_field(name="`votecall`", value="Calls a simple thumb up/ thumb down vote for the message.")
    await ctx.bot.say(embed=embed)
    await ctx.bot.say("If you still have questions, please ping the `@Mods`")

@bot.command(pass_context=True)
async def sleep(ctx):
    sleep = ['Yes, you should use the sleep.', 'But mooooom idonwanna!', 'Whatevs, man.', 'JA!']
    await ctx.bot.say(random.choice(sleep))

@bot.command(pass_context=True)
async def shower(ctx):
    shower = [' you reek already!', ' it`s about time...', ' nah, its cool.', ' I mean, have you already showered this week?',' but only a golden shower.']
    await ctx.bot.say(ctx.message.author.mention+ " " + random.choice(shower))

@bot.command(pass_context=True)
async def joke(ctx):
    joke = [
        'I always get pickle and chutney mixed up.\n'
        'It makes me chuckle.',

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

@bot.command(pass_context=True)
async def roll(ctx, dice_string, mod: int = 0):
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

@bot.command(pass_context=True)
async def bleach(ctx):
    eye_bleach = [
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
    "https://i.imgur.com/KnXrY6R.jpg"
    ]
    await ctx.bot.say(random.choice(eye_bleach))

    # Ebedded bleach doesnt work for mp4
    # "https://i.imgur.com/cQBeAjw.mp4",
    # "https://i.imgur.com/p40Hwwi.jpg",
    # "https://i.imgur.com/Onyvdgh.mp4",
    # "https://i.imgur.com/bGtlZbl.jpg",
    # "https://i.imgur.com/kTmRulV.jpg",
    # "https://i.imgur.com/lmnpp5K.mp4",
    # "https://i.imgur.com/fcRvoJn.jpg",
    # "https://i.imgur.com/07lceng.mp4",
    # "https://i.imgur.com/J1EPxUk.jpg",
    # "https://i.imgur.com/JxO5seE.jpg",
    # "https://i.imgur.com/ViNjAKD.mp4",
    # "https://i.imgur.com/vpDxduH.jpg",
    # "https://i.imgur.com/ngTloKH.jpg",
    # "https://i.imgur.com/IiMIW1h.jpg",
    # "https://i.imgur.com/aC8xiz5.mp4",
    # "https://i.imgur.com/rq56D4o.jpg",
    # "https://i.imgur.com/wwOM7kU.mp4",
    # "https://i.imgur.com/cXP94NP.mp4",
    # "https://i.imgur.com/10b9Y12.mp4",
    # "https://i.imgur.com/KnXrY6R.jpg"
    # ]
    # embed=discord.Embed(color=0x00ff00)
    # embed.set_image(url=random.choice(eye_bleach))
    # await ctx.bot.say(embed=embed)

# TIP System
# Karma System

# #google calendar
# @bot.command()
# async def cal(ctx):
#     ctx.bot.say()

@bot.command(pass_context=True)
async def goodreads(ctx, *keyword_raw):
    keyword = str(keyword_raw)
    x = int(0)
    xml = ElementTree.fromstring(
        requests.get('https://www.goodreads.com/search.xml?key=CGisitAFBAgQpaE1fBbZkQ&q=' + keyword + '&page=1').text)

    for v in xml.find('search/results'):
        book = v.find('best_book')
        author = book.find('author/name').text
        title = book.find('title').text
        book_id = book.find('id').text
        result_list = ('**' + author + '**' + ': ' + title + ' - ' + 'https://www.goodreads.com/book/show/' + book_id + '.It')

        await ctx.bot.say(result_list)

        x = (x + 1)
        if x == 3:
            break

        # ['__class__', '__copy__', '__deepcopy__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', 'append', 'attrib', 'clear', 'extend', 'find', 'findall', 'findtext', 'get', 'getchildren', 'getiterator', 'insert', 'items', 'iter', 'iterfind', 'itertext', 'keys', 'makeelement', 'remove', 'set', 'tag', 'tail', 'text']

##Movie Knights
# https://i.imgur.com/QNiL6SP.gif
# https://i.imgur.com/GDNyuPn.mp4
# https://i.imgur.com/DKJhx9l.gif

@bot.command(pass_context=True)
async def roles(ctx):
    await ctx.bot.say(ctx.message.author.mention + "\'s roles are:")
    for r in ctx.message.author.roles:
        roles_me = r.name
        await ctx.bot.say("`"+roles_me+"`")

# make changes for 3.6
# --------------------
@bot.event
async def on_message(message):
    greeting = ['hello', 'hi', 'hey', 'greetings', 'sup', 'morning']
    greeting_res = ['Quite the *lingo* of the youth, eh? Hi to you too!','I bid you pickly greetings!', 'Sup brooooooo. Or sis, idc. <3', 'Shama-Lama-Ding-Dong right back at you!', 'hi', 'hey', 'greetings', 'sup']
    bye = ['bye', 'see you', 'see ya', 'cya', 'nite', 'good night']
    bye_res = ['Farewell!', 'bye', 'see you', 'see ya', 'cya', 'nite']
    ball_res = ['It is certain.', 'It is decidedly so.', 'Without a doubt.', 'Yes - definitely.', 'You may rely on it.', 'As I see it, yes.', 'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.', 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.', 'Connot predict now.', 'Concentrate and ask again.', 'Don`t count on it.', 'My reply is no.', 'My sources say no.', 'Outlook not so good.']
    str_mcl = message.content.lower()

    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message) and not message.mention_everyone:
        if '8ball' in message.content.lower():
            await bot.send_message(message.channel, random.choice(ball_res))
        elif any(x in str_mcl for x in greeting):
            await bot.send_message(message.channel, random.choice(greeting_res))
        elif any(x in str_mcl for x in bye):
            await bot.send_message(message.channel, random.choice(bye_res))
        # else:
        #     await message.add_reaction('👀')
    if 'votecall' in message.clean_content.lower():
        await bot.add_reaction(message, '👍')
        await bot.add_reaction(message, '👎')
    if 'usa' in message.clean_content.lower():
        await bot.add_reaction(message, '🇺🇸')
    if 'australia' in message.clean_content.lower():
        await bot.add_reaction(message, '🇦🇺')
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
