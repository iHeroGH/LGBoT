from PIL import Image
import requests
import io

import discord
from discord.ext import commands
import voxelbotutils as vbutils

import utils as localutils

class LGBTCommands(vbutils.Cog):

    @vbutils.command(aliases=['flag'])
    async def getflag(self, ctx:vbutils.Context, *, chosen_topic:str = None):
        """
        Gets the flag for the chosen sexuality.
        """

        if not chosen_topic:
            await ctx.send("What LGBT topic would you like to see?")
            await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)
            chosen_topic = ctx.message.content
        
        requester = localutils.Requester(chosen_topic)

        try:
            flag_url = requester.get_flag()
        except Exception:
            return await ctx.send("Something went wrong getting the flag's image - make sure you entered an existing sexuality")
        
        flag_req = requests.get(flag_url).content
        try:
            flag_image = Image.open(io.BytesIO(flag_req))
        except Exception:
            return await ctx.send(f"It seems this flag's file format is currently unsupported :<\n{flag_url}")

        sendable_image = io.BytesIO()
        flag_image.save(sendable_image, format='PNG')
        sendable_image.seek(0)

        await ctx.send(f"The {chosen_topic.title()} Flag", file=discord.File(sendable_image, 'flag.png'))

    @vbutils.command(aliases=['info'])
    async def getinfo(self, ctx:vbutils.Context, *, chosen_topic:str = None):
        """
        Gets the flag for the chosen sexuality.
        """

        if not chosen_topic:
            await ctx.send("What LGBT topic would you like to see?")
            await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)
            chosen_topic = ctx.message.content
        
        requester = localutils.Requester(chosen_topic)

    
        topic_info = requester.get_info()
       

        embed = discord.Embed()
        embed.title = f"{chosen_topic.title()} Information"
        embed.description = topic_info

        await ctx.send(embed=embed)


def setup(bot:vbutils.Bot):
    x = LGBTCommands(bot)
    bot.remove_command("info")
    bot.add_cog(x)
