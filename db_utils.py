import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import json

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

@st.cache_resource
def get_gspread_client():
    creds_dict = json.loads(
        st.secrets["gcp_service_account"]["service_account_json"]
    )
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")

    creds = Credentials.from_service_account_info(
        creds_dict,
        scopes=scope
    )
    return gspread.authorize(creds)

@st.cache_data(ttl=300)  # refresh every 5 minutes
def load_sheet():
    client = get_gspread_client()
    sheet = client.open("rec_database").worksheet("players")
    data = sheet.get_all_records()
    return pd.DataFrame(data)

df = load_sheet()
