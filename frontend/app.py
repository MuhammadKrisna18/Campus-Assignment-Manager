import streamlit as st

from utils.auth import init_session, is_logged_in
from pages.login import render_login
from pages.register import render_register
from pages.dashboard import render_dashboard

st.set_page_config(
    page_title="Campus Assignment Manager",
    page_icon="🎓",
    initial_sidebar_state="collapsed",
)

# Sembunyikan sidebar navigasi bawaan Streamlit
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {display: none;}
    [data-testid="stSidebarCollapsedControl"] {display: none;}
    </style>
    """,
    unsafe_allow_html=True,
)

init_session()

if is_logged_in():
    render_dashboard()
elif st.session_state.page == "register":
    render_register()
else:
    render_login()
