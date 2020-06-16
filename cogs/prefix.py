import json
from pathlib import Path
from discord.ext import commands

jsonFile = Path('miska.json')


class changePrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, prefix):
        with open(jsonFile, 'r') as f:
            miskaJSON = json.load(f)

        miskaJSON[str(ctx.guild.id)]["prefix"] = prefix

        with open(jsonFile, 'w') as f:
            json.dump(miskaJSON, f, indent=4)

        await ctx.send(f'Successfully change prefix to {prefix}')

    @prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention}, you don\'t have the required permissions to manage the server',
                           delete_after=15)
            await ctx.message.delete()
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.author.mention}, you didn\'t specify a new prefix',
                           delete_after=15)
            await ctx.message.delete()


def setup(bot):
    bot.add_cog(changePrefix(bot))