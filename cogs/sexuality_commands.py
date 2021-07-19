import PIL as Image
import io

import voxelbotutils as utils
import discord
from discord.ext import commands

from cogs import utils as localutils


class SexualityCommands(utils.Cog):

    @utils.command(aliases='flag')
    async def getflag(self, ctx:utils.Context, *, chosen_sexuality:str = None):
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

        flag_image = Image.open(flag_url)
        flag_image = flag_image.resize((128, 128), Image.NEAREST)

        sendable_image = io.BytesIO()
        flag_image.save(sendable_image, format='PNG')
        sendable_image.seek(0)

        await ctx.send(f"{chosen_sexuality.title()}'s Flag!", file=discord.File(sendable_image, 'flag.png'))


def setup(bot:utils.Bot):
    x = SexualityCommands(bot)
    bot.add_cog(x)
