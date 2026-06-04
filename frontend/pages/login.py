import streamlit as st

from services.api import login_user, get_current_user
from utils.auth import login, go_to, pop_flash


def render_login():
    st.title("🎓 Campus Assignment Manager")
    st.subheader("Login")

    flash = pop_flash()
    if flash:
        st.success(flash)

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not email or not password:
            st.error("Email dan password harus diisi.")
        else:
            response = login_user(email, password)

            if response.status_code == 200:
                token = response.json()["access_token"]
                user_resp = get_current_user(token)

                if user_resp.status_code == 200:
                    login(token, user_resp.json())
                    st.rerun()
                else:
                    st.error("Gagal mengambil data user.")
            elif response.status_code == 401:
                st.error("Email atau password salah.")
            else:
                st.error("Terjadi kesalahan pada server.")

    st.write("Belum punya akun?")
    if st.button("Register"):
        go_to("register")
        st.rerun()
