import discord

JOKES = (
    """
    If you relish the idea of pickle puns, then you'll be pickled by these jokes. They're i-dill for anyone looking for some pickle fun.

    So enjoy our collection of funny pickle jokes and puns.
    """,
    """
    I always get pickle and chutney mixed up.

    It makes me chuckle.
    """,
    """
    What's green and sour and swims in an aquarium?

    A tro-pickle fish.
    """,
    """
    When the giant cannibals started to soak me in vinegar, I'd had enough.

    "Why don't you pickle someone your own size?" I shouted.
    """,
    """
    What's green and got two wheels?

    A motorpickle.
    """,
    """
    I walked into the kitchen today to find my blonde wife looking very confused while holding a jar of pickle.

    "What's wrong?" I asked her.

    She replied "This jar of pickle says to store it in a cool, dark location."

    I said, "Okay, how about in the fridge?"

    She said "No, silly, there's a little light inside."
    """,
    """
    What do you call a pickle lullaby?

    A cucumber slumber number.
    """,
    """Why are pickles in sandwiches always so polite?

    They're well-bread.
    """,
    """
    This guy had devoted his whole working life to his job in a pickle factory.

    Then one day he got home from work and told his wife he'd been fired from his job.
    
    She was very upset at this and angry at the company he'd worked for, shouting, "You've given that firm twenty years of devoted service. Why the hell did they fire you?"
    
    The guy explained, "For the whole twenty years I worked there I've been tempted to stick my John Thomas in the pickle slicer and today I finally did it!"
    
    The wife screamed in horror and ran over to her husband. Then she pulled his pants down to see what damage had been done.
    
    She let out a big sigh of relief. "You look okay" she said, "So what happened to the pickle slicer?"
    
    The guy said, "They fired her, too."
    """,
    """
    What's a baby gherkin's favorite TV channel?

    Pickleodeon.
    """,
    """
    What do you call a pickle you got at a cheap price?

    A sweet dill.
    """,
    """
    I recently got a new job as a golf caddy, but I was fired after less than an hour.

    The guy asked me for a sand wedge.

    I don't think he likes pickle.
    """,
    """
    Why shouldn't you shoot pool using a pickle?

    Because you'll find the cue cumbersome.
    """,
    """
    What do you get when you cross a pickle with an alligator?

    A crocodill.
    """,
    """
    On what radio station would you hear Bob Dill-on?

    Vlasic rock.
    """,
    """
    I've been feeling really down recently so I thought I'd cheer myself up by making a nice cheese and pickle sandwich.

    But when I picked up the pickle jar, it said "reject if depressed", so now I'm off to take an overdose.
    """,
    """
    What do you call a pickle doctor?

    A dill pusher.
    """,
    """
    I've just got my hand stuck in a jar of gherkins and I can't get it out.

    I'm in a right pickle!
    """,
    """
    Why do gherkins giggle when you touch them?

    They're pickle-ish.
    """,
    """
    What did the pickle say when he was told he was going in to a salad?

    I relish the thought.
    """,
    """
    If Santa had sex with a pickle, what would they call their baby?

    Claussen.
    """,
    """
    What's green and pecks on trees?

    Woody Wood Pickle.
    """,
    """
    What do you do when a pickle wants to play cards?

    Dill'em in.
    """,
    """
    This guy makes a small math error on a report he's written. His boss is mad and tries to belittle him in front of his peers.

    She shouts angrily, "If you had 4 pickles and I asked for one, how many would you have left?"

    The guy replies, "If it was you who asked, I'd still have 4 pickles."
    """,
    """
    What's green and swims in the sea?

    Moby Pickle.
    """,
    """
    What's the difference between a pickle and a psychiatrist?

    If you don't know, you ought to stop talking to your pickle!
    """,
    """
    What do you call a pickle that got run over on the road?

    Road dill.
    """,
    """
    Who's a pickle's favorite artist?

    Salvador Dilli.
    """,
    """
    What's green and wears a cape?

    Super Pickle.
    """,
    """
    What did the arrogant pickle say?

    I'm kind of a big dill.
    """,
    """
    What's a pickle's favorite book?

    To Dill A Mockingbird.
    """,
    """
    Why is the pickle container always open?

    Because it's ajar.
    """,
    """
    Where's a pickle's favorite place to go in London?

    Pickle-dilly Square.
    """,
    """
    What do you call a pickle from the southern backwoods.

    A hill-dilly.
    """,
    """
    What's a pickle's life philosophy?

    Never a dill moment.
    """,
    """
    What did the pickle say to the cat?

    Nothing, pickles can't talk.
    """
)

BLEACHES = (
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
)

USER_GREETINGS = ('hello', 'hi', 'hey', 'greetings', 'sup', 'morning')

BOT_GREETINGS = ('Quite the *lingo* of the youth, eh? Hi to you too!', 'I bid you pickly greetings!',
                 'Sup brooooooo. Or sis, idc. <3', 'Shama-Lama-Ding-Dong right back at you!', 'hi', 'hey',
                 'greetings', 'sup')

USER_BYES = ('bye', 'see you', 'see ya', 'cya', 'nite', 'good night')

BOT_BYES = ('Farewell!', 'bye', 'see you', 'see ya', 'cya', 'nite')

TRIGGERS = {
    'votecall': ('👍', '👎'),
    'australia': ('🇦🇺',),
    'mexico': ('🌮',),
    'ireland': ('🇮🇪',),
    'scotland': ('🏴',),
    'europe': ('🇪🇺',),
    'germany': ('🇩🇪',),
    'united kingdom': ('🇬🇧,'),
    'facepalm': ('🤦',),
    'canada': ('🇨🇦',),
    'sweden': ('🇸🇪',),
    'norway': ('🇳🇴',),
    'finland': ('🇫🇮',),
    'sleep': ('💤',),
    'shower': ('🚿'),
    'love': ('💓'),
    'goodest robot': ('🤖', '🇮', '🇦', '🇲'),
    'sushi': ('🍣'),
}

embed_cmd = discord.Embed(title="COMMANDS",
                          description="You can call a command by typing `@Sir Henry Pickles COMMAND` or `!COMMAND`",
                          color=0x00ff00)
embed_cmd.add_field(name="`help`", value="Sends this per DM. It's the basic commands you can use the Bot for")
embed_cmd.add_field(name="`info`", value="Basic information on the Bot such as name and author")
embed_cmd.add_field(name="`suggestion`", value="Suggest a new funtion or improvement for the Bot. Use with `!suggestion More pickles!`")
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
embed_mod.add_field(name="`prefix`", value="Let\'s you change the used prefix of the Bot")
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

HELP_EMBEDS = (embed_cmd, embed_use, embed_mod, embed_misc)
