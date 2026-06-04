import streamlit as st

from utils.auth import logout


def render_dashboard():
    user = st.session_state.user

    col_info, col_logout = st.columns([4, 1])
    with col_info:
        st.write(f"**{user['full_name']}**  |  {user['email']}")
        st.caption(f"Role: {user['role']}")
    with col_logout:
        if st.button("Logout"):
            logout()
            st.rerun()

    st.title("Dashboard")
    st.write(f"Selamat datang, {user['full_name']}!")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Mata Kuliah", "0")
    col2.metric("Tugas Aktif", "0")
    col3.metric("Tugas Selesai", "0")
    col4.metric("IPK", "-")

    st.subheader("Tugas Mendatang")
    st.info("Belum ada tugas.")

    st.subheader("Jadwal Hari Ini")
    st.info("Belum ada jadwal.")
