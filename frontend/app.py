import streamlit as st

from utils.auth import (
    init_session,
    is_logged_in,
    login,
    get_token_from_cookie,
)

from services.api import (
    get_current_user
)

from pages.login import render_login
from pages.register import render_register
from pages.dashboard import render_dashboard
from pages.course import render_course
from pages.schedule import render_schedule
from pages.assignment import render_assignment
from pages.gpa_tracker import render_gpa_tracker

st.set_page_config(
    page_title="Campus Assignment Manager",
    page_icon="🎓",
    initial_sidebar_state="collapsed",
)

# Hilangkan sidebar bawaan Streamlit
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }

    [data-testid="stSidebarCollapsedControl"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

init_session()

# Restore sesi setelah refresh browser.
# Token tersimpan di cookie (per-browser), jadi setelah refresh kita
# baca token dari cookie lalu ambil ulang data user lewat /auth/me.
if not is_logged_in():

    cookie_token = get_token_from_cookie()

    if cookie_token:

        try:

            response = get_current_user(cookie_token)

            if response.status_code == 200:

                login(
                    cookie_token,
                    response.json()
                )

            else:

                # Token tidak valid/kedaluwarsa -> abaikan.
                st.session_state.token = None

        except Exception:

            st.session_state.token = None

# Routing
if is_logged_in():

    if st.session_state.page == "course":
        render_course()
    elif st.session_state.page == "schedule":
        render_schedule()
    elif st.session_state.page == "assignment":
        render_assignment()
    elif st.session_state.page == "gpa_tracker":
        render_gpa_tracker()
    else:
        render_dashboard()

elif st.session_state.page == "register":

    render_register()

else:

    render_login()