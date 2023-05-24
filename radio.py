#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def get_answers(spreadsheet_id: str, sheet_creds_dict: dict[str, str]) -> list[list[str]]:
    sheet_creds = Credentials.from_authorized_user_info(
        sheet_creds_dict,
        ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    )

    try:
        try:
            service = build("sheets", "v4", credentials=sheet_creds)
        except:
            service = build(
                "sheets",
                "v4",
                credentials=sheet_creds,
                discoveryServiceUrl="https://sheets.googleapis.com/$discovery/rest?version=v4"
            )

        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range="A2:F").execute()
        return result.get("values", [])

    except HttpError:
        return []
