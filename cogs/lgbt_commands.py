import re
from PIL import Image
import requests
import io

import discord
import voxelbotutils as vbutils

import utils as localutils

class LGBTCommands(vbutils.Cog):

    def __init__(self, bot:vbutils.Bot):
        self.bot = bot

    @vbutils.command(aliases=['flag'])
    async def getflag(self, ctx:vbutils.Context, *, chosen_topic:str = None):
        """
        Gets the flag for the chosen sexuality.
        """

        requester, chosen_topic = await localutils.init_setup(ctx, chosen_topic)

        # Silently fail if no requester was gotten - this is probably because they tried to input a command as a topic
        if not requester:
            return

        # Get the flag - this fails if the topic is not found
        try:
            flag_url = requester.get_flag()
        except Exception:
            return await ctx.send("Something went wrong getting the flag's image - make sure you entered an existing topic")
        
        # Turn the image into an Image object from the bytes - this fails if the file format is an SVG
        flag_req = requests.get(flag_url).content
        try:
            flag_bytes = io.BytesIO(flag_req)
            flag_image = Image.open(flag_bytes)
        except Exception:
            return await ctx.send(f"It seems this flag's file format is currently unsupported :<\n{flag_url}")

        # Make the image sendable
        sendable_image = io.BytesIO()
        flag_image.save(sendable_image, format='PNG')
        sendable_image.seek(0)

        # And send it
        await ctx.send(f"The {chosen_topic.title()} Flag", file=discord.File(sendable_image, 'flag.png'))

    @vbutils.command(aliases=['info', 'def', 'desc', 'definition', 'description'])
    async def getinfo(self, ctx:vbutils.Context, *, chosen_topic:str = None):
        """
        Gets the flag for the chosen sexuality.
        """

        requester, chosen_topic = await localutils.init_setup(ctx, chosen_topic)

        # Silently fail if no requester was gotten - this is probably because they tried to input a command as a topic
        if not requester:
            return

        # Get the info - this fails if the topic is not found
        try:
            topic_info = requester.get_info()
        except Exception:
            return await ctx.send("Something went wrong getting the topic's info - make sure you entered an existing topic")

        # Set up the embed
        embed = vbutils.Embed(title= f"{chosen_topic.title()} Information", description=topic_info, use_random_colour=True)
        self.bot.set_footer_from_config(embed)

        # Try to get the flag thumbnail. This may fail, in which case, a thumbnail will not be sent
        try:
            flag_url = requester.get_flag()
            embed.set_thumbnail(url=flag_url)
        except Exception:
            pass
        
        # And send it
        await ctx.send(embed=embed)

def setup(bot:vbutils.Bot):
    x = LGBTCommands(bot)
    bot.remove_command("info")
    bot.add_cog(x)
