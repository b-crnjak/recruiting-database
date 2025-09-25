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

st.header("Recruiting Board")

# Load all players
players = sheet.get_all_records()
df = pd.DataFrame(players)

# Board names (can be expanded)
default_boards = ["Priority Board", "Watchlist", "2025 Targets"]
positions = ["Point Guard", "Shooting Guard", "Small Forward", "Power Forward", "Center"]

if "boards" not in st.session_state:
    st.session_state["boards"] = {name: {pos: [] for pos in positions} for name in default_boards}
else:
    # Migrate any boards that are still lists to dict-of-lists
    for board_name, board_val in st.session_state["boards"].items():
        if isinstance(board_val, list):
            # Convert old list to dict with all players in 'Point Guard' by default
            st.session_state["boards"][board_name] = {pos: [] for pos in positions}
            st.session_state["boards"][board_name]["Point Guard"] = board_val


# Expander for board selection and creation
with st.expander("**Board Selection**", expanded=False):
    
    top_cols = st.columns([2,2,2])

    with top_cols[0]:
        board_names = sorted(list(st.session_state["boards"].keys()))
        selected_board = st.selectbox("Select Board:", board_names, key="select_board")

    def create_board_callback():
        new_board = st.session_state.get("new_board_name", "")
        if new_board and new_board not in st.session_state["boards"]:
            st.session_state["boards"][new_board] = {pos: [] for pos in positions}

    with top_cols[1]:
        new_board_name = st.text_input("Create Board:", key="new_board_name")
        if st.button("Create", key="confirm_create_board_btn"):
            if new_board_name and new_board_name not in st.session_state["boards"]:
                st.session_state["boards"][new_board_name] = {pos: [] for pos in positions}

    with top_cols[2]:
        def remove_board_callback():
            board_to_remove = st.session_state.get("remove_board_name", None)
            if board_to_remove and board_to_remove in st.session_state["boards"]:
                del st.session_state["boards"][board_to_remove]

        board_options = [""] + sorted(list(st.session_state["boards"].keys()))
        remove_board_selected = st.selectbox(
            "Remove Board:",
            board_options,
            index=0,
            key="remove_board_name"
        )
        # Second row: button to confirm removal
        if st.button("Remove", key="confirm_remove_board_btn"):
            if remove_board_selected and remove_board_selected in st.session_state["boards"]:
                del st.session_state["boards"][remove_board_selected]

with st.expander("**Edit Selected Board**", expanded=False):
    row1 = st.columns([2,1,2,1])
    all_board_players = set()
    for pos in positions:
        all_board_players.update(st.session_state["boards"][selected_board][pos])
    available_players = [f"{row['First Name']} {row['Last Name']}" for _, row in df.iterrows() if f"{row['First Name']} {row['Last Name']}" not in all_board_players]
    # Add player search
    add_player = row1[0].text_input("Search to Add Player", value="", key=f"add_{selected_board}_player_search")
    add_position = row1[1].selectbox("Position", positions, key=f"add_{selected_board}_position")
    # Remove player search
    remove_player = row1[2].text_input("Search to Remove Player", value="", key=f"remove_{selected_board}_player_search")
    remove_position = row1[3].selectbox("Position", positions, key=f"remove_{selected_board}_position_any")

    # Second row: buttons for add/remove
    row2 = st.columns([3,3])
    if row2[0].button("Add Player", key=f"add_btn_{selected_board}") and add_player and add_position:
        if add_player in available_players:
            st.session_state["boards"][selected_board][add_position].append(add_player)
            st.success(f"Added {add_player} to {add_position}")
        else:
            st.warning(f"Player '{add_player}' not found or already on board.")
    if row2[1].button("Remove Player", key=f"remove_btn_{selected_board}_any") and remove_player and remove_position:
        if remove_player in st.session_state["boards"][selected_board][remove_position]:
            st.session_state["boards"][selected_board][remove_position].remove(remove_player)
            st.success(f"Removed {remove_player} from {remove_position}")
        else:
            st.info(f"{remove_player} was not found in {remove_position}.")

board_view_label = f"**{selected_board} Board View**"
with st.expander(board_view_label, expanded=True):
    board_cols = st.columns(5)
    for i, pos in enumerate(positions):
        board_cols[i].markdown(f"##### {pos}")
        players_list = st.session_state["boards"][selected_board][pos]
        if players_list:
            for idx, player in enumerate(players_list):
                col1, col2, col3 = board_cols[i].columns([6,1,1])
                col1.write(player)
                if col2.button("↑", key=f"up_{selected_board}_{pos}_{idx}") and idx > 0:
                    players_list[idx], players_list[idx-1] = players_list[idx-1], players_list[idx]
                if col3.button("↓", key=f"down_{selected_board}_{pos}_{idx}") and idx < len(players_list)-1:
                    players_list[idx], players_list[idx+1] = players_list[idx+1], players_list[idx]
        else:
            board_cols[i].info("No players yet.")