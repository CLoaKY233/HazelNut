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
from gmail import *
import otp as o
import writer
import gc



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
            if interaction.user.nick == name1[-1]:
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
         
        
class TrashButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Delete the ticket", style=discord.ButtonStyle.red, emoji="🚮", custom_id="trash")
    async def trash(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()
        await log(interaction.channel) 
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
    
    @button(label = "Join Team",style = discord.ButtonStyle.green,custom_id="team_join_button",emoji = "🐯")
    async def jointheteam(self, interaction:discord.Interaction,button:Button):
        memberrole= interaction.guild.get_role(1216328643014299709)
        verifiedrole = interaction.guild.get_role(1212090229444583464)
        if verifiedrole not in interaction.user.roles:
            await interaction.response.send_message(embed = discord.Embed(
                        title="Verification Error",
                        description="You are not a Verified VITian",
                        color=discord.Color.red()
                        ),ephemeral=True
                    )
            return
        if memberrole in interaction.user.roles:
            await interaction.response.send_message(embed = discord.Embed(
                        title="You are already in a team!",
                        description="You are already in a team.",
                        color=discord.Color.red()
                        ),ephemeral=True
                    )
            return
        joinmodal = teamjoinmodal()
        await interaction.response.send_modal(joinmodal)
        
    
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
    answer = ui.TextInput(label="DO NOT CLOSE THIS WINDOW",
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
        
        member = await finduser(self.answer.value)   
        if member == None:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Invalid!",
                    description="The user you want to invite is either unverified or not in the server yet!.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return
        memberrole = interaction.guild.get_role(1216328643014299709)   
        if memberrole in member.roles:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="User already in a team!",
                    description="The user you want to invite is already in a team.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return
        if member is not None:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title=f"{member.nick} has been invited!",
                    description=f"An invitation mail has been sent to the {member.nick} to join the team!\nThis invite will expire tonight",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            interaction.response.defer
            inviter=(interaction.user.nick).split()
            invitecode = send_invite(self.answer.value,channel.name,inviter[-1])
            
            o.writeinvite(member.nick,invitecode,inviter[-1],interaction.channel.id)
            



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
                .add_field(name="Issue", value=reason, inline=True),
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
            if ch.topic == f"{interaction.user.id}":
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
            topic=f"{interaction.user.id}",
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
                    description=(
                        f"**Team Creator:** {interaction.user.mention}\n\n"
                        "🚀 **Welcome to the Team!** 🚀\n"
                        "Congratulations on creating your team! Now it's time to invite members.\n\n"
                        "**Invite a Member:**\n"
                        "To invite a member to your team, follow these steps:\n"
                        "1. **Check Requirements:** Ensure they are in the server, verified, and not in a team.\n"
                        "2. **Use the Invite Link:** Share the team's invite code with them using the button below!.\n"
                        "3. **Confirm Membership:** Once they join, they'll be added to your team.\n\n"
                        
                    ),
                    color=discord.Color.greyple()
                ).set_thumbnail(url="https://s3-ap-south-1.amazonaws.com/static.awfis.com/wp-content/uploads/2017/07/07184649/ProjectManagement.jpg"),
            view = InviteToTeamButton()
            #view = CloseButton() -> link to invite more member's button!!!
        )
        
class teamjoinmodal(ui.Modal,title = "Join Team"):
    guild = bot.get_guild(1203342217519964170)
    answer1 = ui.TextInput(label="Join Team",
                          style = discord.TextStyle.short,
                          placeholder="Inviter's registeration number here",
                          #default = "Not Provided",
                          required=True,
                          min_length=10,
                          max_length=10)
    answer2 = ui.TextInput(label="Validate invite",
                            style = discord.TextStyle.short,
                            placeholder="Team-code here",
                            required = True,
                            min_length = 8,
                            max_length = 8)
    async def on_submit(self, interaction: discord.Interaction):
        inviter = self.answer1.value
        teamcode = self.answer2.value
        otp,Name,channelid = None,None,None
        otp,name,channelid = o.verifyinvite(interaction.user.nick)
        Team = bot.get_channel(channelid)
        if Team == None:
            await interaction.response.send_message(
                embed=discord.Embed(
                title="Validation failed",
                description=f"Invitation is Invalid!",
                color=discord.Color.red() 
                ),ephemeral=True
            )
            return
        
        guild = bot.get_guild(1203342217519964170)
        memberrole = guild.get_role(1216328643014299709)
        counter = 0 
        for member in Team.members:
            if memberrole in member.roles:
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
        
        #check if team exists
        #check if team limit
        #check if verified
        #check if invite valid
        if (otp == teamcode) and (inviter == name):
            await interaction.user.add_roles(memberrole)
            channel = Team
            o.delete(interaction.user.nick)
            
            await channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
            await channel.send(
                embed=discord.Embed(
                    title="[+]  Team Joined!",
                    description=f"{interaction.user.mention} has joined the team.",
                    color=discord.Color.green()
                )
            )
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Team Joined!",
                    description=f"You have been added to {Team.mention}",
                    color=discord.Color.green()
                ),ephemeral=True
            )
        else:
            await interaction.response.send_message(
            embed=discord.Embed(
                title="Validation failed",
                description=f"Please re-enter the correct credentials as recieved in the mail!",
                color=discord.Color.red()
            ),
            ephemeral=True
            )
            return
        
        

    
    

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
            await ctx.channel.purge(limit=int(amount+1))
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
                title="Ticket Creation",
                description=(
                    "Welcome to our support system! You can create a new ticket by pressing the button below."
                    "\n\n**Please Note**: This is the preferred method for requesting support. "
                    "Our team will assist you as soon as possible."
                ),
                color=discord.Color.blurple()
                ).set_thumbnail(url="https://www.kindpng.com/picc/m/4-41705_support-the-developer-hd-png-download.png")
                .add_field(name="Need Help?", value="If you encounter any issues or have questions, feel free to reach out to us."),
        view = CreateButton()
    )
    teamchannel = bot.get_channel(1212798572886757436)
    await teamchannel.purge()
    await teamchannel.send(
        embed=discord.Embed(
            title="Team Management",
            description=(
                "To get started with team management, follow the steps below:\n\n"
                "1. **Create a New Team**:\n"
                "   Use the <Create Team Button> below to create a new team.\n\n"
                "2. **Join an Existing Team**:\n"
                "   Use the <Join Team Button> below to join an existing team.\n\n"
                "**Please Note**:\n"
                "- To join a team, you must have an invitation from the respective team leader.\n"
                "- You can not join multiple teams simultaneously.\n"
                "- Check your email to see if you have received an invitation.\n"
            ),
            color=discord.Color.blurple())
            .set_thumbnail(url = "https://tryinch.com/wp-content/uploads/2021/11/team-management_2.jpg"),
            view = CreateTeamButton()
    )


    verifychannel=bot.get_channel(1212094690514698331)
    await verifychannel.purge()
    await verifychannel.send(
        
        embed = discord.Embed(
            title="Start Verification Process",
            description=(
                "Click the button below to begin the verification process.\n\n"
                "**Verification Instructions:**\n"
                "• Ensure your nickname is set to your VIT Registration Number before verifying.\n"
                "• Use the Rename Button to set your nickname.\n\n"
                "Thank you for your cooperation!"
            ),
            color=discord.Color.green()  # Adjust color to match the theme
        ).set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQlRyVgpE3fM5dPUvhgEi8GZw-UyprX6juXLO8ThHO4DQ&s")
        .set_author(name="WATCHDOG"),
        view = verifyButton()
    )
    
    
    rules1 = bot.get_channel(1220786021399007388)

    await rules1.purge()

    await rules1.send(
        embed=discord.Embed(
            title="RULES AND REGULATIONS",
            description=(
                "-------------------------------------------------------------------------------------\n"
                "1. All students registering/participating in Project Exhibition must adhere to the rules and guidelines.\n\n"
                "2. Failure to comply with these guidelines might and will reward cancellation of your current project exhibition.\n"
                "-------------------------------------------------------------------------------------\n\n"
                "__\n__\n__\n__\n"
            )
        )
        .add_field(
            name="Section 1, General Rules",
            value=(
                "\n-------------------------------------------------------------------------------------\n"
                "• Be respectful: Treat others with kindness and respect.\n\n"
                "• No discrimination: Avoid any form of discrimination or hate speech.\n\n"
                "• No spam or self-promotion: Refrain from spamming or excessive self-promotion.\n\n"
                "• Respect privacy: Keep personal information private.\n\n"
                "• Follow Discord's rules: Adhere to Discord's Terms of Service.\n\n"
                "• No NSFW content: Avoid sharing explicit or inappropriate content.\n\n"
                "• Listen to moderators: Follow instructions from moderators.\n\n"
                "• Report violations: Report any rule violations to moderators.\n"
                "-------------------------------------------------------------------------------------\n"
                "__\n__\n__\n__\n"
            ),inline=False
        )
        .add_field(
            name="Section 2, Special Rules",
            value=(
                "-------------------------------------------------------------------------------------\n"
                "\n"
                "1. **Ticket Channel:**\n\n"
                "• Use it for issues and questions.\n\n"
                "• Create a ticket for assistance.\n\n"
                "• Close tickets when resolved.\n\n"
                "\n"
                "2. **Team Channel:**\n\n"
                "• Form teams for activities.\n\n"
                "• Keep discussions organized.\n\n"
                "• Respect others' choices."
                "\n-------------------------------------------------------------------------------------\n"
            ),inline=False
        )
        .set_footer(text="CLoaKY\nOwner | Dev | Admin")
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


@bot.command(name = "exportdata")
async def maketeamlist(ctx):
    required_role = discord.utils.get(ctx.guild.roles, id=1221538414847856700)
    if required_role not in ctx.author.roles:
        print(o)
        return
    category = discord.utils.get(ctx.guild.categories, id=1214133586232475708)
    teammemberrole = discord.utils.get(ctx.guild.roles, id=1216328643014299709)   
    n = 0
    channel_counter = 0
    for channel in category.channels:
        channel_counter+=1
        teamlist = [] 
        member_counter = 0
        teamname = channel.name
        
        for member in channel.members:
            if teammemberrole in member.roles:
                member_counter+=1
                reg = member.nick.split()
                teamlist.append(reg[-1])
        n= writer.write(n,member_counter,channel_counter,teamname,teamlist)        
    target_channel_id = 1226460657684316190
    target_channel = ctx.guild.get_channel(target_channel_id)
    if "teams.xlsx" not in os.listdir():
        return
    if target_channel:
        with open('teams.xlsx', 'rb') as file:
            await target_channel.send(file=discord.File(file, 'teams.xlsx'))
        os.remove("teams.xlsx")
    else:
        print("Target channel not found.")            
    







@bot.command(name = "restart")
async def close_bot(ctx):
    required_role_id = 1221538414847856700
    required_role = discord.utils.get(ctx.guild.roles, id=required_role_id)
    if required_role in ctx.author.roles:
        await ctx.send("Closing the bot...")
        await bot.close()
    else:
        await ctx.send("You don't have the permission to use this command")   



cache_clearing_enabled = True  # Initialize cache clearing as enabled by default

@bot.command(name='cacheclear')
async def clear_cache(ctx, mode=None):
    required_role_id = 1221538414847856700  # Replace with your actual role ID
    
    # Check if the user has the required role
    required_role = discord.utils.get(ctx.guild.roles, id=required_role_id)
    if required_role not in ctx.author.roles:
        await ctx.send("You don't have permission to use this command.")
        return

    global cache_clearing_enabled

    if mode is None:
        if cache_clearing_enabled:
            await ctx.send("Cache clearing is currently enabled. Garbage collection will be triggered when you use the `?cacheclear` command.")
        else:
            await ctx.send("Cache clearing is currently disabled. Garbage collection will no longer be triggered automatically.")
    elif mode == "on":
        cache_clearing_enabled = True
        await ctx.send("Cache clearing enabled. Garbage collection will be triggered when you use the `?cacheclear` command.")
    elif mode == "off":
        cache_clearing_enabled = False
        await ctx.send("Cache clearing disabled. Garbage collection will no longer be triggered automatically.")
    else:
        await ctx.send("Invalid usage. Use `?cacheclear` to check status, `?cacheclear on` to enable, or `?cacheclear off` to disable.")
        return

    if cache_clearing_enabled:
        gc.collect()
        await ctx.send("Triggered garbage collection to help free up memory. For significant memory improvements, consider code optimization or restarting the bot periodically.")
    else:
        await ctx.send("Cache clearing is currently disabled. Use `?cacheclear on` to enable it.")


bot.remove_command('help')

@bot.command(name='help')
async def help_command(ctx, command=None):
    if command is None:
        embed = discord.Embed(title='Bot Commands', description='List of available commands:', color=discord.Color.blue())
        
        # Add command descriptions
        embed.add_field(name='?help', value='Displays the list of available commands.', inline=False)
        embed.add_field(name='?prune [amount]', value='Deletes the specified number of messages in the current channel.', inline=False)
        embed.add_field(name='?start', value='Starts the bot.', inline=False)
        embed.add_field(name='?exportdata', value='Exports team data to an Excel file.', inline=False)
        embed.add_field(name='?restart', value='Restarts the bot (requires admin role).', inline=False)
        embed.add_field(name='?cacheclear [mode]', value='Clears the bot cache (requires admin role).', inline=False)
        
        # Add additional information and interaction instructions
        embed.add_field(name='ℹ️ Additional Information', value='To get more details about a specific command, use `?help [command]`.\nFor example, `?help prune` will provide information about the `prune` command.', inline=False)
        embed.add_field(name='🔄 Refresh Help', value='To refresh the help message, use `?help` again.', inline=False)
        
        await ctx.send(embed=embed)
    else:
        if command == 'help':
            description = 'Displays the list of available commands.'
        elif command == 'prune':
            description = 'Deletes the specified number of messages in the current channel.'
        elif command == 'start':
            description = 'Starts the bot.'
        elif command == 'exportdata':
            description = 'Exports team data to an Excel file.'
        elif command == 'restart':
            description = 'Restarts the bot (requires admin role).'
        elif command == 'cacheclear':
            description = 'Clears the bot cache (requires admin role).'
        else:
            await ctx.send(f"Command '{command}' not found. Use `?help` to see the list of available commands.")
            return
        
        embed = discord.Embed(title=f'Command: {command}', description=description, color=discord.Color.blue())
        await ctx.send(embed=embed)











bot.run(os.getenv('DISCORD_TOKEN'))



