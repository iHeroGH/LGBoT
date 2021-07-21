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

        # Ask for a topic if one isn't given
        chosen_topic = chosen_topic or self.ask_for_topic(ctx)
        
        # Set up out request
        requester = localutils.Requester(chosen_topic)

        # Get the flag - this fails if the topic is not found
        try:
            flag_url = requester.get_flag()
        except Exception:
            return await ctx.send("Something went wrong getting the flag's image - make sure you entered an existing sexuality")
        
        # Turn the image into an Image object from the bytes - this fails if the file format is an SVG
        flag_req = requests.get(flag_url).content
        try:
            flag_image = Image.open(io.BytesIO(flag_req))
        except Exception:
            return await ctx.send(f"It seems this flag's file format is currently unsupported :<\n{flag_url}")

        # Make the image sendable
        sendable_image = io.BytesIO()
        flag_image.save(sendable_image, format='PNG')
        sendable_image.seek(0)

        # And send it
        await ctx.send(f"The {chosen_topic.title()} Flag", file=discord.File(sendable_image, 'flag.png'))

    @vbutils.command(aliases=['info'])
    async def getinfo(self, ctx:vbutils.Context, *, chosen_topic:str = None):
        """
        Gets the flag for the chosen sexuality.
        """

        # Ask for a topic if one isn't given
        chosen_topic = chosen_topic or self.ask_for_topic(ctx)
        
        # Set up out request
        requester = localutils.Requester(chosen_topic)

        # Get the info - this fails if the topic is not found
        topic_info = requester.get_info()

        # Set up the embed
        embed = vbutils.Embed(title= f"{chosen_topic.title()} Information", description=topic_info, use_random_colour=True)
        self.bot.set_footer_from_config(embed)

        # Try to get the flag thumbnail. This may fail, in which case, a thumbnail will not be sent
        try:
            embed.set_thumbnail(url=requester.get_flag())
        except Exception:
            pass
        
        # And send it
        await ctx.send(embed=embed)

    async def ask_for_topic(self, ctx):
        """Ask for a topic if one isn't already provided"""
        await ctx.send("What LGBT topic would you like to see?")
        await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)
        chosen_topic = ctx.message.content

        return chosen_topic


def setup(bot:vbutils.Bot):
    x = LGBTCommands(bot)
    bot.remove_command("info")
    bot.add_cog(x)
