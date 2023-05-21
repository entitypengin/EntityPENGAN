#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os

import discord
import discord.app_commands
from discord.ext import tasks

from server import keep_alive

discord_token = os.environ["DISCORD_TOKEN"]
bot_channel_id = int(os.environ["BOT_CHANNEL_ID"])

intents = discord.Intents.default()
intents.message_content = True


class Pengan(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)

    async def on_ready(self):
        print(f"We have logged in as {self.user}")
        await self.change_presence(activity=discord.Game(name="!!help", type=1))

        # async for message in client.get_channel(1064131569159258183).history(limit=20):
        #     print(message.content)
        # await client.get_channel(1060224631216287816).send("""フライングありなのそれ""")
        # await client.get_channel(bot_channel_id).send("""熱帯夜あつい""")

        loop.start()

    async def on_message(self, message: discord.Message):
        print(f"""On {message.channel}, {message.channel.guild} ({message.channel.id})
{message.author}: {message.content}""")
        if message.author == self.user:
            return
        if message.content.startswith("!!help"):
            await message.channel.send("ヘルプ: !!help")


@tasks.loop(seconds=60)
async def loop():
    now = datetime.datetime.now()
    if (now.hour, now.minute) == (22, 0):
        await client.get_channel(bot_channel_id).send("ohayo")
    elif (now.hour, now.minute) == (13, 0):
        await client.get_channel(bot_channel_id).send("oyasumi")
    elif (now.hour, now.minute) == (15, 0):
        await client.get_channel(bot_channel_id).send("geosta")


client = Pengan()


keep_alive()

client.run(discord_token)
