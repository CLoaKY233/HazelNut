  
import asyncio
import discord
from discord.ext import commands
from typing import overload 

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='$', intents=intents)



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    channel = bot.get_channel(1207649126255304714) 
    await channel.send(f"Hello from Hazelnut!\nlogged in as {bot.user}")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello from Hazelnut!")
    
@bot.command()
async def dm(ctx):
    await ctx.author.send("hello")

# @bot.command()
# async def prune(ctx):
#     if isinstance(ctx.channel, discord.DMChannel):
#         await ctx.send("You cannot prune messages in DMs.")
#         return
#     await ctx.send("How many messages do you want to prune from this channel?")

#     def check(message):
#         return message.author == ctx.author and message.channel == ctx.channel

#     try:
#         response = await bot.wait_for("message", check=check, timeout=60)
#         if response.content.isdigit():
#             num_messages = int(response.content)
#             await ctx.send(f"Pruning {num_messages} messages from this channel.")
#             await ctx.channel.purge(limit=num_messages)
#         else:
#             await ctx.send("Please enter a valid number.")
#     except asyncio.TimeoutError:
#         await ctx.send("You took too long to respond.")






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
    
    elif num_messages == "all":
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



bot.run('MTIwNjYzMDk4MzYzNDI1NTg3Mg.GbIrWY.f4L3H4eYVc1TPRZXcBKleNWR0yRrcK-Wcm0nPk')

    
    



