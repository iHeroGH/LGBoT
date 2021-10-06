import voxelbotutils as vbutils


class AliasCommand(vbutils.Cog):

    @vbutils.command(aliases=['alias', 'settings', 'add'])
    @vbutils.has_permissions(manage_guild=True)
    async def addalias(self, ctx:vbutils.Context, alias:str=None, actual_topic:str=None):
        """
        A command to add LGBT aliases (ex: enby - nonbinary).
        """

        # Get an alias
        if not alias:
            await ctx.send("What would you like the alias to be?")
            alias = await self.bot.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
            alias = alias.content

        # Get a topic to correct to
        if not actual_topic:
            await ctx.send(f"What would you like the alias **{alias}** to correct to?")
            actual_topic = await self.bot.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
            actual_topic = actual_topic.content

        # Set up the buttons
        button1 = vbutils.Button("Yes", "yes",  style=vbutils.ButtonStyle.SUCCESS)
        button2 = vbutils.Button("No", "no", style=vbutils.ButtonStyle.DANGER)

        # Put the buttons together
        components = vbutils.MessageComponents(
            vbutils.ActionRow(button1, button2)
        )

        # Send the message with the buttons, wait for a response, then acknowledge the interaction
        confirmation_message = await ctx.send(f"You want to correct **{alias}** to **{actual_topic}**. Is this correct?", components=components)
        payload = await self.bot.wait_for("component_interaction", check=lambda p: p.message.id == confirmation_message.id and p.user == ctx.author)
        await payload.ack()

        # Disable the buttons
        [components.get_component(i).disable() for i in ['yes', 'no']]
        await confirmation_message.edit(components=components)

        # Send a response message if the user doesn't want to add the alias
        if payload.component.custom_id.lower() == "no":
            return await ctx.send(f"Okay, I won't change **{alias}** to **{actual_topic}**.")

        # Input to the database
        try:
            async with self.bot.database() as db:
                await db("""
                    INSERT INTO aliases (guild_id, alias, actual_topic) VALUES ($1, $2, $3)
                    ON CONFLICT (guild_id, alias) DO UPDATE
                    SET actual_topic = $3
                    """, ctx.guild.id, alias, actual_topic)
        except Exception as e:
            return await ctx.send("I ran into an error saving your data.")

        # Send the final message
        await ctx.send(f"Got it! **{alias}** will now correct to **{actual_topic}**.")

    @vbutils.command(aliases=['deletealias', 'delete', 'remove'])
    @vbutils.has_permissions(manage_guild=True)
    async def removealias(self, ctx, alias:str):
        """
        A command to remove LGBT aliases.
        """

        # Input to the database
        try:
            async with self.bot.database() as db:
                # Check if the alias exists
                alias_rows = await db("SELECT * FROM aliases WHERE guild_id = $1 AND alias = $2", ctx.guild.id, alias)
                if alias_rows:
                    # Delete the alias
                    await db("DELETE FROM aliases WHERE guild_id = $1 AND alias = $2", ctx.guild.id, alias)
                else:
                    return await ctx.send("That wasn't an existing alias")
        except Exception:
            return await ctx.send("I ran into an error removing your data.")

        # Send the final message
        await ctx.send(f"Got it! **{alias}** will no longer correct to anything.")

    @vbutils.command(aliases=['deleteall'])
    @vbutils.has_permissions(manage_guild=True)
    async def removeall(self, ctx):
        """
        A command to remove all LGBT aliases.
        """

        # Input to the database
        try:
            async with self.bot.database() as db:
                alias_rows = await db("SELECT * FROM aliases WHERE guild_id = $1", ctx.guild.id)
                if not alias_rows:
                    return await ctx.send("This guild didn't have any aliases to begin with.")
                # Delete all aliases
                await db("DELETE FROM aliases WHERE guild_id = $1", ctx.guild.id)
        except Exception:
            return await ctx.send("I ran into an error removing your data.")

        await ctx.send("Removed all aliases successfully.")

    @vbutils.command(aliases=["list", "aliases"])
    async def listaliases(self, ctx, guild_id:int=None):
        """
        A command to list the aliases for a guild.
        """

        # Make sure we have a guild
        guild_id = guild_id or ctx.guild.id

        # Get the aliases
        async with self.bot.database() as db:
            alias_rows = await db("SELECT * FROM aliases WHERE guild_id = $1", guild_id)

        if not alias_rows:
            return await ctx.send(f"This server has no aliases! Set one up by running `{ctx.clean_prefix}add`.")

        # Set up our dictionary
        aliases = {row['alias']: row['actual_topic'] for row in alias_rows}

        # Set up the message
        message = f"**{ctx.guild.name}**'s aliases:\n"
        message += "__Alias__ - __Topic__\n"
        for alias, topic in aliases.items():
            message += f"**{alias}** - **{topic}**\n"

        # Send the message
        await ctx.send(message)


def setup(bot:vbutils.Bot):
    x = AliasCommand(bot)
    bot.add_cog(x)
