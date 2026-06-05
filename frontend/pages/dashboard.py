import streamlit as st

from utils.auth import logout, go_to
from services.api import get_courses


def render_dashboard():

    user = st.session_state.user
    token = st.session_state.token

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

    st.title(
        "Dashboard"
    )

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

    # ======================
    # DAFTAR MATA KULIAH
    # ======================

    st.subheader(
        "Mata Kuliah Saya"
    )

    response = get_courses(
        token
    )

    if response.status_code == 200:

        courses = response.json()

        if len(courses) == 0:

            st.info(
                "Belum ada mata kuliah."
            )

        else:

            for course in courses:

                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"### {course['course_name']}"
                    )

                    st.write(
                        f"👨‍🏫 Dosen : {course['lecturer_name']}"
                    )

                    st.write(
                        f"🏫 Kelas : {course['class_name']}"
                    )

                    st.write(
                        f"📚 SKS : {course['credits']}"
                    )

    else:

        st.error(
            "Gagal memuat mata kuliah."
        )

    st.divider()

    if st.button(
        "Kelola Mata Kuliah",
        use_container_width=True
    ):
        go_to("course")
        st.rerun()

    if st.button(
        "Kelola Jadwal",
        use_container_width=True
    ):
        go_to("schedule")
        st.rerun()