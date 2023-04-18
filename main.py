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

client = discord.Client(intents=intents)


@tasks.loop(seconds=60)
async def loop():
    now = datetime.datetime.now()
    if (now.hour, now.minute) == (22, 0):
        await client.get_channel(bot_channel_id).send("ohayo")
    elif (now.hour, now.minute) == (13, 0):
        await client.get_channel(bot_channel_id).send("oyasumi")
    elif (now.hour, now.minute) == (15, 0):
        await client.get_channel(bot_channel_id).send("geosta")


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    await client.change_presence(activity=discord.Game(name="!!help", type=1))
    loop.start()


@client.event
async def on_message(message: discord.Message):
    print(f"""On {message.channel}, {message.channel.guild} ({message.channel.id})
{message.author}: {message.content}""")
    if message.author.bot:
        return
    if message.content.startswith("!!help"):
        await message.channel.send("ヘルプ: !!help")


keep_alive()

client.run(discord_token)
