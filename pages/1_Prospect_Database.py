import streamlit as st
import pandas as pd
import ast
from db_utils import sheet

st.header("UNC MBB Prospect Database")

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
    /* Make all headers Carolina blue and center them */
    h1, h2, h3, h4, h5, h6 {
        background-color: #4B9CD3 !important;
        color: #fff !important;
        padding: 0.2em 1em;
        border-radius: 8px;
        margin-bottom: 0.5em;
        font-weight: 700;
        letter-spacing: 0.5px;
        width: 100%;
        display: block;
        text-align: center;
    }
    /* Custom subheader styling */
    .carolina-subheader {
        background-color: #13294B;
        color: #fff !important;
        padding: 0.05em 1em;
        border-radius: 8px;
        margin-bottom: 0.5em;
        font-size: 1.25em;
        font-weight: 600;
        letter-spacing: 0.5px;
        width: 100%;
        display: block;
    }
    </style>
    """,
    unsafe_allow_html=True
)

players = sheet.get_all_records()
df = pd.DataFrame(players)

with st.form("filter_form"):
    cols = st.columns(4)
    filter_firstname = cols[0].text_input("First Name")
    filter_lastname = cols[1].text_input("Last Name")
    filter_classification = cols[2].selectbox("Classification", ["", "High School", "College", "International"])
    filter_grad_year = cols[3].number_input("Graduation Year", min_value=1900, max_value=2100, step=1, format="%d", value=None)

    cols2 = st.columns(4)
    filter_city = cols2[0].text_input("City")
    filter_state = cols2[1].text_input("State")
    filter_current_school = cols2[2].text_input("Current School/Team")
    filter_position = cols2[3].selectbox("Position", ["", "Point Guard", "Shooting Guard", "Wing", "Post"])

    cols3 = st.columns(4)
    filter_tag = cols3[0].selectbox("Evaluation Tag", ["", "Need to Evaluate", "Evaluated"])
    filter_connection = cols3[1].selectbox("Connection", ["", "Jim Tanner", "TJ Beisner", "Buzz Peterson"])

    filter_submit = st.form_submit_button("Apply Filters")

filtered_df = df.copy()
if filter_firstname:
    filtered_df = filtered_df[filtered_df["First Name"].str.contains(filter_firstname, case=False, na=False)]
if filter_lastname:
    filtered_df = filtered_df[filtered_df["Last Name"].str.contains(filter_lastname, case=False, na=False)]
if filter_classification:
    filtered_df = filtered_df[filtered_df["Classification"] == filter_classification]
if filter_grad_year:
    filtered_df = filtered_df[filtered_df["Graduation Year"] == filter_grad_year]
if filter_position:
    filtered_df = filtered_df[filtered_df["Position"] == filter_position]
if filter_city:
    filtered_df = filtered_df[filtered_df["City"].str.contains(filter_city, case=False, na=False)]
if filter_state:
    filtered_df = filtered_df[filtered_df["State or Country"].str.contains(filter_state, case=False, na=False)]
if filter_current_school:
    filtered_df = filtered_df[filtered_df["Current School/Team"].str.contains(filter_current_school, case=False, na=False)]
if filter_tag:
    filtered_df = filtered_df[filtered_df["Evaluation Tag"] == filter_tag]
if filter_connection:
    filtered_df = filtered_df[filtered_df["Connection"] == filter_connection]

if filtered_df.empty:
    st.info("No players match the filter criteria.")
else:
    def safe_float(val, default=0.0):
        try:
            return float(val)
        except (ValueError, TypeError):
            return default
    def safe_int(val, default=0):
        try:
            return int(val)
        except (ValueError, TypeError):
            return default
    for i, row in filtered_df.iterrows():
        grad_year = row.get('Graduation Year','')
        position = row.get('Position','')
        expander_label = f"**{row.get('First Name','')} {row.get('Last Name','')}** · {grad_year} {position}"
        with st.expander(expander_label):

            st.markdown("<hr>", unsafe_allow_html=True)

            st.markdown('<div class="carolina-subheader">General Information</div>', unsafe_allow_html=True)

            gen_cols = st.columns(4)
            gen_cols[0].markdown(f"**Name:** {row.get('First Name','')} {row.get('Last Name','')}")
            gen_cols[1].markdown(f"**Graduation Year:** {row.get('Graduation Year','')}")
            gen_cols[2].markdown(f"**Position:** {row.get('Position','')}")
            gen_cols[3].markdown(f"**Classification:** {row.get('Classification','')}")

            pos_cols = st.columns(4)
            pos_cols[0].markdown(f"**City:** {row.get('City','')}")
            pos_cols[1].markdown(f"**State or Country:** {row.get('State or Country','')}")
            pos_cols[2].markdown(f"**Agent:** {row.get('Agent','')}")
            pos_cols[3].markdown(f"**Years of Eligibility:** {row.get('Years of Eligibility','')}")

            pos_cols2 = st.columns(2)
            pos_cols2[0].markdown(f"**Current School/Team:** {row.get('Current School/Team','')}")
            pos_cols2[1].markdown(f"**Past School(s)/Team(s):** {row.get('Past School(s)/Team(s)','')}")

            st.markdown('<div class="carolina-subheader">Measurables and Statistics</div>', unsafe_allow_html=True)

            meas_cols = st.columns(4)
            meas_cols[0].markdown(f"**Height:** {row.get('Height','')}")
            meas_cols[1].markdown(f"**Weight:** {row.get('Weight','')}")
            meas_cols[2].markdown(f"**Points:** {row.get('Points','')}")
            meas_cols[3].markdown(f"**Rebounds:** {row.get('Rebounds','')}")

            stat_cols = st.columns(4)
            stat_cols[0].markdown(f"**Assists:** {row.get('Assists','')}")
            stat_cols[1].markdown(f"**Ast/TO Ratio:** {row.get('Assist to Turnover Ratio','')}")
            stat_cols[2].markdown(f"**3PT%:** {row.get('3PT%','')}")
            stat_cols[3].markdown(f"**3PT Rate:** {row.get('3PT Rate','')}")

            stat_cols2 = st.columns(4)
            stat_cols2[0].markdown(f"**EFG%:** {row.get('EFG%','')}")
            stat_cols2[1].markdown(f"**PPP:** {row.get('Points Per Possession','')}")

            import ast

            st.markdown('<div class="carolina-subheader">Player Notes</div>', unsafe_allow_html=True)

            notes_cols = st.columns(2)
            fon_raw = row.get('Front Office Notes','')
            sn_raw = row.get('Scouting Notes','')

            notes_cols2 = st.columns(2)
            notes_cols2[0].markdown(f"**Evaluation Tag:** {row.get('Evaluation Tag','')}")
            connection = row.get('Connection','')
            connection_details = row.get('Connection Details','')
            if connection:
                notes_cols2[1].markdown(f"**Connection Details:** {connection}: {connection_details}")
            else:
                notes_cols2[1].markdown(f"**Connection Details:** {connection_details}")

            fon_list = []
            sn_list = []
            try:
                fon_list = ast.literal_eval(fon_raw) if fon_raw else []
            except Exception:
                fon_list = []
            try:
                sn_list = ast.literal_eval(sn_raw) if sn_raw else []
            except Exception:
                sn_list = []
            fon_list = sorted(fon_list, key=lambda x: x.get('timestamp',''), reverse=True)
            sn_list = sorted(sn_list, key=lambda x: x.get('timestamp',''), reverse=True)
            notes_cols[0].markdown("**Front Office Notes:**")
            for note in fon_list:
                date_str = note.get('timestamp','')[:10]
                notes_cols[0].markdown(f"<div style='border:1px solid #ddd; border-radius:8px; padding:8px; margin-bottom:8px; background:#f9f9f9;'><b>{note.get('author','')}</b> <span style='float:right;'>{date_str}</span><br>{note.get('text','')}</div>", unsafe_allow_html=True)
            notes_cols[1].markdown("**Scouting Notes:**")
            for note in sn_list:
                date_str = note.get('timestamp','')[:10]
                notes_cols[1].markdown(f"<div style='border:1px solid #ddd; border-radius:8px; padding:8px; margin-bottom:8px; background:#f9f9f9;'><b>{note.get('author','')}</b> <span style='float:right;'>{date_str}</span><br>{note.get('text','')}</div>", unsafe_allow_html=True)

            action_cols = st.columns([10, 1, 1])
            edit_key = f"edit_{i}"
            delete_key = f"delete_{i}"

            edit_clicked = action_cols[1].button("Edit", key=edit_key)

            delete_clicked = action_cols[2].button("Delete", key=delete_key, type="primary")
            st.markdown("""
            <style>
            [data-testid='baseButton-primary'][aria-label='Delete'],
            [data-testid='baseButton'][aria-label='Delete'] {
                background-color: #d9534f !important;
                color: #fff !important;
                border: none !important;
            }
            </style>
            """, unsafe_allow_html=True)

            if f"editing_{i}" not in st.session_state:
                st.session_state[f"editing_{i}"] = False
            if edit_clicked:
                st.session_state[f"editing_{i}"] = True

            if st.session_state[f"editing_{i}"]:
                with st.form(f"edit_form_{i}"):
                    st.write("**Edit Player Profile**")
                    gen_cols = st.columns(4)
                    first_name = gen_cols[0].text_input("First Name", value=row.get('First Name',''))
                    last_name = gen_cols[1].text_input("Last Name", value=row.get('Last Name',''))
                    grad_year = gen_cols[2].number_input("Graduation Year", min_value=1900, max_value=2100, step=1, value=safe_int(row.get('Graduation Year',1900)))
                    position_options = ["Point Guard", "Shooting Guard", "Wing", "Post"]
                    position_value = row.get('Position', '')
                    if position_value in position_options:
                        position_index = position_options.index(position_value)
                    else:
                        position_index = 0
                    position = gen_cols[3].selectbox("Position", options=position_options, index=position_index)

                    pos_cols = st.columns(4)
                    classification = pos_cols[0].text_input("Classification", value=row.get('Classification',''))
                    city = pos_cols[1].text_input("City", value=row.get('City',''))
                    state = pos_cols[2].text_input("State or Country", value=row.get('State or Country',''))
                    current_school = pos_cols[3].text_input("Current School/Team", value=row.get('Current School/Team',''))

                    meas_cols = st.columns(4)
                    height = meas_cols[0].text_input("Height", value=row.get('Height',''))
                    weight = meas_cols[1].number_input("Weight", min_value=0.0, step=0.1, value=safe_float(row.get('Weight',0)))
                    points = meas_cols[2].number_input("Points", min_value=0.0, step=0.1, value=safe_float(row.get('Points',0)))
                    rebounds = meas_cols[3].number_input("Rebounds", min_value=0.0, step=0.1, value=safe_float(row.get('Rebounds',0)))

                    stat_cols = st.columns(4)
                    assists = stat_cols[0].number_input("Assists", min_value=0.0, step=0.1, value=safe_float(row.get('Assists',0)))
                    ast_to_to = stat_cols[1].number_input("Ast/TO Ratio", min_value=0.0, step=0.1, value=safe_float(row.get('Assist to Turnover Ratio',0)))
                    three_pt_pct = stat_cols[2].number_input("3PT%", min_value=0.0, step=0.1, value=safe_float(row.get('3PT%',0)))
                    three_pt_rate = stat_cols[3].number_input("3PT Rate", min_value=0.0, step=0.1, value=safe_float(row.get('3PT Rate',0)))

                    stat_cols2 = st.columns(4)
                    efg_pct = stat_cols2[0].number_input("EFG%", min_value=0.0, step=0.1, value=safe_float(row.get('EFG%',0)))
                    ppp = stat_cols2[1].number_input("PPP", min_value=0.0, step=0.1, value=safe_float(row.get('Points Per Possession',0)))
                    agent = stat_cols2[2].text_input("Agent", value=row.get('Agent',''))
                    years_elig = stat_cols2[3].number_input("Years of Eligibility", min_value=0, step=1, value=safe_int(row.get('Years of Eligibility',0)))

                    notes_cols = st.columns(2)
                    front_office_notes = notes_cols[0].text_area("Front Office Notes", value=row.get('Front Office Notes',''))
                    scouting_notes = notes_cols[1].text_area("Scouting Notes", value=row.get('Scouting Notes',''))

                    notes_cols2 = st.columns([2,1,1])
                    connection_details = notes_cols2[0].text_area("Connection Details", value=row.get('Connection Details',''))
                    connection_name = notes_cols2[1].selectbox("Connection", options=["", "Jim Tanner", "TJ Beisner", "Buzz Peterson"], index=["", "Jim Tanner", "TJ Beisner", "Buzz Peterson"].index(row.get('Connection','')) if row.get('Connection','') in ["", "Jim Tanner", "TJ Beisner", "Buzz Peterson"] else 0)
                    tag = notes_cols2[2].selectbox("Evaluation Tag", options=["", "Need to Evaluate", "Evaluated"], index=["", "Need to Evaluate", "Evaluated"].index(row.get('Evaluation Tag','')) if row.get('Evaluation Tag','') in ["", "Need to Evaluate", "Evaluated"] else 0)

                    save_btn = st.form_submit_button("Save Changes")
                    cancel_btn = st.form_submit_button("Cancel")
                if save_btn:
                    idx = df[(df['First Name'] == row['First Name']) & (df['Last Name'] == row['Last Name'])].index
                    if len(idx) > 0:
                        update_row = [
                            classification, grad_year, first_name, last_name, position, city, state, current_school,
                            height, weight, points, rebounds, assists, ast_to_to, three_pt_pct, three_pt_rate,
                            efg_pct, ppp, agent, years_elig
                        ]
                        start_col = 1
                        end_col = len(update_row)
                        row_num = idx[0]+2
                        col_letters = [chr(ord('A') + i) for i in range(end_col)]
                        start_cell = f"A{row_num}"
                        end_cell = f"{col_letters[-1]}{row_num}"
                        cell_range = f"{start_cell}:{end_cell}"
                        cell_list = sheet.range(cell_range)
                        for cell, value in zip(cell_list, update_row):
                            cell.value = value
                        sheet.update_cells(cell_list)
                        st.success("Player updated. Please refresh.")
                        st.session_state[f"editing_{i}"] = False
                if cancel_btn:
                    st.session_state[f"editing_{i}"] = False
            if f"delete_confirm_{i}" not in st.session_state:
                st.session_state[f"delete_confirm_{i}"] = False
            if delete_clicked:
                st.session_state[f"delete_confirm_{i}"] = True
            if st.session_state[f"delete_confirm_{i}"]:
                with st.form(f"delete_form_{i}"):
                    st.warning(f"Are you sure you want to delete {row.get('First Name','')} {row.get('Last Name','')}?")
                    confirm_delete = st.form_submit_button("Yes, Delete")
                    cancel_delete = st.form_submit_button("Cancel")
                if confirm_delete:
                    idx = df[(df['First Name'] == row['First Name']) & (df['Last Name'] == row['Last Name'])].index
                    if len(idx) > 0:
                        row_to_delete = int(idx[0]+2)
                        sheet.delete_rows(row_to_delete)
                        st.success("Player deleted. Please refresh.")
                    st.session_state[f"delete_confirm_{i}"] = False
                if cancel_delete:
                    st.session_state[f"delete_confirm_{i}"] = False