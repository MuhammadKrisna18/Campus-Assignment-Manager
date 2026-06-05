import streamlit as st
from streamlit_cookies_controller import CookieController

# Nama cookie tempat token JWT disimpan di browser user.
# Cookie bersifat per-browser, jadi token tidak bocor antar-user
# dan tetap bertahan saat halaman di-refresh.
TOKEN_COOKIE = "cam_token"

# Masa berlaku cookie (detik). Disetel sama dengan masa hidup
# JWT di backend (ACCESS_TOKEN_EXPIRE_MINUTES=60) agar cookie
# kedaluwarsa bersamaan dengan token.
TOKEN_MAX_AGE = 60 * 60


def get_cookie_controller():
    """Ambil (atau buat) CookieController untuk sesi ini."""
    if "cookie_controller" not in st.session_state:
        st.session_state.cookie_controller = CookieController()
    return st.session_state.cookie_controller


def init_session():
    """Inisialisasi session state."""

    # Pastikan controller cookie sudah siap sejak awal.
    get_cookie_controller()

    if "token" not in st.session_state:
        st.session_state.token = None

    if "user" not in st.session_state:
        st.session_state.user = None

    if "page" not in st.session_state:
        st.session_state.page = "login"

    if "flash" not in st.session_state:
        st.session_state.flash = None


def get_token_from_cookie():
    """Baca token dari cookie browser. None bila tidak ada."""
    controller = get_cookie_controller()
    return controller.get(TOKEN_COOKIE)


def set_flash(message):
    """Simpan flash message."""
    st.session_state.flash = message


def pop_flash():
    """Ambil dan hapus flash message."""
    message = st.session_state.get("flash")
    st.session_state.flash = None
    return message


def login(token, user):
    """Simpan data login ke session state dan cookie browser."""

    st.session_state.token = token
    st.session_state.user = user
    st.session_state.page = "dashboard"

    # Simpan token ke cookie agar sesi bertahan saat refresh.
    # max_age dibatasi sama dengan masa hidup JWT (60 menit),
    # same_site='strict' untuk mengurangi risiko CSRF.
    controller = get_cookie_controller()
    controller.set(
        TOKEN_COOKIE,
        token,
        max_age=TOKEN_MAX_AGE,
        same_site="strict",
    )


def logout():
    """Logout user: bersihkan session state dan cookie."""

    st.session_state.token = None
    st.session_state.user = None
    st.session_state.page = "login"

    # Hapus token dari cookie browser.
    controller = get_cookie_controller()
    try:
        controller.remove(TOKEN_COOKIE)
    except Exception:
        pass


def is_logged_in():
    """Cek apakah user sudah login."""

    return (
        st.session_state.token is not None
        and st.session_state.user is not None
    )


def go_to(page):
    """Navigasi halaman."""

    st.session_state.page = page
