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
    filter_position = cols2[3].selectbox("Position", ["", "Pure Point", "Wing", "Stretch Big", "Rim Runner"])

    cols3 = st.columns(4)
    filter_tag = cols3[0].selectbox("Evaluation Tag", ["", "Need to Evaluate", "Bench", "Starter", "All-Conference"])
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
        firstname = row.get('First Name','')
        lastname = row.get('Last Name','')
        position = row.get('Position','')
        classification = row.get('Classification','')
        grad_year = row.get('Graduation Year','')
        player_city = row.get('City','')
        player_state = row.get('State or Country','')
        current_school = row.get('Current School/Team','')
        school_city = row.get('School City','') if 'School City' in row else ''
        school_state = row.get('School State','') if 'School State' in row else ''
        past_schools = row.get('Past School(s)/Team(s)','')
        height = row.get('Height','')
        weight = row.get('Weight','')
        points = row.get('Points','')
        rebounds = row.get('Rebounds','')
        assists = row.get('Assists','')
        ast_to_to = row.get('Assist to Turnover Ratio','')
        three_pt_pct = row.get('3PT%','')
        three_pt_rate = row.get('3PT Rate','')
        efg_pct = row.get('EFG%','')
        ppp = row.get('Points Per Possession','')
        agency = row.get('Agency','') if 'Agency' in row else ''
        agent = row.get('Agent','')
        agent_num = row.get('Agent Phone Number','') if 'Agent Phone Number' in row else ''
        eligibility_years = row.get('Years of Eligibility','')
        nil_min = row.get('NIL Min','') if 'NIL Min' in row else ''
        nil_max = row.get('NIL Max','') if 'NIL Max' in row else ''
        teams_interest = row.get('Teams Interested','') if 'Teams Interested' in row else ''
        connection_name = row.get('Connection','')
        connection_details = row.get('Connection Details','')
        tag = row.get('Evaluation Tag','')
        expander_label = f"**{firstname} {lastname}** · {classification} · {position}"
        with st.expander(expander_label):

            st.markdown("<hr>", unsafe_allow_html=True)

            st.markdown('<div class="carolina-subheader">Player Information</div>', unsafe_allow_html=True)
            gen_cols = st.columns(4)
            gen_cols[0].markdown(f"**First Name:** {firstname}")
            gen_cols[1].markdown(f"**Last Name:** {lastname}")
            gen_cols[2].markdown(f"**Position:** {position}")
            gen_cols[3].markdown(f"**Classification:** {classification}")

            gen_cols2 = st.columns([1,1,2])
            gen_cols2[0].markdown(f"**Graduation Year:** {grad_year}")
            gen_cols2[1].markdown(f"**City:** {player_city}")
            gen_cols2[2].markdown(f"**State or Country:** {player_state}")

            st.markdown('<div class="carolina-subheader">School/Team Information</div>', unsafe_allow_html=True)
            team_cols = st.columns([2,1,2])
            team_cols[0].markdown(f"**Team Name:** {current_school}")
            team_cols[1].markdown(f"**City:** {school_city}")
            team_cols[2].markdown(f"**State or Country:** {school_state}")
            team_cols2 = st.columns(1)
            team_cols2[0].markdown(f"**Past School(s)/Team(s):** {past_schools}")

            # Measurables and Statistics
            st.markdown('<div class="carolina-subheader">Measurables and Statistics</div>', unsafe_allow_html=True)
            meas_cols = st.columns([1,1,2])
            meas_cols[0].markdown(f"**Height:** {height}")
            meas_cols[1].markdown(f"**Weight:** {weight}")

            meas_cols2 = st.columns(4)
            meas_cols2[0].markdown(f"**Points:** {points}")
            meas_cols2[1].markdown(f"**Rebounds:** {rebounds}")
            meas_cols2[2].markdown(f"**Assists:** {assists}")
            meas_cols2[3].markdown(f"**Assist to Turnover Ratio:** {ast_to_to}")

            meas_cols3 = st.columns(4)
            meas_cols3[0].markdown(f"**3PT%:** {three_pt_pct}")
            meas_cols3[1].markdown(f"**3PT Rate:** {three_pt_rate}")
            meas_cols3[2].markdown(f"**EFG%:** {efg_pct}")
            meas_cols3[3].markdown(f"**Points Per Possession:** {ppp}")

            st.markdown('<div class="carolina-subheader">Front Office Information</div>', unsafe_allow_html=True)
            fo_cols = st.columns(4)
            fo_cols[0].markdown(f"**Agency:** {agency}")
            fo_cols[1].markdown(f"**Agent:** {agent}")
            fo_cols[2].markdown(f"**Agent Phone Number:** {agent_num}")
            fo_cols[3].markdown(f"**Years of Eligibility:** {eligibility_years}")

            fo_cols2 = st.columns([1,1,2])
            fo_cols2[0].markdown(f"**NIL Min:** {nil_min}")
            fo_cols2[1].markdown(f"**NIL Max:** {nil_max}")
            fo_cols2[2].markdown(f"**Teams Interested:** {teams_interest}")

            # Front Office Notes as cards
            fon_list = []
            try:
                fon_list = ast.literal_eval(row.get('Front Office Notes','')) if row.get('Front Office Notes','') else []
            except Exception:
                fon_list = []
            st.markdown("**Front Office Notes:**")
            for note in sorted(fon_list, key=lambda x: x.get('timestamp',''), reverse=True):
                date_str = note.get('timestamp','')[:10]
                st.markdown(f"<div style='border:1px solid #ddd; border-radius:8px; padding:8px; margin-bottom:8px; background:#f9f9f9;'><span style='float:right;'>{date_str}</span><br>{note.get('text','')}</div>", unsafe_allow_html=True)

            st.markdown('<div class="carolina-subheader">Connection Details</div>', unsafe_allow_html=True)
            con_cols = st.columns([1,3])
            con_cols[0].markdown(f"**Connection:** {connection_name}")
            con_cols[1].markdown(f"**Connection Details:** {connection_details}")

            st.markdown('<div class="carolina-subheader">Scouting Information</div>', unsafe_allow_html=True)
            scout_cols = st.columns([1,3])
            scout_cols[0].markdown(f"**Evaluation Tag:** {tag}")

            # Front Office Notes as cards
            sn_list = []
            try:
                sn_list = ast.literal_eval(row.get('Scouting Notes','')) if row.get('Scouting Notes','') else []
            except Exception:
                sn_list = []
            st.markdown("**Scouting Notes:**")
            for note in sorted(sn_list, key=lambda x: x.get('timestamp',''), reverse=True):
                date_str = note.get('timestamp','')[:10]
                st.markdown(f"<div style='border:1px solid #ddd; border-radius:8px; padding:8px; margin-bottom:8px; background:#f9f9f9;'><span style='float:right;'>{date_str}</span><br>{note.get('text','')}</div>", unsafe_allow_html=True)
            
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
                    position_options = ["Pure Point", "Wing", "Stretch Big", "Rim Runner"]
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

                    # Display non-editable fields
                    # Add all fields as editable widgets
                    school_city = st.text_input("School City", value=row.get('School City',''))
                    school_state = st.text_input("School State", value=row.get('School State',''))
                    past_schools = st.text_area("Past School(s)/Team(s)", value=row.get('Past School(s)/Team(s)',''))
                    agent_num = st.text_input("Agent Phone Number", value=row.get('Agent Phone Number',''))
                    nil_min = st.number_input("NIL Min", min_value=0.0, step=100.0, value=float(row.get('NIL Min',0)) if row.get('NIL Min','') else 0.0, format="%.0f")
                    nil_max = st.number_input("NIL Max", min_value=0.0, step=100.0, value=float(row.get('NIL Max',0)) if row.get('NIL Max','') else 0.0, format="%.0f")
                    teams_interest = st.text_input("Teams Interested", value=row.get('Teams Interested',''))

                    # Add note fields (append only)
                    notes_cols = st.columns(2)
                    new_front_office_note = notes_cols[0].text_area("Add Front Office Note", value="")
                    new_scouting_note = notes_cols[1].text_area("Add Scouting Note", value="")

                    # Parse previous notes as lists
                    import ast
                    fon_raw = row.get('Front Office Notes','')
                    sn_raw = row.get('Scouting Notes','')
                    try:
                        fon_list = ast.literal_eval(fon_raw) if fon_raw else []
                        if not isinstance(fon_list, list): fon_list = []
                    except Exception:
                        fon_list = []
                    try:
                        sn_list = ast.literal_eval(sn_raw) if sn_raw else []
                        if not isinstance(sn_list, list): sn_list = []
                    except Exception:
                        sn_list = []

                    # Display all previous notes as cards
                    notes_cols[0].markdown("**Previous Front Office Notes:**")
                    for note in sorted(fon_list, key=lambda x: x.get('timestamp',''), reverse=True):
                        date_str = note.get('timestamp','')[:10]
                        notes_cols[0].markdown(f"<div style='border:1px solid #ddd; border-radius:8px; padding:8px; margin-bottom:8px; background:#f9f9f9;'><span style='float:right;'>{date_str}</span><br>{note.get('text','')}</div>", unsafe_allow_html=True)
                    notes_cols[1].markdown("**Previous Scouting Notes:**")
                    for note in sorted(sn_list, key=lambda x: x.get('timestamp','') or '', reverse=True):
                        date_str = note.get('timestamp','')[:10]
                        notes_cols[1].markdown(f"<div style='border:1px solid #ddd; border-radius:8px; padding:8px; margin-bottom:8px; background:#f9f9f9;'><span style='float:right;'>{date_str}</span><br>{note.get('text','')}</div>", unsafe_allow_html=True)

                    notes_cols2 = st.columns([2,1,1])
                    connection_details = notes_cols2[0].text_area("Connection Details", value=row.get('Connection Details',''))
                    connection_name = notes_cols2[1].selectbox("Connection", options=["", "Jim Tanner", "TJ Beisner", "Buzz Peterson"], index=["", "Jim Tanner", "TJ Beisner", "Buzz Peterson"].index(row.get('Connection','')) if row.get('Connection','') in ["", "Jim Tanner", "TJ Beisner", "Buzz Peterson"] else 0)
                    tag = notes_cols2[2].selectbox("Evaluation Tag", options=["", "Need to Evaluate", "Reject", "Hold","Bench", "Starter", "All-Conference"], index=["", "Need to Evaluate", "Reject", "Hold","Bench", "Starter", "All-Conference"].index(row.get('Evaluation Tag','')) if row.get('Evaluation Tag','') in ["", "Need to Evaluate", "Reject", "Hold","Bench", "Starter", "All-Conference"] else 0)

                    save_btn = st.form_submit_button("Save Changes")
                    cancel_btn = st.form_submit_button("Cancel")
                if save_btn:
                    idx = df[(df['First Name'] == row['First Name']) & (df['Last Name'] == row['Last Name'])].index
                    if len(idx) > 0:
                        import datetime
                        now = datetime.datetime.now().isoformat()
                        # Parse previous notes as lists (again, for safety)
                        import ast
                        try:
                            fon_list = ast.literal_eval(fon_raw) if fon_raw else []
                            if not isinstance(fon_list, list): fon_list = []
                        except Exception:
                            fon_list = []
                        try:
                            sn_list = ast.literal_eval(sn_raw) if sn_raw else []
                            if not isinstance(sn_list, list): sn_list = []
                        except Exception:
                            sn_list = []
                        # Append new notes if provided
                        if new_front_office_note.strip():
                            fon_list.append({"timestamp": now, "text": new_front_office_note.strip()})
                        if new_scouting_note.strip():
                            sn_list.append({"timestamp": now, "text": new_scouting_note.strip()})
                        update_row = [
                            first_name,                # First Name
                            last_name,                 # Last Name
                            position,                  # Position
                            classification,            # Classification
                            grad_year,                 # Graduation Year
                            city,                      # City
                            state,                     # State or Country
                            current_school,            # Current School/Team
                            school_city,               # School City
                            school_state,              # School State
                            past_schools,              # Past School(s)/Team(s)
                            height,                    # Height
                            weight,                    # Weight
                            points,                    # Points
                            rebounds,                  # Rebounds
                            assists,                   # Assists
                            ast_to_to,                 # Assist to Turnover Ratio
                            three_pt_pct,              # 3PT%
                            three_pt_rate,             # 3PT Rate
                            efg_pct,                   # EFG%
                            ppp,                       # Points Per Possession
                            agency,                    # Agency
                            agent,                     # Agent
                            agent_num,                 # Agent Phone Number
                            years_elig,                # Years of Eligibility
                            nil_min,                   # NIL Min
                            nil_max,                   # NIL Max
                            teams_interest,            # Teams Interested
                            str(fon_list),             # Front Office Notes (as list)
                            connection_name,           # Connection
                            connection_details,        # Connection Details
                            tag,                       # Evaluation Tag
                            str(sn_list)               # Scouting Notes (as list)
                        ]
                        def colnum_string(n):
                            # 1-indexed
                            string = ''
                            while n > 0:
                                n, remainder = divmod(n - 1, 26)
                                string = chr(65 + remainder) + string
                            return string

                        row_num = idx[0] + 2  # 1-based, plus header
                        start_col = 1
                        end_col = len(update_row)
                        start_cell = f"{colnum_string(start_col)}{row_num}"
                        end_cell = f"{colnum_string(end_col)}{row_num}"
                        cell_range = f"{start_cell}:{end_cell}"
                        # Use update instead of update_cells for reliability
                        sheet.update(cell_range, [update_row])
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