import json
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import ast

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds_dict = json.loads(st.secrets["gcp_service_account"]["service_account_json"])
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(creds)

sheet = client.open("rec_database").worksheet("players")
data = sheet.get_all_records()
df = pd.DataFrame(data)

def initialize_player_notes_column(sheet, notes_col=21):
    """
    Set Player Notes column to [] for all players if blank or not a valid list.
    Assumes first row is header.
    """
    num_rows = sheet.row_count
    for row in range(2, num_rows + 1):
        cell_value = sheet.cell(row, notes_col).value
        try:
            val = ast.literal_eval(cell_value) if cell_value else []
            if not isinstance(val, list):
                raise ValueError
        except Exception:
            sheet.update_cell(row, notes_col, str([]))