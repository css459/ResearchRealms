# Executable for Discord Interface
import os
import re

from discord.ext import commands

from core.command import run_command

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
    # Get the message content, given we already know the command
    msg = _get_message(ctx)

    # Execute the required command using the `run_command` function
    out = run_command('test', msg)

    # `run_command` will return a single value which is passed back to
    # the user
    await ctx.send(out)


bot.run(str(TOKEN))
