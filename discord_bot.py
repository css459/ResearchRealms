# Executable for Discord Interface
import os
import re

import discord
from discord.ext import commands

from core.command import run_command

MAX_MSG_LENGTH_CHARACTERS = 2000
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
    return re.sub(re.compile(regex), '', m, 1).strip()


async def format_message_output_and_send(o, ctx):
    """
    Extracts and formats the command output
    `o` from a standardized dictionary format
    as defined in `command.py`. Otherwise, casts
    the output to a string and attempts to send
    the string with sanity checks.

    :param o:   Output object to send to server. Can be
                dictionary, or single variable cast to string.
    :param ctx: Discord Context
    :return:    `None`
    """
    if isinstance(o, dict):
        try:
            if not o:
                return

            # Supported outputs
            if 'txt' in o:
                txt = o['txt']
                await ctx.send(txt)

            if 'img' in o:
                img_bytes = o['img']
                await ctx.send(file=discord.File(img_bytes, 'attachment.png'))

        except KeyError as e:
            error_str = "COMMAND EXCEPTION: Unrecognized command output.\n" + \
                        'EXCEPTION: ' + str(e)
            await ctx.send(error_str)
    else:
        s = str(o)
        if len(s) <= MAX_MSG_LENGTH_CHARACTERS:
            await ctx.send(s)
        else:
            await ctx.send("COMMAND EXCEPTION: Output exceeds " +
                           str(MAX_MSG_LENGTH_CHARACTERS) + " characters")


@bot.command(name='echo', help='Tests the bot by echoing back what is said')
async def bot_echo(ctx):
    # Get the message content, given we already know the command
    msg = _get_message(ctx)

    # Execute the required command using the `run_command` function
    out = run_command('test', msg)

    # `run_command` will return a single value which is passed back to
    # the user
    await format_message_output_and_send(out, ctx)


@bot.command(name='chart', help='Tests the bot by providing an example image')
async def bot_chart(ctx):
    # Get the message content, given we already know the command
    msg = _get_message(ctx)

    # Execute the required command using the `run_command` function
    out = run_command('testimg', msg)

    # `run_command` will return a single value which is passed back to
    # the user
    await format_message_output_and_send(out, ctx)


@bot.command(name='exec', help='Execute Code')
async def exec_code(ctx):
    msg = _get_message(ctx)
    out = run_command('exec', msg)
    await format_message_output_and_send(out, ctx)


bot.run(str(TOKEN))
