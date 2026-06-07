import streamlit as st

from services.api import register_user
from utils.auth import (
    go_to,
    set_flash
)


def render_register():

    st.title(
        "🎓 Campus Assignment Manager"
    )

    st.subheader(
        "Register"
    )

    full_name = st.text_input(
        "Nama Lengkap"
    )

    email = st.text_input(
        "Email"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm = st.text_input(
        "Konfirmasi Password",
        type="password"
    )

    if st.button(
        "Register",
        use_container_width=True
    ):

        if not full_name or not email or not password:

            st.error(
                "Semua field harus diisi."
            )

        elif len(password) < 6:

            st.error(
                "Password minimal 6 karakter."
            )

        elif password != confirm:

            st.error(
                "Password tidak cocok."
            )

        else:

            with st.spinner(
                "Membuat akun..."
            ):

                response = register_user(
                    full_name,
                    email,
                    password
                )

            if response.status_code == 200:

                set_flash(
                    "Registrasi berhasil. Silakan login."
                )

                go_to(
                    "login"
                )

                st.rerun()

            elif response.status_code == 400:

                st.error(
                    "Email sudah terdaftar."
                )

            else:

                st.error(
                    "Terjadi kesalahan pada server."
                )

    st.write(
        "Sudah punya akun?"
    )

    if st.button(
        "Login",
        use_container_width=True
    ):

        go_to(
            "login"
        )

        st.rerun()