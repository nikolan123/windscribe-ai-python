import discord
from discord.ext import commands
import requests

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

def sendmsg(convoid, msg):
    url = 'https://garry2-be.windscribe.com/message'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://windscribe.com/',
        'Content-Type': 'application/json',
        'Origin': 'https://windscribe.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'TE': 'trailers'
    }

    data = {
        "conversationId": convoid,
        "message": msg,
        "sessionAuth": ""
    }
    response = requests.post(url, headers=headers, json=data, timeout=25)
    response_data = response.json()
    return response_data

@bot.command()
async def convo(ctx, *, inprry):
    chosen_channel = ctx.channel  
    mrembed = discord.Embed(title="Pls wait", description="The mister bot is generating a new session for u to talky")
    neeegdsjs = await ctx.send(embed=mrembed)
    
    # Start conversation loop
    theinm = sendmsg("", inprry)
    mistercid = theinm.get("conversationId")
    mrembed2 = discord.Embed(title="Session generated!")
    mrembed2.add_field(name="Conversation ID", value=mistercid)
    mrembed2.add_field(name="Channel", value=chosen_channel.mention)
    mrembed2.set_footer(text=f"Started by {ctx.author.name}#{ctx.author.discriminator}")
    await neeegdsjs.edit(embed=mrembed2)
    embded = discord.Embed(description=theinm.get("output", [""])[0])
    await ctx.send(embed=embded)
    convrr = True
    while convrr == True:
        user_msg = await bot.wait_for('message', check=lambda m: m.channel == chosen_channel)
        if user_msg.content == "!end":
            await ctx.send("Stopping...")
            convrr = False
            return
        async with ctx.typing():
            response = sendmsg(mistercid, user_msg.content)
            embed = discord.Embed(description=response.get("output", [""])[0])
            await chosen_channel.send(embed=embed)

# Run the bot with your token
bot.run('c')
