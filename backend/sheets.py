import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
import json

class SheetDB:
    def __init__(self):
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        # Load credentials from Streamlit secrets or local file
        try:
            creds_dict = st.secrets["google_credentials"]
        except KeyError:
            with open("credentials.json", "r") as f:
                creds_dict = json.load(f)
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)

        client = gspread.authorize(creds)

        # Sheet name must match EXACTLY
        self.sheet = client.open("ExpenseManager").sheet1

    def append_row(self, data):
        self.sheet.append_row(data)

    def read_all(self):
        return self.sheet.get_all_records()