import json
import os
from discord.ext import commands, tasks

botOwner = 327205633319239681


def getPrefix(bot, message):
    with open('miska.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]["prefix"]


bot = commands.Bot(command_prefix=getPrefix)
bot.remove_command('help')

@bot.command()
async def enable(ctx, extension):
    if ctx.author.id == botOwner:
        bot.load_extension(f'cogs.{extension}')
        await ctx.message.delete()
        print(f'Enabled {extension}')


@bot.command()
async def disable(ctx, extension):
    if ctx.author.id == botOwner:
        bot.unload_extension(f'cogs.{extension}')
        await ctx.message.delete()
        print(f'Disabled {extension}')


@bot.command()
async def reload(ctx, extension):
    if ctx.author.id == botOwner:
        bot.unload_extension(f'cogs.{extension}')
        bot.load_extension(f'cogs.{extension}')
        await ctx.message.delete()
        print(f'Reloaded {extension}')


for f in os.listdir('./cogs'):
    if f.endswith('.py'):
        bot.load_extension(f'cogs.{f[:-3]}')


f = open('token.txt', 'r')
token = f.readlines()
f.close()

bot.run(token[0])