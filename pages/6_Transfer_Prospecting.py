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
st.header("Transfer Prospecting")

try:
    active_sheet = sheet.spreadsheet.worksheet('active')
except Exception:
    st.error("Could not find 'active' worksheet in the Google Sheet.")
    st.stop()

active_records = active_sheet.get_all_records()
df = pd.DataFrame(active_records)

school_options = [''] + sorted([s for s in df['School'].dropna().unique().tolist() if str(s).strip()]) if 'School' in df.columns else ['']
default_school = 'North Carolina' if 'North Carolina' in school_options else school_options[0]

# --- FILTERS ---
filter_cols = st.columns(2)

player_search = filter_cols[0].text_input('Search by Player Name')
selected_school = filter_cols[1].selectbox('Search by School', school_options, index=school_options.index(default_school))

# --- APPLY FILTERS ---
filtered_df = df.copy()
if player_search:
    filtered_df = filtered_df[filtered_df['Player Name'].astype(str).str.contains(player_search, case=False, na=False)]
if selected_school:
    filtered_df = filtered_df[filtered_df['School'] == selected_school]

# Display Filtered Data

# Professional table display with styling
if not filtered_df.empty:
    styled_df = filtered_df.style.set_properties(**{
        'background-color': '#f8f9fa',
        'color': '#212529',
        'border-color': '#dee2e6',
        'font-size': '14px',
        'text-align': 'left'
    }).highlight_null()
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

    with st.expander("Edit Player Tag"):
        tag_options = ["All-Conference", "Starter", "Bench", "Further Evaluation", "Reject", ""]
        player_names = filtered_df['Player Name'].dropna().unique().tolist()
        cols = st.columns(2)
        selected_player = cols[0].selectbox("Select Player", player_names)
        player_row = filtered_df[filtered_df['Player Name'] == selected_player].iloc[0]
        current_tag = player_row.get('Tag', '')
        new_tag = cols[1].selectbox(
            "Tag",
            tag_options,
            index=tag_options.index(current_tag) if current_tag in tag_options else 0,
            key=f"edit_tag_{selected_player}"
        )
        if st.button("Update Tag"):
            school = player_row.get('School', '')
            sheet_idx = df[(df['Player Name'] == selected_player) & (df['School'] == school)].index
            if len(sheet_idx) > 0:
                row_num = int(sheet_idx[0]) + 2
                tag_col_num = list(df.columns).index('Tag') + 1
                cell = f"{chr(64+tag_col_num)}{row_num}"
                active_sheet.update_acell(cell, new_tag)
                st.rerun()