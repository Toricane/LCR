import os
import discord
from discord.ext import commands, tasks
from keep_alive import keep_alive
from itertools import cycle
from discord_slash import SlashCommand
from discord.flags import Intents
import re, ast, inspect
import sys
import datetime
import asyncio
from discord.utils import get
import requests
from discord.errors import Forbidden
from discord_slash.utils import manage_commands, manage_components
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow, create_button

bot = commands.Bot(command_prefix="/", help_command=None)
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

status = cycle(['/help', "the game of Left Center Right"])
guild_ids = [868567807133106206]


@tasks.loop(seconds=15)
async def change_status():
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name=next(status)))


@bot.event
async def on_ready():
    change_status.start()
    print(f'We have logged in as {bot.user}')
    timestamp = datetime.datetime.now()
    print(timestamp.strftime(r"%A, %b %d, %Y, %I:%M %p UTC"))


@bot.command(hidden=True)
async def restart(ctx):
    if ctx.author.id == 721093211577385020:
        await ctx.message.add_reaction('🆗')
        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        await ctx.message.add_reaction('❌')


@bot.command(aliases=["rl"], hidden=True)
async def reload(ctx, extension=None):
    if ctx.author.id == 721093211577385020:
        if extension == None:
            try:
                for filename in os.listdir("./cogs"):
                    if filename.endswith(".py"):
                        bot.unload_extension(f"cogs.{filename[:-3]}")
            except Exception as e:
                await ctx.send(f"{e}")
            try:
                for filename in os.listdir("./cogs"):
                    if filename.endswith(".py"):
                        bot.load_extension(f"cogs.{filename[:-3]}")
            except Exception as e:
                await ctx.send(f"{e}")
            await ctx.send("Successfully reloaded all extensions.")
        else:
            try:
                bot.unload_extension(f"cogs.{extension}")
                bot.load_extension(f"cogs.{extension}")
                await ctx.send(f"Successfully reloaded `cogs/{extension}.py`")
            except Exception as e:
                await ctx.send(f"{e}")
    else:
        await ctx.message.add_reaction('❌')


@bot.command(name="help")
async def dpy_help(ctx):
    embed = discord.Embed(title="Help",
                          description="Please use `/` commands instead!",
                          color=0xf04b14)
    await ctx.send(embed=embed)


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


keep_alive()
bot.run(os.getenv('TOKEN'))
