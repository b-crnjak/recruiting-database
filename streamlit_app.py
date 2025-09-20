import streamlit as st

def check_password():
    st.markdown(
        """
        <style>
        .password-box input {
            font-size: 1.2em;
            padding: 0.5em;
            border-radius: 8px;
            border: 1px solid #ccc;
            width: 100%;
        }
        .password-title {
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 0.5em;
        }
        .password-desc {
            font-size: 1.1em;
            color: #555;
            margin-bottom: 1em;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="password-title">🔒 Enter Password</div>', unsafe_allow_html=True)
    st.markdown('<div class="password-desc">Access to this app is restricted. Please enter the database password below.</div>', unsafe_allow_html=True)

    def password_entered():
        if st.session_state["password"] == "yourpassword":
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password", label_visibility="collapsed")
        st.stop()
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password", label_visibility="collapsed")
        st.error("Password incorrect")
        st.stop()

check_password()

st.switch_page("pages/1_Prospect_Database.py")