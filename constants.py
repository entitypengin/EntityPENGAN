#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os


OHAYO = 0
OYASUMI = 1
CHARGE = 2
GEOSTA = 3
EXCEPTION = -1


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

