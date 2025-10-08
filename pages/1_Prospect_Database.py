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
    /* Custom editing subheader styling */
    .editing-subheader {
        background-color: #8B0000;
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
    filter_tag = cols3[0].selectbox("Evaluation Tag", ["", "Need to Evaluate", "Reject", "Hold", "Bench", "Starter", "All-Conference"])
    filter_connection = cols3[1].selectbox("Connection", ["", "Jim Tanner", "TJ Beisner", "Buzz Peterson"])
    filter_agent = cols3[2].text_input("Agent")

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
if filter_agent:
    filtered_df = filtered_df[filtered_df["Agent"].str.contains(filter_agent, case=False, na=False)]

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
        player_num = row.get('Player Phone #','')
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
        nil_min = row.get('Requested NIL Min','') if 'Requested NIL Min' in row else ''
        nil_max = row.get('Requested NIL Max','') if 'Requested NIL Max' in row else ''
        int_nil_min = row.get('Internal NIL Min','') if 'Internal NIL Min' in row else ''
        int_nil_max = row.get('Internal NIL Max','') if 'Internal NIL Max' in row else ''
        teams_interest = row.get('Teams Interested','') if 'Teams Interested' in row else ''
        team_committed = row.get('Team Committed To','') if 'Team Committed To' in row else ''
        mother_name = row.get("Mother Name",'')
        father_name = row.get("Father Name",'')
        hs_coach_name = row.get("HS Coach Name",'')
        aau_coach_name = row.get("AAU Coach Name",'')
        mother_num = row.get("Mother Phone #",'')
        father_num = row.get("Father Phone #",'')
        hs_coach_num = row.get("HS Coach Phone #",'')
        aau_coach_num = row.get("AAU Coach Phone #",'')
        connection_name = row.get('Connection','')
        connection_details = row.get('Connection Details','')
        tag = row.get('Evaluation Tag','')
        expander_label = f"**{firstname} {lastname}** · {classification} · {position} -- *{tag}*"

        with st.expander(expander_label):

            st.markdown("<hr>", unsafe_allow_html=True)

            st.markdown('<div class="carolina-subheader">Player Information</div>', unsafe_allow_html=True)
            gen_cols = st.columns(4)
            gen_cols[0].markdown(f"**First Name:** {firstname}")
            gen_cols[1].markdown(f"**Last Name:** {lastname}")
            gen_cols[2].markdown(f"**Position:** {position}")
            gen_cols[3].markdown(f"**Classification:** {classification}")

            gen_cols2 = st.columns([1,1,1,1])
            gen_cols2[0].markdown(f"**Graduation Year:** {grad_year}")
            gen_cols2[1].markdown(f"**City:** {player_city}")
            gen_cols2[2].markdown(f"**State or Country:** {player_state}")
            gen_cols2[3].markdown(f"**Player Phone #:** {player_num}")

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
            fo_cols[2].markdown(f"**Agent Phone #:** {agent_num}")
            fo_cols[3].markdown(f"**Years of Eligibility:** {eligibility_years}")

            fo_cols2 = st.columns([1,1,1,1])
            fo_cols2[0].markdown(f"**Requested NIL Min:** {nil_min}")
            fo_cols2[1].markdown(f"**Requested NIL Max:** {nil_max}")
            fo_cols2[2].markdown(f"**Internal NIL Min:** {int_nil_min}")
            fo_cols2[3].markdown(f"**Internal NIL Max:** {int_nil_max}")

            fo_cols3 = st.columns([2,1,1])
            fo_cols3[0].markdown(f"**Teams Interested:** {teams_interest}")
            fo_cols3[1].markdown(f"**Team Committed To:** {team_committed}")

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

            st.markdown('<div class="carolina-subheader">Primary Contacts</div>', unsafe_allow_html=True)
            pc_cols = st.columns(4)
            pc_cols[0].markdown(f"**Mother Name:** {mother_name}")
            pc_cols[1].markdown(f"**Father Name:** {father_name}")
            pc_cols[2].markdown(f"**HS Coach Name:** {hs_coach_name}")
            pc_cols[3].markdown(f"**AAU Coach Name:** {aau_coach_name}")

            pc_cols2 = st.columns(4)
            pc_cols2[0].markdown(f"**Mother Phone #:** {mother_num}")
            pc_cols2[1].markdown(f"**Father Phone #:** {father_num}")
            pc_cols2[2].markdown(f"**HS Coach Phone #:** {hs_coach_num}")
            pc_cols2[3].markdown(f"**AAU Coach Phone #:** {aau_coach_num}")
            
            st.markdown('<div class="carolina-subheader">Connection Details</div>', unsafe_allow_html=True)
            con_cols = st.columns([1,3])
            con_cols[0].markdown(f"**Connection:** {connection_name}")
            con_cols[1].markdown(f"**Connection Details:** {connection_details}")

            st.markdown('<div class="carolina-subheader">Scouting Information</div>', unsafe_allow_html=True)
            scout_cols = st.columns([1,3])
            scout_cols[0].markdown(f"**Evaluation Tag:** {tag}")
            synergy_url = row.get('Synergy Link', '').strip() if 'Synergy Link' in row else ''
            if synergy_url:
                scout_cols[1].markdown(f"[Synergy Link]({synergy_url})", unsafe_allow_html=True)

            # Front Office Notes as cards
            sn_list = []
            try:
                sn_list = ast.literal_eval(row.get('Scouting Notes','')) if row.get('Scouting Notes','') else []
            except Exception:
                sn_list = []
            st.markdown("**Scouting Notes:**")
            for note in sorted(sn_list, key=lambda x: x.get('timestamp',''), reverse=True):
                date_str = note.get('timestamp','')[:10]
                evaluator_str = note.get('evaluator','')
                eval_line = f"<b>Evaluator:</b> {evaluator_str}" if evaluator_str else "<b>Evaluator:</b>"
                date_line = f"<b>Date:</b> {date_str}"
                text_line = note.get('text','')
                st.markdown(f"""
<div style='border:1px solid #ddd; border-radius:8px; padding:8px; margin-bottom:8px; background:#f9f9f9;'>
    <div style='font-weight:bold;'>{eval_line}</div>
    <div style='font-weight:bold;'>{date_line}</div>
    <div>{text_line}</div>
</div>
""", unsafe_allow_html=True)
            
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
                    st.markdown('<div class="editing-subheader">Player Information</div>', unsafe_allow_html=True)
                    gen_cols = st.columns(4)
                    first_name = gen_cols[0].text_input("First Name", value=row.get('First Name',''), key=f"first_name_{i}")
                    last_name = gen_cols[1].text_input("Last Name", value=row.get('Last Name',''), key=f"last_name_{i}")
                    position = gen_cols[2].selectbox("Position", ["", "Pure Point", "Wing", "Stretch Big", "Rim Runner"], index=["", "Pure Point", "Wing", "Stretch Big", "Rim Runner"].index(row.get('Position','')) if row.get('Position','') in ["", "Pure Point", "Wing", "Stretch Big", "Rim Runner"] else 0, key=f"position_{i}")
                    classification = gen_cols[3].selectbox("Classification", ["", "High School", "College", "International"], index=["", "High School", "College", "International"].index(row.get('Classification','')) if row.get('Classification','') in ["", "High School", "College", "International"] else 0, key=f"classification_{i}")

                    gen_cols2 = st.columns([1,1,1,1])
                    grad_year = gen_cols2[0].number_input("Graduation Year", min_value=1900, max_value=2100, step=1, value=None, key=f"grad_year_{i}")
                    player_city = gen_cols2[1].text_input("City", value=row.get('City',''), key=f"player_city_{i}")
                    player_state = gen_cols2[2].text_input("State or Country", value=row.get('State or Country',''), key=f"player_state_{i}")
                    player_num = gen_cols2[3].text_input("Player Phone #", value=row.get('Player Phone #',''), key=f"player_num_{i}")

                    st.markdown('<div class="editing-subheader">School/Team Information</div>', unsafe_allow_html=True)
                    team_cols = st.columns([1,1,2])
                    current_school = team_cols[0].text_input("Team Name", value=row.get('Current School/Team',''), key=f"current_school_{i}")
                    school_city = team_cols[1].text_input("City", value=row.get('School City',''), key=f"school_city_{i}")
                    school_state = team_cols[2].text_input("State or Country", value=row.get('School State',''), key=f"school_state_{i}")

                    team_cols2 = st.columns(1)
                    past_schools = team_cols2[0].text_area("Past School(s)/Team(s)", value=row.get('Past School(s)/Team(s)',''), key=f"past_schools_{i}")

                    st.markdown('<div class="editing-subheader">Measureables and Statistics</div>', unsafe_allow_html=True)
                    meas_cols = st.columns([1,1,2])
                    height = meas_cols[0].text_input("Height", value=row.get('Height',''), key=f"height_{i}")
                    weight = meas_cols[1].number_input("Weight", min_value=0.0, step=0.1, value=safe_float(row.get('Weight',0)), key=f"weight_{i}")

                    meas_cols2 = st.columns(4)
                    points = meas_cols2[0].number_input("Points", min_value=0.0, step=0.1, value=safe_float(row.get('Points',0)), key=f"points_{i}")
                    rebounds = meas_cols2[1].number_input("Rebounds", min_value=0.0, step=0.1, value=safe_float(row.get('Rebounds',0)), key=f"rebounds_{i}")
                    assists = meas_cols2[2].number_input("Assists", min_value=0.0, step=0.1, value=safe_float(row.get('Assists',0)), key=f"assists_{i}")
                    ast_to_to = meas_cols2[3].number_input("Assist to Turnover Ratio", min_value=0.0, step=0.1, value=safe_float(row.get('Assist to Turnover Ratio',0)), key=f"ast_to_to_{i}")

                    meas_cols3 = st.columns(4)
                    three_pt_pct = meas_cols3[0].number_input("3PT%", min_value=0.0, max_value=100.0, step=0.1, value=safe_float(row.get('3PT%',0)), key=f"three_pt_pct_{i}")
                    three_pt_rate = meas_cols3[1].number_input("3PT Rate", min_value=0.0, step=0.1, value=safe_float(row.get('3PT Rate',0)), key=f"three_pt_rate_{i}")
                    efg_pct = meas_cols3[2].number_input("EFG%", min_value=0.0, step=0.1, value=safe_float(row.get('EFG%',0)), key=f"efg_pct_{i}")
                    ppp = meas_cols3[3].number_input("Points Per Possession", min_value=0.0, step=0.1, value=safe_float(row.get('Points Per Possession',0)), key=f"ppp_{i}")

                    st.markdown('<div class="editing-subheader">Front Office Information</div>', unsafe_allow_html=True)
                    fo_cols = st.columns(4)
                    agency = fo_cols[0].text_input("Agency", value=row.get('Agency',''), key=f"agency_{i}")
                    agent = fo_cols[1].text_input("Agent", value=row.get('Agent',''), key=f"agent_{i}")
                    agent_num = fo_cols[2].text_input("Agent Phone Number", value=row.get('Agent Phone Number',''), key=f"agent_num_{i}")
                    years_elig = fo_cols[3].number_input("Years of Eligibility", min_value=0, step=1, value=safe_int(row.get('Years of Eligibility',0)), key=f"years_elig_{i}")

                    fo_cols2 = st.columns([1,1,1,1])
                    nil_min = fo_cols2[0].number_input("Requested NIL Min", min_value=0.0, step=100.0, value=float(row.get('NIL Min',0)) if row.get('NIL Min','') else 0.0, format="%.0f", key=f"nil_min_{i}")
                    nil_max = fo_cols2[1].number_input("Requested NIL Max", min_value=0.0, step=100.0, value=float(row.get('NIL Max',0)) if row.get('NIL Max','') else 0.0, format="%.0f", key=f"nil_max_{i}")
                    int_nil_min = fo_cols2[2].number_input("Internal NIL Min", min_value=0.0, step=100.0, value=float(row.get('Internal NIL Min',0)) if row.get('Internal NIL Min','') else 0.0, format="%.0f", key=f"int_nil_min_{i}")
                    int_nil_max = fo_cols2[3].number_input("Internal NIL Max", min_value=0.0, step=100.0, value=float(row.get('Internal NIL Max',0)) if row.get('Internal NIL Max','') else 0.0, format="%.0f", key=f"int_nil_max_{i}")

                    fo_cols3 = st.columns([2,1,1])
                    teams_interest = fo_cols3[0].text_input("Teams Interested", value=row.get('Teams Interested',''), key=f"teams_interest_{i}")
                    team_committed = fo_cols3[1].text_input("Team Committed To", value=row.get('Team Committed To',''), key=f"team_committed_{i}")

                    fo_cols4 = st.columns(1)
                    new_front_office_note = fo_cols4[0].text_area("Add Front Office Note", value="", key=f"new_fo_note_{i}")

                    st.markdown('<div class="editing-subheader">Primary Contacts</div>', unsafe_allow_html=True)
                    pc_cols = st.columns(4)
                    mother_name = pc_cols[0].text_input("Mother Name", value=row.get("Mother Name",''), key=f"mother_name_{i}")
                    father_name = pc_cols[1].text_input("Father Name", value=row.get("Father Name",''), key=f"father_name_{i}")
                    hs_coach_name = pc_cols[2].text_input("HS Coach Name", value=row.get("HS Coach Name",''), key=f"hs_coach_name_{i}")
                    aau_coach_name = pc_cols[3].text_input("AAU Coach Name", value=row.get("AAU Coach Name",''), key=f"aau_coach_name_{i}")

                    pc_cols2 = st.columns(4)
                    mother_num = pc_cols2[0].text_input("Mother Phone #", value=row.get("Mother Phone #",''), key=f"mother_num_{i}")
                    father_num = pc_cols2[1].text_input("Father Phone #", value=row.get("Father Phone #",''), key=f"father_num_{i}")
                    hs_coach_num = pc_cols2[2].text_input("HS Coach Phone #", value=row.get("HS Coach Phone #",''), key=f"hs_coach_num_{i}")
                    aau_coach_num = pc_cols2[3].text_input("AAU Coach Phone #", value=row.get("AAU Coach Phone #",''), key=f"aau_coach_num_{i}")

                    st.markdown('<div class="editing-subheader">Connection Details</div>', unsafe_allow_html=True)
                    con_cols = st.columns([1,3])
                    connection_name = con_cols[0].selectbox("Connection", ["", "Jim Tanner", "TJ Beisner", "Buzz Peterson"], index=["", "Jim Tanner", "TJ Beisner", "Buzz Peterson"].index(row.get('Connection','')) if row.get('Connection','') in ["", "Jim Tanner", "TJ Beisner", "Buzz Peterson"] else 0, key=f"connection_name_main_{i}")
                    connection_details = con_cols[1].text_area("Connection Details", value=row.get('Connection Details',''), key=f"connection_details_main_{i}")

                    st.markdown('<div class="editing-subheader">Scouting Notes</div>', unsafe_allow_html=True)
                    scout_cols = st.columns([1,1,2])
                    tag = scout_cols[0].selectbox("Evaluation Tag", ["", "Need to Evaluate", "Reject", "Hold", "Bench", "Starter", "All-Conference"], index=["", "Need to Evaluate", "Reject", "Hold", "Bench", "Starter", "All-Conference"].index(row.get('Evaluation Tag','')) if row.get('Evaluation Tag','') in ["", "Need to Evaluate", "Reject", "Hold", "Bench", "Starter", "All-Conference"] else 0, key=f"tag_main_{i}")
                    new_evaluator = scout_cols[1].text_input("Evaluator Name", value="", key=f"new_evaluator_{i}")
                    new_scouting_note = scout_cols[2].text_area("Add Scouting Note", value="", key=f"new_scouting_note_{i}")

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
                            scouting_note = {"timestamp": now, "text": new_scouting_note.strip()}
                            if new_evaluator.strip():
                                scouting_note["evaluator"] = new_evaluator.strip()
                            sn_list.append(scouting_note)
                        update_row = [
                            first_name,                # First Name
                            last_name,                 # Last Name
                            position,                  # Position
                            classification,            # Classification
                            grad_year,                 # Graduation Year
                            player_city,               # City
                            player_state,              # State or Country
                            player_num,                # Player Phone #
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
                            nil_min,                   # Requested NIL Min
                            nil_max,                   # Requested NIL Max
                            int_nil_min,               # Internal NIL Min
                            int_nil_max,               # Internal NIL Max
                            teams_interest,            # Teams Interested
                            team_committed,            # Team Committed To
                            str(fon_list),             # Front Office Notes (as list)
                            mother_name,               # Mother Name
                            father_name,               # Father Name
                            hs_coach_name,             # HS Coach Name
                            aau_coach_name,            # AAU Coach Name
                            mother_num,                # Mother Phone #
                            father_num,                # Father Phone #
                            hs_coach_num,              # HS Coach Phone #
                            aau_coach_num,             # AAU Coach Phone #
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