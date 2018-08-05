import asyncio
import discord
import random
import time
from discord import Game
from discord.ext import commands

#Get the discord.py from here: https://github.com/Rapptz/discord.py

TOKEN = 'NDY5MjY3OTY5MDIxNTc1MjA4.DjFPbA.L6AgX1weEkJD-wHYDWymQfVBAf4'

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

@bot.command(pass_context=True)
async def member(ctx):
    for member in ctx.guild.members:
        await ctx.send(member)

# @bot.command()
# async def member(ctx):
#     role_mod = [475322910635065345]
#     for r in ctx.message.author.roles:
#         pulled_roles = r.id
#         if pulled_roles in role_mod:
#             for member in ctx.guild.members:
#                 return await ctx.send(member)
#     await ctx.send(ctx.message.author.mention+', you\'re not a mod. You can\'t use this command.')

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="Sir Henry Pickles", description="Pickles are love, pickles are life!", color=0xeee657)
    embed.add_field(name="Author", value='<@!410406332143763466>')
    await ctx.send(embed=embed)
bot.remove_command('help')

@bot.command()
async def test(ctx):
    await ctx.send("successful")
    print(ctx.message.author.mention+" used *test*.")
    print('------')

@bot.command()
async def mod(ctx):
    role_mod = [475322910635065345]
    for r in ctx.message.author.roles:
        pulled_roles = r.id
        if pulled_roles in role_mod:
            return await ctx.send(ctx.message.author.mention+', you\'re a mod.')
    await ctx.send(ctx.message.author.mention+', you\'re not a mod.')

@bot.command()
async def roles(ctx):
    roles_me = ctx.message.author.roles
    await ctx.send(ctx.message.author.mention + "\'s roles are: ")
    await ctx.send(roles_me)

@bot.command()
async def sleep(ctx):
    await ctx.send("Yes, "+ctx.message.author.mention+". You should use the sleep.")

@bot.command()
async def shower(ctx):
    shower = [' you reek already!', ' it`s about time...', ' nah, its cool.', ' I mean, have you already showered this week?',' but only a golden shower.']
    await ctx.send("Yes, "+ctx.message.author.mention+ " " + random.choice(shower))

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

@bot.event
async def on_message(message):
    greeting = ['hello', 'hi', 'hey', 'greetings', 'sup', 'morning']
    greeting_res = ['Quite the *lingo* of the youth, eh? Hi to you too!','I bid you pickly greetings!', 'Sup brooooooo. Or sis, idc. <3', 'Shama-Lama-Ding-Dong right back at you!', 'hi', 'hey', 'greetings', 'sup']
    bye = ['bye', 'see you', 'see ya', 'cya', 'nite', 'good night']
    bye_res = ['Farewell!', 'bye', 'see you', 'see ya', 'cya', 'nite']
    ball = ['8ball']
    ball_res = ['It is certain.', 'It is decidedly so.', 'Without a doubt.', 'Yes - definitely.', 'You may rely on it.', 'As I see it, yes.', 'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.', 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.', 'Connot predict now.', 'Concentrate and ask again.', 'Don`t count on it.', 'My reply is no.', 'My sources say no.', 'Outlook not so good.']
    eye_bleach = ['https://imgur.com/r/aww']
    str = message.content.lower()

    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message) and message.mention_everyone is False:
        if 'eye bleach' in message.content.lower():
            await message.channel.send(random.choice(eye_bleach))
        if 'help' in message.content.lower():
                await message.channel.send('If you are in need of immediate assistance, I kindly suggest you to dial 911.')
        elif any(x in str for x in greeting):
            await message.channel.send(random.choice(greeting_res))
        elif any(x in str for x in bye):
            await message.channel.send(random.choice(bye_res))
        elif all(x in str for x in ball):
            await message.channel.send('Answer: '+random.choice(ball_res))
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
