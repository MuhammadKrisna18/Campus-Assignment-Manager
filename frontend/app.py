import streamlit as st

from utils.auth import (
    init_session,
    is_logged_in,
    login
)

from services.api import (
    get_current_user
)

from pages.login import render_login
from pages.register import render_register
from pages.dashboard import render_dashboard
from pages.course import render_course
from pages.schedule import render_schedule

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

# Restore user setelah refresh browser
if (
    st.session_state.token
    and st.session_state.user is None
):
    try:

        response = get_current_user(
            st.session_state.token
        )

        if response.status_code == 200:

            login(
                st.session_state.token,
                response.json()
            )

        else:

            st.session_state.token = None
            st.query_params.clear()

    except Exception:

        st.session_state.token = None
        st.query_params.clear()

# Routing
if is_logged_in():

    if st.session_state.page == "course":
        render_course()
    elif st.session_state.page == "schedule":
        render_schedule()
    else:
        render_dashboard()

elif st.session_state.page == "register":

    render_register()

else:

    render_login()