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
st.header("NIL Database")

# Load NIL Data from Google Sheet
try:
    nil_sheet = sheet.spreadsheet.worksheet('nil')
except Exception:
    st.error("Could not find 'nil' worksheet in the Google Sheet.")
    st.stop()

nil_records = nil_sheet.get_all_records()
df = pd.DataFrame(nil_records)

# --- FILTERS ---
filter_cols = st.columns(5)

# Position Dropdown
position_options = [''] + sorted(df['Position'].dropna().unique().tolist()) if 'Position' in df.columns else ['']
selected_position = filter_cols[0].selectbox('Search by Position', position_options)

# School Text Search
school_search = filter_cols[1].text_input('Search by School')

# Conference Dropdown
conference_options = [''] + sorted(df['Conference'].dropna().unique().tolist()) if 'Conference' in df.columns else ['']
selected_conference = filter_cols[2].selectbox('Conference', conference_options)

# Associated Season Dropdown
season_options = [''] + sorted(df['Associated Season'].dropna().unique().tolist()) if 'Associated Season' in df.columns else ['']
selected_season = filter_cols[3].selectbox('Associated Season', season_options)

# Associated Year Dropdown
year_options = [''] + sorted(df['Associated Year'].dropna().unique().tolist()) if 'Associated Year' in df.columns else ['']
selected_year = filter_cols[4].selectbox('Associated Year', year_options)

# --- FILTERS ---
nil_cols = st.columns(1)

# NIL Value slider
if 'NIL Value' in df.columns:
    nil_numeric = pd.to_numeric(df['NIL Value'], errors='coerce').fillna(0)
    min_nil = float(nil_numeric.min())
    max_nil = float(nil_numeric.max())
    slider_max = max_nil if min_nil != max_nil else max_nil + 1
    nil_range = nil_cols[0].slider('NIL Value Range',
                                      min_value=min_nil, 
                                      max_value=slider_max, 
                                      value=(min_nil, max_nil), 
                                      step=10000.0, 
                                      format="$%d")
else:
    nil_range = (0.0, 0.0)

# --- APPLY FILTERS ---
filtered_df = df.copy()
if selected_position:
    filtered_df = filtered_df[filtered_df['Position'] == selected_position]
if school_search:
    filtered_df = filtered_df[filtered_df['School'].astype(str).str.contains(school_search, case=False, na=False)]
if selected_conference:
    filtered_df = filtered_df[filtered_df['Conference'] == selected_conference]
if selected_season:
	filtered_df = filtered_df[filtered_df['Associated Season'] == selected_season]
if selected_year:
    filtered_df = filtered_df[filtered_df['Associated Year'] == selected_year]
if 'NIL Value' in filtered_df.columns:
    nil_numeric = pd.to_numeric(filtered_df['NIL Value'], errors='coerce').fillna(0)
    filtered_df = filtered_df[(nil_numeric >= nil_range[0]) & (nil_numeric <= nil_range[1])]

# Display Filtered Data
if 'NIL Value' in filtered_df.columns:
    nil_numeric = pd.to_numeric(filtered_df['NIL Value'], errors='coerce').fillna(0)
    filtered_df = filtered_df.assign(_nil_sort=nil_numeric).sort_values('_nil_sort', ascending=False).drop(columns=['_nil_sort'])
st.dataframe(filtered_df, use_container_width=True, hide_index=True)