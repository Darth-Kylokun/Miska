import discord
from discord.ext import commands


class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        await ctx.channel.trigger_typing()
        embed = discord.Embed(color=discord.Color.blue())

        embed.set_author(name="Miska Bot - Help and Documentation", icon_url=self.bot.user.avatar_url)
        embed.set_footer(text=f"{ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Command: upload\nAlias: u", value="Uploads your animal picture, must have the file extension of png, jpg, or gif, if not given a tag the tag will be none", inline=False)
        embed.add_field(name="Command: pic\nAlias: p", value="Returns a random picture from uploaded animal pictures", inline=False)
        embed.add_field(name="Sub-Command of pic: id\nAlias: i", value="Allows you to search a picture by id", inline=False)
        embed.add_field(name="Sub-Command of pic: tag\nAlias: t", value="Allows you to search a picture by tag", inline=False)
        embed.add_field(name="Command: newtag", value="Adds a new tag to the list of whitelisted tags", inline=False)
        embed.add_field(name="Command: tags", value="Sends a list of all whitelisted tags", inline=False)
        embed.add_field(name="Command: retag", value="Allows you to change a pictures tag by giving the pictures id and a new tag", inline=False)
        embed.add_field(name="Command: deletetag", value="Removes a tag from the whitelist", inline=False)
        embed.add_field(name="Command: delete", value="Deletes an uploaded animal picture", inline=False)
        embed.add_field(name="Command: prefix", value="Specifies a new prefix for the server", inline=False)
        embed.add_field(name="Command: help", value="Sends an embed of Miska bot's help and documentation", inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(help(bot))