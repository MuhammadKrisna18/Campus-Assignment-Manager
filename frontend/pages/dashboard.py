import streamlit as st

from utils.auth import logout, go_to


def render_dashboard():
    user = st.session_state.user

    col_info, col_logout = st.columns([4, 1])

    with col_info:
        st.write(
            f"**{user['full_name']}** | {user['email']}"
        )
        st.caption(
            f"Role: {user['role']}"
        )

    with col_logout:
        if st.button("Logout"):
            logout()
            st.rerun()

    st.title("Dashboard")

    st.success(
        f"Selamat datang, {user['full_name']}!"
    )

    st.write(
        """
        Selamat datang di Campus Assignment Manager.

        Sistem ini akan membantu mahasiswa dalam mengelola
        tugas, deadline, dan aktivitas akademik lainnya.
        """
    )

    st.divider()

    st.subheader("Menu")
    if st.button("Mata Kuliah"):
        go_to("course")
        st.rerun()