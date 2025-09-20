import json
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import ast

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds_dict = dict(st.secrets["gcp_service_account"])
creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")

creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(creds)

sheet = client.open("rec_database").worksheet("players")
data = sheet.get_all_records()
df = pd.DataFrame(data)