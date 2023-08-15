#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import random
import re

import discord
from discord.ext import tasks
from replit import db

from constants import (
    Channels,
    DISCORD_TOKEN,
    SHEET_CREDS,
    SPREADSHEET_ID,
    Status,
    messages,
    reactions,
)
import radio
from server import keep_alive


intents = discord.Intents.default()
intents.message_content = True
intents.members = True


class Pengan(discord.Client):
    status: Status = Status.EXCEPTION

    main_channel: discord.TextChannel
    welcome_channel: discord.TextChannel
    radio_answers_channel: discord.TextChannel
    bot_channel: discord.TextChannel

    def __init__(self):
        super().__init__(intents=intents)

    async def on_ready(self) -> None:
        self.main_channel = self.get_channel(Channels.MAIN_CHANNEL_ID)
        self.radio_answers_channel = self.get_channel(Channels.RADIO_ANSWERS_CHANNEL_ID)
        self.bot_channel = self.get_channel(Channels.BOT_CHANNEL_ID)

        last_working = datetime.datetime.fromtimestamp(db["last_working"], datetime.timezone.utc)

        for guild in self.guilds:
            for channel in guild.channels:
                if hasattr(channel, "history"):
                    async for message in channel.history(after=last_working):
                        await self.reaction(message)

        print(f"""We have logged in as {self.user}
""")
        await self.bot_channel.send(f"We have logged in as {self.user}")

        loop.start()

    async def on_member_join(self, member: discord.Member) -> None:
        await member.guild.system_channel.send(f"""{member.mention}がやってきました！
現在のメンバーは{member.guild.member_count}人です""")

    async def on_member_remove(self, member: discord.Member) -> None:
        await member.guild.system_channel.send(f"""{member.mention}が退出しました
現在のメンバーは{member.guild.member_count}人です""")

    async def on_message(self, message: discord.Message) -> None:
        print(f"""On {message.channel}, {message.channel.guild} ({message.channel.id})
{message.author}: {message.content}
""")
        if message.author == self.user:
            return
        if message.content == "!!help":
            await message.channel.send("ヘルプ: !!help")
        if message.content.startswith("!!debug"):
            arg = message.content.split()[1]
            if arg == "ohayo":
                self.status = Status.OHAYO
                await self.update_presence()
                await message.channel.send("OK")
            elif arg == "oyasumi":
                self.status = Status.OYASUMI
                await self.update_presence()
                await message.channel.send("OK")
            elif arg == "charge":
                self.status = Status.CHARGE
                await self.update_presence()
                await message.channel.send("OK")
            elif arg == "geosta":
                self.status = Status.GEOSTA
                await self.update_presence()
                await message.channel.send("OK")

        await self.reaction(message)

    async def reaction(self, message: discord.Message):
        for reaction in reactions:
            if re.search(reaction["regex"], message.content):
                await message.add_reaction(reaction["reaction"])

    async def update_status(self, now) -> None:
        if 13 <= now.hour < 15:
            if self.status != Status.CHARGE:
                self.status = Status.OYASUMI
        elif 15 <= now.hour < 22:
            self.status = Status.GEOSTA
        else:
            self.status = Status.OHAYO

        if now.minute == 0:
            for message in messages:
                if now.hour == message["time"]:
                    await self.main_channel.send(random.choice(message["texts"]))

    async def update_presence(self) -> None:
        if self.status == Status.OHAYO:
            await client.change_presence(
                status=discord.Status.online, activity=discord.Game(name="!!help", type=1)
            )
        elif self.status == Status.OYASUMI:
            await client.change_presence(
                status=discord.Status.idle, activity=discord.Game(name="爆発", type=1)
            )
        elif self.status == Status.CHARGE:
            await client.change_presence(
                status=discord.Status.dnd, activity=discord.Game(name="充電", type=1)
            )
        elif self.status == Status.GEOSTA:
            await client.change_presence(
                status=discord.Status.dnd, activity=discord.Game(name="努力", type=1)
            )

    async def check_radio_answers(self) -> None:
        answers = radio.get_answers(SPREADSHEET_ID, SHEET_CREDS)
        radio_answers_count = len(answers)
        if 0 < (diff := radio_answers_count - db["radio_answers_count"]):
            db["radio_answers_count"] = radio_answers_count
            new = answers[-diff:]
            for answer in new:
                await self.radio_answers_channel.send(f"""{answer[0]}
ラジオネーム: {answer[1]}
性別: {answer[2]}
年代: {answer[3]}
地域: {answer[4]}

{answer[5]}""")


@tasks.loop(seconds=60)
async def loop() -> None:
    try:
        now = datetime.datetime.now(datetime.timezone.utc)

        print(now)

        db["last_working"] = now.timestamp()

        await client.update_status(now)
        await client.update_presence()

        if now.minute % 2 == 0:
            try:
                await client.check_radio_answers()
            except BaseException as e:
                print(e)

    except BaseException as e:
        print(e)

client = Pengan()

keep_alive()

client.run(DISCORD_TOKEN)
