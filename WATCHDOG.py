import discord
from discord.ext import commands
import asyncio
from discord.ui import Button,button,View
import chat_exporter
import os
import datetime
import csv
from discord import *
import io
from gmail import send_otp,Name
import otp as o

bot = commands.Bot(
    command_prefix="?",
    intents = discord.Intents.all(),
    status = discord.Status.dnd,
    activity = discord.Activity(type=discord.ActivityType.watching ,name =("over VITians")),
    guild = discord.Object(id = 1203342217519964170)
)




@bot.event
async def on_member_join(member):
    role_id = 1220440238812299345  # Replace with the desired role ID
    role = member.guild.get_role(role_id)
    await member.add_roles(role)





@bot.event
async def on_command_error(ctx, error):
    # Check if the error occurred in the command invocation context
    if ctx:
        # Get the channel ID where you want to send the error message
        error_channel_id = 1216093670084968488  # Replace with the desired channel ID
        async def send_error_message(channel_id, error_message):
            channel = bot.get_channel(channel_id)
            if channel:
                await channel.send(
                    embed = discord.Embed(
                        title="Error Encountered",
                        description=f"An error occurred: {error_message}",
                        color=discord.Color.red()
                        ).add_field(name="User", value=ctx.author.mention, inline=False
                        ).add_field(name="Channel", value=ctx.channel.mention, inline=False
                        )
                    )
            else:
                print(f"Channel with ID {channel_id} not found.")

        await send_error_message(error_channel_id, error)
    else:
        print(f"An error occurred outside of a command invocation: {error}")
        
        
        
        
@bot.event
async def on_command(ctx):
    channel_id = 1216397600387895297
    async def send_command_log(channel_id):
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(
                embed=discord.Embed(
                    title="Command Invoked",
                    description=f"Command: {ctx.command}",
                    color=discord.Color.dark_teal()
                ).add_field(name="User", value=ctx.author.mention, inline=False
                ).add_field(name="Channel", value=ctx.channel.mention 
                            if not isinstance(ctx.channel,discord.DMChannel) 
                            else "Direct Messages",inline=False
                )
            )
        else:
            print(f"Channel with ID {channel_id} not found.")

    await send_command_log(channel_id)




@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    channel = bot.get_channel(1207734746981998614)
    hello = discord.Embed(
        title=f"Hello from {bot.user.display_name}",
        color=0x00FFFF,
        timestamp=datetime.datetime.now(),
    )
    try:
        hello.set_thumbnail(url=bot.user.avatar.url)
    except AttributeError:  
        hello.set_thumbnail(url="https://wallpaper.dog/large/10964102.jpg")
    hello.add_field(
        name="What can Watchdog do!",
        value=f"{bot.user.display_name} can help you create tickets, teams, verify yourself and much more!",
        inline=False,
    )
    await channel.send(embed=hello)
    bot.add_view(CreateButton())
    bot.add_view(CloseButton())
    bot.add_view(TrashButton())
    bot.add_view(CreateTeamButton())
    bot.add_view(verifyButton())
    bot.add_view(InviteToTeamButton())
    # bot.add_view(NicknameButton())




class verifyButton(View):
    def __init__(self):
        super().__init__(timeout=None)
        
        
    @button(label="Rename", style=discord.ButtonStyle.primary, custom_id="rename", emoji="✏️")   
    async def invite(self, interaction: discord.Interaction, button: Button):
        guild = bot.get_guild(1203342217519964170)
        renamemodal = Renamemodal()
        await interaction.response.send_modal(renamemodal)
        
            
    @button(label="Verify ✅", style=discord.ButtonStyle.success, custom_id="verify")
    async def verify(self, interaction: discord.Interaction, button: Button):
        # await interaction.response.defer(ephemeral=True)
        role = interaction.guild.get_role(1212090229444583464)
        for member in role.members:
            name1 = (member.nick).split() 
            if interaction.user.nick == name1[2]:
                await interaction.response.send_message(
                embed=discord.Embed(
                title="Multiple accounts detected!",
                description="You have already been verified on another account, please log in using that account!",
                color=discord.Color.red()
                ), ephemeral=True
                )
                del name1
                return
            
            
        if role in interaction.user.roles:
            await interaction.response.send_message(embed=discord.Embed(
                title="You are already verified!",
                description="You have already been verified and have the 'Verified' role.",
                color=discord.Color.red()
            ), ephemeral=True)
            return
        verification_modal = verifymodal()  # Pass name1 and otp1
        await interaction.response.send_modal(verification_modal)
        otp = send_otp(interaction.user.nick)
        o.write(interaction.user.nick,otp)
    
class CreateButton(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Create Ticket",style=discord.ButtonStyle.blurple, emoji="🎫",custom_id="ticketopen")
    async def ticket(self, interaction: discord.Interaction, button: Button):
        #await interaction.response.defer(ephemeral=True)
        ticketmodal = Ticketmodal()
        await interaction.response.send_modal(ticketmodal)
class CloseButton(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Close the ticket",style=discord.ButtonStyle.red,custom_id="closeticket",emoji="🔒")
    async def close(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        ticketcategory = discord.utils.get(interaction.guild.categories, id=1213021742780514336)
        if interaction.channel.category != ticketcategory:
            await interaction.channel.send(
                embed = Embed(
                title="Error",
                description="This is not a ticket channel!",
                color=discord.Color.red()
            ))
            return
        await interaction.channel.send("Closing this ticket",delete_after=5)

        category: discord.CategoryChannel = discord.utils.get(interaction.guild.categories, id = 1214909385600671745)
        r1 : discord.Role = interaction.guild.get_role(1216053106064887980)
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            r1: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        await interaction.channel.edit(category=category, overwrites=overwrites)
        await interaction.channel.send(
            embed= discord.Embed(
                description="--------------Ticket Closed!--------------",
                color = discord.Color.red()
            ),
            view = TrashButton()
        )
        await log(interaction.channel)  
class TrashButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Delete the ticket", style=discord.ButtonStyle.red, emoji="🚮", custom_id="trash")
    async def trash(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()
        await interaction.channel.send("Deleting the ticket in 3 seconds")
        await asyncio.sleep(3)

        await interaction.channel.delete()    
class CreateTeamButton(View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @button(label="Create Team", style=discord.ButtonStyle.secondary, custom_id="team_create_button", emoji="🦁")

    async def team(self, interaction: discord.Interaction, button: Button):
        role1 = interaction.guild.get_role(1216328643014299709)
        role2 = interaction.guild.get_role(1214133687181123624)
        if role1 in interaction.user.roles or role2 in interaction.user.roles:
            await interaction.response.send_message(embed = discord.Embed(
                        title="You are already in a team!",
                        description="You are already in a team and have the 'Team' role.",
                        color=discord.Color.red()
                        ),ephemeral=True
                    )
            return
        teammodal = Teammodal()
        await interaction.response.send_modal(teammodal) 
class InviteToTeamButton(View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @button(label="Invite a Member!", style=discord.ButtonStyle.green, custom_id="invite_to_team", emoji="🦅")   
    async def invite(self, interaction: discord.Interaction, button: Button):
        guild = bot.get_guild(1203342217519964170)
        channel = interaction.channel
        role = guild.get_role(1216328643014299709)
        counter = 0 
        for member in channel.members:
            if role in member.roles:
                counter+=1
        if counter >=5:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Team Full!",
                    description="You can't invite more members to this team as it is already full.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return
        invitemodal = Invitemodal()
        await interaction.response.send_modal(invitemodal)
      
    
    @button(label = "leave team", style = discord.ButtonStyle.red,custom_id="leave_team",emoji = "🏴‍☠️")
    async def leave(self, interaction: discord.Interaction, button: Button):
        guild = bot.get_guild(1203342217519964170)
        channel1 = interaction.channel
        teamlead = guild.get_role(1214133687181123624)
        teammember = guild.get_role(1216328643014299709)
        if teamlead in interaction.user.roles and teammember in interaction.user.roles:
            await interaction.response.send_modal(leadleavemodal()) 
        elif teammember in interaction.user.roles:
            await interaction.response.send_modal(memberleavemodal())
  
        
    
        
class memberleavemodal(ui.Modal,title = "Leave Team"):
    guild = bot.get_guild(1203342217519964170)
    answer = ui.TextInput(label="Are you sure you want to Leave this Team?",
                          style=discord.TextStyle.short,
                          placeholder="Please enter the team name to confirm! (discord channel name)",
                          # default = "___",
                          required=True,
                          min_length=3,
                          max_length=15)
    async def on_submit(self, interaction: discord.Interaction):
        if self.answer.value != interaction.channel.name:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Incorrect Team Name!",
                    description="The team name you entered does not match the team name.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return
        teamname = self.answer.value
        channel = interaction.channel
        role = interaction.guild.get_role(1216328643014299709) 
        
        # overwrite = channel.overwrites_for(interaction.user)
        # overwrite.update( read_messages=False, send_messages=False)
        # await channel.set_permissions(interaction.user, overwrite=overwrite)
        
        overwrites = channel.overwrites
        if interaction.user in overwrites: 
            del overwrites[interaction.user]
            await channel.edit(overwrites=overwrites)
        await interaction.user.remove_roles(role)
        await interaction.response.defer(ephemeral=True)
        await interaction.user.send(
            embed=discord.Embed(
                title="Team Left!",
                description=f"You have left the team {teamname}.",
                color=discord.Color.green()
            )
        )  
        await channel.send(
            embed=discord.Embed(
                title="[-]  Team Left!",
                description=f"{interaction.user.mention} has left the team.",
                color=discord.Color.green()
            )
        )

        return 
class leadleavemodal(ui.Modal,title = "Leave Team"):
    
    answer = ui.TextInput(label="Warning! Team will be deleted once you leave",
                          style=discord.TextStyle.short,
                          placeholder="Please enter the team name to confirm! (discord channel name)",
                          # default = "___",
                          required=True,
                          min_length=3,
                          max_length=15)
    async def on_submit(self, interaction: discord.Interaction):
        if self.answer.value != interaction.channel.name:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Incorrect Team Name!",
                    description="The team name you entered does not match the team name.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return   
        teamname = self.answer.value
        channel = interaction.channel
        guild = bot.get_guild(1203342217519964170)
        teamlead = guild.get_role(1214133687181123624)
        teammember = guild.get_role(1216328643014299709)
        await interaction.user.remove_roles(teamlead)
        await interaction.response.defer(ephemeral=True)
        memberlist = []
        for member in channel.members:
            if teammember in member.roles:
                memberlist.append(member)
        await channel.delete()
        for member in memberlist:
            await member.remove_roles(teammember)
            await member.send(
                embed=discord.Embed(
                    title="Team deleted!",
                    description=f"Your team : {channel.name} has been deleted\nthe leader {interaction.user.nick} left the team",
                    color=discord.Color.red()
                )
            )
        del memberlist

        
         

class verifymodal(ui.Modal, title="Verification"):


    guild = bot.get_guild(1203342217519964170)
    answer = ui.TextInput(label="Enter the OTP",
                          style=discord.TextStyle.short,
                          placeholder="Enter the OTP we sent you through Mail!",
                          # default = "___",
                          required=True,
                          min_length=8,
                          max_length=8)

    async def on_submit(self, interaction: discord.Interaction):
        otp = o.show(interaction.user.nick)
        if self.answer.value==str(otp):  # Check against the OTP you sent
            unverified = interaction.guild.get_role(1220440238812299345)
            role = interaction.guild.get_role(1212090229444583464)
            await interaction.user.add_roles(role)
            await interaction.response.send_message(embed=discord.Embed(
                title="Congratulations!",
                description="You have been verified and given the 'Verified' role.",
                color=discord.Color.gold()
            ), ephemeral=True)
            await asyncio.sleep(10)
            await interaction.user.remove_roles(unverified)
            newnick = Name(interaction.user.nick) + " " + interaction.user.nick
            await interaction.user.edit(nick=newnick)
            

        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Incorrect OTP! Please try again!",
                    description="You will be verified once you enter the correct otp!",
                    color=discord.Color.red()
                ), ephemeral=True)
        
class Renamemodal(ui.Modal,title = "Rename"):
    guild = bot.get_guild(1203342217519964170)
    answer = ui.TextInput(label="Enter your Registeration number!",
                          style = discord.TextStyle.short,
                          placeholder="Registeration Number",
                          #default = "___",
                          required=True,
                          min_length=10,
                          max_length=10)
    
    async def on_submit(self, interaction: discord.Interaction):
        nickname = self.answer.value
        await interaction.user.edit(nick=nickname.upper())
        await interaction.response.send_message(embed = discord.Embed(
                        title="Nicknamed!",
                        description="You have been nicknamed to your entered Registeration Number",
                        color=discord.Color.gold()
                        ),ephemeral=True
                    )
        

class Invitemodal(ui.Modal,title = "Invite"):
    guild = bot.get_guild(1203342217519964170)
    answer = ui.TextInput(label="Add a Member",
                          style = discord.TextStyle.long,
                          placeholder="Enter the registeration number of the member you want to invite!",
                          #default = "Not Provided",
                          required=True,
                          min_length=10,
                          max_length=10)
    async def on_submit(self, interaction: discord.Interaction):
        guild = bot.get_guild(1203342217519964170)
        channel = interaction.channel
        role = guild.get_role(1216328643014299709)
        counter = 0 
        for member in channel.members:
            if role in member.roles:
                counter+=1
        if counter >=5:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Team Full!",
                    description="You can't invite more members to this team as it is already full.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return        
        member_regno = (self.answer.value)
        member = await finduser(member_regno)
        if member == None:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Invalid!",
                    description="The user you entered was not found in the server.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return
        verifiedrole = interaction.guild.get_role(1212090229444583464)
        unverifiedrole = interaction.guild.get_role(1220440238812299345)
        # if (verifiedrole not in member.roles) or (unverifiedrole in member.roles) :
        #     await interaction.response.send_message(
        #         embed=discord.Embed(
        #             title="Verification Error",
        #             description="The user you want to add is not a Verified VITian",
        #             color=discord.Color.red()
        #         ),
        #         ephemeral=True
        #     )
        #     return
        role = interaction.guild.get_role(1216328643014299709)
        if role in member.roles:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="User already in a team!",
                    description="The user you entered is already in a team.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return
        await interaction.response.send_message(
            embed=discord.Embed(
                title="User added",
                description=f"{member.mention} has been added to your team.",
                color=discord.Color.green()
            ),
            ephemeral=True
        )
        await member.add_roles(role)
        channel = interaction.channel
        await channel.set_permissions(member, read_messages=True, send_messages=True)
        await channel.send(
            embed=discord.Embed(
                title="[+]  Team Joined!",
                description=f"{member.mention} has joined the team.",
                color=discord.Color.green()
            )
        )
        await member.send(
            embed=discord.Embed(
                title="Team Joined!",
                description=f"You have been added to a team in {interaction.guild.name}.",
                color=discord.Color.green()
            )
        )
        



class Ticketmodal(ui.Modal,title = "Ticket"):
    guild = bot.get_guild(1203342217519964170)
    answer = ui.TextInput(label="Create Ticket!",
                          style = discord.TextStyle.paragraph,
                          placeholder="Reason to Create this ticket :",
                          #default = "Not Provided",
                          required=True,
                          min_length=5,
                          max_length=50)


    async def on_submit(self, interaction: discord.Interaction):
        reason = self.answer.value
        #interaction.response.send_message("you requested to create a ticket! with the reason : {0}".format(reason),ephemeral=True)
        category: discord.CategoryChannel = discord.utils.get(interaction.guild.categories, id=1213021742780514336)
        for ch in category.text_channels:
            if ch.topic == f"{interaction.user.id} DO NOT CHANGE THE TOPIC OF THIS CHANNEL!":
                await interaction.response.send_message("You already have a ticket in {0}".format(ch.mention), ephemeral=True)
                return

        r1 : discord.Role = interaction.guild.get_role(1216053106064887980)
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            r1: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True),
            interaction.user: discord.PermissionOverwrite(read_messages = True, send_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        chname = interaction.user.nick.split()
        channel = await category.create_text_channel(
            name=(f"🐧{chname[-1]}-Ticket"),
            topic=f"{interaction.user.id} DO NOT CHANGE THE TOPIC OF THIS CHANNEL!",
            overwrites=overwrites
        )
        await channel.send(embed = discord.Embed(
                title="Ticket Created!",
                description=f"Don't ping a staff member, they will be here soon.\n\n-----------------\n{interaction.user.mention}'s ticket",
                color=discord.Color.green()).set_thumbnail(url=bot.user.avatar.url).set_author(name="BumbleBee", url=bot.user.avatar.url)
                .add_field(name="Issue", value=reason, inline=False),
                view = CloseButton()
                )
        await interaction.response.send_message(
            embed= discord.Embed(
                description = "Created your ticket in {0}".format(channel.mention),
                color = discord.Color.blurple()
            ),
            ephemeral=True
        )
class Teammodal(ui.Modal,title = "Team!"):
    guild = bot.get_guild(1203342217519964170)
    answer = ui.TextInput(label="Create Team!",
                          style = discord.TextStyle.short,
                          placeholder="What would you like to name your team?",
                          #default = "Not Provided",
                          required=True,
                          min_length=3,
                          max_length=15)


    async def on_submit(self, interaction: discord.Interaction):
        Teamname = self.answer.value
        #interaction.response.send_message("you requested to create a ticket! with the reason : {0}".format(reason),ephemeral=True)
        category: discord.CategoryChannel = discord.utils.get(interaction.guild.categories, id=1214133586232475708)
        for ch in category.text_channels:
            if ch.topic == f"{interaction.user.id}'s team, DO NOT CHANGE THE TOPIC OF THIS CHANNEL!":
                await interaction.response.send_message(f"You already are a part of a Team => {ch.mention}", ephemeral=True)
                return

        r1 : discord.Role = interaction.guild.get_role(1216053106064887980)
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            r1: discord.PermissionOverwrite(read_messages=False, send_messages=False, manage_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages = True, send_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        channel = await category.create_text_channel(
            name=f"{Teamname}",
            topic=f"{interaction.user.id}'s team, DO NOT CHANGE THE TOPIC OF THIS CHANNEL!",
            overwrites=overwrites
        )
        rolelead = interaction.guild.get_role(1214133687181123624)
        await interaction.user.add_roles(rolelead)
        roleteam = interaction.guild.get_role(1216328643014299709)
        await interaction.user.add_roles(roleteam)
        await interaction.response.send_message(
            embed= discord.Embed(
                title="team created",
                description = f"Created your Team {channel.mention}",
                color = discord.Color.blurple()
            ),ephemeral=True
        )   
        await channel.send(
            embed=discord.Embed(
                title=f"{Teamname}",
                description=f"The Team was created by {interaction.user.mention}\nInvite a Member\n• They must be in the server!\n• They must be verified!\n• They must not be in a team!",
                color = discord.Color.greyple()
            ),
            view = InviteToTeamButton()
            #view = CloseButton() -> link to invite more member's button!!!
        )
        


async def log(channel: discord.TextChannel):
    logs = ""
    counter = 0
    async for message in channel.history(limit=None, oldest_first=True):
        timestamp = message.created_at.strftime('%Y-%m-%d %H:%M:%S')
        sender = message.author.name
        content = message.content
        logs += f"{timestamp} | {sender}: {content}\n"

    # Create an in-memory buffer to store the logs
    log_buffer = io.BytesIO(logs.encode('utf-8'))
    log_buffer.seek(0)
    
  # Create the embed object
    embed = discord.Embed(
        title=f"Log for #{channel.name}",
        description=f"Log: {channel.id}",
        timestamp=message.created_at  # Use the latest message's timestamp
  )
    # Get the log upload channel
    guild = channel.guild
    log_upload_channel = discord.utils.get(guild.channels, id=1220744583491620965)
    
    async for messages in log_upload_channel.history(limit = None):
        counter+=1
    # Upload the logs as a .txt file
    messagelog = await log_upload_channel.send( file=discord.File(log_buffer, filename=f"LOG {counter+1} {channel.name}.txt"))
    




@bot.command(name = "prune")
async def delete_messages(ctx, amount ="none"):
    if ctx.author.guild_permissions.administrator:
        if amount == "none":
            await ctx.send("Please specify the amount of messages to delete")
        elif amount.isdigit():
            await ctx.channel.purge(limit=int(amount))
            await ctx.send(f"Deleted {amount} messages", delete_after=5)
        elif amount == "all":
            await ctx.channel.purge(limit=None)
            await ctx.send("Deleted all messages", delete_after=5)
        else:
            await ctx.send("Please enter a valid number")
    else:
        await ctx.send("You don't have the permission to use this command")





@bot.command(name  = "start")
#@commands.has_permissions(administrator=True)
async def start(ctx):
    if ctx.guild is None:
        await ctx.send("This command can only be used in the Ease Exhibit server")
        return
    role = ctx.guild.get_role(1221538414847856700)    
    if not role in ctx.author.roles:
        await ctx.send("You don't have the permission to use this command",delete_after=5)
        return
    await ctx.channel.purge(limit=1)
    ticketchannel = bot.get_channel(1212442019302215700)
    await ticketchannel.purge()
    await ticketchannel.send(
        embed = discord.Embed(
            description = "press the button to create a new ticket!"
        ),
        view = CreateButton()
    )
    teamchannel = bot.get_channel(1212798572886757436)
    await teamchannel.purge()
    await teamchannel.send(
        embed=discord.Embed(
            description="click the button to create a new team!"
        ),
        view = CreateTeamButton()
    )
    # await nickchannel.purge()
    # await nickchannel.send(
    #     embed=discord.Embed(
    #         title = "Click the button Rename yourselves!",
    #         description="• Please make sure your nickname is set to your VIT Registeration Number before verifying!\n  • PS : Give the Devs a coffee Treat!"
    #     ),
    #     view = NicknameButton()
    # )
    verifychannel=bot.get_channel(1212094690514698331)
    await verifychannel.purge()
    await verifychannel.send(
        
        embed = discord.Embed(
            title = "Click the button below to start the verification process!",
            description=f"• Please make sure your nickname is set to your VIT Registeration Number before verifying!\n  • Please use the Rename Button to Nickname Yourselves!\n  • PS : Give the Devs a coffee Treat!"
        ),
        view = verifyButton()
    )
   


async def finduser(regno):
    guild = bot.get_guild(1203342217519964170)
    verifiedrole = guild.get_role(1212090229444583464)
    requser=None
    for member in verifiedrole.members:
        name1 = (member.nick).split()
        if name1[2] == regno:
            requser=member
            break
 # Return None if the user is not found
    return requser


@bot.command(name = "restart")
async def close_bot(ctx):
    required_role_id = 1221538414847856700
    required_role = discord.utils.get(ctx.guild.roles, id=required_role_id)
    if required_role in ctx.author.roles:
        await ctx.send("Closing the bot...")
        await bot.close()
    else:
        await ctx.send("You don't have the permission to use this command")   




bot.run(os.getenv('DISCORD_TOKEN'))
