import disnake
from disnake.ext import commands
import asyncio
import pytimeparse

bot_prefix = "!"
intents = disnake.Intents.default()
intents.typing = False  # Remove these lines
intents.presences = False
intents.message_content = True
bot = commands.Bot(command_prefix=bot_prefix, intents=intents)


CENSORED_WORDS = ['lox', 'Ara', 'vates']


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    words = message.content.split()
    censored_message = []

    for word in words:
        if word.lower() in [censored.lower() for censored in CENSORED_WORDS]:
            censored_word = '*' * len(word)
            censored_message.append(censored_word)
        else:
            censored_message.append(word)

    censored_message = ' '.join(censored_message)
    await message.channel.send(f"This is a Censored word: {censored_message}")
    await bot.process_commands(message)  # Process commands as well


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')


@bot.event
async def on_member_join(member):
    role = member.guild.get_role(1156569853541498960)  # Replace YOUR_ROLE_ID with the actual role ID
    if role:
        await member.add_roles(role)
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
async def mute(ctx, member: disnake.Member, duration: str = None, *, reason=None):
    muted_role = disnake.utils.get(ctx.guild.roles, name="Muted")

    if not muted_role:
        muted_role = await ctx.guild.create_role(name="Muted")

        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, send_messages=False)

    await member.add_roles(muted_role, reason=reason)

    if duration:
        # Parse the duration string into seconds
        seconds = pytimeparse.parse(duration)

        if seconds is None:
            await ctx.send("Invalid duration format. Use something like '30m' for 30 minutes.")
            return

        await ctx.send(f'{member.mention} has been muted for {duration}.')
        await asyncio.sleep(seconds)
        await member.remove_roles(muted_role)
        await ctx.send(f'{member.mention} has been unmuted after {duration}.')
    else:
        await ctx.send(f'{member.mention} has been muted indefinitely.')


@bot.command(name='myhelp')
async def myhelp(ctx):
    prefix = bot.command_prefix
    embed = disnake.Embed(
        title="Bot Commands",
        description=f"List of available commands (prefix: {prefix}):",
        color=disnake.Color.blue()
    )

    embed.add_field(name=f"{prefix}ping", value="Check the bot's latency.", inline=False)
    embed.add_field(name=f"{prefix}kick @user [reason]", value="Kick a user from the server.", inline=False)
    embed.add_field(name=f"{prefix}ban @user [reason]", value="Ban a user from the server.", inline=False)
    embed.add_field(name=f"{prefix}mute @user [reason]", value="Mute a user.", inline=False)
    embed.add_field(name=f"{prefix}userinfo @user", value="Display user information.", inline=False)
    embed.add_field(name=f"{prefix}clearchat [num]", value="Clear chat messages (admin only).", inline=False)
    embed.add_field(name=f"{prefix}unmute @user", value="Unmute a user.", inline=False)
    embed.add_field(name=f"{prefix}unban user_id", value="Unban a user by user ID.", inline=False)

    await ctx.send(embed=embed)



@bot.command()
@commands.has_permissions(manage_messages=True)
async def clearchat(ctx, num: int):
    await ctx.channel.purge(limit=num + 1)
    await ctx.send(f'Cleared {num} messages.', delete_after=5)


@bot.command()
@commands.has_permissions(kick_members=True, administrator=True)
async def unmute(ctx, member: disnake.Member):
    muted_role = disnake.utils.get(ctx.guild.roles, name="Muted")

    if muted_role in member.roles:
        await member.remove_roles(muted_role)
        await ctx.send(f'{member.mention} has been unmuted.')
    else:
        await ctx.send(f'{member.mention} is not muted.')


@bot.command()
@commands.has_permissions(ban_members=True, administrator=True)
async def unban(ctx, user_id: int):
    banned_users = await ctx.guild.bans()

    for ban_entry in banned_users:
        if ban_entry.user.id == user_id:
            await ctx.guild.unban(ban_entry.user)
            await ctx.send(f'User with ID {user_id} has been unbanned.')
            return

    await ctx.send(f'User with ID {user_id} is not banned.')

if __name__ == "__main__":
    bot.run('MTE1NjU2NTI5NjY5MDI0NTc1NA.G-1VGG.4MhfeWsqpW6WTraEENXjxW9Sh981hqpdm7bgHU')
