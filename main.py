#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import random

import discord
from discord.ext import tasks

import radio
from server import keep_alive

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
MAIN_CHANNEL_ID = int(os.environ["MAIN_CHANNEL_ID"])
RADIO_ANSWERS_CHANNEL_ID = int(os.environ["RADIO_ANSWERS_CHANNEL_ID"])
BOT_CHANNEL_ID = int(os.environ["BOT_CHANNEL_ID"])
SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]


SHEET_CREDS = {
    "token": os.environ["SHEET_CREDS_TOKEN"],
    "refresh_token": os.environ["SHEET_CREDS_REFRESH_TOKEN"],
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": os.environ["SHEET_CREDS_CLIENT_ID"],
    "client_secret": os.environ["SHEET_CREDS_CLIENT_SECRET"],
    "scopes": ["https://www.googleapis.com/auth/spreadsheets.readonly"],
    "expiry": "2023-05-24T08:48:49.831711Z"
}


intents = discord.Intents.default()
intents.message_content = True


class Pengan(discord.Client):
    radio_answers_count: int

    last_status: int = -1
    status: int = -1

    OHAYO = 0
    OYASUMI = 1
    CHARGE = 2
    GEOSTA = 3

    def __init__(self):
        super().__init__(intents=intents)

        self.radio_answers_count = len(radio.get_answers(SPREADSHEET_ID, SHEET_CREDS))

    async def on_ready(self) -> None:
        print(f"""We have logged in as {self.user}
""")
        await self.get_channel(BOT_CHANNEL_ID).send(f"We have logged in as {self.user}")

        # async for message in client.get_channel().history(limit=20):
        #     print(message.content)
        # await client.get_channel().send()

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
                self.status = self.OHAYO
                await self.update_presence()
                await message.channel.send("OK")
            elif arg == "oyasumi":
                self.status = self.OYASUMI
                await self.update_presence()
                await message.channel.send("OK")
            elif arg == "charge":
                self.status = self.CHARGE
                await self.update_presence()
                await message.channel.send("OK")
            elif arg == "geosta":
                self.status = self.GEOSTA
                await self.update_presence()
                await message.channel.send("OK")

        if "ohayo" in message.content.lower():
            await message.add_reaction("\U0001f5a4")
        if "oyasumi" in message.content.lower():
            await message.add_reaction("<:emoji_2:1074290659135066163>")
        if "geosta" in message.content.lower() or "努力 未来 a geoffroyi star" in message.content.lower():
            await message.add_reaction("<:PENGIN_LV98:1097096256939114517>")
        if "充 電 し な き ゃ 　敵 の 命 で ね" in message.content.lower():
            if self.status == self.OYASUMI:
                self.status = self.CHARGE
            await message.add_reaction("\U0001f5a4")

    async def update_presence(self) -> None:
        self.last_status = self.status

        now = datetime.datetime.now()
        if 13 <= now.hour < 15:
            if self.status != self.CHARGE:
                self.status = self.OYASUMI
        elif 15 <= now.hour < 22:
            self.status = self.GEOSTA
        else:
            self.status = self.OHAYO

        if self.last_status != -1 and self.last_status != self.status:
            if self.status == self.OHAYO:
                await client.get_channel(MAIN_CHANNEL_ID).send("ohayo")
            elif self.status == self.OYASUMI:
                await client.get_channel(MAIN_CHANNEL_ID).send("oyasumi")
            elif self.status == self.GEOSTA:
                await client.get_channel(MAIN_CHANNEL_ID).send(
                    "geosta" if random.random() < 0.9 else "努力 未来 a geoffroyi star"
                )

        if self.status == self.OHAYO:
            await client.change_presence(
                status=discord.Status.online, activity=discord.Game(name="!!help", type=1)
            )
        elif self.status == self.OYASUMI:
            await client.change_presence(
                status=discord.Status.idle, activity=discord.Game(name="爆発", type=1)
            )
        elif self.status == self.CHARGE:
            await client.change_presence(
                status=discord.Status.dnd, activity=discord.Game(name="充電", type=1)
            )
        elif self.status == self.GEOSTA:
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

    await client.update_presence()

    if now.minute % 2 == 0:
        answers = client.check_radio_answers()
        for answer in answers:
            await client.get_channel(RADIO_ANSWERS_CHANNEL_ID).send(f"""{answer[0]}
ラジオネーム: {answer[1]}
性別: {answer[2]}
年代: {answer[3]}
地域: {answer[4]}

{answer[5]}""")


client = Pengan()

keep_alive()

client.run(DISCORD_TOKEN)
