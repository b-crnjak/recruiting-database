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
    st.header("General Information")
    gen_cols = st.columns(4)
    classification = gen_cols[0].selectbox("Classification *", ["High School", "College", "International"])
    grad_year = gen_cols[1].number_input("Graduation Year", min_value=1900, max_value=2100, step=1, format="%d", value=2026)
    firstname = gen_cols[2].text_input("First Name *")
    lastname = gen_cols[3].text_input("Last Name *")

    gen_cols2 = st.columns(4)
    position = gen_cols2[0].selectbox("Position *", ["Point Guard", "Shooting Guard", "Wing", "Post"])
    city = gen_cols2[1].text_input("City *")
    state = gen_cols2[2].text_input("State or Country *")
    current_school = gen_cols2[3].text_input("Current School/Team *")

    rec_cols = st.columns([2,1,1])
    past_schools = rec_cols[0].text_area("Past School(s)/Team(s)")
    agent = rec_cols[1].text_input("Agent")
    eligibility_years = rec_cols[2].number_input("Years of Eligibility", min_value=0, step=1, format="%d", value=None)

    st.header("Measurables and Statistics")
    meas_cols = st.columns(4)
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
    points = meas_cols[2].number_input("Points", min_value=0.0, step=0.1, format="%.1f", value=None)
    rebounds = meas_cols[3].number_input("Rebounds", min_value=0.0, step=0.1, format="%.1f", value=None)

    meas_cols2 = st.columns(4)
    assists = meas_cols2[0].number_input("Assists", min_value=0.0, step=0.1, format="%.1f", value=None)
    ast_to_to = meas_cols2[1].number_input("Assist to Turnover Ratio", min_value=0.0, step=0.1, format="%.1f", value=None)
    three_pt_pct = meas_cols2[2].number_input("3PT%", min_value=0.0, max_value=100.0, step=0.1, format="%.1f", value=None)
    three_pt_rate = meas_cols2[3].number_input("3PT Rate", min_value=0.0, step=0.1, format="%.1f", value=None)

    meas_cols3 = st.columns(4)
    efg_pct = meas_cols3[0].number_input("EFG%", min_value=0.0, step=0.1, format="%.1f", value=None)
    ppp = meas_cols3[1].number_input("Points Per Possession", min_value=0.0, step=0.1, format="%.1f", value=None)

    st.header("Player Notes")
    notes_cols = st.columns(2)
    front_office_notes_text = notes_cols[0].text_area("Front Office Notes")
    scouting_notes_text = notes_cols[1].text_area("Scouting Notes")

    notes_cols2 = st.columns([1,1,2])
    tag = notes_cols2[0].selectbox("Evaluation Tag", ["", "Need to Evaluate", "Evaluated"])
    connection_name = notes_cols2[1].selectbox("Connection", ["", "Jim Tanner", "TJ Beisner", "Buzz Peterson"])
    connection_details = notes_cols2[2].text_area("Connection Details")

    submit = st.form_submit_button("Add Player")

if submit:
    required_fields = [classification, firstname, lastname, position, city, state, current_school]
    height_error = False
    if height and not height_valid:
        height_error = True
    if all(required_fields) and not height_error:
        import datetime
        now = datetime.datetime.now().isoformat()
        front_office_notes = []
        scouting_notes = []
        if front_office_notes_text:
            front_office_notes.append({"author": "", "timestamp": now, "text": front_office_notes_text})
        if scouting_notes_text:
            scouting_notes.append({"author": "", "timestamp": now, "text": scouting_notes_text})
        row = [
            classification,
            grad_year,
            firstname,
            lastname,
            position,
            city,
            state,
            current_school,
            height,
            weight,
            points,
            rebounds,
            assists,
            ast_to_to,
            three_pt_pct,
            three_pt_rate,
            efg_pct,
            ppp,
            past_schools,
            agent,
            eligibility_years,
            str(front_office_notes),
            str(scouting_notes),
            tag,
            connection_name,
            connection_details
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