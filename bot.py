import discord
from discord import Embed, TextChannel
from discord.ext import commands, tasks
from discord.ext.commands import DefaultHelpCommand, has_permissions
from discord.utils import get
import aiohttp
import asyncio
import re
import emoji

DISCORD_BOT_TOKEN = 'your-discord-bot-token'
TWITCH_CLIENT_ID = 'your-twitch-client-id'
TWITCH_CLIENT_SECRET = 'your-twitch-client-secret'
TWITCH_USERNAME = 'twitch-username'
CHANNEL_ID = 123456789012345678  # Replace with your Discord channel ID

intents = discord.Intents.all()
intents.typing = False
intents.presences = False
intents.messages = True
bot = commands.Bot(command_prefix='.', intents=intents)

live_message_id = None
offline_message_id = None
streamer_is_live = False
first_check = True

#-----------------------------------------------------------------------------------------------------------
# gm/gn message
@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    # Remove all emojis and strip leading/trailing spaces
    content = re.sub(r':[^:]*:', '', emoji.demojize(message.content.lower())).strip()

    if content == "gm japeto":
        await message.channel.send(f'Good morning {message.author.name} :sun_with_face:')
    if content == "gn japeto":
        await message.channel.send(f'Goodnight {message.author.name} :first_quarter_moon_with_face:')
    if content == "good evening japeppy":
        await message.channel.send(f'Good evening {message.author.name} :smile:')
    

    await bot.process_commands(message)  # process commands after checking for "gm japeto"
#-----------------------------------------------------------------------------------------------------------
# send message to a specific channel
@bot.command(name='send_message', help='Sends a custom message to a specified channel.', usage='Usage: !send_message <channel_id> <message>')
async def send_message(ctx, channel_id: int, *, message: str):
    try:
        channel = bot.get_channel(channel_id)
        if channel is not None:
            await channel.send(message)
        else:
            await ctx.send("I couldn't find a channel with that ID!")
    except Exception as e:
        await ctx.send("Command doesn't work")

@send_message.error
async def send_message_error(ctx, error):
    await ctx.channel.purge(limit=1)
    await ctx.send("Usage: !send_message <channel_id> <message>")
# Usage: !send_message <channel_id> <message>

#-----------------------------------------------------------------------------------------------------------
# send a message to a specific channel with embed
@bot.command(name='sendme', help='Sends a custom embed message to a specified channel.', usage='Usage: !sendme <channel_id> "<title>" <color> <message>')
async def sendme(ctx, channel_id: int, title: str, color: str, *, message: str):
    try:
        channel = bot.get_channel(channel_id)
        if channel is not None:
            embed = Embed(title=title, description=message, color=int(color, 16))
            await channel.send(embed=embed)
        else:
            await ctx.send("I couldn't find a channel with that ID!")
    except Exception as e:
        await ctx.send("Command doesn't work")

@sendme.error
async def sendme_error(ctx, error):
    await ctx.channel.purge(limit=1)
    await ctx.send('Usage: !sendme <channel_id> "<title>" <color> <message>')
# Usage: !sendme <channel_id> "<title>" <color> <message>

#-----------------------------------------------------------------------------------------------------------
# give a list of all the channels with their IDs
@bot.command(name='listc', help='Lists all text channels and their IDs')
async def listc(ctx):
    embed = Embed(title="Text Channels", color=0x00ff00)
    for channel in ctx.guild.channels:
        if isinstance(channel, TextChannel):
            embed.add_field(name=channel.name, value=channel.id, inline=False)
    await ctx.send(embed=embed)

@listc.error
async def listc_error(ctx, error):
    await ctx.channel.purge(limit=1)
    await ctx.send("Command doesn't work")
# Usage: !listc

#-----------------------------------------------------------------------------------------------------------
# give a list of colors with there hex value
@bot.command(name='list_colors', help='Displays a list of colors along with their hexadecimal values.')
async def list_colors(ctx):
    colors = {
        "Red": "FF0000",
        "Green": "008000",
        "Blue": "0000FF",
        "Yellow": "FFFF00",
        "Purple": "800080",
        "Cyan": "00FFFF",
        "Magenta": "FF00FF",
        "Lime": "00FF00",
        "Pink": "FFC0CB",
        "Teal": "008080",
        "Lavender": "E6E6FA",
        "Brown": "A52A2A",
        "Beige": "F5F5DC",
        "Maroon": "800000",
        "Mint": "98FF98",
        "Olive": "808000",
        "Apricot": "FBCEB1",
        "Navy": "000080",
        "Grey": "808080",
        "White": "FFFFFF",
        "Black": "000000"
    }

    embed = Embed(title="Colors", description="Here are some common colors and their hexadecimal values:", color=0x00ff00)

    for color, value in colors.items():
        embed.add_field(name=color, value=f"#{value}", inline=True)

    await ctx.send(embed=embed)
@list_colors.error
async def list_colors_error(ctx, error):
    await ctx.channel.purge(limit=1)
    await ctx.send("Command doesn't work")
# Usage: !list_colors

#-----------------------------------------------------------------------------------------------------------
# delete a certain amount of messages
@bot.command(name='purge', help='Deletes a specified number of messages in the current channel.', usage='Usage: !purge <amount>')
@has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)  # +1 to include the command message itself
@purge.error
async def purge_error(ctx, error):
    await ctx.channel.purge(limit=1)
    await ctx.send("Usage: !purge <amount>")
# Usage: !purge <amount>

#-----------------------------------------------------------------------------------------------------------
# better looking help menu
class CustomHelpCommand(DefaultHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        embed = Embed(title="Bot Commands", description='')
        for page in self.paginator.pages:
            embed.description += page
        await destination.send(embed=embed)

bot.help_command = CustomHelpCommand()
#-----------------------------------------------------------------------------------------------------------
# autorole
@bot.event
async def on_member_join(member):
    role = get(member.guild.roles, name="Sock Puppet")  # Replace "your-role-name" with the role you want to assign
    await member.add_roles(role)
#-----------------------------------------------------------------------------------------------------------
# make channel private
@bot.command(name='tp', help='Makes a specificed channel private or not.', usage='Usage: !tp #channel-name')
@commands.has_permissions(manage_channels=True)
async def tp(ctx, channel: discord.TextChannel):
    overwrites = channel.overwrites
    everyone_role = ctx.guild.default_role
    bot_member = ctx.guild.get_member(bot.user.id)
    server_owner = ctx.guild.owner

    if everyone_role not in overwrites or overwrites[everyone_role].read_messages is None:
        # If channel is public, make it private
        overwrites[everyone_role] = discord.PermissionOverwrite(read_messages=False)
        overwrites[bot_member] = discord.PermissionOverwrite(read_messages=True)
        overwrites[server_owner] = discord.PermissionOverwrite(read_messages=True)
        await channel.edit(overwrites=overwrites)
        await ctx.send(f'Channel {channel.mention} is now private.')
    else:
        # If channel is private, make it public
        del overwrites[everyone_role]
        del overwrites[bot_member]
        del overwrites[server_owner]
        await channel.edit(overwrites=overwrites)
        await ctx.send(f'Channel {channel.mention} is now public.')

@tp.error
async def tp_error(ctx, error):
    await ctx.channel.purge(limit=1)
    await ctx.send("Usage: !tp #channel-name")
# Usage: !tp #channel-name

#-----------------------------------------------------------------------------------------------------------
# twich login
async def get_twitch_token():
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            'https://id.twitch.tv/oauth2/token',
            params={
                'client_id': TWITCH_CLIENT_ID,
                'client_secret': TWITCH_CLIENT_SECRET,
                'grant_type': 'client_credentials'
            }
        )
        response_json = await response.json()
        return response_json['access_token']

async def get_user_id(username, token):
    headers = {
        'Client-ID': TWITCH_CLIENT_ID,
        'Authorization': f'Bearer {token}'
    }
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            'https://api.twitch.tv/helix/users',
            headers=headers,
            params={'login': username}
        )
        response_json = await response.json()
        return response_json['data'][0]['id']
#-----------------------------------------------------------------------------------------------------------
# checks if streamer is online or offline
@tasks.loop(minutes=1)
async def check_twitch_status():
    global live_message_id, offline_message_id, streamer_is_live, first_check
    token = await get_twitch_token()
    user_id = await get_user_id(TWITCH_USERNAME, token)

    headers = {
        'Client-ID': TWITCH_CLIENT_ID,
        'Authorization': f'Bearer {token}'
    }
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            'https://api.twitch.tv/helix/streams',
            headers=headers,
            params={'user_id': user_id}
        )
        response_json = await response.json()

    channel = bot.get_channel(CHANNEL_ID)

    if response_json['data'] and not streamer_is_live:
        streamer_is_live = True
        if not first_check:
            if offline_message_id:
                offline_message = await channel.fetch_message(offline_message_id)
                await offline_message.delete()
            message = await channel.send(f'{TWITCH_USERNAME} is now live on Twitch! https://www.twitch.tv/{TWITCH_USERNAME}')
            live_message_id = message.id
    elif not response_json['data'] and streamer_is_live:
        streamer_is_live = False
        if not first_check:
            if live_message_id:
                live_message = await channel.fetch_message(live_message_id)
                await live_message.delete()
            message = await channel.send(f'{TWITCH_USERNAME} is not streaming right now.')
            offline_message_id = message.id

    first_check = False



async def update_bot_presence():
    await bot.wait_until_ready()
    game = discord.Game(name=f"twitch.tv/japeto")
    await bot.change_presence(status=discord.Status.online, activity=game)
#-----------------------------------------------------------------------------------------------------------
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    check_twitch_status.start()
    await update_bot_presence()

    global first_check
    first_check = True

    channel = bot.get_channel(CHANNEL_ID)
    async for message in channel.history(limit=None):
        await message.delete()

    # Get the current stream status from Twitch
    token = await get_twitch_token()
    user_id = await get_user_id(TWITCH_USERNAME, token)

    headers = {
        'Client-ID': TWITCH_CLIENT_ID,
        'Authorization': f'Bearer {token}'
    }
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            'https://api.twitch.tv/helix/streams',
            headers=headers,
            params={'user_id': user_id}
        )
        response_json = await response.json()

    global streamer_is_live, live_message_id, offline_message_id
    streamer_is_live = True if response_json['data'] else False

    if streamer_is_live:
        message = await channel.send(f'{TWITCH_USERNAME} is currently live on Twitch! https://www.twitch.tv/{TWITCH_USERNAME}')
        live_message_id = message.id
    else:
        message = await channel.send(f'{TWITCH_USERNAME} is currently not streaming.')
        offline_message_id = message.id







bot.run(DISCORD_BOT_TOKEN)

