import discord
import requests
import json
import aiohttp
import random
import praw
import os
import time
import delete
import asyncio
import datetime
import kick
import status
import command
import Calculator
import youtube_dl
from discord.ext import commands
from PIL import Image
from io import BytesIO

TOKEN = 'Nzk4NDMxNTEzNjQxMjIyMTY0.X_07Sg.CVgYxSImqxeJKuRA1KX_Q81HwxQ'

client = discord.Client()

@client.event
async def on_ready():
    print('I am ready!')

client = commands.Bot(command_prefix='>', activity=discord.Game(name="!help")) 
client.remove_command('help')

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

@client.command()
async def hi(ctx):
    await ctx.send('Hello!')


@client.command()
async def quote(ctx):
    quote = get_quote()
    await ctx.send(quote)

@client.command(aliases=['memes'])
async def meme(ctx):
    embed = discord.Embed(title = "Meme", description=None)

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed, content=None)

@client.command()
async def say(ctx, *, words):
    time.sleep(0)
    await ctx.message.delete()
    await ctx.send(f"{words}" .format(words))

@client.command()
async def invite(ctx):
    em = discord.Embed(title="Invite URL", description='[Click Here](https://discord.com/oauth2/authorize?client_id=798431513641222164&permissions=8&scope=bot)',color = ctx.author.color)
    await ctx.send(embed = em)

@client.command()
async def server(ctx):
    em = discord.Embed(title="Discord Server", description="[Discord Server](https://discord.gg/9UFn27fj6a)",color = ctx.author.color)
    await ctx.send(embed = em)

@client.command()
async def yt(ctx):
    em = discord.Embed(title="YouTube", description="https://www.youtube.com/channel/UCETRihzhOSobSKIFt6r5FAg",color = ctx.author.color)
    await ctx.send(embed = em)

@client.command()
async def warn( 
          ctx, 
          member: discord.Member = None, 
          reason: str = "No reason provided") -> None:
  if not member:
    await ctx.send("Please mention the member to warn")
    return
  embed = discord.Embed(
              title="Warn",
              description=f'{member.mention} has been warned. \nReason: {reason}'
          )
  await member.send(f'You were warned in {ctx.guild} for {reason}')
  await ctx.send(embed=embed)

@client.command(aliases=["whois"])
async def about(ctx, member: discord.Member = None):
    if not member:  # if member is no mentioned
        member = ctx.message.author  # set member as the author
    roles = [role for role in member.roles]
    embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at,
                          title=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}")

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Display Name:", value=member.display_name)

    embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p IST"))
    embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p IST"))

    embed.add_field(name="Roles:", value="".join([role.mention for role in roles]))
    embed.add_field(name="Highest Role:", value=member.top_role.mention)
    print(member.top_role.mention)
    await ctx.send(embed=embed)

@client.command()
async def avatar(ctx , member: discord.Member):
    await ctx.send(f"{member.avatar_url}")

@client.command()
async def ping(ctx):
    latency = round(client.latency * 1000, 2)
    await ctx.send(f"{latency} ms")

@client.command()
async def sq(ctx, num: int):
    await ctx.send(num * num)


@sq.error
async def squared_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Give me a number to square.")
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send("Give me an integer.")
        return

@client.command()
@commands.has_any_role("「 Owners 」","Foretellers")
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    await ctx.channel.send(f"{member} is banned!")

@client.command()
async def cube(ctx, num: int):
    await ctx.send(num * num * num)


@cube.error
async def cube_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Give me a number to square.")
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send("Give me an integer.")
        return

@client.command()
async def dm(ctx, member : discord.Member, *, reason):
    em = discord.Embed(title='Message',description=f"{reason}")
    em.set_footer(text=f"Sent by {ctx.author}")
    await member.send(embed = em)
    await ctx.send('`Dmed!`')
    return

@dm.error
async def dm_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Name a person to dm.")
        return

@client.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(title="Help", description="Use !help<command> for more info about the command.",color = ctx.author.color)
    embed.add_field(name="Fun", value="(food , meme , ping , hi , beg , bye , food , quote , say , what , about , ffact , treat)", inline = False)
    embed.add_field(name="Maths", value="(cube , square)", inline = False)
    embed.add_field(name="Owner", value="(server , yt)", inline = False)
    embed.add_field(name="Invite", value="(invite)", inline = False)
    embed.add_field(name="Admin Commands", value="(ban , kick , warn , prefix)", inline = False)
    await ctx.send(embed = embed)

@client.command()
async def helpfood(ctx):
    em = discord.Embed(title="Food", description="Get Some Food!",color = ctx.author.color)
    em.add_field(name="*Syntax*", value="!food")
    await ctx.send(embed = em)

@client.command()
async def helpmeme(ctx):
    em = discord.Embed(title="Meme", description="Get A Funny Meme",color = ctx.author.color)
    em.add_field(name="*Syntax*", value="!meme")
    await ctx.send(embed = em)

@client.command()
async def helpping(ctx):
    em = discord.Embed(title="Ping", description="Give The Ping of The Bot",color = ctx.author.color)
    em.add_field(name="*Syntax*", value="!ping")
    await ctx.send(embed = em)

@client.command()
async def helpsay(ctx):
    em = discord.Embed(title="Say", description="Say A Message Through The Bot",color = ctx.author.color)
    em.add_field(name="*Syntax*", value="!say <message>")
    await ctx.send(embed = em)

@client.command()
async def helpquote(ctx):
    em = discord.Embed(title="Quote", description="Get a Inspiratinoal Quote",color = ctx.author.color)
    em.add_field(name="*Syntax*", value="!quote")
    await ctx.send(embed = em)

@client.command()
async def helpabout(ctx):
    em = discord.Embed(title="About", description="Know About A Member!",color = ctx.author.color)
    em.add_field(name="*Syntax*", value="!about <member>")
    await ctx.send(embed = em)

@client.command()
async def helpsquare(ctx):
    em = discord.Embed(title="Square", description="Get The Square Of The Number",color = ctx.author.color)
    em.add_field(name="*Syntax*", value="!sq <number>")
    await ctx.send(embed = em)

@client.command()
async def helpcube(ctx):
    em = discord.Embed(title="Cube", description="Get The Cube Of The Number",color = ctx.author.color)
    em.add_field(name="*Syntax*", value="!cube <number>")
    await ctx.send(embed = em)

@client.command()
async def helpinv(ctx):
    em = discord.Embed(title="Invite A Member", description="Sends a DM to the member you mentioned to invite",color = ctx.author.color)
    em.add_field(name="*Syntax*", value="!inv <member>")
    await ctx.send(embed = em)

@client.command()
async def helpffact(ctx):
    em = discord.Embed(title="Say", description="Random Fun Facts About Friends",color = ctx.author.color)
    em.add_field(name="**Syntax**", value="!ffact")
    await ctx.send(embed = em)
    
@client.command()
async def inv(ctx, member : discord.Member):
    em = discord.Embed(title="Invite URL", description='[Click Here](https://discord.com/oauth2/authorize?client_id=798431513641222164&permissions=8&scope=bot)',color = ctx.author.color)
    await member.send(embed = em)

@client.command()
async def botinfo(ctx):
    em = discord.Embed(title="*Ayush Bot*",color = ctx.author.color)
    em.set_footer(text=f"Requested by {ctx.author}")
    em.add_field(name="The Bot Owner :-", value="JOK★Ayυsн√#6352", inline = False)
    em.add_field(name="The Bot Creator :-", value="JOK★Ayυsн√#6352", inline = False)
    em.add_field(name="The Bot Created On :-", value="1 December 2020 , 11:31 am", inline = False)
    em.add_field(name="Creators YT :-", value="[Subscribe](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline = False)
    em.add_field(name="The Bot Support Server :-", value="[Server](https://discord.gg/9UFn27fj6a)", inline = False)
    em.add_field(name="The Bot Invite Link :-", value="[Invite Link](https://discord.com/oauth2/authorize?client_id=798431513641222164&permissions=8&scope=bot)", inline = False)
    await ctx.send(embed = em)
    
@client.command()
async def ffact(ctx):
    responses = ["*FRIENDS WAS ORIGINALLY CALLED INSOMNIA CAFÉ (AND A BUNCH OF OTHER THINGS).*",
    "*There's a reason the group was always able to sit on their couch at Central Perk(The Couch Was Reserved).*",
    "*THE CAST COULD HAVE BEEN COMPLETELY DIFFERENT.*",
    "*THE PRODUCERS WANTED COURTENEY COX TO PLAY RACHEL, BUT COX RESISTED.*",
    "*THE ROLE OF ROSS GELLER WAS WRITTEN FOR DAVID SCHWIMMER.*",
    "*HE CAST TOOK A TRIP TO LAS VEGAS TOGETHER BEFORE THE SHOW AIRED.*",
    "*The actress who played Emily, Helen Baxendale, was pregnant during the wedding scene.*",
    "*EVERYBODY KNOWS THAT CHANDLER IS THE SACRCASM KING BUT ORIGNALLY JOEY WAS GOING TO BE THE SARCASM KING.*",
    "*THE OPENING CREDITS WERE NOT SHOT IN NEW YORK.*",
    "*CAESAR'S PALACE PLAYED AN IMPORTANT ROLE ON FRIENDS LATER ON.*",
    "*LISA KUDROW DIDN'T KNOW HOW TO PLAY GUITAR.*",
    "*FRIENDS WAS FILMED IN FRONT OF A LIVE AUDIENCE—EXCEPT FOR CLIFFHANGERS.*",
    "*MANY PEOPLE, INCLUDING LISA KUDROW, THOUGHT THAT CHANDLER WAS GAY.*",
    "*THEY WERE THE FIRST TV CAST TO NEGOTIATE AS A GROUP.*",
    "*PHOEBE BUFFAY’S TWIN SISTER, URSULA, WAS ALSO A CHARACTER ON MAD ABOUT YOU.*",
    "*THE APARTMENT NUMBERS SWITCHED DURING THE SERIES.*",
    "*THERE WAS A CONNECTION BETWEEN FRIENDS AND HOME ALONE.*",
    "*KUDROW’S PREGNANCY WAS WRITTEN INTO THE SHOW, BUT COX’S WAS NOT.*",
    "*JOEY’S MAGNA DOODLE ART BECAME A JOB FOR THE CREW.*",
    "*MATT LEBLANC TOOK THE MAGNA DOODLE.*",
    "*THE ACTORS DIDN’T ALWAYS PLAY WELL WITH ANIMALS.*",
    "*THE CAST HAD A HUDDLE BEFORE EVERY EPISODE.*",
    "*FOR THE OPENING CREDITS IN “THE ONE AFTER VEGAS,” EVERYONE WAS GIVEN THE LAST NAME “ARQUETTE.”*",
    "*FOR “THE ONE WITH THE DOLLHOUSE,” THE PROPS DEPARTMENT HAD TO MAKE SIX DIFFERENT CARDBOARD DOLLHOUSES.*",
    "*MATTHEW PERRY STRUGGLED WITH DRUG ADDICTION DURING PRODUCTION.*",
    "*MATT LEBLANC SPENT SEVERAL YEARS HIDING FROM HIS FRIENDS FAME.*",
    "*DAVID SCHWIMMER HAD TROUBLE DEALING WITH HIS IMMEDIATE FAME, TOO.*",
    "*JENNIFER ANISTON ALMOST DIDN’T RETURN FOR THE LAST SEASON.*",
    "*THERE ARE CENTRAL PERK CAFES BASED ON THE FAMOUS COFFEEHOUSE FROM THE SHOW.*",
    "*BRUCE WILLIS APPEARED ON THE SHOW FOR FREE AFTER LOSING A BET TO MATTHEW PERRY.*",
    "*GUNTHER'S BLEACHED HAIR WAS ACCIDENTAL.*",
    "*NONE OF THE ACTORS WAS A HUGE FAN OF THE THEME SONG.*",
    "*THE IDENTITY OF UGLY NAKED GUY WAS NOT REVEALED UNTIL 2016.*",
    "*When Matt LeBlanc auditioned for the role he only had 11 dollars in his pocket.*",
    "*Courteney Cox wanted to play Monica, but was originally offered the role of Rachel.*",
    "*Matt LeBlanc said he really needed to get this job.*",
    "*Monica was originally supposed to end up with Joey and be the series' main couple*",]
    await ctx.send(f'{random.choice(responses)}')

@client.command()
async def roll(ctx):
    responses = ["Map",
    "Shield",
    "Diamond",
    "Jukebox",
    "Dirt",
    "Cobblestone",
    "Dispenser",
    "Iron",
    "Netherite",]
    em = discord.Embed(description=f'The Item Is {random.choice(responses)}.')
    await ctx.send(embed = em)

@client.command(aliases=['howhot', 'hot'])
async def hotcalc(ctx, *, user: discord.Member = None):
    user = user or ctx.author

    random.seed(user.id)
    r = random.randint(1, 100)
    hot = r / 1.17

    emoji = "💔"
    if hot > 25:
        emoji = "❤"
    if hot > 50:
        emoji = "💖"
    if hot > 75:
        emoji = "💞"

    embed = discord.Embed(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")
    await ctx.send(embed=embed)

@client.command(aliases=['slots', 'bet'])
async def slot(ctx):
    emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
    a = random.choice(emojis)
    b = random.choice(emojis)
    c = random.choice(emojis)

    slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

    if (a == b == c):
         await ctx.send(f"{slotmachine} All matching, you won! 🎉")
    elif (a == b) or (a == c) or (b == c):
        await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
    else:
        await ctx.send(f"{slotmachine} No match, you lost 😢")

@client.command(aliases=['cf', 'CF'])
async def coinflip(ctx):
    result = ["Alright It's Heads","Alright It's Tails"]
    embed = discord.Embed(title='CoinFlip',description=random.choice(result))
    embed.set_footer(text=f"Requested By {ctx.author}")
    await ctx.send(embed = embed)

@client.command()
async def treat(ctx, member : discord.Member):
    if member == ctx.author:
        await ctx.send('You Cannot Treat Yourshelf!')
        return
    embed = discord.Embed(description=f"You Offered {member.name} a Treat {member.mention}",color=0x9B59B6)
    timeout=int(30.0)
    message = await ctx.channel.send(embed=embed)

    await message.add_reaction('🍫')

    def check(reaction, user):
        return user == member and str(reaction.emoji) == '🍫'

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)

    except asyncio.TimeoutError:
        msg=(f"{member.mention} didn't accept the treat at time!")
        await ctx.channel.send(msg)

    else:
        await ctx.channel.send(f"{member.mention} You Have Accepted {ctx.author} Treat!!")

@client.command()
async def yn(ctx, member : discord.Member, *, reason):
    if member == ctx.author:
        await ctx.send('You cannnot Y or N yourshelf!!')
        return
    embed = discord.Embed(description=f"{reason}",color=0x9B59B6)
    timeout=int(30.0)
    message = await member.send(embed=embed)

    await message.add_reaction('✔️')
    await message.add_reaction('❌')

    def check(reaction, user):
        return user == member and str(reaction.emoji) == '✔️'

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
    
    except asyncio.TimeoutError:
        msg=(f"He didn't asnwer at time!")
        await ctx.channel.send(msg)

    else:
        await ctx.channel.send(f"{ctx.author} Its true !")

    def check(reaction, user):
        return user == member and str(reaction.emoji) == '❌'

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=30.0,  check=check)

    except asyncio.TimeoutError:
        msg=(f"He didn't asnwer at time!")
        await ctx.channel.send(msg)
    
    else:
        await ctx.channel.send(f"{ctx.author} Its not true as {member.mention}")

@client.command()
async def helptreat(ctx):
    em = discord.Embed(title="Treat", description="Give A treat To the discord member.",color = ctx.author.color)
    em.add_field(name="*Syntax*", value="!treat <member>")
    await ctx.send(embed = em)
    await ctx.send(embed=embed)

@client.command(aliases=['Cf'])
async def catfact(ctx):
  async with aiohttp.ClientSession() as session:
    async with session.get("https://catfact.ninja/fact") as response:
      fact = (await response.json())["fact"]
      embed = discord.Embed(title=f'Cat Fact', description=f'Cat Fact: {fact}', colour=0x400080)
      embed.set_footer(text="")
      await ctx.send(embed=embed)

@client.command()
async def dance(ctx):
    await ctx.send('https://tenor.com/view/chandler-joey-ross-chandler-bing-joey-tribbiani-gif-14043006')

@client.command(help="Play with .rps [your choice]")
async def rpsb(ctx):
    rpsGame = ['rock', 'paper', 'scissors']
    await ctx.send(f"Rock, paper, or scissors? Choose wisely...")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in rpsGame

    user_choice = (await client.wait_for('message', check=check)).content

    comp_choice = random.choice(rpsGame)
    if user_choice == 'rock':
        if comp_choice == 'rock':
            await ctx.send(f'Well, that was weird. We tied.\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'paper':
            await ctx.send(f'Nice try, but I won that time!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'scissors':
            await ctx.send(f"Aw, you beat me. It won't happen again!\nYour choice: {user_choice}\nMy choice: {comp_choice}")

    elif user_choice == 'paper':
        if comp_choice == 'rock':
            await ctx.send(f'The pen beats the sword? More like the paper beats the rock!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'paper':
            await ctx.send(f'Oh, wacky. We just tied. I call a rematch!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'scissors':
            await ctx.send(f"Aw man, you actually managed to beat me.\nYour choice: {user_choice}\nMy choice: {comp_choice}")

    elif user_choice == 'scissors':
        if comp_choice == 'rock':
            await ctx.send(f'HAHA!! I JUST CRUSHED YOU!! I rock!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'paper':
            await ctx.send(f'Bruh. >: |\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'scissors':
            await ctx.send(f"Oh well, we tied.\nYour choice: {user_choice}\nMy choice: {comp_choice}")

@client.command()
async def servers(ctx ):
    servers = len(client.guilds)
    em = discord.Embed(title="Severs", description=f"I'm in {servers} Servers.", colour=0x400080)
    em.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed = em)

@client.command(case_insensitive = True, aliases = ["remind", "remindme", "remind_me"])
async def reminder(ctx, time, *, reminder):
    user = ctx.message.author
    embed = discord.Embed(color=0x55a7f7, timestamp=datetime.datetime.utcnow())
    embed.set_footer(text="If you have any questions, suggestions or bug reports, please join our support Discord Server: link hidden", icon_url=f"{client.user.avatar_url}")
    seconds = 0
    if reminder is None:
        embed.add_field(name='Warning', value='Please specify what do you want me to remind you about.') # Error message
    if time.lower().endswith("d"):
        seconds += int(time[:-1]) * 60 * 60 * 24
        counter = f"{seconds // 60 // 60 // 24} days"
    if time.lower().endswith("h"):
        seconds += int(time[:-1]) * 60 * 60
        counter = f"{seconds // 60 // 60} hours"
    elif time.lower().endswith("m"):
        seconds += int(time[:-1]) * 60
        counter = f"{seconds // 60} minutes"
    elif time.lower().endswith("s"):
        seconds += int(time[:-1])
        counter = f"{seconds} seconds"
    if seconds == 0:
        embed.add_field(name='Warning',
                        value='Please specify a proper duration, send `reminder_help` for more information.')
    elif seconds < 60:
        embed.add_field(name='Warning',
                        value='You have specified a too short duration!\nMinimum duration is 1 minutes.')
    elif seconds > 7776000:
        embed.add_field(name='Warning', value='You have specified a too long duration!\nMaximum duration is 90 days.')
    else:
        eml = discord.Embed(title="Reminder",description=f"Alright, I will remind you about {reminder} in {counter}.")
        await ctx.send(embed = eml)
        await asyncio.sleep(seconds)
        em = discord.Embed(title="Reminder",description=f"Hi, you asked me to remind you about {reminder}.")
        em.set_footer(text=f"{counter} Ago")
        await ctx.author.send(embed = em)

@client.command(aliases = ["movie", "mi", "film"])
async def movie_info(ctx, q):
    data = requests.get('http://www.omdbapi.com/?s='+q+'&apikey=79d58cfc').json()
    title = data['Title']
    embed = discord.Embed(title=f"{q}", description=None)
    embed.set_footer(text=f"Requested by {ctx.author}")
    embed.add_field(name='Movie Name',value=f"{title}")
    await ctx.send(embed=embed)

@client.command()
async def wanted(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author

    wanted = Image.open("wanted.jpg")

    asset = user.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((90,84))

    wanted.paste(pfp, (46,89))

    wanted.save("profile.jpg")

    await ctx.send(file = discord.File("profile.jpg"))

@client.command()
async def rip(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author

    rip = Image.open("rip.jpg")

    asset = user.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((101,93))

    rip.paste(pfp, (43,115))

    rip.save("ripfp.jpg")

    await ctx.send(file = discord.File("ripfp.jpg"))

@client.command()
async def nsfw(ctx):
    embed = discord.Embed(title = "NSFW", description=None)

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/nsfw/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=[random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed, content=None)

client.run(TOKEN)