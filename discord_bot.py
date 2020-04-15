# Executable for Discord Interface
import os

from discord.ext import commands

TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.command(name='echo', help='Tests the bot by echoing back what is said')
async def bot_echo(ctx):
    # print(ctx)
    await ctx.send(" ".join(ctx.message.content.split()[1:]))


bot.run(str(TOKEN))
