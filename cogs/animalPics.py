import discord
import pathlib
import json
import random
import aiohttp
import io
from discord.ext import commands

jsonFile = pathlib.Path('miska.json')


class pictureIdError(commands.CommandError):
    pass


class animalPics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def upload(self, ctx):
        await ctx.channel.trigger_typing()
        with open(jsonFile, 'r') as f:
            miskaJSON = json.load(f)

        archiveOfPics = self.bot.get_user(327205633319239681)

        for x in ctx.message.attachments:
            animalPicURL = x.url
            miskaJSON[str(ctx.guild.id)]["animalURLS"].append([ctx.author.name, animalPicURL])
            async with aiohttp.ClientSession() as session:                                     #start of archival to make sure the link is valid
                async with session.get(animalPicURL) as r:                                     #
                    if r.status != 200:                                                        #
                        return await ctx.send('Failed to archive...')                          #
                    photo = io.BytesIO(await r.read())                                         #
                    await archiveOfPics.send(file=discord.File(photo, 'archive.jpg'))          #End of archival to make sure the is link valid

        with open(jsonFile, 'w') as f:
            json.dump(miskaJSON, f, indent=4)

        await ctx.message.delete()
        await ctx.send('Successfully uploaded :thumbsup:')

    @commands.command()
    @commands.cooldown(5, 1, commands.BucketType.user)
    async def pic(self, ctx, id=-1):
        await ctx.channel.trigger_typing()
        with open(jsonFile, 'r') as f:
            miskaJSON = json.load(f)

        if id == -1:
            picId = random.randint(0, len(miskaJSON[str(ctx.guild.id)]["animalURLS"]))
            picArr = miskaJSON[str(ctx.guild.id)]["animalURLS"][picId]
            picAuthor = picArr[0]
            picURL = picArr[1]

            async with aiohttp.ClientSession() as session:
                async with session.get(picURL) as r:
                    if r.status != 200:
                        return await ctx.send('Failed to upload photo...')
                    photo = io.BytesIO(await r.read())
                    await ctx.send(f"Picture uploaded by {picAuthor}, ID: {picId+1}", file=discord.File(photo, 'animalPic.jpg'))
        else:
            try:
                if id > len(miskaJSON[str(ctx.guild.id)]["animalURLS"]) or id <= 0:
                    raise pictureIdError

                picArr = miskaJSON[str(ctx.guild.id)]["animalURLS"][id-1]
                picAuthor = picArr[0]
                picURL = picArr[1]

                async with aiohttp.ClientSession() as session:
                    async with session.get(picURL) as r:
                        if r.status != 200:
                            return await ctx.send('Failed to upload photo...')
                        photo = io.BytesIO(await r.read())
                        await ctx.send(f"Picture uploaded by {picAuthor}, ID: {id}", file=discord.File(photo, 'animalPic.jpg'))
            except pictureIdError:
                await ctx.message.delete()
                await ctx.send(f'{ctx.author.mention}, you gave a picture id that does not exist',
                               delete_after=15)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def delete(self, ctx, id: int):
        try:
            await ctx.channel.trigger_typing()

            with open(jsonFile, 'r') as f:
                miskaJSON = json.load(f)

            if id > len(miskaJSON[str(ctx.guild.id)]["animalURLS"]) or id <= 0:
                raise pictureIdError

            miskaJSON[str(ctx.guild.id)]["animalURLS"].pop(id-1)

            with open(jsonFile, 'w') as f:
                json.dump(miskaJSON, f, indent=4)

            await ctx.send(f'Successfully deleted picture ID: {id} :thumbsup:')
        except pictureIdError:
            await ctx.message.delete()
            await ctx.send(f'{ctx.author.mention}, you gave a picture id that does not exist',
                           delete_after=15)


    @delete.error
    async def delete_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention}, you don\'t have the required permissions to manage messages',
                           delete_after=15)
            await ctx.message.delete()
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.author.mention}, you didn\'t specify a picture id',
                           delete_after=15)
            await ctx.message.delete()


def setup(bot):
    bot.add_cog(animalPics(bot))