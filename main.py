import disnake
from disnake.ext import commands

bot_prefix = "!"
intents = disnake.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
bot = commands.Bot(command_prefix=bot_prefix, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@bot.event
async def on_member_join(member):
    embed = disnake.Embed(
        title="Welcome to the Server!",
        description=f"Welcome, {member.mention}, to our server!",
        color=disnake.Color.green()
    )

    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Joined at {member.joined_at.strftime('%Y-%m-%d %H:%M:%S')}")

    channel = member.guild.get_channel(1156571012264116236)
    if channel:
        await channel.send(embed=embed)

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'Pong! Latency: {latency}ms')

@bot.command()
@commands.has_permissions(kick_members=True, administrator=True)
async def kick(ctx, member: disnake.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} has been kicked.')

@bot.command()
@commands.has_permissions(ban_members=True, administrator=True)
async def ban(ctx, member: disnake.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} has been banned.')

@bot.command()
@commands.has_permissions(kick_members=True, administrator=True)
async def mute(ctx, member: disnake.Member, *, reason=None):
    muted_role = disnake.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        muted_role = await ctx.guild.create_role(name="Muted")

        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, send_messages=False)

    await member.add_roles(muted_role, reason=reason)
    await ctx.send(f'{member.mention} has been muted.')

@bot.command()
async def help(ctx):
    embed = disnake.Embed(
        title="Bot Commands",
        description="List of available commands:",
        color=disnake.Color.blue()
    )

    embed.add_field(name="!ping", value="Check the bot's latency.", inline=False)
    embed.add_field(name="!kick @user [reason]", value="Kick a user from the server.", inline=False)
    embed.add_field(name="!ban @user [reason]", value="Ban a user from the server.", inline=False)
    embed.add_field(name="!mute @user [reason]", value="Mute a user.", inline=False)
    embed.add_field(name="!userinfo @user", value="Display user information.", inline=False)
    embed.add_field(name="!clearchat [num]", value="Clear chat messages (admin only).", inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def userinfo(ctx, member: disnake.Member = None):
    member = member or ctx.author

    embed = disnake.Embed(
        title=f"{member.display_name}'s Info",
        color=disnake.Color.blue()
    )

    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="Username", value=member.display_name, inline=True)
    embed.add_field(name="User ID", value=member.id, inline=True)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
    embed.add_field(name="Joined Discord", value=member.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)

    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clearchat(ctx, num: int):
    await ctx.channel.purge(limit=num + 1)
    await ctx.send(f'Cleared {num} messages.', delete_after=5)

if __name__ == "__main__":
    bot.run('YOUR_BOT_TOKEN')
