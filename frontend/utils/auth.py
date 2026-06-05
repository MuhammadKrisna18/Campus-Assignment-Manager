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

    # Restore token setelah refresh browser
    if (
        st.session_state.token is None
        and "token" in st.query_params
    ):
        st.session_state.token = st.query_params["token"]


def set_flash(message):
    """Simpan pesan sementara."""
    st.session_state.flash = message


def pop_flash():
    """Ambil lalu hapus flash message."""
    message = st.session_state.get("flash")
    st.session_state.flash = None
    return message


def login(token, user):
    """Simpan data login."""

    st.session_state.token = token
    st.session_state.user = user
    st.session_state.page = "dashboard"

    # Simpan token ke URL agar tidak hilang saat refresh
    st.query_params["token"] = token


def logout():
    """Logout user."""

    st.session_state.token = None
    st.session_state.user = None
    st.session_state.page = "login"

    # Hapus query params
    st.query_params.clear()


def is_logged_in():
    """Cek apakah user sudah login."""

    return (
        st.session_state.token is not None
        and st.session_state.user is not None
    )


def go_to(page):
    """Pindah halaman."""

    st.session_state.page = page