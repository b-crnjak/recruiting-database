import streamlit as st
from db_utils import sheet

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

with st.form("add_player_form"):
    st.header("Player Information")
    gen_cols = st.columns(4)
    firstname = gen_cols[0].text_input("First Name *")
    lastname = gen_cols[1].text_input("Last Name *")
    position = gen_cols[2].selectbox("Position *", ["Pure Point", "Wing", "Stretch Big", "Rim Runner"])
    classification = gen_cols[3].selectbox("Classification *", ["High School", "College", "International"])
    
    gen_cols2 = st.columns([1,1,2])
    grad_year = gen_cols2[0].number_input("Graduation Year *", min_value=1900, max_value=2100, step=1, format="%d", value=2026)
    player_city = gen_cols2[1].text_input("City", key="player_city")
    player_state = gen_cols2[2].text_input("State or Country", key="player_state")

    st.header("School/Team Information")
    team_cols = st.columns([1,1,2])
    current_school = team_cols[0].text_input("Team Name *", key="current_school")
    school_city = team_cols[1].text_input("City", key="school_city")
    school_state = team_cols[2].text_input("State or Country", key="school_state")

    team_cols2 = st.columns(1)
    past_schools = team_cols2[0].text_area("Past School(s)/Team(s)")

    st.header("Measurables and Statistics")
    meas_cols = st.columns([1,1,2])
    height = meas_cols[0].text_input("Height")
    import re
    height_valid = False
    if height:
        match = re.match(r"^(\d)'\s*(\d{1,2})\"$", height.strip())
        if match:
            feet = int(match.group(1))
            inches = int(match.group(2))
            if 0 <= inches <= 11:
                height_valid = True
            else:
                st.warning("Inches must be between 0 and 11.")
        else:
            st.warning("Format correctly: ft' in\"")
    weight = meas_cols[1].number_input("Weight", min_value=0.0, step=0.1, format="%.1f", value=None)

    meas_cols2 = st.columns(4)
    points = meas_cols2[0].number_input("Points", min_value=0.0, step=0.1, format="%.1f", value=None)
    rebounds = meas_cols2[1].number_input("Rebounds", min_value=0.0, step=0.1, format="%.1f", value=None)
    assists = meas_cols2[2].number_input("Assists", min_value=0.0, step=0.1, format="%.1f", value=None)
    ast_to_to = meas_cols2[3].number_input("Assist to Turnover Ratio", min_value=0.0, step=0.1, format="%.1f", value=None)
    
    meas_cols3 = st.columns(4)
    three_pt_pct = meas_cols3[0].number_input("3PT%", min_value=0.0, max_value=100.0, step=0.1, format="%.1f", value=None)
    three_pt_rate = meas_cols3[1].number_input("3PT Rate", min_value=0.0, step=0.1, format="%.1f", value=None)
    efg_pct = meas_cols3[2].number_input("EFG%", min_value=0.0, step=0.1, format="%.1f", value=None)
    ppp = meas_cols3[3].number_input("Points Per Possession", min_value=0.0, step=0.1, format="%.1f", value=None)

    st.header("Front Office Information")
    fo_cols = st.columns(4)
    agency = fo_cols[0].text_input("Agency")
    agent = fo_cols[1].text_input("Agent")
    agent_num = fo_cols[2].text_input("Agent Phone Number")
    eligibility_years = fo_cols[3].number_input("Years of Eligibility", min_value=0, step=1, format="%d", value=None)

    fo_cols2 = st.columns(4)
    nil_min = fo_cols2[0].number_input("NIL Min", min_value=0.0, step=100.0, format="%.0f", value=None)
    nil_max = fo_cols2[1].number_input("NIL Max", min_value=0.0, step=100.0, format="%.0f", value=None)
    teams_interest = fo_cols2[2].text_input("Teams Interested")

    fo_cols3 = st.columns(1)
    front_office_notes_text = fo_cols3[0].text_area("Front Office Notes")

    st.header("Connection Details")
    con_cols = st.columns([1,3])
    connection_name = con_cols[0].selectbox("Connection", ["", "Jim Tanner", "TJ Beisner", "Buzz Peterson"])
    connection_details = con_cols[1].text_area("Connection Details")

    st.header("Scouting Notes")
    scout_cols = st.columns([1,3])
    tag = scout_cols[0].selectbox("Evaluation Tag", ["", "Need to Evaluate", "Bench", "Starter", "All-Conference"])
    scouting_notes_text = scout_cols[1].text_area("Scouting Notes")

    submit = st.form_submit_button("Add Player")

if submit:
    required_fields = [firstname, lastname, position, classification, grad_year, current_school]
    height_error = False
    if height and not height_valid:
        height_error = True
    if all(required_fields) and not height_error:
        import datetime
        now = datetime.datetime.now().isoformat()
        # Always store notes as a list of dicts, even for first note
        front_office_notes = []
        scouting_notes = []
        if front_office_notes_text:
            front_office_notes = [{"timestamp": now, "text": front_office_notes_text}]
        if scouting_notes_text:
            scouting_notes = [{"timestamp": now, "text": scouting_notes_text}]
        row = [
            firstname,                # First Name
            lastname,                 # Last Name
            position,                 # Position
            classification,           # Classification
            grad_year,                # Graduation Year
            player_city,              # City
            player_state,             # State or Country
            current_school,           # Current School/Team
            school_city,              # School City
            school_state,             # School State
            past_schools,             # Past School(s)/Team(s)
            height,                   # Height
            weight,                   # Weight
            points,                   # Points
            rebounds,                 # Rebounds
            assists,                  # Assists
            ast_to_to,                # Assist to Turnover Ratio
            three_pt_pct,             # 3PT%
            three_pt_rate,            # 3PT Rate
            efg_pct,                  # EFG%
            ppp,                      # Points Per Possession
            agency,                   # Agency
            agent,                    # Agent
            agent_num,                # Agent Phone Number
            eligibility_years,        # Years of Eligibility
            nil_min,                  # NIL Min
            nil_max,                  # NIL Max
            teams_interest,           # Teams Interested
            str(front_office_notes),  # Front Office Notes (as list)
            connection_name,          # Connection
            connection_details,       # Connection Details
            tag,                      # Evaluation Tag
            str(scouting_notes)       # Scouting Notes (as list)
        ]
        try:
            sheet.append_row(row)
            st.success(f"Added player: {firstname} {lastname}")
        except Exception as e:
            st.error(f"Failed to add player: {e}")
    elif height_error:
        st.error("Height is not in the correct format.")
    else:
        st.error("Please fill in all required fields marked with *.")