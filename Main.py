import asyncio
import discord
from discord.ext import commands
import time
import datetime
import csv
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


async def add_role_to_user(user_id,role_id):
  guild = bot.get_guild(
      1203342217519964170)  # Replace YOUR_GUILD_ID with your guild's ID
  user = guild.get_member(user_id)
  if user is None:
    print(f"User with ID {user_id} not found in the guild.")
    return

  role = guild.get_role(
      role_id
  )  # Replace YOUR_ROLE_ID with the role's ID you want to add
  if role is None:
    print(f"Role with ID {role_id} not found in the guild.")
    return

  await user.add_roles(role)
  print(f"Role {role.name} added to user {user.name}.")



@bot.event
async def on_ready():

  #ready hello message
  async def Readyhello():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    channel = bot.get_channel(1207734746981998614)
    hello = discord.Embed(title=f"Hello from {bot.user.display_name}",
                          color=0x00FFFF,
                          timestamp=datetime.datetime.now())
    hello.set_thumbnail(url=bot.user.avatar.url)
    hello.add_field(
        name="What can Waffle do!",
        value=
        f"{bot.user.display_name} will handle this exhibition with precision and care!",
        inline=False)
    await channel.send(embed=hello)

  await Readyhello()

  async def find_channel(channel_name):
    guild = bot.get_guild(1203342217519964170)
    for channel in guild.channels:
      if channel.name == channel_name:
        return channel.id
    return None

  async def Ticket():
    guild = bot.get_guild(1203342217519964170)
    channel1 = bot.get_channel(1212442019302215700)
    await channel1.purge()

    ticketembed = discord.Embed(title="Create Ticket!",
                                description=f"do you want to create a ticket?",
                                color=0x00f069,
                                timestamp=datetime.datetime.now())
    ticketembed.add_field(name="Confirmation",
                          value=f"click the reaction to create a ticket",
                          inline=False)

    button = discord.ui.Button(label="Create Ticket",
                               style=discord.ButtonStyle.primary)

    async def button_callback(interaction):
      await interaction.response.defer()

      overwrites = {
          guild.default_role: discord.PermissionOverwrite(
              read_messages=False),  # Hide the channel from @everyone
          interaction.user: discord.PermissionOverwrite(
              read_messages=True)  # Allow the command author to read messages
      }
      channel_name = f"{interaction.user.name}s-ticket"

      channel_names_list = [channel.name for channel in guild.channels]
      if channel_name in channel_names_list:
        existing_channel = await find_channel(channel_name)
        message3 = await interaction.followup.send(
            f"{interaction.user.mention} you already have a ticket! -> <#{existing_channel}> ",
            ephemeral=True)
        await asyncio.sleep(10)
        await message3.delete()
        return
      category1 = discord.utils.get(guild.categories, id=1213021742780514336)
      new_channel = await guild.create_text_channel(channel_name,
                                                    category=category1,
                                                    overwrites=overwrites)
      await new_channel.send(interaction.user.mention)

      message2 = await interaction.followup.send(
          f"your ticket has been created {interaction.user.mention} -> {new_channel.mention}",
          ephemeral=True)
      await new_channel.edit(slowmode_delay=10)
      await asyncio.sleep(10)
      await message2.delete()

    button.callback = button_callback
    view = discord.ui.View()
    view.add_item(button)
    ticketembed.set_thumbnail(
        url=
        "https://www.citypng.com/public/uploads/preview/-11597269407aqavkzrcos.png"
    )

    await channel1.send(embed=ticketembed, view=view)

  await Ticket()

  async def get_dm():
    guild = bot.get_guild(1203342217519964170)
    channel1 = bot.get_channel(1212094690514698331)

    await channel1.purge()

    dmembed = discord.Embed(
        title="Direct Messages",
        description=f"Click the Button to recieve a Message from Waffle!",
        color=0x00f069,
        timestamp=datetime.datetime.now())
    dmembed.set_thumbnail(
        url=
        "https://www.citypng.com/public/uploads/preview/-11597269407aqavkzrcos.png"
    )
    button = discord.ui.Button(label="Recieve D.M.",
                               style=discord.ButtonStyle.secondary)

    async def button_callback(interaction):

      await interaction.response.defer()
      msgembed = discord.Embed(title=f"Hello! {interaction.channel.mention}")
      try:
        msgembed.set_thumbnail(url=interaction.user.avatar.url)
      except AttributeError:
        msgembed.set_thumbnail(url="https://wallpaper.dog/large/10964102.jpg")
      msgembed.add_field(
          name="Verification",
          value=
          "please enter the one time verification code to verify yourself!",
          inline=True)
      await interaction.user.send(embed=msgembed)

    button.callback = button_callback
    view = discord.ui.View()
    view.add_item(button)

    await channel1.send(embed=dmembed, view=view)

  await get_dm()

  async def create_team():
    guild = bot.get_guild(1203342217519964170)
    channel1 = bot.get_channel(1212798572886757436)

    await channel1.purge()

    teamembed = discord.Embed(
        title="Create Team!",
        description=f"Click To Create a Team or Join one!!!",
        color=0xFFFFFF,
        timestamp=datetime.datetime.now())
    teamembed.add_field(
        name="Teams",
        value=
        f"click the reaction to create or join a team with a Unique Team Code!",
        inline=False)

    button1 = discord.ui.Button(label="Create Team",
                                style=discord.ButtonStyle.success)

    async def button_callback(interaction):
      await interaction.response.defer()

      #logic to create team
      print("create")
      #1214133687181123624 role id
      #1214133586232475708 caregory id

#change overwrites later for team members channel visibility
      overwrites = {
          guild.default_role: discord.PermissionOverwrite(
              read_messages=False),  # Hide the channel from @everyone
          interaction.user: discord.PermissionOverwrite(
              read_messages=True)  # Allow the command author to read messages
      }
      channel_name = f"{interaction.user.name}s-team"

      role = discord.utils.get(guild.roles, id=1214133687181123624)
      channel_names_list = [channel.name for channel in guild.channels]
      if channel_name in channel_names_list:
        existing_channel = await find_channel(channel_name)
      if role in interaction.user.roles:
        
        message3 = await interaction.followup.send(
            f"{interaction.user.mention} you already Created a Team! -> <#{existing_channel}> ",
            ephemeral=True)
        await asyncio.sleep(10)
        await message3.delete()
        return
      category1 = discord.utils.get(guild.categories, id=1214133586232475708)
      
      new_channel = await guild.create_text_channel(channel_name,
                                                    category=category1,
                                                    overwrites=overwrites)
      await add_role_to_user(interaction.user.id,1214133687181123624)
      await new_channel.send(interaction.user.mention)

      message2 = await interaction.followup.send(
          f"{interaction.user.mention} You successfully created a Team  -> {new_channel.mention}",
          ephemeral=True)
      await new_channel.edit(slowmode_delay=100)
      await asyncio.sleep(10)
      await message2.delete()


    button1.callback = button_callback

    button2 = discord.ui.Button(label="Join Team",
                                style=discord.ButtonStyle.blurple)

    async def button2_callback(interaction):
      await interaction.response.defer()
      print("join")
      message4 = await interaction.followup.send(f"you have joined a team",
                                                 ephemeral=True)
      await asyncio.sleep(30)
      await message4.delete()
      #logic to join team

    button2.callback = button2_callback

    view = discord.ui.View()
    view.add_item(button1)
    view.add_item(button2)
    teamembed.set_thumbnail(
        url=
        "https://www.citypng.com/public/uploads/preview/-11597269407aqavkzrcos.png"
    )

    await channel1.send(embed=teamembed, view=view)

  await create_team()


@bot.command()
async def hello(ctx):
  greetings = discord.Embed(title=f"Hello from {bot.user.display_name}",
                            color=0x00F069)
  try:
    greetings.set_thumbnail(url=ctx.author.avatar.url)
  except AttributeError:  # Catch AttributeError if the user has no avatar
    # Set a default thumbnail URL
    greetings.set_thumbnail(url="https://wallpaper.dog/large/10964102.jpg")
  greetings.add_field(
      name=f"{bot.user.display_name} is online",
      value=f"{bot.user.display_name} say's Hello! to {ctx.author.mention}",
      inline=False)
  await ctx.send(embed=greetings)


@bot.command()
async def profile(ctx):
  """Sends an embed with the bot's profile picture and information."""
  embed = discord.Embed(title=f"{bot.user.display_name}'s Profile",
                        color=0x00FFFF)  # Adjust color as needed
  embed.set_thumbnail(
      url=bot.user.avatar.url)  # Use avatar.url for avatar image
  embed.add_field(name="Username", value=bot.user.name, inline=False)
  embed.add_field(name="User ID", value=bot.user.id, inline=False)
  await ctx.send(embed=embed)


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


@bot.command()
async def kill(ctx):
  killembed = discord.Embed(
      title="Attention!",
      description="Are you sure you want to shut down the bot?",
      color=0x00ffff,  # Adjust color as needed
      timestamp=datetime.datetime.now())
  killembed.add_field(
      name="Confirmation",
      value="React with ✅ to confirm shutdown, or ❌ to cancel.",
      inline=False)
  if isinstance(ctx.channel, discord.DMChannel):
    if str(ctx.author) == "cloak2822":
      confirmation_msg = await ctx.send(embed=killembed)
      await confirmation_msg.add_reaction("✅")
      await confirmation_msg.add_reaction("❌")

      def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in [
            "✅", "❌"
        ] and reaction.message == confirmation_msg

      try:
        reaction, _ = await bot.wait_for("reaction_add",
                                         timeout=30,
                                         check=check)
        await ctx.send("Thanks for confirming.")
      except asyncio.TimeoutError:
        await ctx.send("Confirmation timed out. Shutting down canceled.")
      else:
        if str(reaction.emoji) == "✅":
          await ctx.send("Shutting down...\nWaffle will miss you! :C")
          await bot.close()
        else:
          await ctx.send("Shutdown canceled.")
    if str(ctx.author) != "cloak2822":

      await ctx.send("nice try Loser!,\nwe got you!")
      print(
          f"user {ctx.author} tried to shut down the bot without permission!")
      return

  if not isinstance(ctx.channel, discord.DMChannel):
    required_role_id = 1207733658237009920
    required_role = discord.utils.get(ctx.guild.roles, id=required_role_id)
    if required_role in ctx.author.roles:

      confirmation_msg = await ctx.send(embed=killembed)
      await confirmation_msg.add_reaction("✅")
      await confirmation_msg.add_reaction("❌")

      def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in [
            "✅", "❌"
        ] and reaction.message == confirmation_msg

      try:
        reaction, _ = await bot.wait_for("reaction_add",
                                         timeout=30,
                                         check=check)
        await ctx.send("Thanks for confirming.")
      except asyncio.TimeoutError:
        await ctx.send("Confirmation timed out. Shutting down canceled.")
        await asyncio.sleep(3)
        await prune(ctx, "4")
      else:
        if str(reaction.emoji) == "✅":
          await ctx.send("Shutting down...\nWaffle will miss you! :C")
          await bot.close()
        else:
          await asyncio.sleep(3)
          await prune(ctx, "4")

    else:
      await ctx.send("You do not have permission to use this command.")
      await asyncio.sleep(3)
      await prune(ctx, "3")


@bot.command()
async def kick(ctx, user_input):
  if str(ctx.author) == "cloak2822":
    try:
      if user_input.startswith("<@"):
        user_id = user_input[2:-1]
        user = await commands.UserConverter().convert(ctx, user_id)
      else:
        user_id = int(user_input)
        user = await bot.fetch_user(user_id)

      if user is None:
        raise ValueError("User not found.")

      kickembed = discord.Embed(
          title="Attention!",
          description=f"Do you want to kick {user.mention}?",
          color=0x00ffff,  # Adjust color as needed
          timestamp=datetime.datetime.now())
      kickembed.add_field(
          name="Confirmation",
          value="React with ✅ to confirm shutdown, or ❌ to cancel.",
          inline=False)
      try:
        kickembed.set_thumbnail(url=user.avatar.url)
      except AttributeError:  # Catch AttributeError if the user has no avatar
        # Set a default thumbnail URL
        kickembed.set_thumbnail(url="https://wallpaper.dog/large/10964102.jpg")

      confirmation_msg = await ctx.send(embed=kickembed)
      await confirmation_msg.add_reaction("✅")
      await confirmation_msg.add_reaction("❌")

      def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in [
            "✅", "❌"
        ] and reaction.message == confirmation_msg

      try:
        reaction, _ = await bot.wait_for("reaction_add",
                                         timeout=30,
                                         check=check)
      except asyncio.TimeoutError:
        await ctx.send("Confirmation timed out. Kick canceled.")
        await asyncio.sleep(3)
        await prune(ctx, "4")
        return

      if str(reaction.emoji) == "✅":
        reason_msg = await ctx.send("Enter a reason for kicking the user:")
        reason_response = await bot.wait_for(
            "message", check=lambda m: m.author == ctx.author)
        reason = reason_response.content

        try:
          await ctx.guild.kick(user, reason=reason)
          await ctx.send(f"{user.mention} has been kicked. Reason: {reason}")
          await asyncio.sleep(3)
          await prune(ctx, "6")
        except discord.DiscordException as e:
          await ctx.send(f"Failed to kick user: {e}")
          await asyncio.sleep(3)
          await prune(ctx, "6")
      else:
        await ctx.send("Kick canceled.")
        await asyncio.sleep(3)
        await prune(ctx, "4")
    except ValueError as e:
      await ctx.send(f"Invalid user input: {e}")

    else:
      return
  else:
    await ctx.send("You do not have permission to use this command.")
    await asyncio.sleep(3)
    await prune(ctx, "3")





@bot.event
async def on_message(message):
  if isinstance(message.channel,
                discord.DMChannel) and message.author != bot.user:
    print(f"Received DM from {message.author}: {message.content}")
    if message.content.isdigit() == True:
      if message.content == "123":
        await message.author.send("you are verified")
        await add_role_to_user(message.author.id,1212090229444583464)
      else:
        await message.author.send("invalid code, try again")
  await bot.process_commands(message)


@bot.command()
async def refresh(ctx):
  required_role_id = 1207733658237009920
  required_role = discord.utils.get(ctx.guild.roles, id=required_role_id)
  if required_role in ctx.author.roles:
    await on_ready()
  else:
    await ctx.send("You do not have permission to use this command.")
    await asyncio.sleep(3)
    await prune(ctx, "2")






bot.run(
    'MTIwNjYzMDk4MzYzNDI1NTg3Mg.GbIrWY.f4L3H4eYVc1TPRZXcBKleNWR0yRrcK-Wcm0nPk')


