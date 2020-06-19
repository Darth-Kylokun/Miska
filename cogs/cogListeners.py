import json
import pathlib
from discord.ext import commands

jsonFile = pathlib.Path('miska.json')


class cogListeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open(jsonFile, 'r') as f:
            miskaJSON = json.load(f)

        miskaJSON[str(guild.id)] = {"prefix": '?', "animalURLS": [], "tags": ["cat", "dog", "bird", "other"]}

        with open(jsonFile, 'w') as f:
            json.dump(miskaJSON, f, indent=4)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Miska has risen")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.message.delete()
            await ctx.send(f'{ctx.author.mention}, invalid command', delete_after=15)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open(jsonFile, 'r') as f:
            miskaJSON = json.load(f)

        miskaJSON.pop(str(guild.id))

        with open(jsonFile, 'w') as f:
            json.dump(miskaJSON, f, indent=4)


def setup(bot):
    bot.add_cog(cogListeners(bot))