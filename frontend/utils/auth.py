import streamlit as st


def init_session():
    """Inisialisasi session state."""

    if "token" not in st.session_state:
        st.session_state.token = None

    if "user" not in st.session_state:
        st.session_state.user = None

    if "page" not in st.session_state:
        st.session_state.page = "login"

    if "flash" not in st.session_state:
        st.session_state.flash = None


def set_flash(message):
    """Simpan flash message."""
    st.session_state.flash = message


def pop_flash():
    """Ambil dan hapus flash message."""
    message = st.session_state.get("flash")
    st.session_state.flash = None
    return message


def login(token, user):
    """Simpan data login."""

    st.session_state.token = token
    st.session_state.user = user
    st.session_state.page = "dashboard"


def logout():
    """Logout user."""

    st.session_state.token = None
    st.session_state.user = None
    st.session_state.page = "login"


def is_logged_in():
    """Cek apakah user sudah login."""

    return (
        st.session_state.token is not None
        and st.session_state.user is not None
    )


def go_to(page):
    """Navigasi halaman."""

    st.session_state.page = page