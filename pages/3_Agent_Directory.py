# Imports
import streamlit as st
import pandas as pd
from db_utils import sheet

# Page Configuration
st.markdown(
    """
    <style>
    .block-container {
        padding-left: 1in !important;
        padding-right: 1in !important;
        padding-top: 1in !important;
        padding-bottom: 1in !important;
        max-width: 100vw;
    }
    </style>
    """,
    unsafe_allow_html=True
)
                                                                        
# Page Title
st.header("Agent Directory")

# Load Agent Data from Google Sheet
try:
    from db_utils import get_worksheet
    agent_sheet = get_worksheet('agents')
except Exception:
    st.error("Could not find 'agents' worksheet in the Google Sheet.")
    st.stop()

agent_records = agent_sheet.get_all_records()
df = pd.DataFrame(agent_records)

# --- FILTERS ---
filter_cols = st.columns(2)

# Agency Dropdown (exclude empty values)
agency_options = [''] + sorted([a for a in df['Agency'].dropna().unique().tolist() if str(a).strip()]) if 'Agency' in df.columns else ['']
selected_agency = filter_cols[0].selectbox('Search by Agency', agency_options)

# Agent Name Text Search
agent_search = filter_cols[1].text_input('Search by Agent Name')

# --- APPLY FILTERS ---
filtered_df = df.copy()
if selected_agency:
    filtered_df = filtered_df[filtered_df['Agency'] == selected_agency]
if agent_search:
    filtered_df = filtered_df[filtered_df['Agent Name'].astype(str).str.contains(agent_search, case=False, na=False)]

# Display Filtered Data
st.dataframe(filtered_df, use_container_width=True, hide_index=True)
