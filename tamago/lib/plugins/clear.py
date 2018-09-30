@client.command(pass_context=True)
async def clear(ctx, amount=5):
    channel = ctx.message.channel
    messages = []

    async for message in client.logs_from(channel, limit=int(amount) + 1):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say('%s messages purged' % amount)
