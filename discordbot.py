import discord
from discord.ext import commands
import aiohttp

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

async def sendmsg(convoid, msg):
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
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data, timeout=aiohttp.ClientTimeout(total=25)) as response:
            response_data = await response.json()  
    return response_data

ongoing_conversations = {}

@bot.command()
async def convo(ctx, *, inprry):
    chosen_channel = ctx.channel

    mrembed = discord.Embed(title="Please wait", description="The mister bot is generating a new session for you to talky.")
    neeegdsjs = await ctx.send(embed=mrembed)

    # Start conversation loop
    theinm = await sendmsg("", inprry)
    mistercid = theinm.get("conversationId")

    mrembed2 = discord.Embed(title="Session generated!")
    mrembed2.add_field(name="Conversation ID", value=mistercid)
    mrembed2.add_field(name="Channel", value=chosen_channel.mention)
    mrembed2.set_footer(text=f"Started by {ctx.author.name}#{ctx.author.discriminator}")
    await neeegdsjs.edit(embed=mrembed2)

    embded = discord.Embed(description=theinm.get("output", [""])[0])
    await ctx.send(embed=embded)

    convrr = True

    # Store the conversation task
    ongoing_conversations[ctx.channel.id] = True

    while convrr:
        # Check if the conversation has been stopped
        if not ongoing_conversations.get(ctx.channel.id):
            await ctx.send("Conversation stopped.")
            break

        user_msg = await bot.wait_for('message', check=lambda m: m.channel == chosen_channel)

        if user_msg.content == "!end":
            await ctx.send("Stopping...")
            convrr = False
            ongoing_conversations[ctx.channel.id] = False
            break
        if not user_msg.content.startswith("#") or user_msg.author.bot :
            async with ctx.typing():
                response = await sendmsg(mistercid, user_msg.content)
                embed = discord.Embed(description=response.get("output", [""])[0].strip("{{action-end-conversation}}").strip("{{action-human}}"))
                view = discord.ui.View()
                if "{{action-end-conversation}}" in response.get("output", [""])[0]:
                    button = discord.ui.Button(style=discord.ButtonStyle.red, label="Agent tried to end the conversation")
                    button.disabled = True
                    view.add_item(button)
                elif "{{action-human}}" in response.get("output", [""])[0]:
                    button = discord.ui.Button(style=discord.ButtonStyle.green, label="Agent is trying to connect you to a human")
                    button.disabled = True
                    view.add_item(button)
                await chosen_channel.send(embed=embed, view=view)

    # Remove the conversation task when it ends
    ongoing_conversations.pop(ctx.channel.id, None)

@bot.command()
async def stop(ctx):
    if ctx.channel.id in ongoing_conversations:
        ongoing_conversations[ctx.channel.id] = False
        await ctx.send("Conversation stopping command received.")
    else:
        await ctx.send("No ongoing conversation to stop.")

# Run the bot with your token
bot.run('gsdsdf')
