from PIL import Image
import requests
import io

import discord
from discord.ext import commands
import voxelbotutils as vbutils

import utils as localutils

class SexualityCommands(vbutils.Cog):

    @vbutils.command(aliases=['flag'])
    async def getflag(self, ctx:vbutils.Context, *, chosen_sexuality:str = None):
        """
        Gets the flag for the chosen sexuality.
        """

        if not chosen_sexuality:
            await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)
            chosen_sexuality = ctx.message.content
        
        requester = localutils.SexualityRequester(chosen_sexuality)

        try:
            flag_url = requester.get_flag()
        except Exception:
            return await ctx.send("Something went wrong getting the flag's image - make sure you entered an existing sexuality")

        flag_image = Image.open(io.BytesIO(requests.get(flag_url).content))
        width, height = flag_image.size
        ratio = width / height
        flag_image = flag_image.resize((1920, round(1920/ratio)), Image.NEAREST)

        sendable_image = io.BytesIO()
        flag_image.save(sendable_image, format='PNG')
        sendable_image.seek(0)

        await ctx.send(f"{chosen_sexuality.title()}'s Flag!", file=discord.File(sendable_image, 'flag.png'))


def setup(bot:vbutils.Bot):
    x = SexualityCommands(bot)
    bot.add_cog(x)
