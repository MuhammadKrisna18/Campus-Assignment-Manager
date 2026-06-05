import streamlit as st

from services.api import (
    get_schedules,
    create_schedule,
    get_courses,
)

from utils.auth import go_to


def render_schedule():

    token = st.session_state.token

    col_title, col_back = st.columns(
        [4, 1]
    )

    with col_title:
        st.title("Jadwal")

    with col_back:
        if st.button("Dashboard"):
            go_to("dashboard")
            st.rerun()

    flash = st.session_state.pop(
        "schedule_flash",
        None
    )

    if flash:
        st.success(flash)

    st.subheader(
        "Daftar Jadwal"
    )

    response = get_schedules(token)

    if response.status_code != 200:

        st.error(
            "Gagal memuat data jadwal."
        )

        return

    schedules = response.json()

    if not schedules:

        st.info(
            "Belum ada jadwal."
        )

    else:

        for schedule in schedules:

            with st.container(
                border=True
            ):

                st.markdown(
                    f"**{schedule['course_name']}**"
                )

                st.write(
                    f"Hari: {schedule['day']} | "
                    f"Ruang: {schedule['room']}"
                )

                st.caption(
                    f"{schedule['start_time']} - "
                    f"{schedule['end_time']}"
                )

    st.divider()

    st.subheader(
        "Tambah Jadwal"
    )

    course_resp = get_courses(token)

    courses = (
        course_resp.json()
        if course_resp.status_code == 200
        else []
    )

    if not courses:

        st.warning(
            "Tambahkan mata kuliah terlebih dahulu "
            "sebelum membuat jadwal."
        )

        return

    course_options = {
        c["course_name"]: c["id"]
        for c in courses
    }

    selected_course = st.selectbox(
        "Mata Kuliah",
        list(course_options.keys())
    )

    day = st.selectbox(
        "Day",
        [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday"
        ]
    )

    room = st.text_input(
        "Room"
    )

    start_time = st.time_input(
        "Start Time"
    )

    end_time = st.time_input(
        "End Time"
    )

    if st.button(
        "Add Schedule",
        type="primary"
    ):

        if not room:

            st.error(
                "Room harus diisi."
            )

        elif end_time <= start_time:

            st.error(
                "Jam selesai harus setelah jam mulai."
            )

        else:

            data = {
                "course_id": course_options[
                    selected_course
                ],
                "day": day,
                "room": room,
                "start_time": start_time.strftime(
                    "%H:%M:%S"
                ),
                "end_time": end_time.strftime(
                    "%H:%M:%S"
                ),
            }

            create_resp = create_schedule(
                token,
                data
            )

            if create_resp.status_code in (
                200,
                201
            ):

                st.session_state.schedule_flash = (
                    "Jadwal ditambahkan."
                )

                st.rerun()

            else:

                try:

                    detail = (
                        create_resp
                        .json()
                        .get(
                            "detail",
                            "Gagal menambahkan jadwal."
                        )
                    )

                except Exception:

                    detail = (
                        "Gagal menambahkan jadwal."
                    )

                st.error(detail)