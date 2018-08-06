import asyncio
import discord
import random
import time
import urllib.request
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot

#Get the discord.py from here: https://github.com/Rapptz/discord.py

TOKEN = 'TOKENGOESHERE'

description = '''Sir Henry Pickles, the pickly Bot!'''
bot = commands.Bot(command_prefix=commands.when_mentioned)

@bot.event
async def on_ready():
    activity = discord.Game(name="with pickles.")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def members(ctx):
    role_mod = [468826620648620042, 475322910635065345]
    for r in ctx.message.author.roles:
        pulled_roles = r.id
        if pulled_roles in role_mod:
            for member in ctx.guild.members:
                print(member)
                await ctx.send(member)
            return
    await ctx.send(ctx.message.author.mention+', you\'re not a mod. You can\'t use this command.')

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="Sir Henry Pickles", description="Pickles are love, pickles are life!", color=0xeee657)
    embed.add_field(name="Author", value='<@!410406332143763466>')
    await ctx.send(embed=embed)
bot.remove_command('help')

@bot.command()
async def gmt(ctx):
    t = time.gmtime()
    await ctx.send("Actual time GMT: " + time.asctime(t))

@bot.command(pass_context = True)
async def clear(ctx):
    role_mod = [468826620648620042, 475322910635065345]
    for r in ctx.message.author.roles:
        pulled_roles = r.id
        if pulled_roles in role_mod:
            e = discord.Embed()
            await ctx.channel.purge(limit=1000)
            await ctx.send("Channel has been cleared of messages.")
            await ctx.send("https://cdn.discordapp.com/attachments/474903005523869715/474903418100645898/FwxbY6j.gif")
            return
    await ctx.send(ctx.message.author.mention+', you\'re not a <@&475322910635065345>. You can\'t use this command.')

@bot.command()
async def test(ctx):
    await ctx.send("successful")
    print(ctx.message.author.mention+" used *test*.")
    print('------')

@bot.command()
async def mod(ctx):
    role_mod = [468826620648620042, 475322910635065345]
    for r in ctx.message.author.roles:
        pulled_roles = r.id
        if pulled_roles in role_mod:
            return await ctx.send(ctx.message.author.mention+', you\'re a mod.')
    await ctx.send(ctx.message.author.mention+', you\'re not a mod.')

@bot.command()
async def help(ctx):
    await ctx.send(
        "\n"
        "----------\n"
        "\n"
        "**Name**: Sir Henry Pickles\n"
        "**Description:** *Basic commands of the bot.*\n"
        "\n"
        "You can call a command by `@Sir Henry Pickles COMMAND`\n"
        "\n"
        "`info`\n" 
        "Basic information on the Bot\n"
        "\n"
        "`test`\n" 
        "Tests if the Bot works properly\n"
        "\n"
        "`greeting`\n" 
        "Say `Hi` to Henry! Or `Hello` or `Morning` or something like this\n"
        "\n"
        "`goodbye`\n" 
        "Same as with greeting. Responds to a variety of goodbyes\n"
        "\n"
        "`sleep`\n" 
        "Let\'s the Bot decide if you should go to bed\n"
        "\n"
        "`shower`\n" 
        "Let\'s the Bot decide if you should take a shower\n"
        "\n"
        "`joke`\n" 
        "Let Henry tell you a joke\n"
        "\n"
        "`8ball`\n" 
        "Ask the oracle\n"
        "\n"
        "`roll`\n" 
        "You can `roll` a dice using `2d8` with 2 being the number\n"
        "of dice you want the bot to roll and 8 being the number of sides\n"
        "the dice has. If you just want the bot to throw one dice, just put `d8`.\n"
        "You can add your modifier too! Simply put `2d8 3` with 3 being your\n"
        "modifier. Negative values do work too!\n"
        "\n"
        "`clear`\n"
        "With this command a Moderator can clear all messages in a\n"
        "channel if something NSFW or otherwise inaapropriate got posted.\n"
        "Other users can use this command aswell - it automatically pings\n"
        "the Moderators for them.\n"
        "\n"
        "`bleach`\n"
        "Applies eye bleach. *Try it!*\n"
        "\n"
        "`roles`\n"
        "Shows you what roles you have.\n"
        "\n"
    )

@bot.command()
async def sleep(ctx):
    sleep = ['Yes, you should use the sleep.', 'But mooooom idonwanna!', 'Whatevs, man.', 'JA!']
    await ctx.send(random.choice(sleep))

@bot.command()
async def shower(ctx):
    shower = [' you reek already!', ' it`s about time...', ' nah, its cool.', ' I mean, have you already showered this week?',' but only a golden shower.']
    await ctx.send(ctx.message.author.mention+ " " + random.choice(shower))

@bot.command()
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
        '\n'
        '',
        ]
    await ctx.send(random.choice(joke))

@bot.command()
async def roll(ctx, dice_string, mod: int = 0):
    count_raw, num_raw = dice_string.split("d")
    if not count_raw:
        count_raw = 1
    count = int(count_raw)
    num = int(num_raw)
    await ctx.send("Rolling "+ str(count) +" d"+ str(num) +" ...")
    await asyncio.sleep( 2 )
    random.seed()
    numbers = []
    for count in range(count):
        number = random.randint(1,num)
        numbers.append(number)
    num_ran_count = (sum(numbers))
    if mod is 0:
        await ctx.send("I rolled a "+ str(num_ran_count) + " for you.")
    else:
        num_ran_count_mod = num_ran_count+mod
        await ctx.send("I rolled "+ str(num_ran_count) + " for you. That\'s a " + str(num_ran_count_mod) + " with your modifier.")

@bot.command()
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
    'https://i.imgur.com/KnXrY6R.jpg'
    ]
    await ctx.send(random.choice(eye_bleach))

# TIP System

# #google calendar
# @bot.command()
# async def cal(ctx):
#     ctx.send()

# #goodreads
# @bot.command()
# async def gr(ctx):
#     contents = urllib.request.urlopen("https://www.goodreads.com/search.xml?key=CGisitAFBAgQpaE1fBbZkQ&q=Ender%27s+Game").read()
#     await ctx.send(contents)

##Movie Knights
# https://i.imgur.com/QNiL6SP.gif
# https://i.imgur.com/GDNyuPn.mp4
# https://i.imgur.com/DKJhx9l.gif

@bot.command()
async def roles(ctx):
    await ctx.send(ctx.message.author.mention + "\'s roles are:")
    for r in ctx.message.author.roles:
        roles_me = r.name
        await ctx.send("`"+roles_me+"`")

@bot.event
async def on_message(message):
    greeting = ['hello', 'hi', 'hey', 'greetings', 'sup', 'morning']
    greeting_res = ['Quite the *lingo* of the youth, eh? Hi to you too!','I bid you pickly greetings!', 'Sup brooooooo. Or sis, idc. <3', 'Shama-Lama-Ding-Dong right back at you!', 'hi', 'hey', 'greetings', 'sup']
    bye = ['bye', 'see you', 'see ya', 'cya', 'nite', 'good night']
    bye_res = ['Farewell!', 'bye', 'see you', 'see ya', 'cya', 'nite']
    ball_res = ['It is certain.', 'It is decidedly so.', 'Without a doubt.', 'Yes - definitely.', 'You may rely on it.', 'As I see it, yes.', 'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.', 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.', 'Connot predict now.', 'Concentrate and ask again.', 'Don`t count on it.', 'My reply is no.', 'My sources say no.', 'Outlook not so good.']
    str = message.content.lower()

    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message) and message.mention_everyone is False:
        if '8ball' in message.content.lower():
            await message.channel.send(random.choice(ball_res))
        if 'help' in message.content.lower():
                await message.channel.send('If you are in need of immediate assistance, I kindly suggest you to call the emergency services.')
        elif any(x in str for x in greeting):
            await message.channel.send(random.choice(greeting_res))
        elif any(x in str for x in bye):
            await message.channel.send(random.choice(bye_res))
        # else:
        #     await message.add_reaction('👀')
    if 'australia' in message.clean_content.lower():
        await message.add_reaction('🇦🇺')
    if 'europe' in message.clean_content.lower():
        await message.add_reaction('🇪🇺')
    if 'facepalm'  in message.clean_content.lower():
        await message.add_reaction('🤦')
    if 'Canada' in message.clean_content.lower():
        await message.add_reaction('🇨🇦')
    if 'sweden' in message.clean_content.lower():
        await message.add_reaction('🇸🇪')
    if 'sleep' in message.clean_content.lower():
        await message.add_reaction('💤')
    if 'sushi' in message.clean_content.lower():
        await message.add_reaction('🍣')
    if 'shower' in message.clean_content.lower():
        await message.add_reaction('🚿')
    if 'love' in message.clean_content.lower():
        await message.add_reaction('💓')
    if 'goodest robot' in message.clean_content.lower():
        await message.add_reaction('🤖')
        await message.add_reaction('🇮')
        await message.add_reaction('🇦')
        await message.add_reaction('🇲')
    if 'nani' in message.clean_content.lower():
        await message.channel.send('NAAAAANNNIIIIII!?!?!?!11')

    await bot.process_commands(message)

bot.run(TOKEN)
