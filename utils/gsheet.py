# -*- coding: utf-8 -*-

from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import pandas as pd

PATH = "./data/"
SCOPES = "https://www.googleapis.com/auth/spreadsheets.readonly"
SPREADSHEET_ID = "1jvek6Kcy-8M92qcDJwXMncfwOwIwJcN8Jur0EojAxPw"
SHEETS = [
    {"sheet_name": "A", "csv_name": "a.csv"},
    {"sheet_name": "B", "csv_name": "b.csv"},
    {"sheet_name": "C", "csv_name": "c.csv"},
]

def extract_sheet():
    store = file.Storage("token.json")
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets("credentials.json", SCOPES)
        creds = tools.run_flow(flow, store)
    service = build("sheets", "v4", http=creds.authorize(Http()))
    sheet = service.spreadsheets()
    dic_df = {}
    for s in SHEETS:
        print("Retrieving " + s["sheet_name"])
        result = (
            sheet.values()
            .get(spreadsheetId=SPREADSHEET_ID, range=s["sheet_name"])
            .execute()
        )
        columns = result["values"][0]
        data = result["values"][1:]
        df = pd.DataFrame(data=data, columns=columns, dtype=str)
        df.to_csv(PATH + s["csv_name"], index=False, encoding="UTF-8")
        dic_df[s["sheet_name"]] = df 
    return dic_df

