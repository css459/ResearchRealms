# Executable for Discord Interface
import os
import re

from discord.ext import commands

TOKEN = os.getenv('TOKEN')
bot = commands.Bot(command_prefix='!')


def _get_message(ctx):
    """
    Gets the command message content and strips off
    the command itself.
    :param ctx: Discord Context of command message
    :return:    Message string only
    """
    m = ctx.message.content
    regex = '\\' + str(bot.command_prefix) + '\\w+'
    return re.sub(re.compile(regex), '', m, 1)


@bot.command(name='echo', help='Tests the bot by echoing back what is said')
async def bot_echo(ctx):
    msg = _get_message(ctx)
    await ctx.send(msg)


bot.run(str(TOKEN))
