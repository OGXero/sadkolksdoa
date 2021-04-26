import discord, datetime , time
from discord.ext import commands
import urllib, json
import requests
import asyncio
import datetime 
import time
from datetime import timedelta



start_time = datetime.datetime.utcnow()


client = commands.Bot(command_prefix = 'x.')
client.remove_command('help')
client.sniped_messages = {}
api_key = 'c3097dd33ccdb526cfe3c577f00714ae'
base_url = 'http://api.openweathermap.org/data/2.5/forecast?id=524901&appid=1b6eb48b110e64f8a63ff9a9c9dc1ede'



@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Xero Tek | x.help'))
    print('Xero is Online')

@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=5):
    await ctx.send(f'https://www.bing.com/th/id/OGC.73639896a25ac288701f0522f0eed186?pid=1.7&rurl=https%3a%2f%2fmedia.tenor.com%2fimages%2f73639896a25ac288701f0522f0eed186%2ftenor.gif&ehk=ua73QDNoMwmtlEGNSYo94FgQMGjga8OBbgr2PUWTXvM%3d')
    await ctx.channel.purge(limit=amount)

@client.command()
async def help (ctx):
    embed = discord.Embed(
        title = 'Xero Bot',
        
        colour = discord.Colour.blue()
    )

    embed.set_footer(text='Developer - OGXero')
    embed.set_image(url='')
    embed.set_thumbnail(url='https://cdn.wallpapersafari.com/16/28/GzAPrt.jpg')
    embed.set_author(name='', icon_url='https://cdn.wallpapersafari.com/16/28/GzAPrt.jpg')
    embed.add_field(name='x.admin', value='Shows All Admin Commands.', inline=False)
    embed.add_field(name='x.general', value='Shows All General Commands.', inline=False)
    embed.add_field(name='x.ping', value='Shows Ping.', inline=False)
    embed.add_field(name='x.misc', value ='Shows all Misc Commands.', inline=False )


    await ctx.send(embed=embed)

@client.command()
async def admin(ctx):
   embed = discord.Embed(
      title = 'Admin Commands.',

      colour = discord.Colour.red()
   )

   embed.add_field(name='x.clear (Amount)', value='Deletes Said amount of messages.',inline=False)
   embed.add_field(name='x.ban', value='Bans a Mentioned User',inline=False)
   embed.add_field(name='x.unban', value='Unbans a Mentioned User',inline=False)
   embed.add_field(name='x.kick', value='Kicks a Mentioned User',inline=False)
   embed.add_field(name='x.mute', value='Mutes a Mentioned User',inline=False)
   embed.add_field(name='x.unmute', value='Unmutes a Mentioned User',inline=False)
   embed.add_field(name='Built in Moderation', value='Instant Deletes any Invite Links (Discord.gg)',inline=False)
   embed.set_footer(text='Developer - OGXero')


   await ctx.send(embed=embed)







@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    embed = discord.Embed(
        title = 'Ban',
        description = f"{member} has been banned", color=0x00ffa5
    )
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(manage_messages=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user.mention} ```HAS BEEN UNBANNED```')
            return

@client.command(description='Mutes the specified user.')
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name='Muted')
    

    if not mutedRole:
        mutedRole = await guild.create_role(name='Muted')

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False)

    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f'```{member.mention} has been muted```')
    

    


    



@client.command(description='Unmutes a Specifed user.')
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name='Muted')

    await member.remove_roles(mutedRole)
    await ctx.send(f'```Unmuted {member.mention}```')
        
@client.command(name='ping', help='this command return the latency')
async def ping(ctx):
    embed = discord.Embed(
    title = 'Ping',
    description = f'**XeroTEKs Ping is {round(client.latency * 1000)}ms**'
)
    embed.set_footer(text='Developer - OGXero')
    await ctx.send(embed=embed)
 

@client.command()
async def userinfo(ctx, member: discord.Member):

    roles = [role for role in member.roles]

    embed = discord.Embed(colour=member.colour, timestamp=ctx.message.created_at)

    embed.set_author(name=f'User Info - {member}')
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)

    embed.add_field(name='ID', value=member.id)
    embed.add_field(name='Guild name:', value=member.display_name)

    embed.add_field(name='Created at:', value=member.created_at.strftime('%a, %#d %B %Y, %I:%M %p GMT'))
    embed.add_field(name='Joined at:', value=member.created_at.strftime('%a, %#d %B %Y, %I:%M %p GMT'))

    embed.add_field(name=f'Roles ({len(roles)})', value=''.join([role.mention for role in roles]))
    embed.add_field(name='Top role:', value=member.top_role.mention)

    embed.add_field(name='Bot', value=member.bot)
    

    await ctx.send(embed=embed)

@client.command()
async def general(ctx):
    embed = discord.Embed(
      title = 'General Commands',

      colour = discord.Colour.green()
)

    embed.add_field(name='x.userinfo', value='Shows info on Mentioned User',inline=False)
    embed.add_field(name='x.snipe', value='Shows Deleted message',inline=False)
    embed.add_field(name='x.version', value='Shows Bot Version',inline=False)
    embed.add_field(name='x.invite', value='Shows Bot Invite Code',inline=False)
    embed.set_footer(text='Developer - OGXero')

    await ctx.send(embed=embed)



@client.event
async def on_message_delete(message):
    client.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)

@client.command()
async def snipe(ctx):
    try:
        contents, author, channel_name, time = client.sniped_messages[ctx.guild.id]

    except:
        await ctx.channel.send('```couldnt find a message to snipe```')
        return




    embed = discord.Embed(description=contents, colour=discord.Colour.purple(), timestamp=time)
    embed.set_author(name=f'{author.name}#{author.discriminator}', icon_url=author.avatar_url)
    embed.set_footer(text=f'Deleted in #{channel_name}')

    await ctx.channel.send(embed=embed)

@client.command()
async def version(ctx):
    embed = discord.Embed(
      title = 'Version',
      description = f'Version 1.0.0'
)
    embed.set_footer(text='Developer - OGXero')
    await ctx.send(embed=embed)

@client.command()
async def invite(ctx):
    await ctx.send(f'https://discord.com/api/oauth2/authorize?client_id=835984320140410880&permissions=8&scope=bot')

@client.event
async def on_message(message):
    if 'discord.gg' in message.content.lower():
        await message.delete()
        await message.channel.send('**Do Not Advertise here!**')
        
    await client.process_commands(message)

@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    embed = discord.Embed(title = 'Kicked', description = f"{member} has been Kicked for the reason **{reason}**")    
    await ctx.send(embed=embed)


@client.command()
async def servers(ctx):
    servers = list(client.guilds)
    embed = discord.Embed(title = 'All Guilds Connected To.', description = f'**\n**'.join([guild.name for guild in servers]))
    embed.set_footer(text='Developer - OGXero')
    await ctx.send(embed=embed)
        


@client.command()
async def misc(ctx):
    embed = discord.Embed(
      title = 'Misc Commands.',

      colour = discord.Colour.random()
)

    embed.add_field(name='x.servers', value='shows What servers XeroBOT is in.',inline=False)
    embed.add_field(name='x.spam', value='Spams messages//=stop to stop Spam',inline=False)
    embed.add_field(name='x.uptime', value='Shows XeroTEK Bot Uptime',inline=False)
    embed.set_footer(text='Developer - OGXero')




    await ctx.send(embed=embed)

@client.command()
async def spam(ctx):

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    stopped = False
    await ctx.send("**I AM SPAMMING!**")
    while not stopped:
        try:
            message = await client.wait_for("message", check=check, timeout=1)
            stopped = True if message.content.lower() == "=stop" else False
        except asyncio.TimeoutError: 
            await ctx.send("**I AM SPAMMING!**")
    await ctx.send("**SPAM HAS ENDED!**")

@client.command()
async def uptime(ctx):
    uptime = datetime.datetime.utcnow() - start_time
    uptime = str(uptime).split('.')[0]
    em = discord.Embed(title='__Uptime__', type='Discord', color=0x00EAFF, timestamp=ctx.message.created_at)
    em.add_field(name='Currently running for', value=f'`'+uptime+'`', inline=True)

    
    await ctx.send(embed=em)












    
        

         
    






    
    
    

   
  
 























client.run('ODM1OTg0MzIwMTQwNDEwODgw.YIXZEQ.9zqGKQ0EfKZ9YNsQCLasn0LUyO8')
