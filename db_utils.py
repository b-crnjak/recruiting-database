import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import json

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

@st.cache_resource
def get_gspread_client():
    creds_dict = json.loads(st.secrets["gcp_service_account"]["service_account_json"])
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    return gspread.authorize(creds)

@st.cache_resource
def get_spreadsheet():
    client = get_gspread_client()
    return client.open("rec_database")

@st.cache_resource
def get_worksheet(worksheet_name):
    spreadsheet = get_spreadsheet()
    return spreadsheet.worksheet(worksheet_name)

# Get the main players worksheet
client = get_gspread_client()
spreadsheet = get_spreadsheet()
sheet = get_worksheet("players")
data = sheet.get_all_records()
df = pd.DataFrame(data)