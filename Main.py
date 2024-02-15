import asyncio
import discord
from discord.ext import commands

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    channel = bot.get_channel(1207734746981998614) 
    await channel.send(f"Hello from Waffle!\nlogged in as {bot.user}")

@bot.command()
async def hello(ctx):
    await ctx.send("A Warm and chocolatey Hello from Waffle!")
    
@bot.command()
async def dm(ctx):
    await ctx.author.send("hello")

@bot.command()
async def prune(ctx, num_messages=""):
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("You cannot prune messages in DMs.")
        return
    
    if num_messages.isdigit():
        num_messages = int(num_messages)
        if num_messages <= 0:
            await ctx.send("Please provide a valid number greater than 0.")
            return

        await ctx.send(f"Pruning {num_messages} messages from this channel.")
        await ctx.channel.purge(limit=num_messages)
    
    elif num_messages.casefold() == "all":
        await ctx.send("Pruning all messages from this channel.")
        await ctx.channel.purge() 
        
    elif num_messages == "":
        await ctx.send("How many messages do you want to prune from this channel?")
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        try:
            response = await bot.wait_for("message", check=check, timeout=10)
            if response.content.isdigit():
                num_messages = int(response.content)
                await ctx.send(f"Pruning {num_messages} messages from this channel.")
                await ctx.channel.purge(limit=num_messages)
            elif response.content.casefold() == "all":
                await ctx.send("Pruning all messages from this channel.")
                await ctx.channel.purge()
            else:
                await ctx.send("Please enter a valid number.")
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond.")
    
@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel) and message.author != bot.user:
        print(f"Received DM from {message.author}: {message.content}")
        if message.content.isdigit() == True:
            if message.content == "123":
                await message.author.send("you are verified")
            else:
                await message.author.send("invalid code, try again")
    await bot.process_commands(message)

@bot.command()
async def shutdown(ctx):
    required_role_id = 1207733658237009920  
    required_role = discord.utils.get(ctx.guild.roles, id=required_role_id)
    if required_role in ctx.author.roles:
        confirmation_msg = await ctx.send("Are you sure you want to shut down the bot? React with ✅ to confirm or ❌ to cancel.")
        await confirmation_msg.add_reaction("✅")
        await confirmation_msg.add_reaction("❌")

        def check(reaction, user):
            return user.guild_permissions.administrator and reaction.message == confirmation_msg and str(reaction.emoji) in ["✅", "❌"]

        try:
            reaction, _ = await bot.wait_for("reaction_add", timeout=30, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Confirmation timed out. Shutting down canceled.")
        else:
            if str(reaction.emoji) == "✅":
                await ctx.send("Shutting down...\nWaffle will miss you! :C")
                await bot.close()
            else:
                await ctx.send("Shutdown canceled.")
    else:
        await ctx.send("You do not have permission to use this command.")



bot.run('MTIwNjYzMDk4MzYzNDI1NTg3Mg.GbIrWY.f4L3H4eYVc1TPRZXcBKleNWR0yRrcK-Wcm0nPk')

    
    



