#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import random

import discord
from discord.ext import tasks

from constants import *
import radio
from server import keep_alive


intents = discord.Intents.default()
intents.message_content = True


class Pengan(discord.Client):
    radio_answers_count: int

    last_status: int = EXCEPTION
    status: int = EXCEPTION

    main_channel: discord.TextChannel
    radio_answers_channel: discord.TextChannel
    bot_channel: discord.TextChannel

    def __init__(self):
        super().__init__(intents=intents)

        self.radio_answers_count = len(radio.get_answers(SPREADSHEET_ID, SHEET_CREDS))

        self.main_channel = self.get_channel(MAIN_CHANNEL_ID)
        self.radio_answers_channel = self.get_channel(RADIO_ANSWERS_CHANNEL_ID)
        self.bot_channel = self.get_channel(BOT_CHANNEL_ID)

    async def on_ready(self) -> None:
        print(f"""We have logged in as {self.user}
""")
        await self.bot_channel.send(f"We have logged in as {self.user}")

        # async for message in client.get_channel().history(limit=20):
        #     print(message.content)
        # await client.get_channel().send()
        self.main_channel.guild.get_member(self.user.id).nick = None

        loop.start()

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
                self.status = OHAYO
                await self.update_presence()
                await message.channel.send("OK")
            elif arg == "oyasumi":
                self.status = OYASUMI
                await self.update_presence()
                await message.channel.send("OK")
            elif arg == "charge":
                self.status = CHARGE
                await self.update_presence()
                await message.channel.send("OK")
            elif arg == "geosta":
                self.status = GEOSTA
                await self.update_presence()
                await message.channel.send("OK")

        if "ohayo" in message.content.lower():
            await message.add_reaction("\U0001f5a4")
        if "oyasumi" in message.content.lower():
            await message.add_reaction("<:emoji_2:1074290659135066163>")
        if "geosta" in message.content.lower() or "努力 未来 a geoffroyi star" in message.content.lower():
            await message.add_reaction("<:PENGIN_LV98:1097096256939114517>")
        if "充 電 し な き ゃ 　敵 の 命 で ね" in message.content.lower():
            if self.status == OYASUMI:
                self.status = CHARGE
            await message.add_reaction("\U0001f5a4")

    async def update_status(self) -> None:
        self.last_status = self.status
        now = datetime.datetime.now()
        if 13 <= now.hour < 15:
            if self.status != CHARGE:
                self.status = OYASUMI
        elif 15 <= now.hour < 22:
            self.status = GEOSTA
        else:
            self.status = OHAYO

        if self.last_status != EXCEPTION and self.last_status != self.status:
            if self.status == OHAYO:
                await self.main_channel.send("ohayo")
            elif self.status == OYASUMI:
                await self.main_channel.send("oyasumi")
            elif self.status == GEOSTA:
                await self.main_channel.send(
                    "geosta" if random.random() < 0.9 else "努力 未来 a geoffroyi star"
                )

    async def update_presence(self) -> None:
        if self.status == OHAYO:
            await client.change_presence(
                status=discord.Status.online, activity=discord.Game(name="!!help", type=1)
            )
        elif self.status == OYASUMI:
            await client.change_presence(
                status=discord.Status.idle, activity=discord.Game(name="爆発", type=1)
            )
        elif self.status == CHARGE:
            await client.change_presence(
                status=discord.Status.dnd, activity=discord.Game(name="充電", type=1)
            )
        elif self.status == GEOSTA:
            await client.change_presence(
                status=discord.Status.dnd, activity=discord.Game(name="努力", type=1)
            )

    def check_radio_answers(self) -> list[list[str]]:
        answers = radio.get_answers(SPREADSHEET_ID, SHEET_CREDS)
        radio_answers_count = len(answers)
        if 0 < (diff := radio_answers_count - self.radio_answers_count):
            self.radio_answers_count = radio_answers_count
            return answers[-diff:]
        return []


@tasks.loop(seconds=60)
async def loop() -> None:
    now = datetime.datetime.now()

    await client.update_status()
    await client.update_presence()

    if now.minute % 2 == 0:
        answers = client.check_radio_answers()
        for answer in answers:
            await client.radio_answers_channel.send(f"""{answer[0]}
ラジオネーム: {answer[1]}
性別: {answer[2]}
年代: {answer[3]}
地域: {answer[4]}

{answer[5]}""")


client = Pengan()

keep_alive()

client.run(DISCORD_TOKEN)
