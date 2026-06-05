import streamlit as st

from utils.auth import logout, go_to

from services.api import (
    fetch_courses,
    fetch_schedules,
    fetch_assignments,
    complete_assignment,
    delete_assignment,
)


PRIORITY_LABEL = {
    "high": "🔴 High",
    "medium": "🟡 Medium",
    "low": "🟢 Low",
}


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

    # Flash message setelah aksi tugas
    flash = st.session_state.pop("assignment_flash", None)
    if flash:
        st.info(flash)

    st.write(
        """
        Selamat datang di Campus Assignment Manager.

        Sistem ini membantu mahasiswa mengelola
        mata kuliah dan jadwal perkuliahan.
        """
    )

    st.divider()

    # ======================
    # RINGKASAN TUGAS
    # ======================

    st.subheader(
        "📝 Ringkasan Tugas"
    )

    try:
        assignments = fetch_assignments(token)
    except Exception:
        assignments = None

    if assignments is None:

        st.error(
            "Gagal memuat tugas."
        )

    elif len(assignments) == 0:

        st.info(
            "Belum ada tugas."
        )

    else:

        total = len(assignments)

        pending = [
            a for a in assignments
            if a["status"] != "completed"
        ]

        completed_count = total - len(pending)

        col_total, col_pending, col_done = st.columns(3)

        with col_total:
            st.metric("Total Tugas", total)

        with col_pending:
            st.metric("Belum Selesai", len(pending))

        with col_done:
            st.metric("Selesai", completed_count)

        # Daftar tugas (urut deadline terdekat) + aksi
        # Selesai dan Hapus.
        assignments_sorted = sorted(
            assignments,
            key=lambda a: a["due_date"]
        )

        for item in assignments_sorted:

            with st.container(border=True):

                col_info, col_status, col_action = st.columns(
                    [4, 2, 2]
                )

                with col_info:

                    st.markdown(
                        f"**{item['title']}**"
                    )

                    st.write(
                        f"{item['course_name']} | "
                        f"Deadline: {item['due_date']}"
                    )

                    st.caption(
                        PRIORITY_LABEL.get(
                            item["priority"], item["priority"]
                        )
                    )

                with col_status:

                    if item["status"] == "completed":
                        st.success("Completed")
                    else:
                        st.warning("Pending")

                with col_action:

                    if item["status"] != "completed":

                        if st.button(
                            "Selesai",
                            key=f"done_{item['id']}",
                        ):

                            done_resp = complete_assignment(
                                token, item["id"]
                            )

                            if done_resp.status_code == 200:
                                st.session_state.assignment_flash = (
                                    "Tugas ditandai selesai."
                                )
                            else:
                                st.session_state.assignment_flash = (
                                    "Gagal memperbarui tugas."
                                )

                            st.rerun()

                    if st.button(
                        "Hapus",
                        key=f"del_{item['id']}",
                    ):

                        del_resp = delete_assignment(
                            token, item["id"]
                        )

                        if del_resp.status_code in (200, 204):
                            st.session_state.assignment_flash = (
                                "Tugas dihapus."
                            )
                        else:
                            st.session_state.assignment_flash = (
                                "Gagal menghapus tugas."
                            )

                        st.rerun()

    st.divider()

    # ======================
    # MATA KULIAH
    # ======================

    st.subheader(
        "📚 Mata Kuliah Saya"
    )

    try:
        courses = fetch_courses(token)
    except Exception:
        courses = None

    if courses is None:

        st.error(
            "Gagal memuat mata kuliah."
        )

    elif len(courses) == 0:

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

                st.write(
                    f"📝 Grade : {course.get('grade') or '-'}"
                )

    st.divider()

    # ======================
    # JADWAL
    # ======================

    st.subheader(
        "🗓️ Jadwal Saya"
    )

    try:
        schedules = fetch_schedules(token)
    except Exception:
        schedules = None

    if schedules is None:

        st.error(
            "Gagal memuat jadwal."
        )

    elif len(schedules) == 0:

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

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

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

    with col3:

        if st.button(
            "Kelola Tugas",
            use_container_width=True
        ):

            go_to("assignment")
            st.rerun()

    with col4:

        if st.button(
            "GPA Tracker",
            use_container_width=True
        ):

            go_to("gpa_tracker")
            st.rerun()
