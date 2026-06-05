import streamlit as st

from services.api import login_user
from utils.auth import (
    login,
    go_to,
    pop_flash
)


def render_login():

    st.title(
        "🎓 Campus Assignment Manager"
    )

    st.subheader(
        "Login"
    )

    flash = pop_flash()

    if flash:
        st.success(flash)

    email = st.text_input(
        "Email"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button(
        "Login",
        use_container_width=True
    ):

        if not email or not password:

            st.error(
                "Email dan password harus diisi."
            )

        else:

            with st.spinner(
                "Memproses login..."
            ):

                response = login_user(
                    email,
                    password
                )

            if response.status_code == 200:

                data = response.json()

                login(
                    data["access_token"],
                    data["user"]
                )

                st.rerun()

            elif response.status_code == 401:

                st.error(
                    "Email atau password salah."
                )

            else:

                st.error(
                    "Terjadi kesalahan pada server."
                )

    st.write(
        "Belum punya akun?"
    )

    if st.button(
        "Register",
        use_container_width=True
    ):

        go_to("register")

        st.rerun()