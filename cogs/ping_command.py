import voxelbotutils as vbutils


class PingCommand(vbutils.Cog):

    @vbutils.command()
    async def ping(self, ctx:vbutils.Context):
        """
        A sexy lil ping command for the bot.
        """

        await ctx.send("Pong!")


def setup(bot:vbutils.Bot):
    x = PingCommand(bot)
    bot.add_cog(x)
