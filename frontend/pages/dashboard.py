import streamlit as st

from datetime import date, timedelta

from utils.auth import logout, go_to

from services.api import (
    fetch_courses,
    fetch_schedules,
    fetch_assignments,
)

# Urutan hari untuk mencocokkan jadwal hari ini
TODAY_NAME = date.today().strftime("%A")  # e.g. "Monday"


def render_dashboard():

    user = st.session_state.user
    token = st.session_state.token

    # --- Header user ---
    col_info, col_logout = st.columns([4, 1])

    with col_info:
        st.write(
            f"**{user['full_name']}** | {user['email']}"
        )
        st.caption(f"Role: {user['role']}")

    with col_logout:
        if st.button("Logout"):
            logout()
            st.rerun()

    st.title("Dashboard")
    st.success(f"Selamat datang, {user['full_name']}!")

    # Flash message setelah aksi
    flash = st.session_state.pop("assignment_flash", None)
    if flash:
        st.info(flash)

    st.divider()

    # ============================================================
    # FETCH DATA
    # ============================================================

    try:
        assignments = fetch_assignments(token)
    except Exception:
        assignments = []

    try:
        schedules = fetch_schedules(token)
    except Exception:
        schedules = []

    try:
        courses = fetch_courses(token)
    except Exception:
        courses = []

    # ============================================================
    # METRIC — Total Task & Completed
    # ============================================================

    st.subheader("📊 Ringkasan")

    total = len(assignments)
    completed = sum(
        1 for a in assignments
        if a["status"] == "completed"
    )
    pending = total - completed

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Task", total)

    with col2:
        st.metric("Completed", completed)

    with col3:
        st.metric("Pending", pending)

    with col4:
        st.metric("Mata Kuliah", len(courses))

    st.divider()

    # ============================================================
    # REMINDER — Upcoming Deadline
    # ============================================================

    st.subheader("⏰ Upcoming Deadline")

    today = date.today()
    tomorrow = today + timedelta(days=1)

    # Filter tugas pending saja, urutkan deadline terdekat
    upcoming = sorted(
        [
            a for a in assignments
            if a["status"] != "completed"
        ],
        key=lambda a: a["due_date"]
    )

    if not upcoming:
        st.info("Tidak ada tugas yang mendesak.")
    else:
        # Reminder warning untuk deadline hari ini / besok
        due_today = [
            a for a in upcoming
            if a["due_date"] == str(today)
        ]

        due_tomorrow = [
            a for a in upcoming
            if a["due_date"] == str(tomorrow)
        ]

        if due_today:
            st.error(
                f"🚨 {len(due_today)} tugas deadline hari ini!"
            )

        if due_tomorrow:
            st.warning(
                f"⚠️ {len(due_tomorrow)} tugas deadline besok"
            )

        # Tampilkan semua tugas yang belum selesai
        for item in upcoming:
            with st.container(border=True):
                col_task, col_date = st.columns([3, 1])

                with col_task:
                    st.write(f"**{item['title']}**")
                    st.caption(
                        f"{item['course_name']} | "
                        f"Priority: {item['priority'].upper()}"
                    )

                with col_date:
                    st.caption(f"📅 {item['due_date']}")


    st.divider()

    # ============================================================
    # TODAY'S SCHEDULE
    # ============================================================

    st.subheader(f"📅 Jadwal Hari Ini ({TODAY_NAME})")

    today_schedules = [
        s for s in schedules
        if s["day"].lower() == TODAY_NAME.lower()
    ]

    if not today_schedules:
        st.info("Tidak ada jadwal untuk hari ini.")
    else:
        for schedule in today_schedules:
            with st.container(border=True):
                col_sub, col_time = st.columns([3, 1])

                with col_sub:
                    st.write(f"**{schedule['course_name']}**")
                    st.caption(f"🏫 Ruang: {schedule['room']}")

                with col_time:
                    st.caption(
                        f"⏰ {schedule['start_time']} - "
                        f"{schedule['end_time']}"
                    )

    st.divider()

    # ============================================================
    # NAVIGASI — badge pending count di tombol Kelola Tugas
    # ============================================================

    pending_count = sum(
        1 for a in assignments if a["status"] == "pending"
    )

    tugas_label = (
        f"Kelola Tugas 🔴 {pending_count}"
        if pending_count > 0
        else "Kelola Tugas"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Kelola Mata Kuliah", width='stretch'):
            go_to("course")
            st.rerun()

    with col2:
        if st.button("Kelola Jadwal", width='stretch'):
            go_to("schedule")
            st.rerun()

    with col3:
        if st.button(tugas_label, width='stretch'):
            go_to("assignment")
            st.rerun()

    with col4:
        if st.button("GPA Tracker", width='stretch'):
            go_to("gpa_tracker")
            st.rerun()
