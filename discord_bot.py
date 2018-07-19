import discord
from discord.ext import commands

#Get the discord.py from here: https://github.com/Rapptz/discord.py

TOKEN = 'HERE GOES THE TOKEN'

description = '''Sir Henry Pickles, the pickly Bot!'''
bot = commands.Bot(command_prefix='?', description=description)
#changing the comman_prefix is critical

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
#this will be printed into the hosts console

@bot.command()
async def test(ctx):
    """Use this to test if I'm working."""
    await ctx.send("successful")

@bot.command()
async def hi(ctx):
    """Just, hi."""
    await ctx.send("Quite the *lingo* of the youth, eh? Hi to you too, "+ctx.message.author.mention+"!")

@bot.command()
async def hello(ctx):
    """Another greeting."""
    await ctx.send("I bid you pickly greetings!")

@bot.command()
async def sup(ctx):
    """Yet another greeting."""
    await ctx.send("Sup brooooooo. Or sis, idc. <3")

@bot.command()
async def sleep(ctx):
    """Sleep?"""
    await ctx.send("Yes, "+ctx.message.author.mention+". You should use the sleep.")

@bot.command()
async def book(ctx):
    """Search for book on goodreads."""
    await ctx.send("http"+"s://www.goodreads.com/search?q="+"Test"+"&search%5Bsource%5D=goodreads&search_type=books&tab=books")
#still working on it. Picture this:
#Someone types "?book Neil Gaiman"
#I imagine to grab "Neil Gaiman" to
#automatically put it into the
#link to search for it. It should
#go where "Test" is right now.

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="Sir Henry Pickles", description="Pickles are love, pickles are life!", color=0xeee657)

    embed.add_field(name="Author", value="._x3l51")

    await ctx.send(embed=embed)

bot.remove_command('help')

@bot.event
async def on_message(message):
    greeting = ['hello', 'hi', 'hey', 'greetings', 'sup']
    #greeting_res = ['hello', 'hi', 'hey', 'greetings', 'sup']
    #This one could work with any() to pick responses at random
    bye = ['bye', 'see you', 'see ya', 'cya', 'nite']
    #bye_res = ['bye', 'see you', 'see ya', 'cya', 'nite'] 
    #This one could work with any() to pick responses at random
    str = message.content.lower()

    if isinstance(message.channel, discord.DMChannel):
        await message.author.send("Cant respond here!")
        return
    if bot.user.mentioned_in(message) and message.mention_everyone is False:
        if 'help' in message.content.lower():
            await message.channel.send('If you are in need of immediate assistance, I kindly suggest you to dial 911.')
        elif any(x in str for x in greeting):
            await message.channel.send('Shama-Lama-Ding-Dong right back at you!')
        elif any(x in str for x in bye):
            await message.channel.send('Have a great one!')
        else:
            await message.add_reaction('👀')
    if 'australia' in message.clean_content.lower():
        await message.add_reaction('🇦🇺')
    if 'europe' in message.clean_content.lower():
        await message.add_reaction('🇪🇺')
    if 'USA'  in message.clean_content.lower():
        await message.add_reaction('🇺🇸')
    if 'Canada' in message.clean_content.lower():
        await message.add_reaction('🇨🇦')
    if 'nani' in message.clean_content.lower():
        await message.channel.send('NAAAAANNNIIIIII!?!?!?!11')

    await bot.process_commands(message)
    #required bc on_message nullifies all other commands

bot.run(TOKEN)
