import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import json
import asyncio



description = '''The official r/ruperrt bot.'''
bot = commands.Bot(command_prefix='r/', description=description)

bot.remove_command('help')



with open('reports.json', encoding='utf-8') as f:
  try:
    report = json.load(f)
  except ValueError:
    report = {}
    report['users'] = []

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print('------')

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello There! {ctx.author.mention}")

@bot.command()
async def faq(ctx):
    embed=discord.Embed(title="r/ruperrt Bot FAQ", description="**Can i apply for staff?** \n Yes, Check out #applications! \n **Can I post things on the subreddit?** \n Yes, if it is approved. \n **Who can i speak to if i need support or some form of help?** \n If you need support, please create a ticket. \n **I have found a rule breaker, what do i do?** \n You can report them to staff with /report <player> <reason> \n **Can i advertise my discord?** \n Unless stated, No.")
    await ctx.send(embed=embed)


@bot.command()
async def help(ctx):
        em = discord.Embed(title="Auroris Tickets Help", description="", color=0x00a8ff)
        em.add_field(name="`.new <message>`", value="This creates a new ticket. Add any words after the command if you'd like to send a message when we initially create your ticket.")
        em.add_field(name="`.close`", value="Use this to close a ticket. This command only works in ticket channels.")
        em.add_field(name="`.addaccess <role_id>`", value="This can be used to give a specific role access to all tickets. This command can only be run if you have an admin-level role for this bot.")
        em.add_field(name="`.delaccess <role_id>`", value="This can be used to remove a specific role's access to all tickets. This command can only be run if you have an admin-level role for this bot.")
        em.add_field(name="`.addpingedrole <role_id>`", value="This command adds a role to the list of roles that are pinged when a new ticket is created. This command can only be run if you have an admin-level role for this bot.")
        em.add_field(name="`.delpingedrole <role_id>`", value="This command removes a role from the list of roles that are pinged when a new ticket is created. This command can only be run if you have an admin-level role for this bot.")
        em.add_field(name="`.addadminrole <role_id>`", value="This command gives all users with a specific role access to the admin-level commands for the bot, such as `.addpingedrole` and `.addaccess`. This command can only be run by users who have administrator permissions for the entire server.")
        em.add_field(name="`.deladminrole <role_id>`", value="This command removes access for all users with the specified role to the admin-level commands for the bot, such as `.addpingedrole` and `.addaccess`. This command can only be run by users who have administrator permissions for the entire server.")
        em.set_footer(text="Auroris Development")
        await ctx.send(embed=em)

@bot.command()
@has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    embed=discord.Embed(title="Kick", description="Member Successfully Kicked.")
    embed.set_footer(text="TVHG Bot")
    await ctx.send(embed=embed)

@bot.command()
@has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    embed=discord.Embed(title="Ban", description="Member Successfully Banned.")
    embed.set_footer(text="TVHG Bot")
    await ctx.send(embed=embed)

@bot.command()
async def haha(ctx):
  await ctx.send("haha")

@bot.command()
async def echo(ctx,* ,echo):
  await ctx.send(echo)

@bot.command()
async def report(ctx, user:discord.User, *, reason=None):
  channel = bot.get_channel(715505968636624906)
  embed=discord.Embed(title="New Report", description=(reason), color=0xff0000)
  embed.set_footer(text=(user))
  await channel.send(embed=embed)
  embed=discord.Embed(title="Successfully Reported", description="Thank you for your report. Staff will review this and decide to take action", color=0xff0000)
  await ctx.send(embed=embed)

@bot.command()
async def afk(ctx):
    await ctx.send(f"{ctx.author.mention} Is now AFK. :thumbsup:")


@bot.command()
async def suggest(ctx, *, suggestion):
  channel = bot.get_channel(714550259203702906)
  embed=discord.Embed(title="New Suggestion", description=(suggestion), color=0x004cff)
  embed.set_footer(text="r/ruperrt b IHasGUI0001")
  await channel.send(embed=embed)

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def purge(ctx, limit: int):
      await ctx.channel.purge(limit=limit)
      await ctx.send('Cleared by {}'.format(ctx.author.mention))

@bot.event
async def on_command_error(self, error):
    channel = bot.get_channel(706180828752904278)
    embed=discord.Embed(title=str(error), color=0xff0000)
    await self.channel.send(embed=embed)
      
@bot.command()
@has_permissions(administrator=True)
async def mute(ctx, user: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await user.add_roles(role)
    await ctx.send("Member Successfully Muted!")
    
@bot.command()
@has_permissions(administrator=True)
async def announce(ctx, *,announcement):
    channel = bot.get_channel(714550884092084267)
    embed=discord.Embed(title="New Announcement!", description=(announcement))
    await channel.send(embed=embed)

@bot.command(pass_context = True)
@has_permissions(manage_roles=True, ban_members=True)
async def warn(ctx,user:discord.User,*reason:str):
  if not reason:
    await ctx.send("Please provide a reason")
    return
  reason = ' '.join(reason)
  for current_user in report['users']:
    if current_user['name'] == user.name:
      current_user['reasons'].append(reason)
      break
  else:
    report['users'].append({
      'name':user.name,
      'reasons': [reason,]
    })
  with open('reports.json','w+') as f:
    json.dump(report,f)


@bot.command(pass_context = True)
async def warnings(ctx,user:discord.User):
  for current_user in report['users']:
    if user.name == current_user['name']:
      await ctx.send(f"{user.name} has been reported {len(current_user['reasons'])} times : {','.join(current_user['reasons'])}")
      break
  else:
    await ctx.send(f"{user.name} has never been reported")  



@bot.command()
async def new(ctx, *, args = None):

    await bot.wait_until_ready()

    if args == None:
        message_content = "Please wait, we will be with you shortly!"
    
    else:
        message_content = "".join(args)

    with open("data.json") as f:
        data = json.load(f)

    ticket_number = int(data["ticket-counter"])
    ticket_number += 1

    ticket_channel = await ctx.guild.create_text_channel("ticket-{}".format(ticket_number))
    await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)

    for role_id in data["valid-roles"]:
        role = ctx.guild.get_role(role_id)

        await ticket_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
    
    await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

    em = discord.Embed(title="New ticket from {}#{}".format(ctx.author.name, ctx.author.discriminator), description= "{}".format(message_content), color=0x00a8ff)

    await ticket_channel.send(embed=em)

    pinged_msg_content = ""
    non_mentionable_roles = []

    if data["pinged-roles"] != []:

        for role_id in data["pinged-roles"]:
            role = ctx.guild.get_role(role_id)

            pinged_msg_content += role.mention
            pinged_msg_content += " "

            if role.mentionable:
                pass
            else:
                await role.edit(mentionable=True)
                non_mentionable_roles.append(role)
        
        await ticket_channel.send(pinged_msg_content)

        for role in non_mentionable_roles:
            await role.edit(mentionable=False)
    
    data["ticket-channel-ids"].append(ticket_channel.id)

    data["ticket-counter"] = int(ticket_number)
    with open("data.json", 'w') as f:
        json.dump(data, f)
    
    created_em = discord.Embed(title="r/ruperrt Tickets", description="Your ticket has been created at {}".format(ticket_channel.mention), color=0x00a8ff)
    
    await ctx.send(embed=created_em)

@bot.command()
async def close(ctx):
    with open('data.json') as f:
        data = json.load(f)

    if ctx.channel.id in data["ticket-channel-ids"]:

        channel_id = ctx.channel.id

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() == "close"

        try:

            em = discord.Embed(title="r/ruperrt Tickets", description="Are you sure you want to close this ticket? Reply with `close` if you are sure.", color=0x00a8ff)
        
            await ctx.send(embed=em)
            await bot.wait_for('message', check=check, timeout=60)
            await ctx.channel.delete()

            index = data["ticket-channel-ids"].index(channel_id)
            del data["ticket-channel-ids"][index]

            with open('data.json', 'w') as f:
                json.dump(data, f)
        
        except asyncio.TimeoutError:
            em = discord.Embed(title="r/ruperrt Tickets", description="You have run out of time to close this ticket. Please run the command again.", color=0x00a8ff)
            await ctx.send(embed=em)




































































bot.run('TOKEN')
