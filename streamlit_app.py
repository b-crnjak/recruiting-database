import json
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import ast
import streamlit_authenticator as stauth

users = {
    "usernames": {
        "bcrnjak": {"name": "John Doe", "password": "frontoffice23"},
        "jtanner": {"name": "Jane Smith", "password": "frontoffice23"},
        "tbeisner": {"name": "Tom Beisner", "password": "frontoffice23"}
    }
}

authenticator = stauth.Authenticate(
    users,
    "my_cookie_name",
    "my_signature_key",
    cookie_expiry_days=1
)

login_result = authenticator.login(location='main')

if login_result is not None:
    name, authentication_status, username = login_result
else:
    st.warning("Login widget did not render. Please check your Streamlit setup.")
    st.stop()

if authentication_status:
    st.switch_page("pages/1_Prospect_Database.py")
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]

    creds_dict = dict(st.secrets["gcp_service_account"])
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")

    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)

    sheet = client.open("rec_database").worksheet("players")
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
elif authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")

