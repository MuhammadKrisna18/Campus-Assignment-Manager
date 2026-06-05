import streamlit as st

from utils.auth import logout, go_to

from services.api import (
    get_courses,
    get_schedules
)


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

        Sistem ini membantu mahasiswa mengelola
        mata kuliah dan jadwal perkuliahan.
        """
    )

    st.divider()

    # ======================
    # MATA KULIAH
    # ======================

    st.subheader(
        "📚 Mata Kuliah Saya"
    )

    course_response = get_courses(
        token
    )

    if course_response.status_code == 200:

        courses = course_response.json()

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

    # ======================
    # JADWAL
    # ======================

    st.subheader(
        "🗓️ Jadwal Saya"
    )

    schedule_response = get_schedules(
        token
    )

    if schedule_response.status_code == 200:

        schedules = schedule_response.json()

        if len(schedules) == 0:

            st.info(
                "Belum ada jadwal."
            )

        else:

            for schedule in schedules:

                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"### {schedule['course_name']}"
                    )

                    st.write(
                        f"📅 Hari : {schedule['day']}"
                    )

                    st.write(
                        f"🏫 Ruang : {schedule['room']}"
                    )

                    st.write(
                        f"⏰ {schedule['start_time']} - "
                        f"{schedule['end_time']}"
                    )

    else:

        st.error(
            "Gagal memuat jadwal."
        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Kelola Mata Kuliah",
            use_container_width=True
        ):

            go_to("course")
            st.rerun()

    with col2:

        if st.button(
            "Kelola Jadwal",
            use_container_width=True
        ):

            go_to("schedule")
            st.rerun()