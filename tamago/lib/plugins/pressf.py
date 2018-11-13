import asyncio
import discord
from discord.ext import commands
from tamago.lib  import utils


class PressF:
    """You can now pay repect to a person"""

    def __init__(self, client):
        self.client = client
        self.messager = {}
        self.messagem = {}

    @commands.command(pass_context=True, no_pm=True)
    async def pressf(self, ctx, user : discord.User=None):
        """Pay Respects by pressing f"""

        author = ctx.message.author
        channel = ctx.message.channel
        if channel.id in self.messager or channel.id in self.messagem:
            return await ctx.send("Oops! I'm still paying respects in this channel, you'll have to wait until I'm done.")

        if user:
            answer = user.display_name
        else:
            await ctx.send("What do you want to pay respects to?")
            message = await self.client.wait_for('message', timeout=120)

            if message is None:
                return await ctx.say("You took too long to reply.")

            answer = message.content

        msg = "Everyone, let's pay respects to **{}**! Press f reaction on this message to pay respects.".format(answer)

        message = await ctx.send(msg)

        try:
            await ctx.message.add_reaction("\U0001f1eb")
            self.messager[channel.id] = []
            react = True
        except:
            self.messagem[channel.id] = []
            react = False
            await self.client.edit_message(message, "Everyone, let's pay respects to **{}**! Type `f` reaction on the this message to pay respects.".format(answer))
            await self.client.wait_for_message(channel=ctx.message.channel)

        await asyncio.sleep(120)
        await self.client.delete_message(message)
        if react:
            amount = len(self.messager[channel.id])
        else:
            amount = len(self.messagem[channel.id])

        await ctx.say("**{}** {} paid respects to **{}**.".format(amount, "person has" if str(amount) == "1" else "people have", answer))

        if react:
            del self.messager[channel.id]
        else:
            del self.messagem[channel.id]

    async def on_reaction_add(self, reaction, user):
        message = reaction.message
        channel = message.channel
        if user.id == self.client.user.id:
            return
        if channel.id not in self.messager:
            return
        if user.id not in self.messager[channel.id]:
            if str(reaction.emoji) == "\U0001f1eb":
                await self.client.send_message(channel, "**{}** has paid respects.".format(user.display_name))
                self.messager[channel.id].append(user.id)

    async def on_message(self, message):
        channel = message.channel
        user = message.author
        if channel.id not in self.messagem:
            return
        if user.id not in self.messagem[channel.id]:
            if message.content.lower() == "f":
                await self.client.send_message(channel, "**{}** has paid respects.".format(user.display_name))
                self.messagem[channel.id].append(user.id)

def setup(client):
    client.add_cog(PressF(client))
