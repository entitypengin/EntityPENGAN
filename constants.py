#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum
import json
import os
from typing import Any


class Status(Enum):
    OHAYO = 0
    OYASUMI = 1
    CHARGE = 2
    GEOSTA = 3
    EXCEPTION = -1


class Channels:
    MAIN_CHANNEL_ID = int(os.environ["MAIN_CHANNEL_ID"])
    RADIO_ANSWERS_CHANNEL_ID = int(os.environ["RADIO_ANSWERS_CHANNEL_ID"])
    BOT_CHANNEL_ID = int(os.environ["BOT_CHANNEL_ID"])


DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
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

with open("messages.json") as f:
    messages_data = json.load(f)

messages: list[dict[str, Any]] = messages_data["messages"]
reactions: list[dict[str, Any]] = messages_data["reactions"]

