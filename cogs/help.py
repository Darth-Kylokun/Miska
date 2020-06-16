import discord
from discord.ext import commands


class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        await ctx.channel.trigger_typing()
        embed = discord.Embed(color=discord.Color.blue())

        embed.set_footer(text=f"{ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        embed.set_author(name="Miska Bot - Help and Documentation", icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Command: upload", value="Uploads your animal picture", inline=False)
        embed.add_field(name="Command: pic", value="Return a random picture from animal pictures that have been uploaded optionally you can specify a pictures id", inline=False)
        embed.add_field(name="Command: delete", value="Deletes a uploaded animal picture", inline=False)
        embed.add_field(name="Command: prefix", value="Specifies a new prefix for the server", inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(help(bot))