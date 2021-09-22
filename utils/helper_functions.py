import utils as localutils


async def ask_for_topic(ctx, send_message: bool = True) -> str:
    """Ask for a topic if one isn't already provided"""

    # Ask for a topic
    if send_message:
        await ctx.send("What LGBT topic would you like to see?")

    # Wait for a topic
    chosen_topic_message = await ctx.bot.wait_for(
        'message', 
        check=lambda m: m.author == ctx.author and m.channel == ctx.channel, 
        timeout=30
    )
    chosen_topic = chosen_topic_message.content

    # Make sure it isn't a command
    if chosen_topic.startswith(ctx.prefix):
        return None

    # Return the topic
    return await autocorrect_alias(ctx, chosen_topic)


async def get_request(ctx, chosen_topic:str) -> localutils.Requester:
    """Keeps asking for a topic until a valid one is chosen. Returns a tuple (Requester Obj, Topic)"""

    try:
        if not chosen_topic:
            return (None, None)

        # Get the request
        requester = await localutils.Requester.get_requester(chosen_topic)

    # Custom error for when the topic isn't found
    except localutils.TopicNotFoundError:

        # Ask again
        await ctx.send("That topic wasn't found - input a different topic.")
        chosen_topic = await ask_for_topic(ctx, False)

        # Try again
        return await get_request(ctx, chosen_topic)

    # Return it
    return (requester, chosen_topic)


async def autocorrect_alias(ctx, chosen_topic):
    """Set an alias to the actual topic"""

    # Get the alias from the database
    async with ctx.bot.database() as db:
        alias_rows = await db("SELECT * FROM aliases WHERE guild_id = $1 AND alias = $2", ctx.guild.id, chosen_topic)

    # If there's an alias, return the actual topic, otherwise, return the original topic
    return alias_rows[0]['actual_topic'] if alias_rows else chosen_topic


async def init_setup(ctx, chosen_topic):
    """Initialise the setup for the commands info and flag"""

    # Ask for a topic if one isn't given
    chosen_topic = await autocorrect_alias(ctx, chosen_topic) or await ask_for_topic(ctx)
    
    # Get the Requester object
    requester, chosen_topic = await localutils.get_request(ctx, chosen_topic)

    # Silently fail if no requester was gotten - this is probably because they tried to input a command as a topic
    if not requester:
        return
    return (requester, chosen_topic,)